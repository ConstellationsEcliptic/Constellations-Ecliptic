-- CE commerce persistence contract candidate R0.
-- PostgreSQL syntax; candidate-only. D1/D2 policy is intentionally not selected here.
-- Production use requires approved policy, schema review, migrations, access controls,
-- data-retention review, and concurrency/recovery testing beyond this prototype.

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

CREATE TABLE ce_deep_sky_order (
    logical_purchase_id TEXT PRIMARY KEY,
    account_id TEXT NOT NULL,
    service_date_utc DATE NOT NULL,
    status TEXT NOT NULL CHECK (status IN (
        'RESERVED', 'DEBIT_COMMITTED', 'RECONCILIATION_REQUIRED',
        'FULFILLED', 'TERMINAL_NONDELIVERY', 'RESERVATION_REJECTED'
    )),
    cap_trigger_decision TEXT CHECK (
        cap_trigger_decision IS NULL OR cap_trigger_decision IN ('D1_A', 'D1_B')
    ),
    quota_effect BOOLEAN,
    reading_debit_entry_id TEXT UNIQUE REFERENCES ce_credit_ledger_entry(entry_id),
    created_at TIMESTAMPTZ NOT NULL,
    completed_at TIMESTAMPTZ,
    CHECK (
      (status = 'FULFILLED' AND completed_at IS NOT NULL)
      OR (status <> 'FULFILLED' AND completed_at IS NULL)
    )
);

-- Exactly one current slot record per authenticated account and UTC service date.
-- Business logic must lock this row and consult the approved D1/D2 policy before
-- making a transition. This table does not choose whether a terminally reversed
-- purchase consumes the cap.
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
CREATE FUNCTION ce_validate_credit_ledger_entry() RETURNS trigger AS $
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
        PERFORM 1
          FROM ce_deep_sky_order o
         WHERE o.logical_purchase_id = NEW.reference_id
           AND o.account_id = NEW.account_id
           AND o.status = 'RESERVED'
         FOR UPDATE;
        IF NOT FOUND THEN
            RAISE EXCEPTION 'reading debit must match a reserved order for the same account';
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
$ LANGUAGE plpgsql;

CREATE TRIGGER ce_credit_ledger_entry_validate
BEFORE INSERT ON ce_credit_ledger_entry
FOR EACH ROW EXECUTE FUNCTION ce_validate_credit_ledger_entry();

CREATE FUNCTION ce_immutable_credit_ledger_entry() RETURNS trigger AS $
BEGIN
    RAISE EXCEPTION 'credit ledger entries are append-only';
END;
$ LANGUAGE plpgsql;

CREATE TRIGGER ce_credit_ledger_entry_no_update
BEFORE UPDATE OR DELETE ON ce_credit_ledger_entry
FOR EACH ROW EXECUTE FUNCTION ce_immutable_credit_ledger_entry();

CREATE FUNCTION ce_validate_topup_transition() RETURNS trigger AS $
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
$ LANGUAGE plpgsql;

CREATE TRIGGER ce_topup_order_validate_transition
BEFORE UPDATE ON ce_topup_order
FOR EACH ROW EXECUTE FUNCTION ce_validate_topup_transition();

CREATE FUNCTION ce_validate_order_transition() RETURNS trigger AS $
BEGIN
    IF NEW.logical_purchase_id <> OLD.logical_purchase_id
       OR NEW.account_id <> OLD.account_id
       OR NEW.service_date_utc <> OLD.service_date_utc
       OR NEW.created_at <> OLD.created_at THEN
        RAISE EXCEPTION 'logical purchase identity, account, and service date are immutable';
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
$ LANGUAGE plpgsql;

CREATE TRIGGER ce_deep_sky_order_validate_transition
BEFORE UPDATE ON ce_deep_sky_order
FOR EACH ROW EXECUTE FUNCTION ce_validate_order_transition();

CREATE FUNCTION ce_validate_quota_event() RETURNS trigger AS $
DECLARE
    o ce_deep_sky_order%ROWTYPE;
BEGIN
    SELECT * INTO o FROM ce_deep_sky_order
     WHERE logical_purchase_id = NEW.logical_purchase_id
     FOR KEY SHARE;
    IF NOT FOUND OR o.account_id <> NEW.account_id OR o.service_date_utc <> NEW.service_date_utc THEN
        RAISE EXCEPTION 'quota event must match its immutable order, account, and service date';
    END IF;
    IF NEW.event_type = 'SLOT_RELEASED' THEN
        IF NEW.policy_decision_reference IS NULL OR NEW.terminal_evidence_reference IS NULL
           OR o.status <> 'TERMINAL_NONDELIVERY'
           OR EXISTS (
             SELECT 1 FROM ce_reading_entitlement e
              WHERE e.logical_purchase_id = NEW.logical_purchase_id
           )
           OR NOT EXISTS (
             SELECT 1 FROM ce_credit_ledger_entry restoration
              WHERE restoration.entry_type = 'DEEP_SKY_READING_DEBIT_RESTORATION'
                AND restoration.reference_id = o.reading_debit_entry_id
                AND restoration.account_id = o.account_id
           ) THEN
            RAISE EXCEPTION 'slot release requires explicit policy, terminal evidence, and exact restoration';
        END IF;
    END IF;
    RETURN NEW;
END;
$ LANGUAGE plpgsql;

CREATE TRIGGER ce_quota_event_validate
BEFORE INSERT ON ce_quota_event
FOR EACH ROW EXECUTE FUNCTION ce_validate_quota_event();

CREATE FUNCTION ce_validate_daily_slot() RETURNS trigger AS $
DECLARE
    o ce_deep_sky_order%ROWTYPE;
BEGIN
    SELECT * INTO o FROM ce_deep_sky_order
     WHERE logical_purchase_id = NEW.active_logical_purchase_id
     FOR KEY SHARE;
    IF NOT FOUND OR o.account_id <> NEW.account_id OR o.service_date_utc <> NEW.service_date_utc THEN
        RAISE EXCEPTION 'daily slot must match the order account and immutable UTC service date';
    END IF;
    IF NEW.slot_state = 'CONSUMED' AND o.quota_effect IS DISTINCT FROM TRUE THEN
        RAISE EXCEPTION 'slot cannot be marked consumed before an explicit cap effect is established';
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
    RETURN NEW;
END;
$ LANGUAGE plpgsql;

CREATE TRIGGER ce_daily_purchase_slot_validate
BEFORE INSERT OR UPDATE ON ce_daily_purchase_slot
FOR EACH ROW EXECUTE FUNCTION ce_validate_daily_slot();

CREATE FUNCTION ce_immutable_provider_event() RETURNS trigger AS $
BEGIN
    RAISE EXCEPTION 'provider event evidence is append-only';
END;
$ LANGUAGE plpgsql;

CREATE TRIGGER ce_provider_event_no_update
BEFORE UPDATE OR DELETE ON ce_provider_event
FOR EACH ROW EXECUTE FUNCTION ce_immutable_provider_event();

CREATE FUNCTION ce_immutable_quota_event() RETURNS trigger AS $
BEGIN
    RAISE EXCEPTION 'quota event evidence is append-only';
END;
$ LANGUAGE plpgsql;

CREATE TRIGGER ce_quota_event_no_update
BEFORE UPDATE OR DELETE ON ce_quota_event
FOR EACH ROW EXECUTE FUNCTION ce_immutable_quota_event();
