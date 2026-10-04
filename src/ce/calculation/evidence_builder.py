from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ce.calculation.contracts import CalculationResultDraft
from ce.calculation.evidence import EvidencePacket
from ce.foundation.status import CalculationStatus


class EvidenceIssuanceError(ValueError):
    """A result cannot be converted into a reconstruction-sufficient packet."""


def issue_evidence_packet(
    result: CalculationResultDraft,
    *,
    input_identity: Mapping[str, Any],
    profile_version: Mapping[str, Any],
    timezone_context: Mapping[str, Any],
) -> EvidencePacket:
    """Issue one immutable packet without synthesizing missing calculation facts."""

    if result.status not in {
        CalculationStatus.VALID,
        CalculationStatus.NATAL_EVIDENCE_VARIABLE,
    }:
        raise EvidenceIssuanceError(
            f"result_status_not_evidence_issuable:{result.status.value}"
        )

    if result.calculation_id is None:
        raise EvidenceIssuanceError("calculation_id_missing")
    if result.observation_interval is None:
        raise EvidenceIssuanceError("observation_interval_missing")
    if not isinstance(input_identity, Mapping):
        raise EvidenceIssuanceError("input_identity_mapping_required")
    if not isinstance(profile_version, Mapping):
        raise EvidenceIssuanceError("profile_version_mapping_required")
    if not isinstance(timezone_context, Mapping):
        raise EvidenceIssuanceError("timezone_context_mapping_required")

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
        input_identity=dict(input_identity),
        profile_version=dict(profile_version),
        observation_instant_or_interval={
            "start": result.observation_interval[0],
            "end": result.observation_interval[1],
        },
        timezone_context=dict(timezone_context),
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
    )
