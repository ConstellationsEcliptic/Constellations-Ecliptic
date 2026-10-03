from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field, fields
from datetime import datetime, timezone
from types import MappingProxyType
import math
import re
from typing import Any

from ce.foundation.hashing import sha256_bytes
from ce.foundation.identity import CANONICAL_EXECUTION_PROFILE_ID, CANONICAL_EXECUTION_PROFILE_REVISION
from ce.foundation.serialization import canonical_json


_SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")
_UTC_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?Z$")


def _freeze(value: Any) -> Any:
    if isinstance(value, Mapping):
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(_freeze(item) for item in value)
    if isinstance(value, tuple):
        return tuple(_freeze(item) for item in value)
    return value


def _canonical_domain_errors(value: Any, path: str) -> tuple[str, ...]:
    if isinstance(value, Mapping):
        errors: list[str] = []
        for key, item in value.items():
            if not isinstance(key, str):
                errors.append(f"invalid:{path}:mapping_key_string_required")
                child = f"{path}.<nonstring-key>"
            else:
                child = f"{path}.{key}"
            errors.extend(_canonical_domain_errors(item, child))
        return tuple(errors)

    if isinstance(value, (list, tuple)):
        errors: list[str] = []
        for index, item in enumerate(value):
            errors.extend(_canonical_domain_errors(item, f"{path}[{index}]"))
        return tuple(errors)

    if value is None or isinstance(value, (str, int, bool)):
        return ()

    if isinstance(value, float):
        if not math.isfinite(value):
            return (f"invalid:{path}:finite_number_required",)
        return ()

    return (f"invalid:{path}:canonical_json_value_required",)


def _valid_utc(value: Any) -> bool:
    if not isinstance(value, str) or not _UTC_RE.fullmatch(value):
        return False
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError:
        return False
    return parsed.tzinfo is not None and parsed.utcoffset() == timezone.utc.utcoffset(parsed)


def _record_errors(
    records: Any,
    *,
    path: str,
    required_keys: tuple[str, ...],
    utc_keys: tuple[str, ...] = (),
    numeric_keys: tuple[str, ...] = (),
) -> tuple[str, ...]:
    if not isinstance(records, (list, tuple)):
        return (f"invalid:{path}:sequence_required",)

    errors: list[str] = []
    for index, record in enumerate(records):
        entry_path = f"{path}[{index}]"
        if not isinstance(record, Mapping):
            errors.append(f"invalid:{entry_path}:mapping_required")
            continue

        for key in required_keys:
            if key not in record:
                errors.append(f"invalid:{entry_path}:missing:{key}")

        errors.extend(_canonical_domain_errors(record, entry_path))

        for key in utc_keys:
            value = record.get(key)
            if value is not None and not _valid_utc(value):
                errors.append(f"invalid:{entry_path}:{key}:utc_required")

        for key in numeric_keys:
            value = record.get(key)
            if value is not None and (
                type(value) not in (int, float) or (isinstance(value, float) and not math.isfinite(value))
            ):
                errors.append(f"invalid:{entry_path}:{key}:finite_number_required")

    return tuple(errors)


@dataclass(frozen=True)
class EvidencePacketRef:
    """Compound identity binding a result to one EvidencePacket issuance."""

    evidence_packet_id: str
    content_sha256: str

    def __post_init__(self) -> None:
        if not isinstance(self.evidence_packet_id, str) or not self.evidence_packet_id.strip():
            raise ValueError("invalid:evidence_packet_ref:evidence_packet_id")
        if not isinstance(self.content_sha256, str) or not _SHA256_RE.fullmatch(self.content_sha256):
            raise ValueError("invalid:evidence_packet_ref:content_sha256")

    @classmethod
    def from_packet(cls, packet: "EvidencePacket") -> "EvidencePacketRef":
        if not isinstance(packet, EvidencePacket):
            raise TypeError("evidence_packet_required")
        return cls(packet.evidence_packet_id, packet.content_sha256())

    def matches(self, packet: "EvidencePacket") -> bool:
        return (
            isinstance(packet, EvidencePacket)
            and self.evidence_packet_id == packet.evidence_packet_id
            and self.content_sha256 == packet.content_sha256()
        )

    def as_dict(self) -> dict[str, str]:
        return {
            "evidence_packet_id": self.evidence_packet_id,
            "content_sha256": self.content_sha256,
        }


@dataclass(frozen=True)
class EvidencePacket:
    evidence_packet_id: str
    input_identity: dict[str, Any]
    profile_version: dict[str, Any]
    observation_instant_or_interval: dict[str, Any]
    timezone_context: dict[str, Any]
    execution_profile_id: str
    calculation_version: str
    object_records: tuple[dict[str, Any], ...]
    geometry_records: tuple[dict[str, Any], ...]
    effective_orb_records: tuple[dict[str, Any], ...]
    kinematics: tuple[dict[str, Any], ...]
    exact_events: tuple[dict[str, Any], ...]
    window_segments: tuple[dict[str, Any], ...]
    scenario_stability_state: str
    warnings: tuple[str, ...]
    errors: tuple[str, ...]
    numerical_tolerances: dict[str, Any]
    solver_metadata: dict[str, Any]
    actual_ephemeris_resolution: dict[str, Any]
    calculation_flags: dict[str, Any]
    _canonical_bytes: bytes = field(init=False, repr=False, compare=False)

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []

        if not isinstance(self.evidence_packet_id, str) or not self.evidence_packet_id.strip():
            errors.append("invalid:evidence_packet_id")
        if not isinstance(self.calculation_version, str) or not self.calculation_version.strip():
            errors.append("invalid:calculation_version")
        if self.execution_profile_id != CANONICAL_EXECUTION_PROFILE_ID:
            errors.append("unrecognized:execution_profile_id")

        mappings = (
            "input_identity", "profile_version", "observation_instant_or_interval",
            "timezone_context", "numerical_tolerances", "solver_metadata",
            "actual_ephemeris_resolution", "calculation_flags",
        )
        for name in mappings:
            value = getattr(self, name)
            if not isinstance(value, Mapping):
                errors.append(f"invalid:{name}:mapping_required")
            else:
                errors.extend(_canonical_domain_errors(value, name))

        profile = self.profile_version
        if isinstance(profile, Mapping):
            if profile.get("id") != CANONICAL_EXECUTION_PROFILE_ID:
                errors.append("invalid:profile_version:id")
            if profile.get("revision") != CANONICAL_EXECUTION_PROFILE_REVISION:
                errors.append("invalid:profile_version:revision")

        observation = self.observation_instant_or_interval
        if isinstance(observation, Mapping):
            start = observation.get("start")
            end = observation.get("end")
            if not _valid_utc(start):
                errors.append("invalid:observation_instant_or_interval:start")
            if end is not None and not _valid_utc(end):
                errors.append("invalid:observation_instant_or_interval:end")
            if _valid_utc(start) and _valid_utc(end):
                start_dt = datetime.fromisoformat(start[:-1] + "+00:00")
                end_dt = datetime.fromisoformat(end[:-1] + "+00:00")
                if end_dt < start_dt:
                    errors.append("invalid:observation_instant_or_interval:order")

        errors.extend(_record_errors(
            self.object_records,
            path="object_records",
            required_keys=("object_id", "object_status", "requested_flags", "actual_flags"),
            numeric_keys=("longitude", "latitude", "distance", "speed"),
        ))
        errors.extend(_record_errors(
            self.geometry_records,
            path="geometry_records",
            required_keys=("transit_object", "natal_object_or_scenario", "aspect", "directed_branch",
                           "signed_deviation", "absolute_deviation", "effective_orb", "qualification_state",
                           "kinematic_state"),
            utc_keys=("event_time_utc",),
            numeric_keys=("directed_branch", "signed_deviation", "absolute_deviation", "effective_orb", "transit_speed"),
        ))
        errors.extend(_record_errors(
            self.effective_orb_records,
            path="effective_orb_records",
            required_keys=("transit_object", "natal_object_or_scenario", "aspect", "effective_orb"),
            numeric_keys=("effective_orb",),
        ))
        errors.extend(_record_errors(
            self.kinematics,
            path="kinematics",
            required_keys=("transit_object", "aspect", "kinematic_state"),
            numeric_keys=("transit_speed",),
        ))
        errors.extend(_record_errors(
            self.exact_events,
            path="exact_events",
            required_keys=("event_time_utc", "residual"),
            utc_keys=("event_time_utc",),
            numeric_keys=("residual",),
        ))
        errors.extend(_record_errors(
            self.window_segments,
            path="window_segments",
            required_keys=("entry_utc", "exact_events_utc", "exit_utc"),
            utc_keys=("entry_utc", "exit_utc"),
        ))

        if not isinstance(self.scenario_stability_state, str) or not self.scenario_stability_state.strip():
            errors.append("invalid:scenario_stability_state")

        for name in ("warnings", "errors"):
            value = getattr(self, name)
            if not isinstance(value, (list, tuple)):
                errors.append(f"invalid:{name}:sequence_required")
                continue
            for index, item in enumerate(value):
                if not isinstance(item, str):
                    errors.append(f"invalid:{name}[{index}]:string_required")

        return tuple(errors)

    def __post_init__(self) -> None:
        errors = self.validate()
        if errors:
            raise ValueError(";".join(errors))

        for item in fields(self):
            if item.name != "_canonical_bytes":
                object.__setattr__(self, item.name, _freeze(getattr(self, item.name)))

        payload = {
            item.name: getattr(self, item.name)
            for item in fields(self)
            if item.name != "_canonical_bytes"
        }
        object.__setattr__(self, "_canonical_bytes", canonical_json(payload))

    def canonical_bytes(self) -> bytes:
        return self._canonical_bytes

    def content_sha256(self) -> str:
        return sha256_bytes(self._canonical_bytes)
