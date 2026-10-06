from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
import re

from ce.calculation.evidence import EvidencePacket
from ce.foundation.hashing import sha256_bytes
from ce.foundation.serialization import canonical_json
from ce.signal.engine import SignalEngine


QUALIFIED_SIGNAL_RECORD_SCHEMA_VERSION = "CE-QUALIFIED-SIGNAL-RECORD-V1"
_SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")
_UTC_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?Z$")


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

    def __post_init__(self) -> None:
        if self.schema_version != QUALIFIED_SIGNAL_RECORD_SCHEMA_VERSION:
            raise ValueError("qualified_signal_schema_version_mismatch")
        if not isinstance(self.signal_id, str) or not self.signal_id.startswith("CE-SIGNAL-"):
            raise ValueError("qualified_signal_id_invalid")
        if not isinstance(self.evidence_packet_ref, str) or ":" not in self.evidence_packet_ref:
            raise ValueError("qualified_signal_evidence_ref_invalid")
        packet_id, content_hash = self.evidence_packet_ref.split(":", 1)
        if not packet_id.strip() or not _SHA256_RE.fullmatch(content_hash):
            raise ValueError("qualified_signal_evidence_ref_invalid")
        if not isinstance(self.timestamp_observation_utc, str) or not _UTC_RE.fullmatch(self.timestamp_observation_utc):
            raise ValueError("qualified_signal_observation_time_invalid")
        if self.qualification_status != "VALID":
            raise ValueError("qualified_signal_status_invalid")
        if not isinstance(self.classification, str) or not self.classification.strip():
            raise ValueError("qualified_signal_classification_invalid")
        if self.kinematic_phase not in {"EXACT", "APPLYING", "SEPARATING", "MIXED"}:
            raise ValueError("qualified_signal_phase_invalid")
        if self.phase_uniformity not in {"UNIFORM", "MIXED"}:
            raise ValueError("qualified_signal_phase_uniformity_invalid")
        if not self.canon_input_valid:
            raise ValueError("qualified_signal_canon_input_invalid")
        if not isinstance(self.environment_pin, str) or not self.environment_pin.startswith("sha256:") or not _SHA256_RE.fullmatch(self.environment_pin[7:]):
            raise ValueError("qualified_signal_environment_pin_invalid")


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


def issue_qualified_signal_record(packet: EvidencePacket) -> QualifiedSignalRecord:
    """Derive one normative signal record from an immutable EvidencePacket.

    The caller cannot provide a precomputed SignalResult. Qualification is
    recomputed only at the Signal Engine layer from evidence; astronomical
    coordinates themselves are never recomputed here.
    """
    if not isinstance(packet, EvidencePacket):
        raise ValueError("qualified_signal_evidence_packet_required")
    packet_errors = packet.validate(require_issued=True)
    if packet_errors:
        raise ValueError(";".join(f"qualified_signal_evidence:{e}" for e in packet_errors))
    if not packet.runtime_identity_sha256:
        raise ValueError("qualified_signal_runtime_identity_required")

    result = SignalEngine().evaluate(packet)
    if result.status.value != "VALID" or not result.canon_input_valid:
        raise ValueError("qualified_signal_result_not_eligible")
    expected_ref = f"{packet.evidence_packet_id}:{packet.content_sha256()}"
    if result.evidence_packet_ref != expected_ref:
        raise ValueError("qualified_signal_evidence_reference_mismatch")
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

    identity_payload = {
        "schema_version": QUALIFIED_SIGNAL_RECORD_SCHEMA_VERSION,
        "signal_engine_contract": "CE-SIGNAL-ENGINE-V1-R1",
        "evidence_packet_content_sha256": packet.content_sha256(),
        "evidence_packet_ref": expected_ref,
        "classification": result.classification,
        "phase": result.phase,
        "uncertainty_state": result.uncertainty_state,
        "observation_start_utc": observation_start,
    }
    signal_id = "CE-SIGNAL-" + sha256_bytes(canonical_json(identity_payload))

    requires_disclaimer = result.uncertainty_state in {"POSSIBLE", "MIXED"}

    return QualifiedSignalRecord(
        schema_version=QUALIFIED_SIGNAL_RECORD_SCHEMA_VERSION,
        signal_id=signal_id,
        evidence_packet_ref=expected_ref,
        timestamp_observation_utc=observation_start,
        qualification_status=result.status.value,
        classification=result.classification,
        kinematic_phase=result.phase,
        phase_uniformity=phase_uniformity,
        canon_input_valid=True,
        requires_uncertainty_disclaimer=requires_disclaimer,
        environment_pin="sha256:" + packet.runtime_identity_sha256,
    )
