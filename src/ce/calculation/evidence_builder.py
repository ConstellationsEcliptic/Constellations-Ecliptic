from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ce.calculation.contracts import CalculationRequest, CalculationResultDraft
from ce.calculation.evidence import EvidencePacket
from ce.foundation.identity import CANONICAL_EXECUTION_PROFILE_ID, CANONICAL_EXECUTION_PROFILE_REVISION, RuntimeIdentity
from ce.foundation.provenance import derive_provenance_root_sha256, runtime_identity_sha256
from ce.foundation.status import CalculationStatus


class EvidenceIssuanceError(ValueError):
    """A result cannot be converted into a reconstruction-sufficient packet."""


def _canonical_input_identity(request: CalculationRequest) -> dict[str, Any]:
    birth = request.birth
    return {
        "request_id": request.request_id,
        "birth_date": birth.birth_date.isoformat(),
        "birth_city": birth.birth_city,
        "timezone_id": birth.timezone_id,
        "timezone_version": birth.timezone_version,
        "natal_birth_state": birth.natal_birth_state.value,
        "calendar_policy_id": request.calendar_policy_id,
    }


def _canonical_profile_version() -> dict[str, Any]:
    return {
        "id": CANONICAL_EXECUTION_PROFILE_ID,
        "revision": CANONICAL_EXECUTION_PROFILE_REVISION,
        "implementation_plan_version": "1.3.1",
        "technical_contracts_version": "1.1",
        "execution_profile_version": "1.3",
    }


def _canonical_timezone_context(request: CalculationRequest) -> dict[str, Any]:
    birth = request.birth
    if birth.timezone_version != "2026d":
        raise EvidenceIssuanceError("timezone_version_not_current_canonical")
    return {
        "database": "IANA",
        "id": birth.timezone_id,
        "version": birth.timezone_version,
    }


def issue_evidence_packet(
    result: CalculationResultDraft,
    *,
    request: CalculationRequest,
    runtime_identity: RuntimeIdentity,
) -> EvidencePacket:
    """Issue one immutable packet from an explicit request/runtime provenance root.

    Caller-supplied input/profile/timezone mappings are intentionally not accepted.
    They are derived from the CalculationRequest and RuntimeIdentity instead.
    """

    if result.status not in {
        CalculationStatus.VALID,
        CalculationStatus.NATAL_EVIDENCE_VARIABLE,
    }:
        raise EvidenceIssuanceError(
            f"result_status_not_evidence_issuable:{result.status.value}"
        )
    if not isinstance(request, CalculationRequest):
        raise EvidenceIssuanceError("calculation_request_required")
    if not isinstance(runtime_identity, RuntimeIdentity):
        raise EvidenceIssuanceError("runtime_identity_required")
    request_errors = request.validate()
    if request_errors:
        raise EvidenceIssuanceError("request_invalid:" + ";".join(request_errors))

    if result.calculation_id is None:
        raise EvidenceIssuanceError("calculation_id_missing")
    if result.request_id != request.request_id:
        raise EvidenceIssuanceError("request_id_mismatch")
    if result.execution_profile_id != request.execution_profile_id:
        raise EvidenceIssuanceError("execution_profile_id_mismatch")

    expected_interval = (
        request.target_interval_start_utc,
        request.target_interval_end_utc,
    )
    if result.observation_interval != expected_interval:
        raise EvidenceIssuanceError("observation_interval_request_mismatch")

    if runtime_identity.validate_shape():
        raise EvidenceIssuanceError(
            "runtime_identity_invalid:" + ";".join(runtime_identity.validate_shape())
        )

    input_identity = _canonical_input_identity(request)
    profile_version = _canonical_profile_version()
    timezone_context = _canonical_timezone_context(request)
    runtime_digest = runtime_identity_sha256(runtime_identity)
    provenance_root = derive_provenance_root_sha256(
        calculation_id=result.calculation_id,
        request_id=request.request_id,
        input_identity=input_identity,
        profile_version=profile_version,
        timezone_context=timezone_context,
        execution_profile_id=result.execution_profile_id,
        calculation_version=result.calculation_version,
        runtime_identity_digest=runtime_digest,
    )

    object_records = tuple(item.as_dict() for item in result.object_records)
    if result.status is CalculationStatus.VALID and not object_records:
        raise EvidenceIssuanceError("valid_result_requires_object_records")

    if any(
        item.get("object_status") == CalculationStatus.VALID.value
        and item.get("actual_flags") is None
        for item in object_records
    ):
        raise EvidenceIssuanceError("valid_object_missing_actual_flags")

    return EvidencePacket.issue(
        calculation_id=result.calculation_id,
        input_identity=input_identity,
        profile_version=profile_version,
        observation_instant_or_interval={
            "start": result.observation_interval[0],
            "end": result.observation_interval[1],
        },
        timezone_context=timezone_context,
        execution_profile_id=result.execution_profile_id,
        calculation_version=result.calculation_version,
        object_records=object_records,
        geometry_records=tuple(result.geometry_records),
        effective_orb_records=tuple(
            {
                "transit_object": item.get("transit_object", ""),
                "natal_object_or_scenario": item.get("natal_object_or_scenario", ""),
                "aspect": item.get("aspect", ""),
                "effective_orb": item.get("effective_orb"),
            }
            for item in result.geometry_records
            if isinstance(item, Mapping) and "effective_orb" in item
        ),
        kinematics=tuple(
            {
                "transit_object": item.get("transit_object", ""),
                "aspect": item.get("aspect", ""),
                "kinematic_state": item.get("kinematic_state", ""),
                "transit_speed": item.get("transit_speed"),
            }
            for item in result.geometry_records
            if isinstance(item, Mapping)
            and "kinematic_state" in item
        ),
        exact_events=tuple(result.event_records),
        window_segments=tuple(result.window_segments),
        scenario_stability_state=result.scenario_state.value,
        scenario_window_state=result.window_classification.value,
        possible_window_segments=tuple(result.possible_window_segments),
        robust_window_segments=tuple(result.robust_window_segments),
        scenario_observations=tuple(result.scenario_observations),
        warnings=tuple(result.warnings),
        errors=tuple(result.errors),
        numerical_tolerances=dict(
            result.solver_metadata.get("tolerances", {})
        )
        if isinstance(result.solver_metadata, Mapping)
        else {},
        solver_metadata=dict(result.solver_metadata),
        actual_ephemeris_resolution=dict(result.actual_ephemeris_resolution),
        calculation_flags=dict(result.calculation_flags),
        runtime_identity_sha256=runtime_digest,
        provenance_root_sha256=provenance_root,
    )
