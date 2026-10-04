from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ce.calculation.evidence import EvidencePacket
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
    """Fail-closed downstream boundary.

    This stage materializes only the normative integrity gate. Qualification
    semantics remain read-only and are not inferred when the evidence schema
    does not explicitly carry the required state.
    """

    @staticmethod
    def _failure() -> SignalResult:
        return SignalResult(
            status=CalculationStatus.CALCULATION_FAILURE,
            classification=None,
            phase=None,
            uncertainty_state=None,
            evidence_packet_ref=None,
            canon_input_valid=False,
        )

    def evaluate(self, calculation_result: Any) -> SignalResult:
        # Signal Engine accepts EvidencePacket only at this boundary. No duck
        # typing is permitted because an arbitrary object could carry stale or
        # alternate numerical state.
        if not isinstance(calculation_result, EvidencePacket):
            return self._failure()

        packet_errors = calculation_result.validate()
        if packet_errors:
            return self._failure()

        calculation_status = calculation_result.calculation_flags.get("calculation_status")
        if calculation_status != CalculationStatus.VALID.value:
            return self._failure()

        resolution = calculation_result.actual_ephemeris_resolution
        resolution_status = resolution.get("ephemeris_resolution_status")
        if resolution_status is None:
            # "status" is retained as an explicitly supported compatibility
            # spelling already used by current EvidencePacket fixtures.
            resolution_status = resolution.get("status")
        if resolution_status != "MATCH":
            return self._failure()

        if calculation_result.errors:
            return self._failure()

        # Qualification is deliberately not inferred from incomplete evidence.
        # A future qualification stage must consume the packet read-only and
        # emit a new qualified-signal identity.
        ref = f"{calculation_result.evidence_packet_id}:{calculation_result.content_sha256()}"
        return SignalResult(
            status=CalculationStatus.NOT_IMPLEMENTED,
            classification=None,
            phase=None,
            uncertainty_state=None,
            evidence_packet_ref=ref,
            canon_input_valid=False,
        )
