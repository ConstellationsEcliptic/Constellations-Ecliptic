from __future__ import annotations

import re
from dataclasses import dataclass, asdict
from typing import Any

from .serialization import canonical_json


CANONICAL_EXECUTION_PROFILE_ID = "CE-CALC-V1-EP-001"
CANONICAL_EXECUTION_PROFILE_REVISION = 2

_COMMIT_RE = re.compile(r"^[0-9a-fA-F]{40}$")
_SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")
_RUNTIME_IMAGE_RE = re.compile(r"^sha256:[0-9a-fA-F]{64}$")


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

    def validate_shape(self) -> tuple[str, ...]:
        errors: list[str] = []

        if self.execution_profile_id != CANONICAL_EXECUTION_PROFILE_ID:
            errors.append("unrecognized:execution_profile_id")
        if self.execution_profile_revision != CANONICAL_EXECUTION_PROFILE_REVISION:
            errors.append("unrecognized:execution_profile_revision")

        shaped_fields = {
            "source_commit": (self.source_commit, _COMMIT_RE, "40-hex"),
            "source_tree_sha256_v2": (self.source_tree_sha256_v2, _SHA256_RE, "64-hex"),
            "dependency_lock_digest": (self.dependency_lock_digest, _SHA256_RE, "64-hex"),
            "timezone_bundle_digest": (self.timezone_bundle_digest, _SHA256_RE, "64-hex"),
            "ephemeris_bundle_digest": (self.ephemeris_bundle_digest, _SHA256_RE, "64-hex"),
        }
        for name, (value, pattern, description) in shaped_fields.items():
            if value is not None:
                if not isinstance(value, str) or not pattern.fullmatch(value):
                    errors.append(f"malformed:{name}:{description}")

        if self.runtime_image_digest is not None:
            if not isinstance(self.runtime_image_digest, str) or not _RUNTIME_IMAGE_RE.fullmatch(
                self.runtime_image_digest
            ):
                errors.append("malformed:runtime_image_digest:sha256-prefixed")

        return tuple(errors)
