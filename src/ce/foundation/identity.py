from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any

from .serialization import canonical_json


@dataclass(frozen=True)
class RuntimeIdentity:
    execution_profile_id: str
    execution_profile_revision: int
    source_commit: str | None
    source_tree_sha256_v2: str | None
    runtime_image_digest: str | None
    dependency_lock_digest: str | None
    timezone_bundle_digest: str | None
    ephemeris_bundle_digest: str | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def canonical_bytes(self) -> bytes:
        return canonical_json(self.to_dict())
