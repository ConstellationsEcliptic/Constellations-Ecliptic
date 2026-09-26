from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import Any

from ce.foundation.hashing import sha256_bytes
from ce.foundation.serialization import canonical_json


class FrozenDict(dict):
    """Dict-shaped mapping that rejects all in-place mutation."""

    def _blocked(self, *args: Any, **kwargs: Any) -> None:
        raise TypeError("EvidencePacket mappings are immutable")

    __setitem__ = __delitem__ = clear = pop = popitem = setdefault = update = _blocked


def _freeze(value: Any) -> Any:
    if isinstance(value, dict):
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

    def __post_init__(self) -> None:
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
