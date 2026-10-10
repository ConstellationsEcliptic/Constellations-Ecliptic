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
        'PAYMENT_PENDING', 'RECONCILIATION_REQUIRED',
        'PAYMENT_FAILED', 'CREDIT_FULFILLED'
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
