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

    if isinstance(value, float) and not math.isfinite(value):
        return (f"invalid:{path}:finite_number_required",)

    if value is None or isinstance(value, (str, int, float, bool)):
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
    kinematics: tuple[dict[str, Any], ...]
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
            if not _valid_utc(start):
                errors.append("invalid:observation_instant_or_interval:start")
            end = observation.get("end")
            if end is not None and not _valid_utc(end):
                errors.append("invalid:observation_instant_or_interval:end")
            if _valid_utc(start) and _valid_utc(end):
                start_dt = datetime.fromisoformat(start[:-1] + "+00:00")
                end_dt = datetime.fromisoformat(end[:-1] + "+00:00")
                if end_dt < start_dt:
                    errors.append("invalid:observation_instant_or_interval:order")

        for name in ("object_records", "geometry_records", "kinematics"):
            value = getattr(self, name)
            if not isinstance(value, (list, tuple)):
                errors.append(f"invalid:{name}:sequence_required")
                continue
            for index, item in enumerate(value):
                if not isinstance(item, Mapping):
                    errors.append(f"invalid:{name}[{index}]:mapping_required")
                else:
                    errors.extend(_canonical_domain_errors(item, f"{name}[{index}]"))

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
