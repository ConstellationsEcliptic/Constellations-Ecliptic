from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from ce.foundation.hashing import sha256_bytes
from ce.foundation.serialization import canonical_json


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

    def canonical_bytes(self) -> bytes:
        return canonical_json(asdict(self))

    def content_sha256(self) -> str:
        return sha256_bytes(self.canonical_bytes())
