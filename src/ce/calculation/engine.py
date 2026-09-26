from __future__ import annotations

from ce.calculation.contracts import CalculationRequest, CalculationResult
from ce.ephemeris.adapter import EphemerisAdapter
from ce.foundation.identity import RuntimeIdentity
from ce.foundation.status import CalculationStatus, ScenarioState
from ce.runtime.gates import authorize_runtime


class CalculationEngine:
    def __init__(self, runtime_identity: RuntimeIdentity, ephemeris: EphemerisAdapter) -> None:
        self._runtime_identity = runtime_identity
        self._ephemeris = ephemeris

    def _invalid_request(self, request: CalculationRequest, errors: tuple[str, ...]) -> CalculationResult:
        return CalculationResult(
            request_id=request.request_id if isinstance(request.request_id, str) else "",
            status=CalculationStatus.INVALID_INPUT,
            execution_profile_id=request.execution_profile_id if isinstance(request.execution_profile_id, str) else "",
            scenario_state=ScenarioState.NONE,
            normalized_time=None,
            errors=errors,
            provenance={},
        )

    def calculate(self, request: CalculationRequest) -> CalculationResult:
        request_errors = request.validate()
        if request_errors:
            return self._invalid_request(request, request_errors)

        if request.execution_profile_id != self._runtime_identity.execution_profile_id:
            return self._invalid_request(request, ("request_execution_profile_mismatch",))

        gate = authorize_runtime(self._runtime_identity)
        if gate.authority.value != "AUTHORIZED":
            return CalculationResult(
                request_id=request.request_id,
                status=CalculationStatus.NON_AUTHORIZED,
                execution_profile_id=request.execution_profile_id,
                scenario_state=ScenarioState.NONE,
                normalized_time=None,
                errors=gate.reasons,
                provenance={},
            )

        return CalculationResult(
            request_id=request.request_id,
            status=CalculationStatus.NOT_IMPLEMENTED,
            execution_profile_id=request.execution_profile_id,
            scenario_state=ScenarioState.NONE,
            normalized_time=None,
            errors=("authoritative_calculation_adapter_not_established",),
            provenance={},
        )
