from __future__ import annotations

from dataclasses import dataclass

from ce.foundation.status import CalculationStatus


@dataclass(frozen=True)
class SignalResult:
    status: CalculationStatus
    classification: str | None
    phase: str | None
    uncertainty_state: str | None
    evidence_packet_ref: str | None
    canon_input_valid: bool


class SignalEngine:
    """Fail-closed foundation boundary; qualification rules are not yet materialized."""

    def evaluate(self, calculation_result: object) -> SignalResult:
        return SignalResult(
            status=CalculationStatus.NOT_IMPLEMENTED,
            classification=None,
            phase=None,
            uncertainty_state=None,
            evidence_packet_ref=None,
            canon_input_valid=False,
        )
