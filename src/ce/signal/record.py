from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Mapping

from ce.calculation.evidence import EvidencePacket
from ce.foundation.hashing import sha256_bytes
from ce.foundation.serialization import canonical_json
from ce.signal.engine import SignalResult


QUALIFIED_SIGNAL_RECORD_SCHEMA_VERSION = "CE-QUALIFIED-SIGNAL-RECORD-V1"


@dataclass(frozen=True)
class QualifiedSignalRecord:
    schema_version: str
    signal_id: str
    evidence_packet_ref: str
    timestamp_observation_utc: str
    qualification_status: str
    classification: str
    kinematic_phase: str
    phase_uniformity: str
    canon_input_valid: bool
    requires_uncertainty_disclaimer: bool
    environment_pin: str


def _phase_states(packet: EvidencePacket) -> tuple[str, ...]:
    states: set[str] = set()
    for record in packet.geometry_records:
        if isinstance(record, Mapping):
            state = record.get("kinematic_state")
            if isinstance(state, str) and state.strip():
                states.add(state)
    if not states:
        for record in packet.kinematics:
            if isinstance(record, Mapping):
                state = record.get("kinematic_state")
                if isinstance(state, str) and state.strip():
                    states.add(state)
    return tuple(sorted(states))


def _signal_identity_payload(packet: EvidencePacket) -> dict[str, object]:
    identities: set[tuple[str, str, str, float]] = set()
    for record in packet.geometry_records:
        if not isinstance(record, Mapping):
            continue
        transit = record.get("transit_object")
        natal = record.get("natal_object_or_scenario")
        aspect = record.get("aspect")
        branch = record.get("directed_branch")
        if (
            isinstance(transit, str)
            and transit
            and isinstance(natal, str)
            and natal
            and isinstance(aspect, str)
            and aspect
            and isinstance(branch, (int, float))
            and not isinstance(branch, bool)
        ):
            identities.add((transit, natal, aspect, float(branch)))
    if not identities:
        raise ValueError("qualified_signal_identity_geometry_missing")

    observation_start = packet.observation_instant_or_interval.get("start")
    if not isinstance(observation_start, str) or not observation_start:
        raise ValueError("qualified_signal_observation_start_missing")

    return {
        "transit_natal_aspect_branches": [
            {
                "transit_object": transit,
                "natal_object_or_scenario": natal,
                "aspect": aspect,
                "directed_branch": branch,
            }
            for transit, natal, aspect, branch in sorted(identities)
        ],
        "observation_start_utc": observation_start,
        "calculation_environment": {
            "execution_profile_id": packet.execution_profile_id,
            "profile_version": packet.profile_version,
            "calculation_version": packet.calculation_version,
            "timezone_context": packet.timezone_context,
            "actual_ephemeris_resolution": packet.actual_ephemeris_resolution,
            "calculation_flags": packet.calculation_flags,
            "solver_metadata": packet.solver_metadata,
            "numerical_tolerances": packet.numerical_tolerances,
        },
    }


def issue_qualified_signal_record(
    packet: EvidencePacket,
    result: SignalResult,
) -> QualifiedSignalRecord:
    """Materialize the normative record from already-qualified immutable evidence."""

    if not isinstance(packet, EvidencePacket):
        raise ValueError("qualified_signal_evidence_packet_required")
    if not isinstance(result, SignalResult):
        raise ValueError("qualified_signal_result_required")
    if result.status.value != "VALID" or not result.canon_input_valid:
        raise ValueError("qualified_signal_result_not_eligible")
    if not result.classification:
        raise ValueError("qualified_signal_classification_missing")
    if not result.phase:
        raise ValueError("qualified_signal_phase_missing")

    observation_start = packet.observation_instant_or_interval.get("start")
    if not isinstance(observation_start, str) or not observation_start:
        raise ValueError("qualified_signal_observation_start_missing")

    phases = _phase_states(packet)
    if not phases:
        raise ValueError("qualified_signal_phase_evidence_missing")
    phase_uniformity = "UNIFORM" if len(phases) == 1 else "MIXED"
    if result.phase == "MIXED" and phase_uniformity != "MIXED":
        raise ValueError("qualified_signal_phase_uniformity_conflict")

    identity_payload = _signal_identity_payload(packet)
    signal_id = "CE-SIGNAL-" + sha256_bytes(
        canonical_json(identity_payload)
    )
    environment_pin = "sha256:" + sha256_bytes(
        canonical_json(identity_payload["calculation_environment"])
    )

    requires_disclaimer = result.uncertainty_state in {"POSSIBLE", "MIXED"}

    return QualifiedSignalRecord(
        schema_version=QUALIFIED_SIGNAL_RECORD_SCHEMA_VERSION,
        signal_id=signal_id,
        evidence_packet_ref=result.evidence_packet_ref
        or f"{packet.evidence_packet_id}:{packet.content_sha256()}",
        timestamp_observation_utc=observation_start,
        qualification_status=result.status.value,
        classification=result.classification,
        kinematic_phase=result.phase,
        phase_uniformity=phase_uniformity,
        canon_input_valid=True,
        requires_uncertainty_disclaimer=requires_disclaimer,
        environment_pin=environment_pin,
    )
