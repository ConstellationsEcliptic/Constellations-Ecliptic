"""CE commerce reference model — isolated, candidate-only, non-production."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from enum import Enum
from typing import Dict, Optional, Tuple


class CommerceError(Exception): pass
class InvalidIdentity(CommerceError): pass
class InvalidTransition(CommerceError): pass
class QuotaBlocked(CommerceError): pass
class PolicyDecisionRequired(CommerceError): pass
class InvalidFulfillment(CommerceError): pass
class FulfillmentAdmissionBlocked(CommerceError): pass
class LedgerConflict(CommerceError): pass


class CapTrigger(str, Enum):
    # Owner selected D1-A on 2026-10-10; D1-B is retained only for counterfactual tests.
    PURCHASE_DEBIT_COMMITTED = "D1_A_PURCHASE_DEBIT_COMMITTED"
    VALID_READING_ACCESSIBLE = "D1_B_VALID_READING_ACCESSIBLE"


class TerminalFailurePolicy(str, Enum):
    # Owner selected D2-B on 2026-10-10; D2-A is retained only for counterfactual tests.
    RETAIN_SAME_DATE_SLOT = "D2_A_RETAIN_SAME_DATE_SLOT"
    RELEASE_IF_ORIGINAL_DATE_CURRENT = "D2_B_RELEASE_IF_ORIGINAL_DATE_CURRENT"


class FulfillmentAdmissionState(str, Enum):
    # New purchases/debits require an explicit healthy admission state.
    READY = "READY"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"


class OrderStatus(str, Enum):
    RESERVED = "RESERVED"
    DEBIT_COMMITTED = "DEBIT_COMMITTED"
    RECONCILIATION_REQUIRED = "RECONCILIATION_REQUIRED"
    FULFILLED = "FULFILLED"
    TERMINAL_NONDELIVERY = "TERMINAL_NONDELIVERY"
    RESERVATION_REJECTED = "RESERVATION_REJECTED"


class QuotaResolution(str, Enum):
    RESERVATION_ONLY = "RESERVATION_ONLY"
    PURCHASE_TRIGGER_COMMITTED = "PURCHASE_TRIGGER_COMMITTED"
    WAITING_FOR_FULFILLMENT = "WAITING_FOR_FULFILLMENT"
    CAP_TRIGGER_NOT_SELECTED = "CAP_TRIGGER_NOT_SELECTED"
    FULFILLMENT_TRIGGER_COMMITTED = "FULFILLMENT_TRIGGER_COMMITTED"
    TERMINAL_FAILURE_SLOT_EFFECT_UNRESOLVED = "TERMINAL_FAILURE_SLOT_EFFECT_UNRESOLVED"
    TERMINAL_FAILURE_RETAINED = "TERMINAL_FAILURE_RETAINED"
    RELEASED_ON_ORIGINAL_DATE = "RELEASED_ON_ORIGINAL_DATE"
    ORIGINAL_DATE_EXPIRED_NO_TRANSFER = "ORIGINAL_DATE_EXPIRED_NO_TRANSFER"
    PREDEBIT_RESERVATION_RELEASED = "PREDEBIT_RESERVATION_RELEASED"
    PREDEBIT_RESERVATION_EXPIRED_NO_TRANSFER = "PREDEBIT_RESERVATION_EXPIRED_NO_TRANSFER"


@dataclass(frozen=True)
class CreditEntry:
    entry_id: str
    account_id: str
    delta: int
    purpose: str
    reference_id: str


class CreditLedger:
    """In-memory ledger semantics; not a database/concurrency implementation."""

    def __init__(self) -> None:
        self.entries: Dict[str, CreditEntry] = {}
        self._balances: Dict[str, int] = {}
        self._restoration_by_debit: Dict[str, str] = {}

    def balance(self, account_id: str) -> int:
        return self._balances.get(account_id, 0)

    def post(self, entry: CreditEntry) -> bool:
        if not entry.entry_id or not entry.account_id or not entry.reference_id:
            raise InvalidIdentity("entry, account, and reference IDs are required")
        prior = self.entries.get(entry.entry_id)
        if prior is not None:
            if prior != entry:
                raise LedgerConflict("entry ID reused with different economic meaning")
            return False
        if entry.delta < 0 and self.balance(entry.account_id) + entry.delta < 0:
            raise LedgerConflict("Credits balance cannot become negative")
        self.entries[entry.entry_id] = entry
        self._balances[entry.account_id] = self.balance(entry.account_id) + entry.delta
        return True

    def restore_reading_debit(self, restoration_id: str, debit_id: str, account_id: str) -> bool:
        debit = self.entries.get(debit_id)
        if debit is None or debit.account_id != account_id:
            raise LedgerConflict("restoration must reference this account's existing debit")
        if debit.purpose != "DEEP_SKY_READING_DEBIT" or debit.delta >= 0:
            raise LedgerConflict("only a reading debit can be restored")
        previous_id = self._restoration_by_debit.get(debit_id)
        expected = CreditEntry(
            restoration_id, account_id, -debit.delta,
            "DEEP_SKY_READING_DEBIT_RESTORATION", debit_id
        )
        if previous_id is not None:
            if previous_id == restoration_id and self.entries.get(previous_id) == expected:
                return False
            raise LedgerConflict("reading debit already has a different restoration")
        self.post(expected)
        self._restoration_by_debit[debit_id] = restoration_id
        return True

    def debit_restored_exactly_once(self, debit_id: str) -> bool:
        restoration_id = self._restoration_by_debit.get(debit_id)
        debit = self.entries.get(debit_id)
        restoration = self.entries.get(restoration_id) if restoration_id else None
        return bool(
            debit and restoration
            and restoration.account_id == debit.account_id
            and restoration.delta == -debit.delta
            and restoration.purpose == "DEEP_SKY_READING_DEBIT_RESTORATION"
            and restoration.reference_id == debit_id
        )


@dataclass(frozen=True)
class TerminalFailureEvidence:
    no_valid_reading_accessible: bool
    no_operation_can_still_deliver: bool
    no_entitlement_exists: bool
    all_relevant_operations_closed: bool

    @property
    def complete(self) -> bool:
        return all((
            self.no_valid_reading_accessible,
            self.no_operation_can_still_deliver,
            self.no_entitlement_exists,
            self.all_relevant_operations_closed,
        ))


@dataclass(frozen=True)
class PreDebitFailureEvidence:
    no_reading_debit_committed: bool
    no_operation_can_still_commit_or_deliver: bool
    all_relevant_operations_closed: bool
    evidence_reference: str

    @property
    def complete(self) -> bool:
        return all((
            self.no_reading_debit_committed,
            self.no_operation_can_still_commit_or_deliver,
            self.all_relevant_operations_closed,
            bool(self.evidence_reference and self.evidence_reference.strip()),
        ))


@dataclass
class Order:
    logical_purchase_id: str
    account_id: str
    service_date_utc: date
    status: OrderStatus = OrderStatus.RESERVED
    reading_debit_entry_id: Optional[str] = None
    entitlement_id: Optional[str] = None
    reading_reference: Optional[str] = None
    reading_content_hash: Optional[str] = None
    quota_effect: Optional[bool] = None
    quota_resolution: QuotaResolution = QuotaResolution.RESERVATION_ONLY
    terminal_restoration_id: Optional[str] = None
    predebit_failure_evidence_reference: Optional[str] = None
    provider_events: Dict[Tuple[str, str], str] = field(default_factory=dict)


class CommerceReferenceModel:
    """Candidate model; owner-selected D1-A/D2-B defaults and fail-closed admission gate."""

    def __init__(
        self,
        *,
        cap_trigger: Optional[CapTrigger] = CapTrigger.PURCHASE_DEBIT_COMMITTED,
        terminal_failure_policy: Optional[TerminalFailurePolicy] = TerminalFailurePolicy.RELEASE_IF_ORIGINAL_DATE_CURRENT,
        fulfillment_admission: FulfillmentAdmissionState = FulfillmentAdmissionState.UNKNOWN,
        fulfillment_admission_expires_at: Optional[datetime] = None,
        fulfillment_attestation_reference: Optional[str] = None,
    ) -> None:
        self.cap_trigger = cap_trigger
        self.terminal_failure_policy = terminal_failure_policy
        self.fulfillment_admission = FulfillmentAdmissionState.UNKNOWN
        self.fulfillment_admission_expires_at: Optional[datetime] = None
        self.fulfillment_attestation_reference: Optional[str] = None
        self.set_fulfillment_admission(
            fulfillment_admission,
            attestation_reference=fulfillment_attestation_reference,
            valid_until=fulfillment_admission_expires_at,
        )
        self.orders: Dict[str, Order] = {}
        self.ledger = CreditLedger()
        # Provider event IDs are unique within each provider across all orders.
        self._provider_events: Dict[Tuple[str, str], Tuple[str, str]] = {}

    def set_fulfillment_admission(
        self,
        state: FulfillmentAdmissionState,
        *,
        attestation_reference: Optional[str] = None,
        valid_until: Optional[datetime] = None,
    ) -> None:
        """Set the simulated gate; READY requires evidence and a future expiry."""
        if not isinstance(state, FulfillmentAdmissionState):
            raise InvalidIdentity("fulfillment admission must be an explicit known enum state")
        if state == FulfillmentAdmissionState.READY:
            if not attestation_reference or not attestation_reference.strip() or not valid_until:
                raise InvalidIdentity("READY admission requires health attestation and expiry")
            valid_until_utc = self._utc(valid_until)
            now_utc = datetime.now(timezone.utc)
            if valid_until_utc <= now_utc:
                raise InvalidIdentity("READY admission attestation must not already be expired")
            if valid_until_utc > now_utc + timedelta(minutes=5):
                raise InvalidIdentity("READY admission lease exceeds the provisional five-minute candidate ceiling")
            self.fulfillment_admission_expires_at = valid_until_utc
            self.fulfillment_attestation_reference = attestation_reference
        else:
            if attestation_reference is not None or valid_until is not None:
                raise InvalidIdentity("non-READY admission must not carry active READY attestation")
            self.fulfillment_admission_expires_at = None
            self.fulfillment_attestation_reference = None
        self.fulfillment_admission = state

    def _admission_is_ready(self) -> bool:
        expires = self.fulfillment_admission_expires_at
        return bool(
            self.fulfillment_admission == FulfillmentAdmissionState.READY
            and self.fulfillment_attestation_reference
            and expires is not None
            and expires > datetime.now(timezone.utc)
        )

    @staticmethod
    def _utc(timestamp: datetime) -> datetime:
        if timestamp.tzinfo is None or timestamp.utcoffset() is None:
            raise InvalidIdentity("server timestamp must be timezone-aware")
        return timestamp.astimezone(timezone.utc)

    def confirm_and_reserve(self, account_id: str, logical_purchase_id: str,
                            server_confirmed_at: datetime) -> Order:
        """Bind a confirmed logical order to the server-derived, immutable UTC date."""
        if not account_id or not logical_purchase_id:
            raise InvalidIdentity("account and logical purchase IDs are required")
        confirmed_utc = self._utc(server_confirmed_at)
        existing = self.orders.get(logical_purchase_id)
        if existing:
            if existing.account_id != account_id:
                raise InvalidIdentity("logical purchase ID cannot cross accounts")
            # Existing logical-order retries remain available for reconciliation even
            # while the gate is closed; they do not create a new purchase.
            return existing
        if not self._admission_is_ready():
            raise FulfillmentAdmissionBlocked(
                "new Deep Sky purchase requires a current READY health attestation"
            )

        service_date = confirmed_utc.date()
        account_orders = [o for o in self.orders.values() if o.account_id == account_id]
        for prior in account_orders:
            if prior.service_date_utc != service_date and prior.status in {
                OrderStatus.RESERVED, OrderStatus.DEBIT_COMMITTED,
                OrderStatus.RECONCILIATION_REQUIRED,
            }:
                raise PolicyDecisionRequired(
                    "new-date eligibility while a prior order is unresolved is not disposed"
                )
        for prior in account_orders:
            if prior.service_date_utc != service_date:
                continue
            if prior.status in {
                OrderStatus.RESERVED, OrderStatus.DEBIT_COMMITTED,
                OrderStatus.RECONCILIATION_REQUIRED,
            }:
                raise QuotaBlocked("another logical order for this account/date is unresolved")
            if prior.quota_effect is None:
                raise PolicyDecisionRequired("prior order's cap effect is unresolved")
            if prior.quota_effect:
                raise QuotaBlocked("daily cap is already consumed for this account/date")
            if prior.status == OrderStatus.TERMINAL_NONDELIVERY and self.terminal_failure_policy is None:
                raise PolicyDecisionRequired("terminal-failure slot effect has no selected policy")

        order = Order(logical_purchase_id, account_id, service_date)
        self.orders[logical_purchase_id] = order
        return order

    def commit_reading_debit(self, logical_purchase_id: str, debit_id: str, cost: int) -> bool:
        order = self._order(logical_purchase_id)
        if not debit_id or cost <= 0:
            raise InvalidIdentity("debit ID and positive Credits cost are required")
        if order.reading_debit_entry_id:
            if order.reading_debit_entry_id != debit_id:
                raise LedgerConflict("order already has a different reading debit")
            self.ledger.post(CreditEntry(
                debit_id, order.account_id, -cost, "DEEP_SKY_READING_DEBIT", logical_purchase_id
            ))
            return False
        if order.status != OrderStatus.RESERVED:
            raise InvalidTransition("new debit requires RESERVED state; reconcile unknown outcomes first")
        # Recheck admission at D1-A's effective-purchase debit boundary.
        # Idempotent replay of an already committed debit returned above.
        if not self._admission_is_ready():
            raise FulfillmentAdmissionBlocked(
                "new reading debit requires a current READY health attestation"
            )
        self.ledger.post(CreditEntry(
            debit_id, order.account_id, -cost, "DEEP_SKY_READING_DEBIT", logical_purchase_id
        ))
        order.reading_debit_entry_id = debit_id
        order.status = OrderStatus.DEBIT_COMMITTED
        if self.cap_trigger == CapTrigger.PURCHASE_DEBIT_COMMITTED:
            order.quota_effect = True
            order.quota_resolution = QuotaResolution.PURCHASE_TRIGGER_COMMITTED
        elif self.cap_trigger == CapTrigger.VALID_READING_ACCESSIBLE:
            order.quota_effect = False
            order.quota_resolution = QuotaResolution.WAITING_FOR_FULFILLMENT
        else:
            order.quota_effect = None
            order.quota_resolution = QuotaResolution.CAP_TRIGGER_NOT_SELECTED
        return True

    def mark_outcome_unknown(self, logical_purchase_id: str) -> None:
        order = self._order(logical_purchase_id)
        if order.status in {OrderStatus.FULFILLED, OrderStatus.TERMINAL_NONDELIVERY}:
            return
        if order.status not in {
            OrderStatus.RESERVED, OrderStatus.DEBIT_COMMITTED, OrderStatus.RECONCILIATION_REQUIRED
        }:
            raise InvalidTransition("cannot mark this state as unknown")
        order.status = OrderStatus.RECONCILIATION_REQUIRED

    def record_provider_event(self, logical_purchase_id: str, provider: str,
                              event_id: str, canonical_payload: str) -> bool:
        order = self._order(logical_purchase_id)
        if not provider or not event_id:
            raise InvalidIdentity("provider and event IDs are required")
        key = (provider, event_id)
        current = (logical_purchase_id, canonical_payload)
        previous = self._provider_events.get(key)
        if previous is not None:
            if previous != current:
                raise LedgerConflict("provider event ID reused with a different order/payload")
            return False
        self._provider_events[key] = current
        order.provider_events[key] = canonical_payload
        return True

    def fulfill_validated_reading(self, logical_purchase_id: str, *, entitlement_id: str,
                                  reading_reference: str, content_hash: str,
                                  output_valid: bool, accessible: bool) -> bool:
        order = self._order(logical_purchase_id)
        if not output_valid or not accessible:
            raise InvalidFulfillment("fulfillment requires validated output and actual access")
        if not entitlement_id or not reading_reference or not content_hash:
            raise InvalidIdentity("entitlement, reading reference, and hash are required")
        if not order.reading_debit_entry_id:
            raise InvalidTransition("paid reading cannot fulfill before debit commit")
        submitted = (entitlement_id, reading_reference, content_hash)
        existing = (order.entitlement_id, order.reading_reference, order.reading_content_hash)
        if order.status == OrderStatus.FULFILLED:
            if submitted != existing:
                raise LedgerConflict("fulfillment replay conflicts with existing output")
            return False
        if order.status == OrderStatus.TERMINAL_NONDELIVERY:
            raise InvalidTransition("terminally failed order cannot fulfill")
        order.entitlement_id, order.reading_reference, order.reading_content_hash = submitted
        order.status = OrderStatus.FULFILLED
        order.quota_effect = True if self.cap_trigger is not None else None
        order.quota_resolution = (
            QuotaResolution.FULFILLMENT_TRIGGER_COMMITTED
            if self.cap_trigger is not None else QuotaResolution.CAP_TRIGGER_NOT_SELECTED
        )
        return True

    def confirm_predebit_failure(self, logical_purchase_id: str, *,
                                 evidence: PreDebitFailureEvidence,
                                 close_at: datetime) -> bool:
        """Close a positively evidenced reservation failure before any reading debit."""
        order = self._order(logical_purchase_id)
        closed_utc = self._utc(close_at)
        if order.status == OrderStatus.RESERVATION_REJECTED:
            if order.predebit_failure_evidence_reference == evidence.evidence_reference:
                return False
            raise LedgerConflict("pre-debit failure replay conflicts with the recorded evidence")
        if order.status not in {OrderStatus.RESERVED, OrderStatus.RECONCILIATION_REQUIRED}:
            raise InvalidTransition("pre-debit failure applies only to an unresolved order")
        if order.reading_debit_entry_id is not None:
            raise InvalidTransition("a committed reading debit must use the D2-B post-debit remedy path")
        if any(entry.purpose == "DEEP_SKY_READING_DEBIT" and entry.reference_id == logical_purchase_id
               for entry in self.ledger.entries.values()):
            raise LedgerConflict("ledger contains a reading debit despite the order's uncommitted state")
        if order.entitlement_id is not None:
            raise InvalidTransition("pre-debit failure cannot close an order with a reading entitlement")
        if not evidence.complete:
            raise InvalidTransition("pre-debit failure evidence is incomplete")
        order.status = OrderStatus.RESERVATION_REJECTED
        order.predebit_failure_evidence_reference = evidence.evidence_reference
        order.quota_effect = False
        order.quota_resolution = (
            QuotaResolution.PREDEBIT_RESERVATION_RELEASED
            if closed_utc.date() == order.service_date_utc
            else QuotaResolution.PREDEBIT_RESERVATION_EXPIRED_NO_TRANSFER
        )
        return True

    def confirm_terminal_non_delivery(self, logical_purchase_id: str, *,
                                      evidence: TerminalFailureEvidence,
                                      restoration_id: str, close_at: datetime) -> bool:
        """Requires positive terminal evidence and an exactly-once debit restoration."""
        order = self._order(logical_purchase_id)
        closed_utc = self._utc(close_at)
        if order.status == OrderStatus.TERMINAL_NONDELIVERY:
            if order.terminal_restoration_id == restoration_id:
                return False
            raise LedgerConflict("terminal failure replay uses a different restoration ID")
        if order.status == OrderStatus.FULFILLED or order.entitlement_id is not None:
            raise InvalidTransition("fulfilled order cannot become terminal non-delivery")
        if not order.reading_debit_entry_id:
            raise InvalidTransition("terminal non-delivery path requires a committed reading debit")
        if not evidence.complete:
            raise InvalidTransition("terminal non-delivery evidence is incomplete")
        self.ledger.restore_reading_debit(
            restoration_id, order.reading_debit_entry_id, order.account_id
        )
        if not self.ledger.debit_restored_exactly_once(order.reading_debit_entry_id):
            raise LedgerConflict("ledger does not prove exact one-time restoration")

        order.status = OrderStatus.TERMINAL_NONDELIVERY
        order.terminal_restoration_id = restoration_id
        if self.terminal_failure_policy is None:
            order.quota_effect = True if order.quota_effect is True else None
            order.quota_resolution = QuotaResolution.TERMINAL_FAILURE_SLOT_EFFECT_UNRESOLVED
        elif self.terminal_failure_policy == TerminalFailurePolicy.RETAIN_SAME_DATE_SLOT:
            order.quota_effect = True
            order.quota_resolution = QuotaResolution.TERMINAL_FAILURE_RETAINED
        else:
            order.quota_effect = False
            order.quota_resolution = (
                QuotaResolution.RELEASED_ON_ORIGINAL_DATE
                if closed_utc.date() == order.service_date_utc
                else QuotaResolution.ORIGINAL_DATE_EXPIRED_NO_TRANSFER
            )
        return True

    def _order(self, logical_purchase_id: str) -> Order:
        try:
            return self.orders[logical_purchase_id]
        except KeyError as exc:
            raise InvalidIdentity("unknown logical purchase ID") from exc
