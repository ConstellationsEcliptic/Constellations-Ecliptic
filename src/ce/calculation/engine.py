from __future__ import annotations

from ce.calculation.contracts import CalculationRequest, CalculationResult
from ce.ephemeris.adapter import EphemerisAdapter
from ce.foundation.status import CALENDAR_POLICY_GREGORIAN_ONLY, CalculationStatus, ScenarioState
from ce.runtime.gates import authorize_runtime
from ce.foundation.identity import RuntimeIdentity


class CalculationEngine:
    def __init__(self, runtime_identity: RuntimeIdentity, ephemeris: EphemerisAdapter) -> None:
        self._runtime_identity = runtime_identity
        self._ephemeris = ephemeris

    def calculate(self, request: CalculationRequest) -> CalculationResult:
        if request.calendar_policy_id != CALENDAR_POLICY_GREGORIAN_ONLY:
            return CalculationResult(
                request_id=request.request_id,
                status=CalculationStatus.INPUT_UNSUPPORTED,
                execution_profile_id=request.execution_profile_id,
                scenario_state=ScenarioState.NONE,
                normalized_time=None,
                errors=("unsupported_calendar_policy",),
                provenance={"calendar_policy_id": request.calendar_policy_id},
            )

        gate = authorize_runtime(self._runtime_identity)
        if gate.authority.value != "AUTHORIZED":
            return CalculationResult(
                request_id=request.request_id,
                status=CalculationStatus.NON_AUTHORIZED,
                execution_profile_id=request.execution_profile_id,
                scenario_state=ScenarioState.NONE,
                normalized_time=None,
                errors=gate.reasons,
                provenance={"runtime_authority": gate.authority.value},
            )
        # No astronomical calculation is permitted in this foundation until the
        # authoritative native Swiss Ephemeris binding is installed and verified.
        return CalculationResult(
            request_id=request.request_id,
            status=CalculationStatus.NOT_IMPLEMENTED,
            execution_profile_id=request.execution_profile_id,
            scenario_state=ScenarioState.NONE,
            normalized_time=None,
            errors=("authoritative_calculation_adapter_not_established",),
            provenance={"runtime_authority": gate.authority.value},
        )
