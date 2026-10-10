from datetime import datetime, timezone, timedelta
import time
import unittest

from commerce_model import (
    CapTrigger, CommerceReferenceModel, CreditEntry, InvalidFulfillment,
    InvalidIdentity, InvalidTransition, LedgerConflict, OrderStatus,
    PolicyDecisionRequired, QuotaBlocked, QuotaResolution,
    TerminalFailureEvidence, TerminalFailurePolicy,
    FulfillmentAdmissionState, FulfillmentAdmissionBlocked,
)

UTC = timezone.utc
FULL_TERMINAL_EVIDENCE = TerminalFailureEvidence(True, True, True, True)


class CommerceReferenceModelTests(unittest.TestCase):
    def model(self, **kwargs):
        # Existing positive-path tests explicitly simulate an attested healthy service.
        kwargs.setdefault("fulfillment_admission", FulfillmentAdmissionState.READY)
        kwargs.setdefault("fulfillment_admission_expires_at", datetime.now(UTC) + timedelta(minutes=5))
        kwargs.setdefault("fulfillment_attestation_reference", "unit-test-health-attestation")
        return CommerceReferenceModel(**kwargs)

    def funded(self, model, account="acct", credits=20):
        model.ledger.post(CreditEntry(
            "topup-grant-1", account, credits, "TOPUP_CREDIT_GRANT", "provider-tx-1"
        ))

    def test_server_time_is_converted_to_utc_service_date(self):
        model = self.model(cap_trigger=CapTrigger.PURCHASE_DEBIT_COMMITTED)
        local = datetime(2026, 10, 11, 7, 30, tzinfo=timezone(timedelta(hours=8)))
        order = model.confirm_and_reserve("acct", "order-1", local)
        self.assertEqual(order.service_date_utc.isoformat(), "2026-10-10")

    def test_naive_server_timestamp_fails_closed(self):
        with self.assertRaises(InvalidIdentity):
            self.model().confirm_and_reserve(
                "acct", "order-1", datetime(2026, 10, 10, 9, 0)
            )

    def test_order_retry_never_redates_original_purchase(self):
        model = self.model()
        first = model.confirm_and_reserve(
            "acct", "order-1", datetime(2026, 10, 10, 23, 59, tzinfo=UTC)
        )
        replay = model.confirm_and_reserve(
            "acct", "order-1", datetime(2026, 10, 11, 0, 2, tzinfo=UTC)
        )
        self.assertIs(first, replay)
        self.assertEqual(replay.service_date_utc.isoformat(), "2026-10-10")

    def test_same_day_second_distinct_active_order_is_blocked(self):
        model = self.model()
        model.confirm_and_reserve("acct", "order-1", datetime(2026, 10, 10, 12, tzinfo=UTC))
        with self.assertRaises(QuotaBlocked):
            model.confirm_and_reserve("acct", "order-2", datetime(2026, 10, 10, 12, 1, tzinfo=UTC))

    def test_different_accounts_have_separate_daily_reservations(self):
        model = self.model(cap_trigger=CapTrigger.PURCHASE_DEBIT_COMMITTED)
        model.confirm_and_reserve("acct-1", "order-1", datetime(2026, 10, 10, 12, tzinfo=UTC))
        model.confirm_and_reserve("acct-2", "order-2", datetime(2026, 10, 10, 12, tzinfo=UTC))
        self.assertEqual(model.orders["order-2"].account_id, "acct-2")

    def test_credits_topup_does_not_create_a_reading_order_or_consume_cap(self):
        model = self.model(cap_trigger=CapTrigger.PURCHASE_DEBIT_COMMITTED)
        self.funded(model, credits=20)
        self.assertEqual(model.ledger.balance("acct"), 20)
        order = model.confirm_and_reserve("acct", "order-1", datetime(2026, 10, 10, 12, tzinfo=UTC))
        self.assertEqual(order.quota_effect, None)
        self.assertEqual(order.quota_resolution, QuotaResolution.RESERVATION_ONLY)

    def test_debit_replay_is_idempotent_and_different_amount_conflicts(self):
        model = self.model(cap_trigger=CapTrigger.PURCHASE_DEBIT_COMMITTED)
        self.funded(model)
        model.confirm_and_reserve("acct", "order-1", datetime(2026, 10, 10, 12, tzinfo=UTC))
        self.assertTrue(model.commit_reading_debit("order-1", "debit-1", 4))
        self.assertFalse(model.commit_reading_debit("order-1", "debit-1", 4))
        self.assertEqual(model.ledger.balance("acct"), 16)
        with self.assertRaises(LedgerConflict):
            model.commit_reading_debit("order-1", "debit-1", 5)

    def test_insufficient_credits_does_not_partially_commit(self):
        model = self.model(cap_trigger=CapTrigger.PURCHASE_DEBIT_COMMITTED)
        model.confirm_and_reserve("acct", "order-1", datetime(2026, 10, 10, 12, tzinfo=UTC))
        with self.assertRaises(LedgerConflict):
            model.commit_reading_debit("order-1", "debit-1", 4)
        self.assertEqual(model.ledger.balance("acct"), 0)
        self.assertIsNone(model.orders["order-1"].reading_debit_entry_id)
        self.assertEqual(model.orders["order-1"].status, OrderStatus.RESERVED)

    def test_unknown_outcome_never_becomes_terminal_or_releases_same_day_slot(self):
        model = self.model(cap_trigger=CapTrigger.PURCHASE_DEBIT_COMMITTED)
        self.funded(model)
        model.confirm_and_reserve("acct", "order-1", datetime(2026, 10, 10, 23, 58, tzinfo=UTC))
        model.commit_reading_debit("order-1", "debit-1", 4)
        model.mark_outcome_unknown("order-1")
        self.assertEqual(model.orders["order-1"].status, OrderStatus.RECONCILIATION_REQUIRED)
        self.assertTrue(model.orders["order-1"].quota_effect)
        with self.assertRaises(QuotaBlocked):
            model.confirm_and_reserve("acct", "order-2", datetime(2026, 10, 10, 23, 59, tzinfo=UTC))

    def test_cross_date_purchase_while_prior_order_unknown_is_not_guessed(self):
        model = self.model(cap_trigger=CapTrigger.PURCHASE_DEBIT_COMMITTED)
        self.funded(model)
        model.confirm_and_reserve("acct", "order-1", datetime(2026, 10, 10, 23, 58, tzinfo=UTC))
        model.commit_reading_debit("order-1", "debit-1", 4)
        model.mark_outcome_unknown("order-1")
        with self.assertRaises(PolicyDecisionRequired):
            model.confirm_and_reserve("acct", "order-2", datetime(2026, 10, 11, 0, 2, tzinfo=UTC))

    def test_provider_event_is_deduplicated_globally_and_conflicts_are_rejected(self):
        model = self.model()
        model.confirm_and_reserve("acct", "order-1", datetime(2026, 10, 10, 12, tzinfo=UTC))
        self.assertTrue(model.record_provider_event("order-1", "provider-x", "evt-1", "status=succeeded"))
        self.assertFalse(model.record_provider_event("order-1", "provider-x", "evt-1", "status=succeeded"))
        with self.assertRaises(LedgerConflict):
            model.record_provider_event("order-1", "provider-x", "evt-1", "status=failed")
        model.confirm_and_reserve("acct-2", "order-2", datetime(2026, 10, 11, 12, tzinfo=UTC))
        with self.assertRaises(LedgerConflict):
            model.record_provider_event("order-2", "provider-x", "evt-1", "status=succeeded")

    def test_unvalidated_or_inaccessible_reading_cannot_fulfill(self):
        model = self.model(cap_trigger=CapTrigger.VALID_READING_ACCESSIBLE)
        self.funded(model)
        model.confirm_and_reserve("acct", "order-1", datetime(2026, 10, 10, 12, tzinfo=UTC))
        model.commit_reading_debit("order-1", "debit-1", 4)
        with self.assertRaises(InvalidFulfillment):
            model.fulfill_validated_reading("order-1", entitlement_id="ent-1",
                reading_reference="read-1", content_hash="hash-1", output_valid=True, accessible=False)
        with self.assertRaises(InvalidFulfillment):
            model.fulfill_validated_reading("order-1", entitlement_id="ent-1",
                reading_reference="read-1", content_hash="hash-1", output_valid=False, accessible=True)

    def test_fulfillment_replay_creates_no_second_entitlement(self):
        model = self.model(cap_trigger=CapTrigger.PURCHASE_DEBIT_COMMITTED)
        self.funded(model)
        model.confirm_and_reserve("acct", "order-1", datetime(2026, 10, 10, 12, tzinfo=UTC))
        model.commit_reading_debit("order-1", "debit-1", 4)
        kwargs = dict(entitlement_id="ent-1", reading_reference="read-1",
                      content_hash="hash-1", output_valid=True, accessible=True)
        self.assertTrue(model.fulfill_validated_reading("order-1", **kwargs))
        self.assertFalse(model.fulfill_validated_reading("order-1", **kwargs))
        self.assertEqual(model.orders["order-1"].entitlement_id, "ent-1")
        with self.assertRaises(InvalidTransition):
            model.confirm_terminal_non_delivery("order-1", evidence=FULL_TERMINAL_EVIDENCE,
                restoration_id="restore-1", close_at=datetime(2026, 10, 10, 13, tzinfo=UTC))

    def test_terminal_failure_requires_complete_evidence_and_exact_credit_restore(self):
        model = self.model(cap_trigger=CapTrigger.PURCHASE_DEBIT_COMMITTED,
            terminal_failure_policy=TerminalFailurePolicy.RELEASE_IF_ORIGINAL_DATE_CURRENT)
        self.funded(model)
        model.confirm_and_reserve("acct", "order-1", datetime(2026, 10, 10, 12, tzinfo=UTC))
        model.commit_reading_debit("order-1", "debit-1", 4)
        incomplete = TerminalFailureEvidence(True, False, True, True)
        with self.assertRaises(InvalidTransition):
            model.confirm_terminal_non_delivery("order-1", evidence=incomplete,
                restoration_id="restore-1", close_at=datetime(2026, 10, 10, 13, tzinfo=UTC))
        self.assertEqual(model.ledger.balance("acct"), 16)
        self.assertTrue(model.confirm_terminal_non_delivery("order-1", evidence=FULL_TERMINAL_EVIDENCE,
            restoration_id="restore-1", close_at=datetime(2026, 10, 10, 13, tzinfo=UTC)))
        self.assertEqual(model.ledger.balance("acct"), 20)
        self.assertFalse(model.confirm_terminal_non_delivery("order-1", evidence=FULL_TERMINAL_EVIDENCE,
            restoration_id="restore-1", close_at=datetime(2026, 10, 10, 13, 1, tzinfo=UTC)))
        self.assertEqual(model.ledger.balance("acct"), 20)
        order2 = model.confirm_and_reserve("acct", "order-2", datetime(2026, 10, 10, 14, tzinfo=UTC))
        self.assertEqual(order2.service_date_utc.isoformat(), "2026-10-10")

    def test_restore_cannot_be_repeated_under_a_new_identity(self):
        model = self.model(cap_trigger=CapTrigger.PURCHASE_DEBIT_COMMITTED,
            terminal_failure_policy=TerminalFailurePolicy.RELEASE_IF_ORIGINAL_DATE_CURRENT)
        self.funded(model)
        model.confirm_and_reserve("acct", "order-1", datetime(2026, 10, 10, 12, tzinfo=UTC))
        model.commit_reading_debit("order-1", "debit-1", 4)
        model.confirm_terminal_non_delivery("order-1", evidence=FULL_TERMINAL_EVIDENCE,
            restoration_id="restore-1", close_at=datetime(2026, 10, 10, 13, tzinfo=UTC))
        with self.assertRaises(LedgerConflict):
            model.ledger.restore_reading_debit("restore-2", "debit-1", "acct")

    def test_release_after_utc_midnight_does_not_transfer_old_slot(self):
        model = self.model(cap_trigger=CapTrigger.PURCHASE_DEBIT_COMMITTED,
            terminal_failure_policy=TerminalFailurePolicy.RELEASE_IF_ORIGINAL_DATE_CURRENT)
        self.funded(model)
        model.confirm_and_reserve("acct", "order-1", datetime(2026, 10, 10, 23, 55, tzinfo=UTC))
        model.commit_reading_debit("order-1", "debit-1", 4)
        model.confirm_terminal_non_delivery("order-1", evidence=FULL_TERMINAL_EVIDENCE,
            restoration_id="restore-1", close_at=datetime(2026, 10, 11, 0, 5, tzinfo=UTC))
        old = model.orders["order-1"]
        self.assertEqual(old.service_date_utc.isoformat(), "2026-10-10")
        self.assertEqual(old.quota_resolution, QuotaResolution.ORIGINAL_DATE_EXPIRED_NO_TRANSFER)
        new = model.confirm_and_reserve("acct", "order-2", datetime(2026, 10, 11, 0, 6, tzinfo=UTC))
        self.assertEqual(new.service_date_utc.isoformat(), "2026-10-11")

    def test_retain_slot_policy_blocks_same_day_retry_after_restoration(self):
        model = self.model(cap_trigger=CapTrigger.PURCHASE_DEBIT_COMMITTED,
            terminal_failure_policy=TerminalFailurePolicy.RETAIN_SAME_DATE_SLOT)
        self.funded(model)
        model.confirm_and_reserve("acct", "order-1", datetime(2026, 10, 10, 12, tzinfo=UTC))
        model.commit_reading_debit("order-1", "debit-1", 4)
        model.confirm_terminal_non_delivery("order-1", evidence=FULL_TERMINAL_EVIDENCE,
            restoration_id="restore-1", close_at=datetime(2026, 10, 10, 13, tzinfo=UTC))
        with self.assertRaises(QuotaBlocked):
            model.confirm_and_reserve("acct", "order-2", datetime(2026, 10, 10, 14, tzinfo=UTC))

    def test_fulfillment_cap_trigger_is_not_consumed_until_accessible_reading(self):
        model = self.model(cap_trigger=CapTrigger.VALID_READING_ACCESSIBLE)
        self.funded(model)
        order = model.confirm_and_reserve("acct", "order-1", datetime(2026, 10, 10, 12, tzinfo=UTC))
        model.commit_reading_debit("order-1", "debit-1", 4)
        self.assertFalse(order.quota_effect)
        self.assertEqual(order.quota_resolution, QuotaResolution.WAITING_FOR_FULFILLMENT)
        model.fulfill_validated_reading("order-1", entitlement_id="ent-1",
            reading_reference="read-1", content_hash="hash-1", output_valid=True, accessible=True)
        self.assertTrue(order.quota_effect)
        self.assertEqual(order.quota_resolution, QuotaResolution.FULFILLMENT_TRIGGER_COMMITTED)
        with self.assertRaises(QuotaBlocked):
            model.confirm_and_reserve("acct", "order-2", datetime(2026, 10, 10, 14, tzinfo=UTC))

    def test_owner_selected_policy_defaults_and_health_interlock_fail_closed(self):
        # Constructor defaults carry the owner disposition, while an unknown service
        # health state cannot admit a new order.
        model = CommerceReferenceModel()
        self.assertEqual(model.cap_trigger, CapTrigger.PURCHASE_DEBIT_COMMITTED)
        self.assertEqual(
            model.terminal_failure_policy,
            TerminalFailurePolicy.RELEASE_IF_ORIGINAL_DATE_CURRENT,
        )
        with self.assertRaises(FulfillmentAdmissionBlocked):
            model.confirm_and_reserve(
                "acct", "order-unknown-health",
                datetime(2026, 10, 10, 12, tzinfo=UTC),
            )

        ready = self.model()
        self.funded(ready)
        order = ready.confirm_and_reserve(
            "acct", "order-1", datetime(2026, 10, 10, 12, tzinfo=UTC)
        )
        ready.set_fulfillment_admission(FulfillmentAdmissionState.BLOCKED)
        # Existing logical-order replay stays addressable but cannot create a new order.
        self.assertIs(order, ready.confirm_and_reserve(
            "acct", "order-1", datetime(2026, 10, 10, 12, 1, tzinfo=UTC)
        ))
        with self.assertRaises(FulfillmentAdmissionBlocked):
            ready.confirm_and_reserve(
                "acct", "order-2", datetime(2026, 10, 10, 12, 2, tzinfo=UTC)
            )
        with self.assertRaises(FulfillmentAdmissionBlocked):
            ready.commit_reading_debit("order-1", "debit-1", 4)
        self.assertEqual(ready.ledger.balance("acct"), 20)
        ready.set_fulfillment_admission(FulfillmentAdmissionState.UNKNOWN)
        with self.assertRaises(FulfillmentAdmissionBlocked):
            ready.commit_reading_debit("order-1", "debit-1", 4)
        ready.set_fulfillment_admission(
            FulfillmentAdmissionState.READY,
            attestation_reference="test-health-recovered",
            valid_until=datetime.now(UTC) + timedelta(minutes=5),
        )
        self.assertTrue(ready.commit_reading_debit("order-1", "debit-1", 4))
        ready.set_fulfillment_admission(FulfillmentAdmissionState.BLOCKED)
        self.assertFalse(ready.commit_reading_debit("order-1", "debit-1", 4))
        self.assertEqual(ready.ledger.balance("acct"), 16)
        # Existing debit/operation can still complete while admission for new
        # purchases is BLOCKED; the gate is not an automatic cancellation policy.
        self.assertTrue(ready.fulfill_validated_reading(
            "order-1", entitlement_id="ent-1", reading_reference="read-1",
            content_hash="hash-1", output_valid=True, accessible=True,
        ))
        self.assertEqual(ready.orders["order-1"].status, OrderStatus.FULFILLED)

    def test_expired_or_unattested_ready_state_fails_closed(self):
        with self.assertRaises(InvalidIdentity):
            CommerceReferenceModel(
                fulfillment_admission=FulfillmentAdmissionState.READY
            )
        model = self.model(
            fulfillment_admission_expires_at=datetime.now(UTC) + timedelta(seconds=0.15),
        )
        time.sleep(0.20)
        with self.assertRaises(FulfillmentAdmissionBlocked):
            model.confirm_and_reserve(
                "acct", "order-expired-health",
                datetime(2026, 10, 10, 12, tzinfo=UTC),
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
