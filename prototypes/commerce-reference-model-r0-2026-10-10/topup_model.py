"""CE Credits top-up reference model — in-memory, candidate-only."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, Mapping, Optional, Tuple

from commerce_model import CreditEntry, CreditLedger, InvalidIdentity, LedgerConflict


class ProviderObservationError(Exception):
    pass


class TopUpStatus(str, Enum):
    PAYMENT_PENDING = "PAYMENT_PENDING"
    RECONCILIATION_REQUIRED = "RECONCILIATION_REQUIRED"
    PAYMENT_FAILED = "PAYMENT_FAILED"
    CREDIT_FULFILLED = "CREDIT_FULFILLED"


class ProviderPaymentStatus(str, Enum):
    PENDING = "PENDING"
    UNKNOWN = "UNKNOWN"
    FAILED = "FAILED"
    SUCCEEDED = "SUCCEEDED"


class ObservationSource(str, Enum):
    WEBHOOK = "WEBHOOK"
    AUTHORITATIVE_STATUS_LOOKUP = "AUTHORITATIVE_STATUS_LOOKUP"


@dataclass(frozen=True)
class CreditsSku:
    """Server-owned SKU definition; never build price/credits from client fields."""
    sku_id: str
    amount_minor: int
    currency: str
    credits_granted: int

    def __post_init__(self) -> None:
        if not self.sku_id or self.amount_minor <= 0 or self.credits_granted <= 0:
            raise InvalidIdentity("SKU ID, positive amount, and positive Credits are required")
        if len(self.currency) != 3 or not self.currency.isalpha() or self.currency.upper() != self.currency:
            raise InvalidIdentity("currency must be a 3-letter uppercase code")


@dataclass(frozen=True)
class ProviderObservation:
    """Adapter output after provider-specific verification/retrieval.

    This value object does not verify signatures itself. Production code must only
    construct it inside the trusted provider adapter after signature, account/order
    association, environment, amount, currency, and provider-status checks.
    """
    provider: str
    event_id: str
    provider_transaction_ref: str
    payment_status: ProviderPaymentStatus
    payload_fingerprint: str
    source: ObservationSource
    verification_ref: str
    adapter_validation_passed: bool


@dataclass
class TopUpOrder:
    logical_topup_id: str
    account_id: str
    idempotency_key: str
    sku: CreditsSku
    created_at_utc: datetime
    status: TopUpStatus = TopUpStatus.PAYMENT_PENDING
    provider: Optional[str] = None
    provider_transaction_ref: Optional[str] = None
    credits_granted: int = 0
    completed_at_utc: Optional[datetime] = None
    failure_observed: bool = False


class CreditsTopUpModel:
    """In-memory top-up model; not a durable or production payment integration."""

    def __init__(self, sku_catalog: Mapping[str, CreditsSku], ledger: Optional[CreditLedger] = None):
        self.sku_catalog = dict(sku_catalog)
        if any(k != v.sku_id for k, v in self.sku_catalog.items()):
            raise InvalidIdentity("SKU catalog keys must match server-owned SKU IDs")
        self.ledger = ledger or CreditLedger()
        self.orders: Dict[str, TopUpOrder] = {}
        self._idempotency: Dict[Tuple[str, str], str] = {}
        self._provider_transactions: Dict[Tuple[str, str], str] = {}
        self._provider_events: Dict[Tuple[str, str], Tuple[str, str, str, ProviderPaymentStatus]] = {}

    @staticmethod
    def _server_utc(timestamp: datetime) -> datetime:
        if timestamp.tzinfo is None or timestamp.utcoffset() is None:
            raise InvalidIdentity("server timestamp must be timezone-aware")
        return timestamp.astimezone(timezone.utc)

    def create_topup(self, *, account_id: str, logical_topup_id: str,
                     idempotency_key: str, sku_id: str,
                     server_created_at: datetime) -> TopUpOrder:
        if not account_id or not logical_topup_id or not idempotency_key:
            raise InvalidIdentity("account, logical top-up, and idempotency identities are required")
        try:
            sku = self.sku_catalog[sku_id]
        except KeyError as exc:
            raise InvalidIdentity("unknown SKU; price and Credits are server-configured") from exc
        created = self._server_utc(server_created_at)
        key = (account_id, idempotency_key)
        previous_id = self._idempotency.get(key)
        if previous_id is not None:
            previous = self.orders[previous_id]
            if previous.logical_topup_id != logical_topup_id or previous.sku != sku:
                raise LedgerConflict("idempotency key reused for a different top-up")
            return previous
        existing = self.orders.get(logical_topup_id)
        if existing is not None:
            if existing.account_id != account_id or existing.idempotency_key != idempotency_key or existing.sku != sku:
                raise LedgerConflict("logical top-up ID reused with conflicting identity or SKU")
            return existing
        order = TopUpOrder(logical_topup_id, account_id, idempotency_key, sku, created)
        self.orders[logical_topup_id] = order
        self._idempotency[key] = logical_topup_id
        return order

    def apply_provider_observation(self, logical_topup_id: str,
                                   observation: ProviderObservation,
                                   server_observed_at: datetime) -> bool:
        """Apply a provider-adapter observation without trusting browser assertions."""
        order = self._order(logical_topup_id)
        observed_at = self._server_utc(server_observed_at)
        required = (
            observation.provider, observation.event_id,
            observation.provider_transaction_ref, observation.payload_fingerprint,
            observation.verification_ref,
        )
        if not all(required) or not observation.adapter_validation_passed:
            raise ProviderObservationError("provider observation is not accepted adapter-verified evidence")

        tx_key = (observation.provider, observation.provider_transaction_ref)
        tx_owner = self._provider_transactions.get(tx_key)
        if tx_owner is not None and tx_owner != logical_topup_id:
            raise LedgerConflict("provider transaction reference is already bound to another logical top-up")
        if order.provider_transaction_ref and (
            order.provider != observation.provider
            or order.provider_transaction_ref != observation.provider_transaction_ref
        ):
            raise LedgerConflict("logical top-up cannot silently switch provider transaction identity")

        if (
            order.failure_observed
            and observation.payment_status == ProviderPaymentStatus.SUCCEEDED
            and observation.source != ObservationSource.AUTHORITATIVE_STATUS_LOOKUP
        ):
            raise ProviderObservationError(
                "success after a prior failure observation requires authoritative provider status lookup"
            )

        event_key = (observation.provider, observation.event_id)
        event_value = (
            logical_topup_id,
            observation.provider_transaction_ref,
            observation.payload_fingerprint,
            observation.payment_status,
        )
        old_event = self._provider_events.get(event_key)
        if old_event is not None:
            if old_event != event_value:
                raise LedgerConflict("provider event ID reused with different order, transaction, payload, or status")
            return False

        if order.status == TopUpStatus.CREDIT_FULFILLED:
            # Preserve monotonic fulfillment; a contradictory provider event needs review.
            if observation.payment_status != ProviderPaymentStatus.SUCCEEDED:
                raise LedgerConflict("post-fulfillment non-success observation requires reconciliation; no automatic clawback")
            # A distinct success event for the same transaction is safe and grants nothing twice.
        elif order.status == TopUpStatus.PAYMENT_FAILED:
            if observation.payment_status == ProviderPaymentStatus.SUCCEEDED:
                if observation.source != ObservationSource.AUTHORITATIVE_STATUS_LOOKUP:
                    raise ProviderObservationError("success after failure requires authoritative provider status lookup")
            elif observation.payment_status == ProviderPaymentStatus.UNKNOWN:
                order.status = TopUpStatus.RECONCILIATION_REQUIRED
            elif observation.payment_status == ProviderPaymentStatus.PENDING:
                order.status = TopUpStatus.RECONCILIATION_REQUIRED
            else:
                self._provider_events[event_key] = event_value
                self._provider_transactions[tx_key] = logical_topup_id
                order.provider = observation.provider
                order.provider_transaction_ref = observation.provider_transaction_ref
                return False

        self._provider_events[event_key] = event_value
        self._provider_transactions[tx_key] = logical_topup_id
        order.provider = observation.provider
        order.provider_transaction_ref = observation.provider_transaction_ref

        if observation.payment_status == ProviderPaymentStatus.UNKNOWN:
            if order.status != TopUpStatus.CREDIT_FULFILLED:
                order.status = TopUpStatus.RECONCILIATION_REQUIRED
            return True
        if observation.payment_status == ProviderPaymentStatus.PENDING:
            if order.status != TopUpStatus.CREDIT_FULFILLED:
                order.status = TopUpStatus.PAYMENT_PENDING
            return True
        if observation.payment_status == ProviderPaymentStatus.FAILED:
            if order.status != TopUpStatus.CREDIT_FULFILLED:
                order.status = TopUpStatus.PAYMENT_FAILED
                order.failure_observed = True
                order.failure_observed = True
            return True

        # The trusted adapter must already have verified provider state and its
        # association with this server-owned order, amount, and currency.
        grant_id = f"topup-credit-grant:{logical_topup_id}"
        entry = CreditEntry(
            entry_id=grant_id,
            account_id=order.account_id,
            delta=order.sku.credits_granted,
            purpose="TOPUP_CREDIT_GRANT",
            reference_id=observation.provider_transaction_ref,
        )
        self.ledger.post(entry)  # unique immutable grant identity makes replay idempotent
        order.status = TopUpStatus.CREDIT_FULFILLED
        order.credits_granted = order.sku.credits_granted
        order.completed_at_utc = observed_at
        return True

    def _order(self, logical_topup_id: str) -> TopUpOrder:
        try:
            return self.orders[logical_topup_id]
        except KeyError as exc:
            raise InvalidIdentity("unknown logical top-up ID") from exc
