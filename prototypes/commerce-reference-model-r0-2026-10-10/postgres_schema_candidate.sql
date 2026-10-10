-- CE commerce persistence contract candidate R0.
-- PostgreSQL syntax; candidate-only. Owner disposition dated 2026-10-10 selects D1-A, D2-B,
-- and the fail-closed fulfillment-health interlock for candidate implementation.
-- Production use still requires normative/source review, migrations, access controls,
-- health-state audit/recovery design, data-retention review, and independent testing.

CREATE TABLE ce_credits_sku (
    sku_id TEXT NOT NULL,
    sku_revision TEXT NOT NULL,
    amount_minor BIGINT NOT NULL CHECK (amount_minor > 0),
    currency CHAR(3) NOT NULL CHECK (currency ~ '^[A-Z]{3}$'),
    credits_granted BIGINT NOT NULL CHECK (credits_granted > 0),
    sku_status TEXT NOT NULL CHECK (sku_status IN ('AVAILABLE', 'RETIRED')),
    created_at TIMESTAMPTZ NOT NULL,
    PRIMARY KEY (sku_id, sku_revision)
);

CREATE TABLE ce_topup_order (
    logical_topup_id TEXT PRIMARY KEY,
    account_id TEXT NOT NULL,
    idempotency_key TEXT NOT NULL,
    sku_id TEXT NOT NULL,
    sku_revision TEXT NOT NULL,
    amount_minor BIGINT NOT NULL CHECK (amount_minor > 0),
    currency CHAR(3) NOT NULL CHECK (currency ~ '^[A-Z]{3}$'),
    credits_to_grant BIGINT NOT NULL CHECK (credits_to_grant > 0),
    status TEXT NOT NULL CHECK (status IN (
        'PAYMENT_PENDING', 'PAYMENT_CONFIRMED',
        'RECONCILIATION_REQUIRED', 'PAYMENT_FAILED', 'CREDIT_FULFILLED'
    )),
    provider_name TEXT,
    provider_transaction_ref TEXT,
    created_at TIMESTAMPTZ NOT NULL,
    completed_at TIMESTAMPTZ,
    failure_observed BOOLEAN NOT NULL DEFAULT FALSE,
    UNIQUE (account_id, idempotency_key),
    UNIQUE (provider_name, provider_transaction_ref),
    FOREIGN KEY (sku_id, sku_revision) REFERENCES ce_credits_sku(sku_id, sku_revision),
    CHECK ((provider_name IS NULL) = (provider_transaction_ref IS NULL)),
    CHECK (
      (status = 'CREDIT_FULFILLED' AND completed_at IS NOT NULL)
      OR (status <> 'CREDIT_FULFILLED' AND completed_at IS NULL)
    )
);

CREATE TABLE ce_provider_event (
    provider_name TEXT NOT NULL,
    provider_event_id TEXT NOT NULL,
    logical_topup_id TEXT NOT NULL REFERENCES ce_topup_order(logical_topup_id),
    provider_transaction_ref TEXT NOT NULL,
    payload_fingerprint TEXT NOT NULL,
    verified_amount_minor BIGINT NOT NULL CHECK (verified_amount_minor > 0),
    verified_currency CHAR(3) NOT NULL CHECK (verified_currency ~ '^[A-Z]{3}$'),
    observed_status TEXT NOT NULL CHECK (observed_status IN (
        'PENDING', 'UNKNOWN', 'FAILED', 'SUCCEEDED'
    )),
    observation_source TEXT NOT NULL CHECK (observation_source IN (
        'WEBHOOK', 'AUTHORITATIVE_STATUS_LOOKUP'
    )),
    verification_reference TEXT NOT NULL,
    received_at TIMESTAMPTZ NOT NULL,
    PRIMARY KEY (provider_name, provider_event_id),
    FOREIGN KEY (provider_name, provider_transaction_ref)
      REFERENCES ce_topup_order(provider_name, provider_transaction_ref)
);

CREATE TABLE ce_credit_ledger_entry (
    entry_id TEXT PRIMARY KEY,
    account_id TEXT NOT NULL,
    entry_type TEXT NOT NULL CHECK (entry_type IN (
        'TOPUP_CREDIT_GRANT',
        'DEEP_SKY_READING_DEBIT',
        'DEEP_SKY_READING_DEBIT_RESTORATION'
    )),
    delta BIGINT NOT NULL CHECK (delta <> 0),
    reference_id TEXT NOT NULL,
    parent_entry_id TEXT REFERENCES ce_credit_ledger_entry(entry_id),
    created_at TIMESTAMPTZ NOT NULL,
    UNIQUE (entry_type, reference_id),
    UNIQUE (parent_entry_id),
    CHECK (
        (entry_type = 'TOPUP_CREDIT_GRANT' AND delta > 0 AND parent_entry_id IS NULL)
        OR
        (entry_type = 'DEEP_SKY_READING_DEBIT' AND delta < 0 AND parent_entry_id IS NULL)
        OR
        (entry_type = 'DEEP_SKY_READING_DEBIT_RESTORATION'
            AND delta > 0 AND parent_entry_id IS NOT NULL)
    )
);

-- Explicit service-admission state. UNKNOWN is the initial fail-closed state.
-- READY is only valid until ready_expires_at; expired attestations fail closed.
CREATE TABLE ce_purchase_admission_state (
    singleton_id SMALLINT PRIMARY KEY CHECK (singleton_id = 1),
    admission_state TEXT NOT NULL CHECK (admission_state IN ('READY', 'BLOCKED', 'UNKNOWN')),
    reason_reference TEXT NOT NULL CHECK (btrim(reason_reference) <> ''),
    health_attestation_reference TEXT,
    ready_expires_at TIMESTAMPTZ,
    state_version BIGINT NOT NULL DEFAULT 0 CHECK (state_version >= 0),
    updated_at TIMESTAMPTZ NOT NULL,
    CHECK (
        (admission_state = 'READY'
          AND health_attestation_reference IS NOT NULL
          AND btrim(health_attestation_reference) <> ''
          AND ready_expires_at IS NOT NULL)
        OR
        (admission_state <> 'READY'
          AND health_attestation_reference IS NULL
          AND ready_expires_at IS NULL)
    )
);

INSERT INTO ce_purchase_admission_state
    (singleton_id, admission_state, reason_reference, health_attestation_reference,
     ready_expires_at, state_version, updated_at)
VALUES
    (1, 'UNKNOWN', 'INITIAL_HEALTH_NOT_ATTESTED', NULL, NULL, 0, CURRENT_TIMESTAMP);

-- One immutable event per version. Inserting a valid event atomically changes current state
-- via the AFTER INSERT trigger below; direct state updates without an event are rejected.
CREATE TABLE ce_purchase_admission_event (
    event_id TEXT PRIMARY KEY,
    singleton_id SMALLINT NOT NULL DEFAULT 1 CHECK (singleton_id = 1),
    state_version BIGINT NOT NULL CHECK (state_version > 0),
    previous_state TEXT NOT NULL CHECK (previous_state IN ('READY', 'BLOCKED', 'UNKNOWN')),
    new_state TEXT NOT NULL CHECK (new_state IN ('READY', 'BLOCKED', 'UNKNOWN')),
    reason_reference TEXT NOT NULL CHECK (btrim(reason_reference) <> ''),
    health_attestation_reference TEXT,
    ready_expires_at TIMESTAMPTZ,
    actor_reference TEXT NOT NULL CHECK (btrim(actor_reference) <> ''),
    changed_at TIMESTAMPTZ NOT NULL,
    UNIQUE (singleton_id, state_version),
    CHECK (
        (new_state = 'READY'
          AND health_attestation_reference IS NOT NULL
          AND btrim(health_attestation_reference) <> ''
          AND ready_expires_at IS NOT NULL)
        OR
        (new_state <> 'READY'
          AND health_attestation_reference IS NULL
          AND ready_expires_at IS NULL)
    )
);

CREATE FUNCTION ce_validate_purchase_admission_event() RETURNS trigger AS $CE$
DECLARE
    current_state ce_purchase_admission_state%ROWTYPE;
BEGIN
    -- Timestamp is database-owned; clients cannot backdate/forward-date a health transition.
    NEW.changed_at := statement_timestamp();
    SELECT * INTO current_state
      FROM ce_purchase_admission_state
     WHERE singleton_id = 1
     FOR UPDATE;
    IF NOT FOUND
       OR NEW.previous_state <> current_state.admission_state
       OR NEW.state_version <> current_state.state_version + 1 THEN
        RAISE EXCEPTION 'admission event must match the current state and next version';
    END IF;
    IF NEW.new_state = 'READY'
       AND (NEW.health_attestation_reference IS NULL
            OR btrim(NEW.health_attestation_reference) = ''
            OR NEW.ready_expires_at IS NULL
            OR NEW.ready_expires_at <= statement_timestamp()
            OR NEW.ready_expires_at > statement_timestamp() + INTERVAL '5 minutes') THEN
        RAISE EXCEPTION 'READY admission requires a non-empty health attestation and expiry within the provisional five-minute lease ceiling';
    END IF;
    RETURN NEW;
END;
$CE$ LANGUAGE plpgsql;

CREATE TRIGGER ce_purchase_admission_event_validate_insert
BEFORE INSERT ON ce_purchase_admission_event
FOR EACH ROW EXECUTE FUNCTION ce_validate_purchase_admission_event();

CREATE FUNCTION ce_validate_purchase_admission_state_update() RETURNS trigger AS $CE$
BEGIN
    IF NEW.singleton_id <> OLD.singleton_id
       OR NEW.state_version <> OLD.state_version + 1
       OR NOT EXISTS (
          SELECT 1 FROM ce_purchase_admission_event e
           WHERE e.singleton_id = NEW.singleton_id
             AND e.state_version = NEW.state_version
             AND e.previous_state = OLD.admission_state
             AND e.new_state = NEW.admission_state
             AND e.reason_reference = NEW.reason_reference
             AND e.health_attestation_reference IS NOT DISTINCT FROM NEW.health_attestation_reference
             AND e.ready_expires_at IS NOT DISTINCT FROM NEW.ready_expires_at
             AND e.changed_at = NEW.updated_at
       ) THEN
        RAISE EXCEPTION 'admission state update requires a matching versioned audit event';
    END IF;
    RETURN NEW;
END;
$CE$ LANGUAGE plpgsql;

CREATE TRIGGER ce_purchase_admission_state_validate_update
BEFORE UPDATE ON ce_purchase_admission_state
FOR EACH ROW EXECUTE FUNCTION ce_validate_purchase_admission_state_update();

CREATE FUNCTION ce_reject_purchase_admission_state_delete() RETURNS trigger AS $CE$
BEGIN
    RAISE EXCEPTION 'current purchase-admission state cannot be deleted; transition it through an audit event';
END;
$CE$ LANGUAGE plpgsql;

CREATE TRIGGER ce_purchase_admission_state_no_delete
BEFORE DELETE ON ce_purchase_admission_state
FOR EACH ROW EXECUTE FUNCTION ce_reject_purchase_admission_state_delete();

CREATE FUNCTION ce_apply_purchase_admission_event() RETURNS trigger AS $CE$
BEGIN
    UPDATE ce_purchase_admission_state
       SET admission_state = NEW.new_state,
           reason_reference = NEW.reason_reference,
           health_attestation_reference = NEW.health_attestation_reference,
           ready_expires_at = NEW.ready_expires_at,
           state_version = NEW.state_version,
           updated_at = NEW.changed_at
     WHERE singleton_id = NEW.singleton_id;
    RETURN NEW;
END;
$CE$ LANGUAGE plpgsql;

CREATE TRIGGER ce_purchase_admission_event_apply
AFTER INSERT ON ce_purchase_admission_event
FOR EACH ROW EXECUTE FUNCTION ce_apply_purchase_admission_event();

CREATE FUNCTION ce_immutable_purchase_admission_event() RETURNS trigger AS $CE$
BEGIN
    RAISE EXCEPTION 'purchase-admission audit events are append-only';
END;
$CE$ LANGUAGE plpgsql;

CREATE TRIGGER ce_purchase_admission_event_no_update
BEFORE UPDATE OR DELETE ON ce_purchase_admission_event
FOR EACH ROW EXECUTE FUNCTION ce_immutable_purchase_admission_event();

CREATE TABLE ce_deep_sky_order (
    logical_purchase_id TEXT PRIMARY KEY,
    account_id TEXT NOT NULL,
    service_date_utc DATE NOT NULL,
    status TEXT NOT NULL CHECK (status IN (
        'RESERVED', 'DEBIT_COMMITTED', 'RECONCILIATION_REQUIRED',
        'FULFILLED', 'TERMINAL_NONDELIVERY', 'RESERVATION_REJECTED'
    )),
    cap_trigger_decision TEXT NOT NULL DEFAULT 'D1_A' CHECK (cap_trigger_decision = 'D1_A'),
    quota_effect BOOLEAN,
    reading_debit_entry_id TEXT UNIQUE REFERENCES ce_credit_ledger_entry(entry_id),
    created_at TIMESTAMPTZ NOT NULL,
    completed_at TIMESTAMPTZ,
    CHECK (
      (status = 'FULFILLED' AND completed_at IS NOT NULL)
      OR (status <> 'FULFILLED' AND completed_at IS NULL)
    )
);

-- Exactly one slot record per authenticated account and UTC service date.
-- D1-A makes the slot effective at committed reading debit; D2-B governs terminal release.
-- Transitions require evidence and must not transfer an expired date's slot.
CREATE FUNCTION ce_require_purchase_admission_ready() RETURNS trigger AS $CE$
DECLARE
    gate ce_purchase_admission_state%ROWTYPE;
BEGIN
    SELECT * INTO gate
      FROM ce_purchase_admission_state
     WHERE singleton_id = 1
     FOR SHARE;
    IF NOT FOUND OR gate.admission_state <> 'READY'
       OR gate.ready_expires_at IS NULL
       OR gate.ready_expires_at <= statement_timestamp() THEN
        RAISE EXCEPTION 'new Deep Sky purchase blocked: fulfillment admission is not currently READY';
    END IF;
    IF NEW.status <> 'RESERVED' OR NEW.reading_debit_entry_id IS NOT NULL THEN
        RAISE EXCEPTION 'new logical purchase must begin RESERVED without a committed reading debit';
    END IF;
    IF NEW.service_date_utc <> (statement_timestamp() AT TIME ZONE 'UTC')::date THEN
        RAISE EXCEPTION 'new Deep Sky purchase service date must be the server-derived current UTC date';
    END IF;
    IF NEW.cap_trigger_decision <> 'D1_A' THEN
        RAISE EXCEPTION 'new Deep Sky purchase must bind the selected D1-A policy';
    END IF;
    RETURN NEW;
END;
$CE$ LANGUAGE plpgsql;

CREATE TRIGGER ce_deep_sky_order_admission_guard
BEFORE INSERT ON ce_deep_sky_order
FOR EACH ROW EXECUTE FUNCTION ce_require_purchase_admission_ready();

CREATE TABLE ce_daily_purchase_slot (
    account_id TEXT NOT NULL,
    service_date_utc DATE NOT NULL,
    active_logical_purchase_id TEXT NOT NULL UNIQUE
      REFERENCES ce_deep_sky_order(logical_purchase_id),
    slot_state TEXT NOT NULL CHECK (slot_state IN (
        'RESERVED', 'CONSUMED', 'RECONCILIATION_REQUIRED',
        'RELEASED', 'EXPIRED_UNTRANSFERRED'
    )),
    state_version BIGINT NOT NULL DEFAULT 1 CHECK (state_version > 0),
    updated_at TIMESTAMPTZ NOT NULL,
    PRIMARY KEY (account_id, service_date_utc)
);

-- Append-only transition evidence. A release requires explicit policy and
-- terminal-evidence references; a caller cannot release based on timeout alone.
CREATE TABLE ce_quota_event (
    quota_event_id TEXT PRIMARY KEY,
    idempotency_key TEXT NOT NULL UNIQUE,
    account_id TEXT NOT NULL,
    service_date_utc DATE NOT NULL,
    logical_purchase_id TEXT NOT NULL REFERENCES ce_deep_sky_order(logical_purchase_id),
    event_type TEXT NOT NULL CHECK (event_type IN (
        'RESERVED', 'CAP_CONSUMED', 'RECONCILIATION_REQUIRED',
        'SLOT_RELEASED', 'SLOT_EXPIRED_UNTRANSFERRED', 'SLOT_RETAINED'
    )),
    policy_decision_reference TEXT,
    terminal_evidence_reference TEXT,
    occurred_at TIMESTAMPTZ NOT NULL,
    CHECK (
        event_type <> 'SLOT_RELEASED'
        OR (
            policy_decision_reference IS NOT NULL
            AND terminal_evidence_reference IS NOT NULL
        )
    )
);

CREATE TABLE ce_reading_entitlement (
    entitlement_id TEXT PRIMARY KEY,
    logical_purchase_id TEXT NOT NULL UNIQUE
      REFERENCES ce_deep_sky_order(logical_purchase_id),
    account_id TEXT NOT NULL,
    reading_reference TEXT NOT NULL,
    reading_content_hash TEXT NOT NULL,
    validated_at TIMESTAMPTZ NOT NULL,
    accessible_at TIMESTAMPTZ NOT NULL,
    CHECK (accessible_at >= validated_at)
);

-- These tables are deliberately free of card numbers, CVV, raw credentials,
-- birth data, reading bodies, persistent reflection text, and personal profiling.


-- Terminal failure evidence must be recorded before a reading debit can be restored.
-- These flags are assertions that must be backed by evidence_ref in the application layer.
CREATE TABLE ce_terminal_failure_evidence (
    logical_purchase_id TEXT PRIMARY KEY REFERENCES ce_deep_sky_order(logical_purchase_id),
    no_valid_reading_accessible BOOLEAN NOT NULL CHECK (no_valid_reading_accessible),
    no_operation_can_still_deliver BOOLEAN NOT NULL CHECK (no_operation_can_still_deliver),
    no_entitlement_exists BOOLEAN NOT NULL CHECK (no_entitlement_exists),
    all_relevant_operations_closed BOOLEAN NOT NULL CHECK (all_relevant_operations_closed),
    evidence_reference TEXT NOT NULL,
    confirmed_at TIMESTAMPTZ NOT NULL
);

-- Enforce financial invariants in the database in addition to application checks.
CREATE FUNCTION ce_validate_credit_ledger_entry() RETURNS trigger AS $CE$
DECLARE
    t ce_topup_order%ROWTYPE;
    d ce_credit_ledger_entry%ROWTYPE;
    f ce_terminal_failure_evidence%ROWTYPE;
BEGIN
    IF NEW.entry_type = 'TOPUP_CREDIT_GRANT' THEN
        SELECT * INTO t
          FROM ce_topup_order
         WHERE logical_topup_id = NEW.reference_id
         FOR UPDATE;
        IF NOT FOUND
           OR t.account_id <> NEW.account_id
           OR NEW.delta <> t.credits_to_grant
           OR t.status <> 'PAYMENT_CONFIRMED'
           OR t.provider_name IS NULL
           OR t.provider_transaction_ref IS NULL THEN
            RAISE EXCEPTION 'top-up grant does not match a confirmed server-owned order';
        END IF;
        IF NOT EXISTS (
            SELECT 1 FROM ce_provider_event e
             WHERE e.logical_topup_id = t.logical_topup_id
               AND e.provider_name = t.provider_name
               AND e.provider_transaction_ref = t.provider_transaction_ref
               AND e.observed_status = 'SUCCEEDED'
               AND e.verification_reference <> ''
        ) THEN
            RAISE EXCEPTION 'top-up grant requires a matching verified success observation';
        END IF;
    ELSIF NEW.entry_type = 'DEEP_SKY_READING_DEBIT' THEN
        -- Recheck the health gate at the effective-purchase debit boundary.
        PERFORM 1
          FROM ce_purchase_admission_state
         WHERE singleton_id = 1
           AND admission_state = 'READY'
           AND ready_expires_at > statement_timestamp()
         FOR SHARE;
        IF NOT FOUND THEN
            RAISE EXCEPTION 'new reading debit blocked: fulfillment admission is not currently READY';
        END IF;
        PERFORM 1
          FROM ce_deep_sky_order o
         WHERE o.logical_purchase_id = NEW.reference_id
           AND o.account_id = NEW.account_id
           AND o.status = 'RESERVED'
         FOR UPDATE;
        IF NOT FOUND THEN
            RAISE EXCEPTION 'reading debit must match a reserved order for the same account';
        END IF;
        -- The one-per-account/UTC-date reservation is the admission lock. A caller
        -- cannot bypass it by inserting an order row directly and posting a debit.
        IF NOT EXISTS (
            SELECT 1
              FROM ce_daily_purchase_slot s
              JOIN ce_deep_sky_order o
                ON o.logical_purchase_id = s.active_logical_purchase_id
             WHERE s.active_logical_purchase_id = NEW.reference_id
               AND s.account_id = NEW.account_id
               AND s.service_date_utc = o.service_date_utc
               AND s.slot_state = 'RESERVED'
               AND o.status = 'RESERVED'
        ) THEN
            RAISE EXCEPTION 'reading debit requires the matching reserved account/UTC-date slot';
        END IF;
    ELSIF NEW.entry_type = 'DEEP_SKY_READING_DEBIT_RESTORATION' THEN
        SELECT * INTO d
          FROM ce_credit_ledger_entry
         WHERE entry_id = NEW.parent_entry_id
         FOR KEY SHARE;
        IF NOT FOUND
           OR d.entry_type <> 'DEEP_SKY_READING_DEBIT'
           OR d.account_id <> NEW.account_id
           OR NEW.delta <> -d.delta
           OR NEW.reference_id <> d.entry_id THEN
            RAISE EXCEPTION 'reading debit restoration must exactly reverse its referenced debit';
        END IF;
        -- Only an order that is still reconciling may enter the terminal non-delivery
        -- path. A fulfilled order keeps its historical purchase effect and is not a
        -- candidate for D2-B debit restoration.
        IF NOT EXISTS (
            SELECT 1 FROM ce_deep_sky_order o
             WHERE o.logical_purchase_id = d.reference_id
               AND o.account_id = NEW.account_id
               AND o.reading_debit_entry_id = d.entry_id
               AND o.status IN ('DEBIT_COMMITTED', 'RECONCILIATION_REQUIRED')
        ) THEN
            RAISE EXCEPTION 'reading debit restoration requires a non-fulfilled, unresolved order';
        END IF;
        SELECT * INTO f
          FROM ce_terminal_failure_evidence
         WHERE logical_purchase_id = d.reference_id
         FOR KEY SHARE;
        IF NOT FOUND
           OR NOT f.no_valid_reading_accessible
           OR NOT f.no_operation_can_still_deliver
           OR NOT f.no_entitlement_exists
           OR NOT f.all_relevant_operations_closed
           OR f.evidence_reference = '' THEN
            RAISE EXCEPTION 'reading debit restoration requires complete terminal-failure evidence';
        END IF;
        IF EXISTS (
            SELECT 1 FROM ce_reading_entitlement e
             WHERE e.logical_purchase_id = d.reference_id
        ) THEN
            RAISE EXCEPTION 'cannot restore a reading debit when a reading entitlement exists';
        END IF;
    END IF;
    RETURN NEW;
END;
$CE$ LANGUAGE plpgsql;

CREATE TRIGGER ce_credit_ledger_entry_validate
BEFORE INSERT ON ce_credit_ledger_entry
FOR EACH ROW EXECUTE FUNCTION ce_validate_credit_ledger_entry();

CREATE FUNCTION ce_immutable_credit_ledger_entry() RETURNS trigger AS $CE$
BEGIN
    RAISE EXCEPTION 'credit ledger entries are append-only';
END;
$CE$ LANGUAGE plpgsql;

CREATE TRIGGER ce_credit_ledger_entry_no_update
BEFORE UPDATE OR DELETE ON ce_credit_ledger_entry
FOR EACH ROW EXECUTE FUNCTION ce_immutable_credit_ledger_entry();

-- A debit restoration and terminal non-delivery must commit atomically. The deferred
-- constraint trigger prevents an autocommitted Credits restoration from leaving the
-- order active or unresolved if the terminal state transition never commits.
CREATE FUNCTION ce_validate_restoration_commits_terminal_order() RETURNS trigger AS $CE$
DECLARE
    o ce_deep_sky_order%ROWTYPE;
BEGIN
    SELECT * INTO o
      FROM ce_deep_sky_order
     WHERE reading_debit_entry_id = NEW.parent_entry_id;
    IF NOT FOUND
       OR o.account_id <> NEW.account_id
       OR o.status <> 'TERMINAL_NONDELIVERY' THEN
        RAISE EXCEPTION 'reading debit restoration must commit atomically with terminal non-delivery';
    END IF;
    RETURN NULL;
END;
$CE$ LANGUAGE plpgsql;

CREATE CONSTRAINT TRIGGER ce_restoration_requires_terminal_order
AFTER INSERT ON ce_credit_ledger_entry
DEFERRABLE INITIALLY DEFERRED
FOR EACH ROW
WHEN (NEW.entry_type = 'DEEP_SKY_READING_DEBIT_RESTORATION')
EXECUTE FUNCTION ce_validate_restoration_commits_terminal_order();

CREATE FUNCTION ce_validate_topup_transition() RETURNS trigger AS $CE$
BEGIN
    IF NEW.logical_topup_id <> OLD.logical_topup_id
       OR NEW.account_id <> OLD.account_id
       OR NEW.idempotency_key <> OLD.idempotency_key
       OR NEW.sku_id <> OLD.sku_id
       OR NEW.sku_revision <> OLD.sku_revision
       OR NEW.amount_minor <> OLD.amount_minor
       OR NEW.currency <> OLD.currency
       OR NEW.credits_to_grant <> OLD.credits_to_grant
       OR NEW.created_at <> OLD.created_at THEN
        RAISE EXCEPTION 'server-owned top-up identity and commercial terms are immutable';
    END IF;
    IF OLD.provider_transaction_ref IS NOT NULL
       AND (NEW.provider_transaction_ref <> OLD.provider_transaction_ref
            OR NEW.provider_name <> OLD.provider_name) THEN
        RAISE EXCEPTION 'provider transaction identity cannot be silently replaced';
    END IF;
    IF OLD.status = 'CREDIT_FULFILLED' AND NEW.status <> OLD.status THEN
        RAISE EXCEPTION 'fulfilled top-up state is immutable; use a separate remedy record';
    END IF;
    IF NEW.status = 'CREDIT_FULFILLED' AND OLD.status <> 'CREDIT_FULFILLED' THEN
        IF NEW.completed_at IS NULL OR NOT EXISTS (
            SELECT 1 FROM ce_credit_ledger_entry le
             WHERE le.entry_type = 'TOPUP_CREDIT_GRANT'
               AND le.reference_id = NEW.logical_topup_id
               AND le.account_id = NEW.account_id
               AND le.delta = NEW.credits_to_grant
        ) THEN
            RAISE EXCEPTION 'top-up cannot be fulfilled without its one matching committed credit grant';
        END IF;
    END IF;
    RETURN NEW;
END;
$CE$ LANGUAGE plpgsql;

CREATE TRIGGER ce_topup_order_validate_transition
BEFORE UPDATE ON ce_topup_order
FOR EACH ROW EXECUTE FUNCTION ce_validate_topup_transition();

-- Record failure observation monotonically; recovery after failure needs authoritative lookup.
CREATE OR REPLACE FUNCTION ce_validate_topup_transition() RETURNS trigger AS $CE$
BEGIN
    IF NEW.logical_topup_id <> OLD.logical_topup_id
       OR NEW.account_id <> OLD.account_id
       OR NEW.idempotency_key <> OLD.idempotency_key
       OR NEW.sku_id <> OLD.sku_id
       OR NEW.sku_revision <> OLD.sku_revision
       OR NEW.amount_minor <> OLD.amount_minor
       OR NEW.currency <> OLD.currency
       OR NEW.credits_to_grant <> OLD.credits_to_grant
       OR NEW.created_at <> OLD.created_at THEN
        RAISE EXCEPTION 'server-owned top-up identity and commercial terms are immutable';
    END IF;
    IF OLD.provider_transaction_ref IS NOT NULL
       AND (NEW.provider_transaction_ref <> OLD.provider_transaction_ref
            OR NEW.provider_name <> OLD.provider_name) THEN
        RAISE EXCEPTION 'provider transaction identity cannot be silently replaced';
    END IF;
    IF OLD.status = 'CREDIT_FULFILLED' AND NEW.status <> OLD.status THEN
        RAISE EXCEPTION 'fulfilled top-up state is immutable; use a separate remedy record';
    END IF;
    NEW.failure_observed := OLD.failure_observed OR NEW.status = 'PAYMENT_FAILED';
    IF NEW.status = 'PAYMENT_CONFIRMED' AND OLD.failure_observed
       AND NOT EXISTS (
          SELECT 1 FROM ce_provider_event e
           WHERE e.logical_topup_id = NEW.logical_topup_id
             AND e.provider_name = NEW.provider_name
             AND e.provider_transaction_ref = NEW.provider_transaction_ref
             AND e.observed_status = 'SUCCEEDED'
             AND e.observation_source = 'AUTHORITATIVE_STATUS_LOOKUP'
       ) THEN
        RAISE EXCEPTION 'success after a prior failure requires authoritative status lookup';
    END IF;
    IF NEW.status = 'PAYMENT_CONFIRMED'
       AND NOT EXISTS (
          SELECT 1 FROM ce_provider_event e
           WHERE e.logical_topup_id = NEW.logical_topup_id
             AND e.provider_name = NEW.provider_name
             AND e.provider_transaction_ref = NEW.provider_transaction_ref
             AND e.observed_status = 'SUCCEEDED'
       ) THEN
        RAISE EXCEPTION 'payment confirmation requires a matching provider success observation';
    END IF;
    IF NEW.status = 'PAYMENT_FAILED'
       AND NOT EXISTS (
          SELECT 1 FROM ce_provider_event e
           WHERE e.logical_topup_id = NEW.logical_topup_id
             AND e.provider_name = NEW.provider_name
             AND e.provider_transaction_ref = NEW.provider_transaction_ref
             AND e.observed_status = 'FAILED'
       ) THEN
        RAISE EXCEPTION 'payment failure requires a matching provider failure observation';
    END IF;
    IF NEW.status = 'CREDIT_FULFILLED' AND OLD.status <> 'CREDIT_FULFILLED' THEN
        IF NEW.completed_at IS NULL OR NOT EXISTS (
            SELECT 1 FROM ce_credit_ledger_entry le
             WHERE le.entry_type = 'TOPUP_CREDIT_GRANT'
               AND le.reference_id = NEW.logical_topup_id
               AND le.account_id = NEW.account_id
               AND le.delta = NEW.credits_to_grant
        ) THEN
            RAISE EXCEPTION 'top-up cannot be fulfilled without its one matching committed credit grant';
        END IF;
    END IF;
    RETURN NEW;
END;
$CE$ LANGUAGE plpgsql;

CREATE FUNCTION ce_validate_order_transition() RETURNS trigger AS $CE$
BEGIN
    IF NEW.logical_purchase_id <> OLD.logical_purchase_id
       OR NEW.account_id <> OLD.account_id
       OR NEW.service_date_utc <> OLD.service_date_utc
       OR NEW.created_at <> OLD.created_at
       OR NEW.cap_trigger_decision <> OLD.cap_trigger_decision THEN
        RAISE EXCEPTION 'logical purchase identity, account, service date, and selected D1 policy are immutable';
    END IF;
    IF OLD.reading_debit_entry_id IS NOT NULL
       AND NEW.reading_debit_entry_id IS DISTINCT FROM OLD.reading_debit_entry_id THEN
        RAISE EXCEPTION 'committed reading debit identity is immutable';
    END IF;
    IF OLD.status = 'FULFILLED' AND NEW.status <> OLD.status THEN
        RAISE EXCEPTION 'fulfilled order history is immutable; use a separate remedy record';
    END IF;
    -- D2-B terminal non-delivery closes the logical purchase permanently. A restored
    -- debit cannot be reactivated into a payable/fulfillable state or gain a new entitlement.
    IF OLD.status = 'TERMINAL_NONDELIVERY'
       AND (
           NEW.status IS DISTINCT FROM OLD.status
           OR NEW.quota_effect IS DISTINCT FROM OLD.quota_effect
           OR NEW.completed_at IS DISTINCT FROM OLD.completed_at
       ) THEN
        RAISE EXCEPTION 'terminal non-delivery is immutable; create a separately authorized new logical purchase';
    END IF;
    IF NEW.status = 'RESERVED' AND NEW.reading_debit_entry_id IS NOT NULL THEN
        RAISE EXCEPTION 'a RESERVED order cannot already carry a committed reading debit';
    END IF;
    IF NEW.status = 'DEBIT_COMMITTED' AND NEW.reading_debit_entry_id IS NULL THEN
        RAISE EXCEPTION 'D1-A requires the committed reading debit on the effective-purchase transition';
    END IF;
    IF NEW.reading_debit_entry_id IS NOT NULL AND NOT EXISTS (
        SELECT 1 FROM ce_credit_ledger_entry le
         WHERE le.entry_id = NEW.reading_debit_entry_id
           AND le.account_id = NEW.account_id
           AND le.entry_type = 'DEEP_SKY_READING_DEBIT'
           AND le.reference_id = NEW.logical_purchase_id
    ) THEN
        RAISE EXCEPTION 'order debit reference does not match its ledger debit';
    END IF;
    -- D1-A: once the verified reading debit is bound, the daily cap effect is true.
    -- D2-B: validated terminal non-delivery removes that effect only after evidence
    -- and exact restoration pass the terminal-state guard below.
    IF NEW.status = 'TERMINAL_NONDELIVERY' THEN
        NEW.quota_effect := FALSE;
    ELSIF NEW.reading_debit_entry_id IS NOT NULL THEN
        NEW.quota_effect := TRUE;
    ELSIF NEW.quota_effect IS TRUE THEN
        RAISE EXCEPTION 'a daily-cap effect cannot exist without a committed reading debit';
    END IF;
    IF NEW.status = 'FULFILLED' AND OLD.status <> 'FULFILLED' THEN
        IF NEW.reading_debit_entry_id IS NULL OR NEW.completed_at IS NULL
           OR NOT EXISTS (
             SELECT 1 FROM ce_reading_entitlement e
              WHERE e.logical_purchase_id = NEW.logical_purchase_id
                AND e.account_id = NEW.account_id
                AND e.validated_at IS NOT NULL
                AND e.accessible_at IS NOT NULL
           ) THEN
            RAISE EXCEPTION 'order cannot be fulfilled without a committed debit and accessible validated entitlement';
        END IF;
    END IF;
    IF NEW.status = 'TERMINAL_NONDELIVERY' AND OLD.status <> 'TERMINAL_NONDELIVERY' THEN
        IF NEW.reading_debit_entry_id IS NULL
           OR EXISTS (
             SELECT 1 FROM ce_reading_entitlement e
              WHERE e.logical_purchase_id = NEW.logical_purchase_id
           )
           OR NOT EXISTS (
             SELECT 1 FROM ce_terminal_failure_evidence f
              WHERE f.logical_purchase_id = NEW.logical_purchase_id
                AND f.no_valid_reading_accessible
                AND f.no_operation_can_still_deliver
                AND f.no_entitlement_exists
                AND f.all_relevant_operations_closed
                AND f.evidence_reference <> ''
           )
           OR NOT EXISTS (
             SELECT 1 FROM ce_credit_ledger_entry restoration
              JOIN ce_credit_ledger_entry debit
                ON debit.entry_id = restoration.parent_entry_id
              WHERE restoration.entry_type = 'DEEP_SKY_READING_DEBIT_RESTORATION'
                AND restoration.parent_entry_id = NEW.reading_debit_entry_id
                AND debit.reference_id = NEW.logical_purchase_id
                AND restoration.account_id = NEW.account_id
                AND restoration.delta = -debit.delta
           ) THEN
            RAISE EXCEPTION 'terminal non-delivery requires no entitlement, complete evidence, and exact restoration';
        END IF;
    END IF;
    RETURN NEW;
END;
$CE$ LANGUAGE plpgsql;

CREATE TRIGGER ce_deep_sky_order_validate_transition
BEFORE UPDATE ON ce_deep_sky_order
FOR EACH ROW EXECUTE FUNCTION ce_validate_order_transition();

CREATE FUNCTION ce_validate_quota_event() RETURNS trigger AS $CE$
DECLARE
    o ce_deep_sky_order%ROWTYPE;
    utc_today DATE;
BEGIN
    utc_today := (statement_timestamp() AT TIME ZONE 'UTC')::date;
    SELECT * INTO o FROM ce_deep_sky_order
     WHERE logical_purchase_id = NEW.logical_purchase_id
     FOR KEY SHARE;
    IF NOT FOUND OR o.account_id <> NEW.account_id OR o.service_date_utc <> NEW.service_date_utc THEN
        RAISE EXCEPTION 'quota event must match its immutable order, account, and service date';
    END IF;
    IF NEW.event_type IN ('SLOT_RELEASED', 'SLOT_EXPIRED_UNTRANSFERRED') THEN
        IF NEW.policy_decision_reference IS NULL OR btrim(NEW.policy_decision_reference) = ''
           OR NEW.terminal_evidence_reference IS NULL OR btrim(NEW.terminal_evidence_reference) = ''
           OR o.status <> 'TERMINAL_NONDELIVERY'
           OR EXISTS (
             SELECT 1 FROM ce_reading_entitlement e
              WHERE e.logical_purchase_id = NEW.logical_purchase_id
           )
           OR NOT EXISTS (
             SELECT 1 FROM ce_terminal_failure_evidence f
              WHERE f.logical_purchase_id = NEW.logical_purchase_id
                AND f.no_valid_reading_accessible
                AND f.no_operation_can_still_deliver
                AND f.no_entitlement_exists
                AND f.all_relevant_operations_closed
                AND f.evidence_reference = NEW.terminal_evidence_reference
           )
           OR NOT EXISTS (
             SELECT 1 FROM ce_credit_ledger_entry restoration
              WHERE restoration.entry_type = 'DEEP_SKY_READING_DEBIT_RESTORATION'
                AND restoration.reference_id = o.reading_debit_entry_id
                AND restoration.account_id = o.account_id
                AND restoration.delta > 0
                AND restoration.parent_entry_id = o.reading_debit_entry_id
           ) THEN
            RAISE EXCEPTION 'terminal slot transition requires complete failure evidence, exact restoration, and policy reference';
        END IF;
        IF NEW.event_type = 'SLOT_RELEASED' AND NEW.service_date_utc <> utc_today THEN
            RAISE EXCEPTION 'D2-B permits release only while the original UTC service date is current';
        ELSIF NEW.event_type = 'SLOT_EXPIRED_UNTRANSFERRED' AND NEW.service_date_utc >= utc_today THEN
            RAISE EXCEPTION 'a slot may be marked expired-untransferred only after its original UTC date';
        END IF;
    END IF;
    RETURN NEW;
END;
$CE$ LANGUAGE plpgsql;

CREATE TRIGGER ce_quota_event_validate
BEFORE INSERT ON ce_quota_event
FOR EACH ROW EXECUTE FUNCTION ce_validate_quota_event();

CREATE FUNCTION ce_validate_daily_slot() RETURNS trigger AS $CE$
DECLARE
    o ce_deep_sky_order%ROWTYPE;
    utc_today DATE;
BEGIN
    utc_today := (statement_timestamp() AT TIME ZONE 'UTC')::date;
    SELECT * INTO o FROM ce_deep_sky_order
     WHERE logical_purchase_id = NEW.active_logical_purchase_id
     FOR KEY SHARE;
    IF NOT FOUND OR o.account_id <> NEW.account_id OR o.service_date_utc <> NEW.service_date_utc THEN
        RAISE EXCEPTION 'daily slot must match the order account and immutable UTC service date';
    END IF;
    IF NEW.slot_state = 'CONSUMED' AND o.quota_effect IS DISTINCT FROM TRUE THEN
        RAISE EXCEPTION 'slot cannot be marked consumed before an explicit cap effect is established';
    END IF;
    IF TG_OP = 'UPDATE' AND OLD.slot_state = 'RELEASED' AND NEW.slot_state = 'RESERVED' THEN
        IF NEW.service_date_utc <> utc_today
           OR NEW.active_logical_purchase_id = OLD.active_logical_purchase_id
           OR NEW.state_version <> OLD.state_version + 1
           OR NOT EXISTS (
             SELECT 1 FROM ce_quota_event e
              WHERE e.logical_purchase_id = OLD.active_logical_purchase_id
                AND e.account_id = OLD.account_id
                AND e.service_date_utc = OLD.service_date_utc
                AND e.event_type = 'SLOT_RELEASED'
                AND e.policy_decision_reference IS NOT NULL
                AND e.terminal_evidence_reference IS NOT NULL
           ) THEN
            RAISE EXCEPTION 'same-date slot reuse requires D2-B release evidence and a versioned new reservation';
        END IF;
    END IF;
    IF NEW.slot_state = 'RELEASED' AND NEW.service_date_utc <> utc_today THEN
        RAISE EXCEPTION 'D2-B releases only the current UTC service date; do not transfer expired slots';
    END IF;
    IF NEW.slot_state = 'EXPIRED_UNTRANSFERRED' AND NEW.service_date_utc >= utc_today THEN
        RAISE EXCEPTION 'slot expiry requires the original UTC service date to have passed';
    END IF;
    IF NEW.slot_state = 'RELEASED' AND NOT EXISTS (
        SELECT 1 FROM ce_quota_event e
         WHERE e.logical_purchase_id = NEW.active_logical_purchase_id
           AND e.account_id = NEW.account_id
           AND e.service_date_utc = NEW.service_date_utc
           AND e.event_type = 'SLOT_RELEASED'
           AND e.policy_decision_reference IS NOT NULL
           AND e.terminal_evidence_reference IS NOT NULL
    ) THEN
        RAISE EXCEPTION 'released slot requires an append-only quota event with policy/evidence references';
    END IF;
    IF NEW.slot_state = 'EXPIRED_UNTRANSFERRED' AND NOT EXISTS (
        SELECT 1 FROM ce_quota_event e
         WHERE e.logical_purchase_id = NEW.active_logical_purchase_id
           AND e.account_id = NEW.account_id
           AND e.service_date_utc = NEW.service_date_utc
           AND e.event_type = 'SLOT_EXPIRED_UNTRANSFERRED'
           AND e.policy_decision_reference IS NOT NULL
           AND e.terminal_evidence_reference IS NOT NULL
    ) THEN
        RAISE EXCEPTION 'expired slot requires an append-only quota event documenting no transfer';
    END IF;
    RETURN NEW;
END;
$CE$ LANGUAGE plpgsql;

CREATE TRIGGER ce_daily_purchase_slot_validate
BEFORE INSERT OR UPDATE ON ce_daily_purchase_slot
FOR EACH ROW EXECUTE FUNCTION ce_validate_daily_slot();

CREATE FUNCTION ce_immutable_provider_event() RETURNS trigger AS $CE$
BEGIN
    RAISE EXCEPTION 'provider event evidence is append-only';
END;
$CE$ LANGUAGE plpgsql;

CREATE TRIGGER ce_provider_event_no_update
BEFORE UPDATE OR DELETE ON ce_provider_event
FOR EACH ROW EXECUTE FUNCTION ce_immutable_provider_event();

CREATE FUNCTION ce_immutable_quota_event() RETURNS trigger AS $CE$
BEGIN
    RAISE EXCEPTION 'quota event evidence is append-only';
END;
$CE$ LANGUAGE plpgsql;

CREATE TRIGGER ce_quota_event_no_update
BEFORE UPDATE OR DELETE ON ce_quota_event
FOR EACH ROW EXECUTE FUNCTION ce_immutable_quota_event();


CREATE FUNCTION ce_validate_entitlement_insert() RETURNS trigger AS $$
DECLARE
    o ce_deep_sky_order%ROWTYPE;
BEGIN
    SELECT * INTO o
      FROM ce_deep_sky_order
     WHERE logical_purchase_id = NEW.logical_purchase_id
     FOR UPDATE;
    IF NOT FOUND
       OR o.account_id <> NEW.account_id
       OR o.status NOT IN ('DEBIT_COMMITTED', 'RECONCILIATION_REQUIRED')
       OR o.reading_debit_entry_id IS NULL
       OR NOT EXISTS (
          SELECT 1 FROM ce_credit_ledger_entry le
           WHERE le.entry_id = o.reading_debit_entry_id
             AND le.account_id = o.account_id
             AND le.entry_type = 'DEEP_SKY_READING_DEBIT'
             AND le.reference_id = o.logical_purchase_id
       )
       OR EXISTS (
          SELECT 1 FROM ce_credit_ledger_entry restoration
           WHERE restoration.entry_type = 'DEEP_SKY_READING_DEBIT_RESTORATION'
             AND restoration.parent_entry_id = o.reading_debit_entry_id
             AND restoration.reference_id = o.reading_debit_entry_id
             AND restoration.account_id = o.account_id
             AND restoration.delta > 0
       ) THEN
        RAISE EXCEPTION 'entitlement requires an active order with a committed, unrestored reading debit';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER ce_reading_entitlement_validate_insert
BEFORE INSERT ON ce_reading_entitlement
FOR EACH ROW EXECUTE FUNCTION ce_validate_entitlement_insert();

CREATE FUNCTION ce_immutable_terminal_failure_evidence() RETURNS trigger AS $$
BEGIN
    RAISE EXCEPTION 'terminal failure evidence is append-only';
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER ce_terminal_failure_evidence_no_update
BEFORE UPDATE OR DELETE ON ce_terminal_failure_evidence
FOR EACH ROW EXECUTE FUNCTION ce_immutable_terminal_failure_evidence();


CREATE FUNCTION ce_immutable_credits_sku() RETURNS trigger AS $CE$
BEGIN
    RAISE EXCEPTION 'a published SKU revision is immutable; publish a new revision instead';
END;
$CE$ LANGUAGE plpgsql;

CREATE TRIGGER ce_credits_sku_no_update
BEFORE UPDATE OR DELETE ON ce_credits_sku
FOR EACH ROW EXECUTE FUNCTION ce_immutable_credits_sku();

CREATE FUNCTION ce_validate_topup_insert() RETURNS trigger AS $CE$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM ce_credits_sku s
         WHERE s.sku_id = NEW.sku_id
           AND s.sku_revision = NEW.sku_revision
           AND s.sku_status = 'AVAILABLE'
           AND s.amount_minor = NEW.amount_minor
           AND s.currency = NEW.currency
           AND s.credits_granted = NEW.credits_to_grant
    ) THEN
        RAISE EXCEPTION 'top-up terms must exactly match an available immutable server-owned SKU revision';
    END IF;
    RETURN NEW;
END;
$CE$ LANGUAGE plpgsql;

CREATE TRIGGER ce_topup_order_validate_insert
BEFORE INSERT ON ce_topup_order
FOR EACH ROW EXECUTE FUNCTION ce_validate_topup_insert();

CREATE FUNCTION ce_validate_provider_event_insert() RETURNS trigger AS $CE$
DECLARE
    t ce_topup_order%ROWTYPE;
BEGIN
    SELECT * INTO t FROM ce_topup_order
     WHERE logical_topup_id = NEW.logical_topup_id
     FOR KEY SHARE;
    IF NOT FOUND
       OR t.provider_name <> NEW.provider_name
       OR t.provider_transaction_ref <> NEW.provider_transaction_ref
       OR t.amount_minor <> NEW.verified_amount_minor
       OR t.currency <> NEW.verified_currency
       OR NEW.verification_reference = '' THEN
        RAISE EXCEPTION 'provider observation must match the bound order, transaction, amount, currency, and verification reference';
    END IF;
    RETURN NEW;
END;
$CE$ LANGUAGE plpgsql;

CREATE TRIGGER ce_provider_event_validate_insert
BEFORE INSERT ON ce_provider_event
FOR EACH ROW EXECUTE FUNCTION ce_validate_provider_event_insert();
