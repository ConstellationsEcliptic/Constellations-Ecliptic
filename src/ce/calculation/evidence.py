from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field, fields
from typing import Any

from ce.foundation.hashing import sha256_bytes
from ce.foundation.identity import CANONICAL_EXECUTION_PROFILE_ID
from ce.foundation.serialization import canonical_json


class FrozenDict(dict):
    """Dict-shaped mapping that rejects all in-place mutation."""

    def _blocked(self, *args: Any, **kwargs: Any) -> None:
        raise TypeError("EvidencePacket mappings are immutable")

    __setitem__ = __delitem__ = clear = pop = popitem = setdefault = update = _blocked
    __ior__ = _blocked


_STRING_FIELDS = (
    "evidence_packet_id",
    "calculation_version",
)

_MAPPING_FIELDS = (
    "input_identity",
    "profile_version",
    "observation_instant_or_interval",
    "timezone_context",
    "numerical_tolerances",
    "solver_metadata",
    "actual_ephemeris_resolution",
    "calculation_flags",
)

_RECORD_FIELDS = (
    "object_records",
    "geometry_records",
    "kinematics",
)

_MESSAGE_FIELDS = (
    "warnings",
    "errors",
)


def _freeze(value: Any) -> Any:
    if isinstance(value, Mapping):
        return FrozenDict({key: _freeze(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(_freeze(item) for item in value)
    if isinstance(value, tuple):
        return tuple(_freeze(item) for item in value)
    return value


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

        for field_name in _STRING_FIELDS:
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"invalid:{field_name}")

        execution_profile_id = self.execution_profile_id
        if not isinstance(execution_profile_id, str) or not execution_profile_id.strip():
            errors.append("invalid:execution_profile_id")
        elif execution_profile_id != CANONICAL_EXECUTION_PROFILE_ID:
            errors.append("unrecognized:execution_profile_id")

        for field_name in _MAPPING_FIELDS:
            if not isinstance(getattr(self, field_name), Mapping):
                errors.append(f"invalid:{field_name}:mapping_required")

        for field_name in _RECORD_FIELDS:
            value = getattr(self, field_name)
            if not isinstance(value, (list, tuple)):
                errors.append(f"invalid:{field_name}:sequence_required")
                continue
            for index, item in enumerate(value):
                if not isinstance(item, Mapping):
                    errors.append(f"invalid:{field_name}[{index}]:mapping_required")

        for field_name in _MESSAGE_FIELDS:
            value = getattr(self, field_name)
            if not isinstance(value, (list, tuple)):
                errors.append(f"invalid:{field_name}:sequence_required")
                continue
            for index, item in enumerate(value):
                if not isinstance(item, str):
                    errors.append(f"invalid:{field_name}[{index}]:string_required")

        return tuple(errors)

    def __post_init__(self) -> None:
        errors = self.validate()
        if errors:
            raise ValueError(";".join(errors))

        for item in fields(self):
            if item.name == "_canonical_bytes":
                continue
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
