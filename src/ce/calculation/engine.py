from __future__ import annotations

from ce.calculation.contracts import CalculationRequest, CalculationResult
from ce.ephemeris.adapter import EphemerisAdapter
from ce.foundation.identity import CANONICAL_EXECUTION_PROFILE_ID, RuntimeIdentity
from ce.foundation.status import CalculationStatus, ScenarioState
from ce.runtime.gates import authorize_runtime


class CalculationEngine:
    def __init__(self, runtime_identity: RuntimeIdentity, ephemeris: EphemerisAdapter) -> None:
        self._runtime_identity = runtime_identity
        self._ephemeris = ephemeris

    def _invalid_request(self, request: object, errors: tuple[str, ...]) -> CalculationResult:
        request_id_value = getattr(request, "request_id", None)
        request_id = (
            request_id_value
            if isinstance(request_id_value, str) and request_id_value.strip()
            else "INVALID_INPUT"
        )
        return CalculationResult(
            request_id=request_id,
            status=CalculationStatus.INVALID_INPUT,
            execution_profile_id=CANONICAL_EXECUTION_PROFILE_ID,
            scenario_state=ScenarioState.NONE,
            normalized_time=None,
            errors=errors,
            provenance={},
        )

    def calculate(self, request: CalculationRequest) -> CalculationResult:
        if not isinstance(request, CalculationRequest):
            return self._invalid_request(request, ("invalid_request_type",))

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
