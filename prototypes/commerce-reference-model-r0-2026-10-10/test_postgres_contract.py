"""Integration tests for candidate persistence invariants against PostgreSQL."""
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timedelta, timezone
import os
from pathlib import Path
import threading
import time
import unittest
import uuid

import psycopg
from psycopg import errors

DATABASE_URL = os.environ.get("CE_TEST_DATABASE_URL")
SCHEMA_SQL = Path(__file__).with_name("postgres_schema_candidate.sql").read_text(encoding="utf-8")
UTC = timezone.utc
NOW = datetime.now(UTC).replace(microsecond=0)
SERVICE_DATE = NOW.date()


@unittest.skipUnless(DATABASE_URL, "CE_TEST_DATABASE_URL is not set; PostgreSQL integration tests skipped")
class PostgresCommerceContractTests(unittest.TestCase):
    def setUp(self):
        self.schema = "ce_test_" + uuid.uuid4().hex
        self.conn = psycopg.connect(DATABASE_URL, autocommit=True)
        self.conn.execute(f'CREATE SCHEMA "{self.schema}"')
        self.conn.execute(f'SET search_path TO "{self.schema}"')
        self.conn.execute(SCHEMA_SQL, prepare=False)
        self.conn.execute(
            """INSERT INTO ce_credits_sku
            (sku_id, sku_revision, amount_minor, currency, credits_granted, sku_status, created_at)
            VALUES ('sku-test','r0',299,'USD',4,'AVAILABLE',%s)""",
            (NOW,),
        )

    def tearDown(self):
        self.conn.execute("SET search_path TO public")
        self.conn.execute(f'DROP SCHEMA IF EXISTS "{self.schema}" CASCADE')
        self.conn.close()

    def set_admission_state(self, new_state, *, reason, health_reference=None, lease_seconds=300):
        current = self.conn.execute(
            "SELECT admission_state, state_version FROM ce_purchase_admission_state WHERE singleton_id=1"
        ).fetchone()
        previous_state, previous_version = current
        changed_at = datetime.now(UTC)
        expires = (
            changed_at + timedelta(seconds=lease_seconds)
            if new_state == "READY" else None
        )
        event_id = "admission-" + uuid.uuid4().hex
        self.conn.execute(
            """INSERT INTO ce_purchase_admission_event
               (event_id, singleton_id, state_version, previous_state, new_state,
                reason_reference, health_attestation_reference, ready_expires_at,
                actor_reference, changed_at)
               VALUES (%s,1,%s,%s,%s,%s,%s,%s,'test-operator',%s)""",
            (event_id, previous_version + 1, previous_state, new_state,
             reason, health_reference if new_state == "READY" else None, expires, changed_at),
        )
        updated = self.conn.execute(
            "SELECT admission_state, state_version FROM ce_purchase_admission_state WHERE singleton_id=1"
        ).fetchone()
        self.assertEqual(updated, (new_state, previous_version + 1))
        return expires

    def insert_topup(self, topup_id="topup-1", account="acct-1", idem="idem-1",
                     provider="provider-test", tx_ref="provider-tx-1",
                     status="PAYMENT_PENDING", amount=299, currency="USD", credits=4):
        self.conn.execute(
            """INSERT INTO ce_topup_order
            (logical_topup_id, account_id, idempotency_key, sku_id, sku_revision,
             amount_minor, currency, credits_to_grant, status, provider_name,
             provider_transaction_ref, created_at)
            VALUES (%s,%s,%s,'sku-test','r0',%s,%s,%s,%s,%s,%s,%s)""",
            (topup_id, account, idem, amount, currency, credits, status,
             provider, tx_ref, NOW),
        )

    def insert_provider_success(self, topup_id="topup-1", provider="provider-test",
                                tx_ref="provider-tx-1", event_id="evt-1",
                                amount=299, currency="USD"):
        self.conn.execute(
            """INSERT INTO ce_provider_event
            (provider_name, provider_event_id, logical_topup_id, provider_transaction_ref,
             payload_fingerprint, verified_amount_minor, verified_currency,
             observed_status, observation_source, verification_reference, received_at)
            VALUES (%s,%s,%s,%s,'sha256:fingerprint',%s,%s,'SUCCEEDED','WEBHOOK','verify-ref',%s)""",
            (provider, event_id, topup_id, tx_ref, amount, currency, NOW),
        )

    def insert_reading_order(self, order_id="order-1", account="acct-1",
                             service_date=SERVICE_DATE, status="RESERVED", ensure_ready=True,
                             reserve_slot=True):
        if ensure_ready:
            state = self.conn.execute(
                "SELECT admission_state, ready_expires_at FROM ce_purchase_admission_state WHERE singleton_id=1"
            ).fetchone()
            if (state[0] != "READY" or state[1] is None
                    or state[1] <= datetime.now(UTC)):
                self.set_admission_state(
                    "READY", reason="test-fixture-attested-ready",
                    health_reference="test-health-attestation",
                )
        self.conn.execute(
            """INSERT INTO ce_deep_sky_order
            (logical_purchase_id, account_id, service_date_utc, status, created_at)
            VALUES (%s,%s,%s,%s,%s)""",
            (order_id, account, service_date, status, NOW),
        )
        if reserve_slot:
            self.conn.execute(
                """INSERT INTO ce_daily_purchase_slot
                (account_id, service_date_utc, active_logical_purchase_id, slot_state, updated_at)
                VALUES (%s,%s,%s,'RESERVED',%s)""",
                (account, service_date, order_id, NOW),
            )

    def insert_debit_and_bind_order(self, order_id="order-1", account="acct-1",
                                    debit_id="debit-1", amount=-4):
        # The reading debit and D1-A quota effect must commit atomically with order state.
        with self.conn.transaction():
            self.conn.execute(
                """INSERT INTO ce_credit_ledger_entry
                (entry_id, account_id, entry_type, delta, reference_id, created_at)
                VALUES (%s,%s,'DEEP_SKY_READING_DEBIT',%s,%s,%s)""",
                (debit_id, account, amount, order_id, NOW),
            )
            self.conn.execute(
                """UPDATE ce_deep_sky_order
                   SET status='DEBIT_COMMITTED', reading_debit_entry_id=%s
                 WHERE logical_purchase_id=%s""",
                (debit_id, order_id),
            )

    def test_schema_creates_expected_controlled_tables(self):
        names = {
            row[0] for row in self.conn.execute(
                """SELECT table_name FROM information_schema.tables
                   WHERE table_schema=%s""", (self.schema,)
            ).fetchall()
        }
        self.assertTrue({
            "ce_credits_sku", "ce_topup_order", "ce_provider_event", "ce_credit_ledger_entry",
            "ce_deep_sky_order", "ce_daily_purchase_slot", "ce_quota_event",
            "ce_reading_entitlement", "ce_terminal_failure_evidence", "ce_purchase_admission_state",
            "ce_purchase_admission_event",
        }.issubset(names))



    def test_admission_state_cannot_change_without_matching_versioned_event(self):
        with self.assertRaises(errors.RaiseException):
            self.conn.execute(
                """UPDATE ce_purchase_admission_state
                      SET admission_state='BLOCKED', reason_reference='unsourced-direct-update',
                          state_version=1, updated_at=%s
                    WHERE singleton_id=1""",
                (NOW,),
            )
        self.assertEqual(
            self.conn.execute(
                "SELECT admission_state, state_version FROM ce_purchase_admission_state WHERE singleton_id=1"
            ).fetchone(),
            ("UNKNOWN", 0),
        )
        self.set_admission_state("BLOCKED", reason="approved-test-reason")
        event_id = self.conn.execute(
            "SELECT event_id FROM ce_purchase_admission_event WHERE state_version=1"
        ).fetchone()[0]
        with self.assertRaises(errors.RaiseException):
            self.conn.execute(
                "UPDATE ce_purchase_admission_event SET reason_reference='rewritten' WHERE event_id=%s",
                (event_id,),
            )
        with self.assertRaises(errors.RaiseException):
            self.conn.execute(
                "DELETE FROM ce_purchase_admission_event WHERE event_id=%s", (event_id,)
            )
        self.assertEqual(
            self.conn.execute("SELECT COUNT(*) FROM ce_purchase_admission_event").fetchone()[0], 1
        )
        with self.assertRaises(errors.RaiseException):
            self.conn.execute("DELETE FROM ce_purchase_admission_state WHERE singleton_id=1")
        self.assertEqual(
            self.conn.execute(
                "SELECT admission_state FROM ce_purchase_admission_state WHERE singleton_id=1"
            ).fetchone()[0],
            "BLOCKED",
        )

    def test_ready_admission_requires_health_evidence_and_expiry(self):
        with self.assertRaises(errors.RaiseException):
            self.set_admission_state(
                "READY", reason="missing-health-attestation",
                health_reference=None,
            )
        with self.assertRaises(errors.RaiseException):
            self.set_admission_state(
                "READY", reason="overlong-health-lease",
                health_reference="health-attestation-overlong",
                lease_seconds=301,
            )
        # A valid short-lived attestation is accepted, but stale readiness fails closed.
        expiry = self.set_admission_state(
            "READY", reason="short-lease-test",
            health_reference="short-lived-health-attestation", lease_seconds=0.6,
        )
        self.assertGreater(expiry, datetime.now(UTC))
        time.sleep(0.75)
        with self.assertRaises(errors.RaiseException):
            self.insert_reading_order(order_id="expired-health-order", ensure_ready=False)
        self.assertEqual(
            self.conn.execute("SELECT COUNT(*) FROM ce_deep_sky_order").fetchone()[0], 0
        )

    def test_fulfillment_health_interlock_blocks_new_order_and_effective_purchase_debit(self):
        # Schema default is UNKNOWN; non-ready states require explicit audited transition.
        initial = self.conn.execute(
            "SELECT admission_state, state_version, ready_expires_at FROM ce_purchase_admission_state WHERE singleton_id=1"
        ).fetchone()
        self.assertEqual(initial, ("UNKNOWN", 0, None))
        self.set_admission_state("BLOCKED", reason="test-service-known-unavailable")
        with self.assertRaises(errors.RaiseException):
            self.insert_reading_order(order_id="blocked-order", ensure_ready=False)
        self.assertEqual(
            self.conn.execute("SELECT COUNT(*) FROM ce_deep_sky_order").fetchone()[0], 0
        )

        self.set_admission_state(
            "READY", reason="test-service-recovered",
            health_reference="test-health-attestation",
        )
        self.insert_reading_order(order_id="accepted-before-health-change", ensure_ready=False)
        self.set_admission_state("UNKNOWN", reason="test-health-no-longer-attested")
        with self.assertRaises(errors.RaiseException):
            self.insert_debit_and_bind_order(
                order_id="accepted-before-health-change", debit_id="debit-gated"
            )
        self.assertEqual(
            self.conn.execute(
                "SELECT COUNT(*) FROM ce_credit_ledger_entry WHERE entry_type='DEEP_SKY_READING_DEBIT'"
            ).fetchone()[0],
            0,
        )
        self.set_admission_state(
            "READY", reason="test-health-explicitly-ready",
            health_reference="test-health-attestation",
        )
        self.insert_debit_and_bind_order(
            order_id="accepted-before-health-change", debit_id="debit-gated"
        )
        self.assertEqual(
            self.conn.execute(
                "SELECT COUNT(*) FROM ce_credit_ledger_entry WHERE entry_type='DEEP_SKY_READING_DEBIT'"
            ).fetchone()[0],
            1,
        )
        self.assertEqual(
            self.conn.execute(
                "SELECT quota_effect FROM ce_deep_sky_order WHERE logical_purchase_id='accepted-before-health-change'"
            ).fetchone()[0],
            True,
            "D1-A must consume quota when the reading debit is committed",
        )

        # Health admission gates only NEW purchases/debits. It must not abandon a
        # previously committed order that can still deliver a validated reading.
        self.set_admission_state("BLOCKED", reason="new-purchases-paused-during-existing-fulfillment")
        self.conn.execute(
            """INSERT INTO ce_reading_entitlement
               (entitlement_id, logical_purchase_id, account_id, reading_reference,
                reading_content_hash, validated_at, accessible_at)
               VALUES ('existing-entitlement','accepted-before-health-change','acct-1',
                       'reading-existing','hash-existing',%s,%s)""",
            (NOW, NOW),
        )
        self.conn.execute(
            """UPDATE ce_deep_sky_order
                  SET status='FULFILLED', completed_at=%s
                WHERE logical_purchase_id='accepted-before-health-change'""",
            (NOW,),
        )
        self.assertEqual(
            self.conn.execute(
                "SELECT status FROM ce_deep_sky_order WHERE logical_purchase_id='accepted-before-health-change'"
            ).fetchone()[0],
            "FULFILLED",
            "health interlock must not cancel existing fulfillable operations",
        )

    def test_topup_terms_must_match_an_available_server_owned_sku(self):
        with self.assertRaises(errors.RaiseException):
            self.insert_topup(amount=150)
        with self.assertRaises(errors.RaiseException):
            self.conn.execute(
                "UPDATE ce_credits_sku SET sku_status='RETIRED' WHERE sku_id='sku-test' AND sku_revision='r0'"
            )

    def test_provider_event_amount_and_currency_must_match_the_topup(self):
        self.insert_topup()
        with self.assertRaises(errors.RaiseException):
            self.insert_provider_success(amount=300)
        with self.assertRaises(errors.RaiseException):
            self.insert_provider_success(event_id="evt-currency", currency="IDR")
        self.assertEqual(self.conn.execute("SELECT COUNT(*) FROM ce_provider_event").fetchone()[0], 0)

    def test_account_idempotency_key_is_unique(self):
        self.insert_topup()
        with self.assertRaises(errors.UniqueViolation):
            self.insert_topup(topup_id="topup-2", idem="idem-1")

    def test_provider_transaction_reference_is_unique(self):
        self.insert_topup()
        with self.assertRaises(errors.UniqueViolation):
            self.insert_topup(topup_id="topup-2", account="acct-2", idem="idem-2")

    def test_pending_topup_cannot_receive_credit_grant(self):
        self.insert_topup()
        self.insert_provider_success()
        with self.assertRaises(errors.RaiseException):
            self.conn.execute(
                """INSERT INTO ce_credit_ledger_entry
                (entry_id, account_id, entry_type, delta, reference_id, created_at)
                VALUES ('grant-1','acct-1','TOPUP_CREDIT_GRANT',4,'topup-1',%s)""",
                (NOW,),
            )
        self.assertEqual(self.conn.execute("SELECT COUNT(*) FROM ce_credit_ledger_entry").fetchone()[0], 0)

    def test_confirmed_success_can_grant_once_then_close_fulfillment(self):
        self.insert_topup()
        self.insert_provider_success()
        self.conn.execute("UPDATE ce_topup_order SET status='PAYMENT_CONFIRMED' WHERE logical_topup_id='topup-1'")
        self.conn.execute(
            """INSERT INTO ce_credit_ledger_entry
            (entry_id, account_id, entry_type, delta, reference_id, created_at)
            VALUES ('grant-1','acct-1','TOPUP_CREDIT_GRANT',4,'topup-1',%s)""",
            (NOW,),
        )
        # A distinct ledger identity still cannot create a second grant for the same top-up.
        with self.assertRaises(errors.UniqueViolation):
            self.conn.execute(
                """INSERT INTO ce_credit_ledger_entry
                (entry_id, account_id, entry_type, delta, reference_id, created_at)
                VALUES ('grant-2','acct-1','TOPUP_CREDIT_GRANT',4,'topup-1',%s)""",
                (NOW,),
            )
        self.conn.execute(
            "UPDATE ce_topup_order SET status='CREDIT_FULFILLED', completed_at=%s WHERE logical_topup_id='topup-1'",
            (NOW,),
        )
        self.assertEqual(self.conn.execute("SELECT status FROM ce_topup_order").fetchone()[0], "CREDIT_FULFILLED")

    def test_provider_event_evidence_is_unique_and_append_only(self):
        self.insert_topup()
        self.insert_provider_success()
        with self.assertRaises(errors.UniqueViolation):
            self.insert_provider_success(event_id="evt-1")
        with self.assertRaises(errors.RaiseException):
            self.conn.execute("DELETE FROM ce_provider_event WHERE provider_event_id='evt-1'")

    def test_daily_account_date_slot_is_unique_under_concurrent_reservation(self):
        self.set_admission_state(
            "READY", reason="concurrency-test-health-ready",
            health_reference="test-health-attestation",
        )
        barrier = threading.Barrier(2)

        def attempt(order_id: str) -> bool:
            conn = psycopg.connect(DATABASE_URL, autocommit=True)
            try:
                conn.execute(f'SET search_path TO "{self.schema}"')
                try:
                    with conn.transaction():
                        conn.execute(
                            """INSERT INTO ce_deep_sky_order
                            (logical_purchase_id, account_id, service_date_utc, status, created_at)
                            VALUES (%s,'shared-acct',%s,'RESERVED',%s)""",
                            (order_id, SERVICE_DATE, NOW),
                        )
                        barrier.wait(timeout=5)
                        row = conn.execute(
                            """INSERT INTO ce_daily_purchase_slot
                            (account_id, service_date_utc, active_logical_purchase_id,
                             slot_state, updated_at)
                            VALUES ('shared-acct',%s,%s,'RESERVED',%s)
                            ON CONFLICT (account_id, service_date_utc) DO NOTHING
                            RETURNING active_logical_purchase_id""",
                            (SERVICE_DATE, order_id, NOW),
                        ).fetchone()
                        if row is None:
                            raise RuntimeError("RESERVATION_NOT_WON")
                    return True
                except RuntimeError as exc:
                    if str(exc) == "RESERVATION_NOT_WON":
                        return False
                    raise
            finally:
                conn.close()

        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(attempt, ["order-a", "order-b"]))
        self.assertEqual(sorted(results), [False, True])
        self.assertEqual(
            self.conn.execute("SELECT COUNT(*) FROM ce_daily_purchase_slot").fetchone()[0], 1
        )
        self.assertEqual(
            self.conn.execute("SELECT COUNT(*) FROM ce_deep_sky_order").fetchone()[0], 1,
            "losing reservation transaction must roll back the unreserved order",
        )

    def test_slot_cannot_be_marked_consumed_without_explicit_cap_effect(self):
        self.insert_reading_order()
        with self.assertRaises(errors.RaiseException):
            self.conn.execute(
                """UPDATE ce_daily_purchase_slot
                   SET slot_state='CONSUMED', state_version=state_version+1, updated_at=%s
                 WHERE account_id='acct-1' AND service_date_utc=%s""",
                (NOW, SERVICE_DATE),
            )

    def test_daily_slot_identity_and_active_purchase_cannot_be_rebound(self):
        self.insert_reading_order()
        self.insert_reading_order(
            order_id="order-2", account="acct-1", reserve_slot=False
        )
        self.insert_reading_order(
            order_id="order-3", account="acct-2", reserve_slot=False
        )
        with self.assertRaises(errors.RaiseException):
            self.conn.execute(
                """UPDATE ce_daily_purchase_slot
                   SET active_logical_purchase_id='order-2',
                       state_version=state_version+1
                 WHERE account_id='acct-1' AND service_date_utc=%s""",
                (SERVICE_DATE,),
            )
        with self.assertRaises(errors.RaiseException):
            self.conn.execute(
                """UPDATE ce_daily_purchase_slot
                   SET account_id='acct-2', active_logical_purchase_id='order-3',
                       state_version=state_version+1
                 WHERE account_id='acct-1' AND service_date_utc=%s""",
                (SERVICE_DATE,),
            )
        with self.assertRaises(errors.RaiseException):
            self.conn.execute(
                """UPDATE ce_daily_purchase_slot
                   SET updated_at=%s
                 WHERE account_id='acct-1' AND service_date_utc=%s""",
                (NOW, SERVICE_DATE),
            )
        with self.assertRaises(errors.RaiseException):
            self.conn.execute(
                "DELETE FROM ce_daily_purchase_slot WHERE account_id='acct-1' AND service_date_utc=%s",
                (SERVICE_DATE,),
            )
        self.assertEqual(
            self.conn.execute(
                """SELECT account_id, service_date_utc, active_logical_purchase_id, slot_state, state_version
                     FROM ce_daily_purchase_slot"""
            ).fetchone(),
            ("acct-1", SERVICE_DATE, "order-1", "RESERVED", 1),
        )

    def test_reading_debit_requires_account_day_slot_reservation(self):
        self.insert_reading_order(reserve_slot=False)
        with self.assertRaises(errors.RaiseException):
            self.insert_debit_and_bind_order()
        self.assertEqual(
            self.conn.execute(
                "SELECT status, reading_debit_entry_id FROM ce_deep_sky_order WHERE logical_purchase_id='order-1'"
            ).fetchone(),
            ("RESERVED", None),
        )
        self.assertEqual(
            self.conn.execute(
                "SELECT COUNT(*) FROM ce_credit_ledger_entry WHERE entry_type='DEEP_SKY_READING_DEBIT'"
            ).fetchone()[0],
            0,
        )

    def test_reading_entitlement_requires_bound_committed_debit(self):
        self.insert_reading_order()
        with self.assertRaises(errors.RaiseException):
            self.conn.execute(
                """INSERT INTO ce_reading_entitlement
                (entitlement_id, logical_purchase_id, account_id, reading_reference,
                 reading_content_hash, validated_at, accessible_at)
                VALUES ('ent-1','order-1','acct-1','read-1','hash-1',%s,%s)""",
                (NOW, NOW),
            )
        self.assertEqual(self.conn.execute("SELECT COUNT(*) FROM ce_reading_entitlement").fetchone()[0], 0)

    def test_fulfillment_requires_accessible_validated_entitlement(self):
        self.insert_reading_order()
        self.insert_debit_and_bind_order()
        self.conn.execute(
            """INSERT INTO ce_reading_entitlement
            (entitlement_id, logical_purchase_id, account_id, reading_reference,
             reading_content_hash, validated_at, accessible_at)
            VALUES ('ent-1','order-1','acct-1','read-1','hash-1',%s,%s)""",
            (NOW, NOW),
        )
        self.conn.execute(
            "UPDATE ce_deep_sky_order SET status='FULFILLED', completed_at=%s WHERE logical_purchase_id='order-1'",
            (NOW,),
        )
        with self.assertRaises(errors.RaiseException):
            self.conn.execute(
                "UPDATE ce_deep_sky_order SET status='DEBIT_COMMITTED' WHERE logical_purchase_id='order-1'"
            )

    def test_predebit_failure_requires_evidence_and_same_transaction_slot_release(self):
        self.insert_reading_order()
        with self.conn.transaction():
            self.conn.execute(
                """INSERT INTO ce_predebit_failure_evidence
                (logical_purchase_id, no_reading_debit_committed,
                 no_operation_can_still_commit_or_deliver, all_relevant_operations_closed,
                 evidence_reference, confirmed_at)
                VALUES ('order-1',TRUE,TRUE,TRUE,'predebit-evidence-1',%s)""",
                (NOW,),
            )
            self.conn.execute(
                "UPDATE ce_deep_sky_order SET status='RESERVATION_REJECTED' WHERE logical_purchase_id='order-1'"
            )
            self.conn.execute(
                """INSERT INTO ce_quota_event
                (quota_event_id, idempotency_key, account_id, service_date_utc,
                 logical_purchase_id, event_type, policy_decision_reference,
                 predebit_evidence_reference, occurred_at)
                VALUES ('predebit-qe-1','predebit-qe-idem-1','acct-1',%s,'order-1',
                        'PREDEBIT_RESERVATION_RELEASED','approved-predebit-policy',
                        'predebit-evidence-1',%s)""",
                (SERVICE_DATE, NOW),
            )
            self.conn.execute(
                """UPDATE ce_daily_purchase_slot
                   SET slot_state='RELEASED', state_version=state_version+1, updated_at=%s
                 WHERE account_id='acct-1' AND service_date_utc=%s""",
                (NOW, SERVICE_DATE),
            )
        self.assertEqual(
            self.conn.execute(
                "SELECT status, quota_effect, reading_debit_entry_id FROM ce_deep_sky_order WHERE logical_purchase_id='order-1'"
            ).fetchone(),
            ("RESERVATION_REJECTED", False, None),
        )
        self.assertEqual(
            self.conn.execute(
                "SELECT slot_state, state_version FROM ce_daily_purchase_slot WHERE account_id='acct-1' AND service_date_utc=%s",
                (SERVICE_DATE,),
            ).fetchone(),
            ("RELEASED", 2),
        )
        self.insert_reading_order(order_id="order-2", account="acct-1", reserve_slot=False)
        self.conn.execute(
            """UPDATE ce_daily_purchase_slot
                  SET active_logical_purchase_id='order-2', slot_state='RESERVED',
                      state_version=state_version+1, updated_at=%s
                WHERE account_id='acct-1' AND service_date_utc=%s""",
            (NOW, SERVICE_DATE),
        )
        self.assertEqual(
            self.conn.execute(
                "SELECT active_logical_purchase_id, slot_state, state_version FROM ce_daily_purchase_slot WHERE account_id='acct-1' AND service_date_utc=%s",
                (SERVICE_DATE,),
            ).fetchone(),
            ("order-2", "RESERVED", 3),
        )
        self.assertEqual(
            self.conn.execute(
                "SELECT COUNT(*) FROM ce_credit_ledger_entry WHERE entry_type='DEEP_SKY_READING_DEBIT'"
            ).fetchone()[0],
            0,
        )

    def test_predebit_rejection_cannot_close_an_order_after_reading_debit(self):
        self.insert_reading_order()
        self.insert_debit_and_bind_order()
        with self.assertRaises(errors.RaiseException):
            self.conn.execute(
                """INSERT INTO ce_predebit_failure_evidence
                (logical_purchase_id, no_reading_debit_committed,
                 no_operation_can_still_commit_or_deliver, all_relevant_operations_closed,
                 evidence_reference, confirmed_at)
                VALUES ('order-1',TRUE,TRUE,TRUE,'false-predebit-evidence',%s)""",
                (NOW,),
            )
        self.assertEqual(
            self.conn.execute(
                "SELECT COUNT(*) FROM ce_predebit_failure_evidence WHERE logical_purchase_id='order-1'"
            ).fetchone()[0],
            0,
        )
        with self.assertRaises(errors.RaiseException):
            self.conn.execute(
                "UPDATE ce_deep_sky_order SET status='RESERVATION_REJECTED' WHERE logical_purchase_id='order-1'"
            )
        self.assertEqual(
            self.conn.execute(
                "SELECT status, reading_debit_entry_id FROM ce_deep_sky_order WHERE logical_purchase_id='order-1'"
            ).fetchone(),
            ("DEBIT_COMMITTED", "debit-1"),
        )

    def test_predebit_evidence_requires_all_terminal_preconditions(self):
        self.insert_reading_order()
        # The BEFORE INSERT contract guard rejects incomplete evidence before
        # the table-level CHECK constraint is evaluated.
        with self.assertRaises(errors.RaiseException):
            self.conn.execute(
                """INSERT INTO ce_predebit_failure_evidence
                (logical_purchase_id, no_reading_debit_committed,
                 no_operation_can_still_commit_or_deliver, all_relevant_operations_closed,
                 evidence_reference, confirmed_at)
                VALUES ('order-1',TRUE,FALSE,TRUE,'incomplete-predebit-evidence',%s)""",
                (NOW,),
            )
        self.assertEqual(
            self.conn.execute(
                "SELECT COUNT(*) FROM ce_predebit_failure_evidence WHERE logical_purchase_id='order-1'"
            ).fetchone()[0],
            0,
        )

    def test_terminal_failure_requires_evidence_and_exact_restoration(self):
        self.insert_reading_order()
        self.insert_debit_and_bind_order()
        with self.assertRaises(errors.RaiseException):
            self.conn.execute(
                "UPDATE ce_deep_sky_order SET status='TERMINAL_NONDELIVERY' WHERE logical_purchase_id='order-1'"
            )
        self.conn.execute(
            """INSERT INTO ce_terminal_failure_evidence
            (logical_purchase_id, no_valid_reading_accessible, no_operation_can_still_deliver,
             no_entitlement_exists, all_relevant_operations_closed, evidence_reference, confirmed_at)
            VALUES ('order-1',TRUE,TRUE,TRUE,TRUE,'terminal-evidence-ref',%s)""",
            (NOW,),
        )
        with self.conn.transaction():
            self.conn.execute(
                """INSERT INTO ce_credit_ledger_entry
                (entry_id, account_id, entry_type, delta, reference_id, parent_entry_id, created_at)
                VALUES ('restore-1','acct-1','DEEP_SKY_READING_DEBIT_RESTORATION',4,'debit-1','debit-1',%s)""",
                (NOW,),
            )
            with self.assertRaises(errors.UniqueViolation):
                with self.conn.transaction():
                    self.conn.execute(
                        """INSERT INTO ce_credit_ledger_entry
                        (entry_id, account_id, entry_type, delta, reference_id, parent_entry_id, created_at)
                        VALUES ('restore-2','acct-1','DEEP_SKY_READING_DEBIT_RESTORATION',4,'debit-1','debit-1',%s)""",
                        (NOW,),
                    )
            self.conn.execute(
                "UPDATE ce_deep_sky_order SET status='TERMINAL_NONDELIVERY' WHERE logical_purchase_id='order-1'"
            )

    def test_terminal_nondelivery_cannot_be_reactivated_or_grant_entitlement_after_restore(self):
        self.insert_reading_order()
        self.insert_debit_and_bind_order()
        self.conn.execute(
            """INSERT INTO ce_terminal_failure_evidence
            (logical_purchase_id, no_valid_reading_accessible, no_operation_can_still_deliver,
             no_entitlement_exists, all_relevant_operations_closed, evidence_reference, confirmed_at)
            VALUES ('order-1',TRUE,TRUE,TRUE,TRUE,'terminal-evidence-ref',%s)""",
            (NOW,),
        )

        with self.conn.transaction():
            self.conn.execute(
                """INSERT INTO ce_credit_ledger_entry
                (entry_id, account_id, entry_type, delta, reference_id, parent_entry_id, created_at)
                VALUES ('restore-1','acct-1','DEEP_SKY_READING_DEBIT_RESTORATION',4,'debit-1','debit-1',%s)""",
                (NOW,),
            )
            # A restored debit cannot regain a reading entitlement even before the
            # terminal state update within the same transaction.
            with self.assertRaises(errors.RaiseException):
                with self.conn.transaction():
                    self.conn.execute(
                        """INSERT INTO ce_reading_entitlement
                        (entitlement_id, logical_purchase_id, account_id, reading_reference,
                         reading_content_hash, validated_at, accessible_at)
                        VALUES ('ent-after-restore','order-1','acct-1','read-1','hash-1',%s,%s)""",
                        (NOW, NOW),
                    )
            self.conn.execute(
                "UPDATE ce_deep_sky_order SET status='TERMINAL_NONDELIVERY' WHERE logical_purchase_id='order-1'"
            )

        with self.assertRaises(errors.RaiseException):
            self.conn.execute(
                "UPDATE ce_deep_sky_order SET status='DEBIT_COMMITTED' WHERE logical_purchase_id='order-1'"
            )
        with self.assertRaises(errors.RaiseException):
            self.conn.execute(
                """INSERT INTO ce_reading_entitlement
                (entitlement_id, logical_purchase_id, account_id, reading_reference,
                 reading_content_hash, validated_at, accessible_at)
                VALUES ('ent-after-terminal','order-1','acct-1','read-1','hash-1',%s,%s)""",
                (NOW, NOW),
            )
        self.assertEqual(
            self.conn.execute(
                "SELECT status, quota_effect FROM ce_deep_sky_order WHERE logical_purchase_id='order-1'"
            ).fetchone(),
            ("TERMINAL_NONDELIVERY", False),
        )
        self.assertEqual(
            self.conn.execute(
                "SELECT COUNT(*) FROM ce_reading_entitlement WHERE logical_purchase_id='order-1'"
            ).fetchone()[0],
            0,
        )

    def test_debit_restoration_cannot_commit_without_terminal_transition(self):
        self.insert_reading_order()
        self.insert_debit_and_bind_order()
        self.conn.execute(
            """INSERT INTO ce_terminal_failure_evidence
            (logical_purchase_id, no_valid_reading_accessible, no_operation_can_still_deliver,
             no_entitlement_exists, all_relevant_operations_closed, evidence_reference, confirmed_at)
            VALUES ('order-1',TRUE,TRUE,TRUE,TRUE,'terminal-evidence-ref',%s)""",
            (NOW,),
        )
        with self.assertRaises(errors.RaiseException):
            self.conn.execute(
                """INSERT INTO ce_credit_ledger_entry
                (entry_id, account_id, entry_type, delta, reference_id, parent_entry_id, created_at)
                VALUES ('restore-1','acct-1','DEEP_SKY_READING_DEBIT_RESTORATION',4,'debit-1','debit-1',%s)""",
                (NOW,),
            )
        self.assertEqual(
            self.conn.execute(
                "SELECT status FROM ce_deep_sky_order WHERE logical_purchase_id='order-1'"
            ).fetchone()[0],
            "DEBIT_COMMITTED",
        )
        self.assertEqual(
            self.conn.execute(
                "SELECT COUNT(*) FROM ce_credit_ledger_entry WHERE entry_type='DEEP_SKY_READING_DEBIT_RESTORATION'"
            ).fetchone()[0],
            0,
        )

    def test_debit_restoration_cannot_reverse_a_fulfilled_order(self):
        self.insert_reading_order()
        self.insert_debit_and_bind_order()
        self.conn.execute(
            """INSERT INTO ce_reading_entitlement
            (entitlement_id, logical_purchase_id, account_id, reading_reference,
             reading_content_hash, validated_at, accessible_at)
            VALUES ('ent-1','order-1','acct-1','read-1','hash-1',%s,%s)""",
            (NOW, NOW),
        )
        self.conn.execute(
            "UPDATE ce_deep_sky_order SET status='FULFILLED', completed_at=%s WHERE logical_purchase_id='order-1'",
            (NOW,),
        )
        self.conn.execute("DELETE FROM ce_reading_entitlement WHERE logical_purchase_id='order-1'")
        self.conn.execute(
            """INSERT INTO ce_terminal_failure_evidence
            (logical_purchase_id, no_valid_reading_accessible, no_operation_can_still_deliver,
             no_entitlement_exists, all_relevant_operations_closed, evidence_reference, confirmed_at)
            VALUES ('order-1',TRUE,TRUE,TRUE,TRUE,'false-terminal-evidence',%s)""",
            (NOW,),
        )
        with self.assertRaises(errors.RaiseException):
            self.conn.execute(
                """INSERT INTO ce_credit_ledger_entry
                (entry_id, account_id, entry_type, delta, reference_id, parent_entry_id, created_at)
                VALUES ('restore-1','acct-1','DEEP_SKY_READING_DEBIT_RESTORATION',4,'debit-1','debit-1',%s)""",
                (NOW,),
            )
        self.assertEqual(
            self.conn.execute(
                "SELECT status, quota_effect FROM ce_deep_sky_order WHERE logical_purchase_id='order-1'"
            ).fetchone(),
            ("FULFILLED", True),
        )

    def test_slot_release_needs_terminal_evidence_and_a_policy_event(self):
        self.insert_reading_order()
        self.insert_debit_and_bind_order()
        self.conn.execute(
            """INSERT INTO ce_terminal_failure_evidence
            (logical_purchase_id, no_valid_reading_accessible, no_operation_can_still_deliver,
             no_entitlement_exists, all_relevant_operations_closed, evidence_reference, confirmed_at)
            VALUES ('order-1',TRUE,TRUE,TRUE,TRUE,'terminal-evidence-ref',%s)""",
            (NOW,),
        )
        with self.conn.transaction():
            self.conn.execute(
                """INSERT INTO ce_credit_ledger_entry
                (entry_id, account_id, entry_type, delta, reference_id, parent_entry_id, created_at)
                VALUES ('restore-1','acct-1','DEEP_SKY_READING_DEBIT_RESTORATION',4,'debit-1','debit-1',%s)""",
                (NOW,),
            )
            self.conn.execute(
                "UPDATE ce_deep_sky_order SET status='TERMINAL_NONDELIVERY' WHERE logical_purchase_id='order-1'"
            )
        with self.assertRaises(errors.RaiseException):
            self.conn.execute(
                "UPDATE ce_daily_purchase_slot SET slot_state='RELEASED', state_version=2, updated_at=%s WHERE account_id='acct-1' AND service_date_utc=%s",
                (NOW, SERVICE_DATE),
            )
        self.conn.execute(
            """INSERT INTO ce_quota_event
            (quota_event_id, idempotency_key, account_id, service_date_utc,
             logical_purchase_id, event_type, policy_decision_reference,
             terminal_evidence_reference, occurred_at)
            VALUES ('qe-1','qe-idem-1','acct-1',%s,'order-1','SLOT_RELEASED',
                    'approved-policy-ref','terminal-evidence-ref',%s)""",
            (SERVICE_DATE, NOW),
        )
        self.conn.execute(
            "UPDATE ce_daily_purchase_slot SET slot_state='RELEASED', state_version=2, updated_at=%s WHERE account_id='acct-1' AND service_date_utc=%s",
            (NOW, SERVICE_DATE),
        )
        self.assertEqual(
            self.conn.execute("SELECT slot_state FROM ce_daily_purchase_slot").fetchone()[0],
            "RELEASED",
        )
        self.assertEqual(
            self.conn.execute("SELECT quota_effect FROM ce_deep_sky_order WHERE logical_purchase_id='order-1'").fetchone()[0],
            False,
            "D2-B clears the quota effect after a validated terminal non-delivery",
        )
        self.insert_reading_order(order_id="order-2", account="acct-1", reserve_slot=False)
        self.conn.execute(
            """UPDATE ce_daily_purchase_slot
                  SET active_logical_purchase_id='order-2', slot_state='RESERVED',
                      state_version=state_version+1, updated_at=%s
                WHERE account_id='acct-1' AND service_date_utc=%s""",
            (NOW, SERVICE_DATE),
        )
        self.assertEqual(
            self.conn.execute("SELECT active_logical_purchase_id, slot_state FROM ce_daily_purchase_slot").fetchone(),
            ("order-2", "RESERVED"),
            "a proven D2-B release permits a new same-date reservation",
        )

    def test_service_date_and_order_identity_are_immutable(self):
        self.insert_reading_order()
        with self.assertRaises(errors.RaiseException):
            self.conn.execute(
                "UPDATE ce_deep_sky_order SET service_date_utc=%s WHERE logical_purchase_id='order-1'",
                (date(2026, 10, 11),),
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
