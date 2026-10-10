from datetime import datetime, timezone
import unittest

from commerce_model import (
    CapTrigger, CommerceReferenceModel, LedgerConflict, CreditLedger, InvalidIdentity,
)
from topup_model import (
    CreditsSku, CreditsTopUpModel, ObservationSource, ProviderObservation,
    ProviderObservationError, ProviderPaymentStatus, TopUpStatus,
)

UTC = timezone.utc
T0 = datetime(2026, 10, 10, 12, 0, tzinfo=UTC)
SKU = CreditsSku("credits-pack-test", 299, "USD", 4)


def observation(*, event="evt-1", status=ProviderPaymentStatus.SUCCEEDED,
                txn="provider-tx-1", fingerprint="sha256:abc",
                verified=True, source=ObservationSource.WEBHOOK):
    return ProviderObservation(
        provider="provider-test", event_id=event, provider_transaction_ref=txn,
        logical_topup_id="topup-1", account_id="acct-1",
        amount_minor=299, currency="USD",
        payment_status=status, payload_fingerprint=fingerprint, source=source,
        verification_ref="verification-record-1" if verified else "",
        adapter_validation_passed=verified,
    )


class CreditsTopUpModelTests(unittest.TestCase):
    def setUp(self):
        self.ledger = CreditLedger()
        self.model = CreditsTopUpModel({"credits-pack-test": SKU}, self.ledger)
        self.order = self.model.create_topup(
            account_id="acct-1", logical_topup_id="topup-1",
            idempotency_key="idem-1", sku_id="credits-pack-test",
            server_created_at=T0,
        )

    def test_sku_price_and_credits_are_server_owned(self):
        self.assertEqual(self.order.sku.amount_minor, 299)
        self.assertEqual(self.order.sku.currency, "USD")
        self.assertEqual(self.order.sku.credits_granted, 4)
        with self.assertRaises(InvalidIdentity):
            self.model.create_topup(
                account_id="acct-1", logical_topup_id="topup-2",
                idempotency_key="idem-2", sku_id="client-priced-pack",
                server_created_at=T0,
            )

    def test_creation_retry_with_same_idempotency_key_returns_same_order(self):
        again = self.model.create_topup(
            account_id="acct-1", logical_topup_id="topup-1",
            idempotency_key="idem-1", sku_id="credits-pack-test",
            server_created_at=datetime(2026, 10, 11, 0, 1, tzinfo=UTC),
        )
        self.assertIs(again, self.order)
        self.assertEqual(len(self.model.orders), 1)

    def test_idempotency_key_cannot_be_reused_for_different_topup(self):
        with self.assertRaises(LedgerConflict):
            self.model.create_topup(
                account_id="acct-1", logical_topup_id="topup-2",
                idempotency_key="idem-1", sku_id="credits-pack-test",
                server_created_at=T0,
            )

    def test_provider_observation_must_match_server_owned_amount_and_currency(self):
        mismatched = ProviderObservation(
            provider="provider-test", event_id="evt-amount",
            provider_transaction_ref="provider-tx-1",
            logical_topup_id="topup-1", account_id="acct-1",
            amount_minor=1, currency="USD",
            payment_status=ProviderPaymentStatus.SUCCEEDED,
            payload_fingerprint="sha256:bad-amount",
            source=ObservationSource.WEBHOOK,
            verification_ref="verification-record-1",
            adapter_validation_passed=True,
        )
        with self.assertRaises(ProviderObservationError):
            self.model.apply_provider_observation("topup-1", mismatched, T0)
        self.assertEqual(self.ledger.balance("acct-1"), 0)

    def test_provider_observation_must_match_server_owned_order_and_account(self):
        mismatched = ProviderObservation(
            provider="provider-test", event_id="evt-account",
            provider_transaction_ref="provider-tx-1",
            logical_topup_id="some-other-order", account_id="acct-2",
            amount_minor=299, currency="USD",
            payment_status=ProviderPaymentStatus.SUCCEEDED,
            payload_fingerprint="sha256:bad-account",
            source=ObservationSource.WEBHOOK,
            verification_ref="verification-record-1",
            adapter_validation_passed=True,
        )
        with self.assertRaises(ProviderObservationError):
            self.model.apply_provider_observation("topup-1", mismatched, T0)
        self.assertEqual(self.ledger.balance("acct-1"), 0)

    def test_unknown_intermediate_state_does_not_bypass_authoritative_reconciliation_after_failure(self):
        self.model.apply_provider_observation(
            "topup-1", observation(status=ProviderPaymentStatus.FAILED), T0
        )
        self.model.apply_provider_observation(
            "topup-1", observation(event="evt-unknown", status=ProviderPaymentStatus.UNKNOWN,
                                   fingerprint="sha256:unknown"), T0
        )
        with self.assertRaises(ProviderObservationError):
            self.model.apply_provider_observation(
                "topup-1", observation(event="evt-late-success",
                                      fingerprint="sha256:late-success"), T0
            )
        self.assertEqual(self.ledger.balance("acct-1"), 0)

    def test_unverified_provider_observation_is_rejected(self):
        with self.assertRaises(ProviderObservationError):
            self.model.apply_provider_observation(
                "topup-1", observation(verified=False), T0
            )
        self.assertEqual(self.ledger.balance("acct-1"), 0)
        self.assertEqual(self.order.status, TopUpStatus.PAYMENT_PENDING)

    def test_unknown_provider_state_never_grants_credits(self):
        self.model.apply_provider_observation(
            "topup-1", observation(status=ProviderPaymentStatus.UNKNOWN), T0
        )
        self.assertEqual(self.order.status, TopUpStatus.RECONCILIATION_REQUIRED)
        self.assertEqual(self.order.credits_granted, 0)
        self.assertEqual(self.ledger.balance("acct-1"), 0)

    def test_pending_provider_state_never_grants_credits(self):
        self.model.apply_provider_observation(
            "topup-1", observation(status=ProviderPaymentStatus.PENDING), T0
        )
        self.assertEqual(self.order.status, TopUpStatus.PAYMENT_PENDING)
        self.assertEqual(self.ledger.balance("acct-1"), 0)

    def test_definitive_failure_does_not_grant_credits(self):
        self.model.apply_provider_observation(
            "topup-1", observation(status=ProviderPaymentStatus.FAILED), T0
        )
        self.assertEqual(self.order.status, TopUpStatus.PAYMENT_FAILED)
        self.assertEqual(self.ledger.balance("acct-1"), 0)

    def test_verified_success_grants_credits_once(self):
        self.model.apply_provider_observation("topup-1", observation(), T0)
        self.assertEqual(self.order.status, TopUpStatus.CREDIT_FULFILLED)
        self.assertEqual(self.order.credits_granted, 4)
        self.assertEqual(self.ledger.balance("acct-1"), 4)
        self.assertEqual(self.order.completed_at_utc, T0)

    def test_duplicate_provider_event_is_idempotent(self):
        self.assertTrue(self.model.apply_provider_observation("topup-1", observation(), T0))
        self.assertFalse(self.model.apply_provider_observation("topup-1", observation(), T0))
        self.assertEqual(self.ledger.balance("acct-1"), 4)
        self.assertEqual(len(self.ledger.entries), 1)

    def test_distinct_success_events_for_same_transaction_do_not_double_grant(self):
        self.model.apply_provider_observation("topup-1", observation(), T0)
        second = observation(event="evt-2", fingerprint="sha256:second")
        self.model.apply_provider_observation("topup-1", second, T0)
        self.assertEqual(self.ledger.balance("acct-1"), 4)
        self.assertEqual(len(self.ledger.entries), 1)

    def test_reused_provider_event_id_with_different_payload_conflicts(self):
        self.model.apply_provider_observation("topup-1", observation(), T0)
        with self.assertRaises(LedgerConflict):
            self.model.apply_provider_observation(
                "topup-1", observation(fingerprint="sha256:changed"), T0
            )
        self.assertEqual(self.ledger.balance("acct-1"), 4)

    def test_provider_transaction_reference_cannot_move_to_another_order(self):
        self.model.apply_provider_observation("topup-1", observation(), T0)
        self.model.create_topup(
            account_id="acct-2", logical_topup_id="topup-2",
            idempotency_key="idem-2", sku_id="credits-pack-test",
            server_created_at=T0,
        )
        with self.assertRaises(LedgerConflict):
            self.model.apply_provider_observation(
                "topup-2", observation(event="evt-other"), T0
            )
        self.assertEqual(self.ledger.balance("acct-2"), 0)

    def test_success_after_failure_requires_authoritative_status_lookup(self):
        self.model.apply_provider_observation(
            "topup-1", observation(status=ProviderPaymentStatus.FAILED), T0
        )
        with self.assertRaises(ProviderObservationError):
            self.model.apply_provider_observation(
                "topup-1", observation(event="evt-late-success"), T0
            )
        good_lookup = observation(
            event="status-query-1",
            status=ProviderPaymentStatus.SUCCEEDED,
            source=ObservationSource.AUTHORITATIVE_STATUS_LOOKUP,
            fingerprint="sha256:lookup-result",
        )
        self.model.apply_provider_observation("topup-1", good_lookup, T0)
        self.assertEqual(self.order.status, TopUpStatus.CREDIT_FULFILLED)
        self.assertEqual(self.ledger.balance("acct-1"), 4)

    def test_topup_does_not_create_a_deep_sky_purchase_or_consume_its_daily_cap(self):
        cap_model = CommerceReferenceModel(
            cap_trigger=CapTrigger.PURCHASE_DEBIT_COMMITTED
        )
        cap_model.confirm_and_reserve(
            "acct-1", "deep-sky-order-1", T0
        )
        topups = CreditsTopUpModel({"credits-pack-test": SKU}, cap_model.ledger)
        topups.create_topup(
            account_id="acct-1", logical_topup_id="topup-independent",
            idempotency_key="idem-independent", sku_id="credits-pack-test",
            server_created_at=T0,
        )
        topups.apply_provider_observation(
            "topup-independent", observation(txn="provider-tx-topup"), T0
        )
        self.assertEqual(len(cap_model.orders), 1)
        self.assertEqual(cap_model.ledger.balance("acct-1"), 4)
        self.assertEqual(cap_model.orders["deep-sky-order-1"].quota_effect, None)


if __name__ == "__main__":
    unittest.main(verbosity=2)
