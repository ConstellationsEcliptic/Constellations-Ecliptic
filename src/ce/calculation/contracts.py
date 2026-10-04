from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field, fields
from datetime import date, datetime, timezone
import math
import re
from typing import Any

from ce.calculation.evidence import EvidencePacket, EvidencePacketRef
from ce.foundation.identity import CANONICAL_EXECUTION_PROFILE_ID, CANONICAL_EXECUTION_PROFILE_REVISION, RuntimeIdentity
from ce.foundation.serialization import canonical_json
from ce.foundation.status import (
    CALENDAR_POLICY_GREGORIAN_ONLY,
    CalculationStatus,
    NatalBirthState,
    ScenarioState,
)


_COMMIT_RE = re.compile(r"^[0-9a-fA-F]{40}$")
_SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")
_RUNTIME_IMAGE_RE = re.compile(r"^sha256:[0-9a-fA-F]{64}$")
_UTC_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?Z$")


def _freeze(value: Any) -> Any:
    from types import MappingProxyType

    if isinstance(value, Mapping):
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(_freeze(item) for item in value)
    if isinstance(value, tuple):
        return tuple(_freeze(item) for item in value)
    return value


def _nonempty(value: Any, name: str) -> str | None:
    return None if isinstance(value, str) and value.strip() else f"invalid:{name}"


def _valid_utc(value: Any) -> bool:
    if not isinstance(value, str) or not _UTC_RE.fullmatch(value):
        return False
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError:
        return False
    return parsed.tzinfo is not None and parsed.utcoffset() == timezone.utc.utcoffset(parsed)


def _finite_number(value: Any) -> bool:
    return type(value) in (int, float) and (type(value) is int or math.isfinite(value))


@dataclass(frozen=True)
class BirthInput:
    """Current V1 natal input: birth time is deliberately absent."""

    birth_date: date
    birth_city: str
    timezone_id: str
    timezone_version: str | None
    natal_birth_state: NatalBirthState = NatalBirthState.ZERO_BIRTH_TIME

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []
        if type(self.birth_date) is not date:
            errors.append("invalid:birth_date")
        if not isinstance(self.natal_birth_state, NatalBirthState):
            errors.append("invalid:natal_birth_state")
        if _nonempty(self.birth_city, "birth_city") is not None:
            errors.append("invalid:birth_city")
        if _nonempty(self.timezone_id, "timezone_id") is not None:
            errors.append("invalid:timezone_id")
        if self.timezone_version is not None and not isinstance(self.timezone_version, str):
            errors.append("invalid:timezone_version")
        return tuple(errors)

    def __post_init__(self) -> None:
        errors = self.validate()
        if errors:
            raise ValueError(";".join(errors))


@dataclass(frozen=True)
class CalculationRequest:
    request_id: str
    birth: BirthInput
    target_interval_start_utc: str
    target_interval_end_utc: str
    execution_profile_id: str
    calendar_policy_id: str = CALENDAR_POLICY_GREGORIAN_ONLY

    def validate(self) -> tuple[str, ...]:
        errors = []
        if _nonempty(self.request_id, "request_id"):
            errors.append(f"invalid:request_id")
        if not isinstance(self.birth, BirthInput):
            errors.append("invalid:birth")
        elif (birth_errors := self.birth.validate()):
            errors.extend(birth_errors)
        if not _valid_utc(self.target_interval_start_utc):
            errors.append("invalid:target_interval_start_utc")
        if not _valid_utc(self.target_interval_end_utc):
            errors.append("invalid:target_interval_end_utc")
        if _valid_utc(self.target_interval_start_utc) and _valid_utc(self.target_interval_end_utc):
            start = datetime.fromisoformat(self.target_interval_start_utc[:-1] + "+00:00")
            end = datetime.fromisoformat(self.target_interval_end_utc[:-1] + "+00:00")
            if end <= start:
                errors.append("invalid:target_interval_order")
        if self.execution_profile_id != CANONICAL_EXECUTION_PROFILE_ID:
            errors.append("invalid:execution_profile_id:canonical_required")
        if not isinstance(self.calendar_policy_id, str) or not self.calendar_policy_id.strip():
            errors.append("invalid:calendar_policy_id")
        return tuple(errors)

    def __post_init__(self) -> None:
        errors = self.validate()
        if errors:
            raise ValueError(";".join(errors))


@dataclass(frozen=True)
class ObjectState:
    object_id: str
    longitude_deg: float | None
    speed_deg_per_day: float | None
    status: CalculationStatus

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []
        if _nonempty(self.object_id, "object_id"):
            errors.append("invalid:object_id")
        if not isinstance(self.status, CalculationStatus):
            errors.append("invalid:object_state_status")
            return tuple(errors)
        if self.status in {CalculationStatus.VALID, CalculationStatus.NATAL_EVIDENCE_VARIABLE}:
            if self.longitude_deg is None or not _finite_number(self.longitude_deg):
                errors.append("valid_object_requires_finite_longitude")
            elif not 0.0 <= float(self.longitude_deg) < 360.0:
                errors.append("valid_object_requires_normalized_longitude")
            if self.speed_deg_per_day is not None and not _finite_number(self.speed_deg_per_day):
                errors.append("valid_object_speed_must_be_finite")
        else:
            for value, name in (
                (self.longitude_deg, "longitude"),
                (self.speed_deg_per_day, "speed"),
            ):
                if value is not None and not _finite_number(value):
                    errors.append(f"nonvalid_object_{name}_must_be_finite_or_none")
        return tuple(errors)

    def __post_init__(self) -> None:
        errors = self.validate()
        if errors:
            raise ValueError(";".join(errors))


def _validate_runtime_provenance(provenance: Mapping[str, Any], runtime_identity: RuntimeIdentity) -> tuple[str, ...]:
    errors: list[str] = []
    required = {
        "source_commit": _COMMIT_RE,
        "source_tree_sha256_v2": _SHA256_RE,
        "dependency_lock_digest": _SHA256_RE,
        "timezone_bundle_digest": _SHA256_RE,
        "ephemeris_bundle_digest": _SHA256_RE,
        "runtime_image_digest": _RUNTIME_IMAGE_RE,
    }
    for name, pattern in required.items():
        value = provenance.get(name)
        if not isinstance(value, str) or not pattern.fullmatch(value):
            errors.append(f"provenance:malformed:{name}")
        elif getattr(runtime_identity, name) != value:
            errors.append(f"provenance:mismatch:{name}")
    calculation_version = provenance.get("calculation_version")
    if not isinstance(calculation_version, str) or not calculation_version.strip():
        errors.append("provenance:invalid:calculation_version")
    errors.extend(f"runtime_identity:{e}" for e in runtime_identity.validate_shape())
    return tuple(errors)


@dataclass(frozen=True)
class CalculationResult:
    request_id: str
    status: CalculationStatus
    execution_profile_id: str
    scenario_state: ScenarioState
    normalized_time: str | None
    calculation_id: str | None = None
    observation_interval: tuple[str, str] | None = None
    object_states: tuple[ObjectState, ...] = field(default_factory=tuple)
    geometry_records: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    event_records: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    window_segments: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    warnings: tuple[str, ...] = field(default_factory=tuple)
    errors: tuple[str, ...] = field(default_factory=tuple)
    provenance: dict[str, Any] = field(default_factory=dict)
    evidence_packet_ref: EvidencePacketRef | None = field(
        default=None, init=False, repr=False, compare=False
    )
    _runtime_identity: RuntimeIdentity | None = field(
        default=None, kw_only=True, repr=False, compare=False
    )
    _evidence_packet: EvidencePacket | None = field(
        default=None, kw_only=True, repr=False, compare=False
    )
    _canonical_bytes: bytes = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        for item in fields(self):
            if item.name in {"evidence_packet_ref", "_runtime_identity", "_evidence_packet", "_canonical_bytes"}:
                continue
            object.__setattr__(self, item.name, _freeze(getattr(self, item.name)))

        packet = self._evidence_packet
        if packet is not None and not isinstance(packet, EvidencePacket):
            raise ValueError("invalid:evidence_packet")
        if packet is not None:
            packet_errors = packet.validate()
            if packet_errors:
                raise ValueError(";".join(f"evidence_packet:{e}" for e in packet_errors))
        ref = EvidencePacketRef.from_packet(packet) if packet is not None else None
        object.__setattr__(self, "evidence_packet_ref", ref)

        errors = self.validate()
        if errors:
            raise ValueError(";".join(errors))

        payload = {
            "request_id": self.request_id,
            "status": self.status.value,
            "execution_profile_id": self.execution_profile_id,
            "scenario_state": self.scenario_state.value,
            "normalized_time": self.normalized_time,
            "calculation_id": self.calculation_id,
            "observation_interval": list(self.observation_interval) if self.observation_interval is not None else None,
            "object_states": [
                {
                    "object_id": item.object_id,
                    "longitude_deg": item.longitude_deg,
                    "speed_deg_per_day": item.speed_deg_per_day,
                    "status": item.status.value,
                }
                for item in self.object_states
            ],
            "geometry_records": list(self.geometry_records),
            "event_records": list(self.event_records),
            "window_segments": list(self.window_segments),
            "warnings": list(self.warnings),
            "errors": list(self.errors),
            "provenance": self.provenance,
            "evidence_packet_ref": ref.as_dict() if ref else None,
        }
        object.__setattr__(self, "_canonical_bytes", canonical_json(payload))

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []

        if _nonempty(self.request_id, "request_id"):
            errors.append("invalid:request_id")
        if self.execution_profile_id != CANONICAL_EXECUTION_PROFILE_ID:
            errors.append("invalid:execution_profile_id:canonical_required")
        if not isinstance(self.scenario_state, ScenarioState):
            errors.append("invalid:scenario_state")

        if self.normalized_time is not None and not _valid_utc(self.normalized_time):
            errors.append("invalid:normalized_time")

        for index, state in enumerate(self.object_states):
            if not isinstance(state, ObjectState):
                errors.append(f"invalid:object_states[{index}]")
            else:
                errors.extend(f"object_states[{index}]:{e}" for e in state.validate())

        for name, required, utc_keys in (
            ("geometry_records", ("transit_object", "natal_object_or_scenario", "aspect", "directed_branch", "signed_deviation", "absolute_deviation", "effective_orb", "qualification_state", "kinematic_state"), ("event_time_utc",)),
            ("event_records", ("event_time_utc", "residual"), ("event_time_utc",)),
            ("window_segments", ("entry_utc", "exact_events_utc", "exit_utc"), ("entry_utc", "exit_utc")),
        ):
            records = getattr(self, name)
            if not isinstance(records, (tuple, list)):
                errors.append(f"invalid:{name}:sequence_required")
                continue
            for index, record in enumerate(records):
                if not isinstance(record, Mapping):
                    errors.append(f"invalid:{name}[{index}]:mapping_required")
                    continue
                for key in required:
                    if key not in record:
                        errors.append(f"invalid:{name}[{index}]:missing:{key}")
                for key in utc_keys:
                    if record.get(key) is not None and not _valid_utc(record.get(key)):
                        errors.append(f"invalid:{name}[{index}]:{key}:utc_required")
                if name == "window_segments" and record.get("exact_events_utc") is not None:
                    events = record.get("exact_events_utc")
                    if not isinstance(events, (tuple, list)) or any(not _valid_utc(v) for v in events):
                        errors.append(f"invalid:{name}[{index}]:exact_events_utc")

        for field_name in ("warnings", "errors"):
            value = getattr(self, field_name)
            if not isinstance(value, (tuple, list)):
                errors.append(f"invalid:{field_name}:sequence_required")
            elif any(not isinstance(item, str) for item in value):
                errors.append(f"invalid:{field_name}:string_required")

        if self.status is CalculationStatus.VALID:
            if self.calculation_id is None or not isinstance(self.calculation_id, str) or not self.calculation_id.strip():
                errors.append("valid_result_requires_calculation_id")
            if self.observation_interval is None or len(self.observation_interval) != 2:
                errors.append("valid_result_requires_observation_interval")
            elif not _valid_utc(self.observation_interval[0]) or not _valid_utc(self.observation_interval[1]):
                errors.append("valid_result_requires_valid_observation_interval")
            elif datetime.fromisoformat(self.observation_interval[1][:-1] + "+00:00") < datetime.fromisoformat(self.observation_interval[0][:-1] + "+00:00"):
                errors.append("valid_result_observation_interval_order")
            if self.status is CalculationStatus.VALID and self.normalized_time is None:
                errors.append("valid_result_requires_normalized_time")
            if self.status is CalculationStatus.VALID:
                if not self.object_states:
                    errors.append("valid_result_requires_object_states")
                elif any(item.status is not CalculationStatus.VALID for item in self.object_states):
                    errors.append("valid_result_requires_all_objects_valid")
            elif any(item.status not in {CalculationStatus.VALID, CalculationStatus.NATAL_EVIDENCE_VARIABLE} for item in self.object_states):
                errors.append("variable_result_contains_unpublishable_object_state")
            if self.status is CalculationStatus.VALID and self.errors:
                errors.append("valid_result_cannot_have_errors")
            if self.scenario_state is ScenarioState.NONE:
                errors.append("calculated_result_requires_scenario_state")
            if self._runtime_identity is None:
                errors.append("calculated_result_requires_runtime_identity")
            else:
                errors.extend(_validate_runtime_provenance(self.provenance, self._runtime_identity))
            if self._evidence_packet is None or self.evidence_packet_ref is None:
                errors.append("calculated_result_requires_evidence_packet")
            elif not self.evidence_packet_ref.matches(self._evidence_packet):
                errors.append("evidence_packet:reference_mismatch")
        else:
            if self.evidence_packet_ref is not None:
                errors.append("nonvalid_result_evidence_packet_requires_null")
            if any(item.status is CalculationStatus.VALID for item in self.object_states):
                errors.append("nonvalid_result_cannot_contain_valid_object_state")

        return tuple(errors)

    def canonical_bytes(self) -> bytes:
        return self._canonical_bytes
