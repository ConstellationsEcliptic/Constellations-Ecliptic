from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import Any

from .serialization import canonical_json


CANONICAL_EXECUTION_PROFILE_ID = "CE-CALC-V1-EP-001"
CANONICAL_EXECUTION_PROFILE_REVISION = 4

_COMMIT_RE = re.compile(r"^[0-9a-fA-F]{40}$")
_SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")
_RUNTIME_IMAGE_RE = re.compile(r"^sha256:[0-9a-fA-F]{64}$")


@dataclass(frozen=True)
class RuntimeIdentity:
    """Identity of one CE execution environment.

    Identity is descriptive, not self-authorizing. Authority remains a
    separate governance boundary.
    """

    execution_profile_id: str
    execution_profile_revision: int
    source_commit: str | None
    source_tree_sha256_v2: str | None
    runtime_image_digest: str | None
    dependency_lock_digest: str | None
    timezone_bundle_digest: str | None
    ephemeris_bundle_digest: str | None
    source_authority_digest: str | None = None
    trusted_build_digest: str | None = None
    provenance_signature_digest: str | None = None
    runtime_environment_digest: str | None = None
    runtime_environment_kind: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def canonical_bytes(self) -> bytes:
        return canonical_json(self.to_dict())

    def validate_shape(self) -> tuple[str, ...]:
        errors: list[str] = []

        if self.execution_profile_id != CANONICAL_EXECUTION_PROFILE_ID:
            errors.append("unrecognized:execution_profile_id")
        if type(self.execution_profile_revision) is not int:
            errors.append("invalid:execution_profile_revision:type")
        elif self.execution_profile_revision != CANONICAL_EXECUTION_PROFILE_REVISION:
            errors.append("unrecognized:execution_profile_revision")

        shaped = {
            "source_commit": (self.source_commit, _COMMIT_RE, "40-hex"),
            "source_tree_sha256_v2": (self.source_tree_sha256_v2, _SHA256_RE, "64-hex"),
            "dependency_lock_digest": (self.dependency_lock_digest, _SHA256_RE, "64-hex"),
            "timezone_bundle_digest": (self.timezone_bundle_digest, _SHA256_RE, "64-hex"),
            "ephemeris_bundle_digest": (self.ephemeris_bundle_digest, _SHA256_RE, "64-hex"),
            "source_authority_digest": (self.source_authority_digest, _SHA256_RE, "64-hex"),
            "trusted_build_digest": (self.trusted_build_digest, _SHA256_RE, "64-hex"),
            "provenance_signature_digest": (self.provenance_signature_digest, _SHA256_RE, "64-hex"),
            "runtime_environment_digest": (self.runtime_environment_digest, _SHA256_RE, "64-hex"),
        }
        for name, (value, pattern, description) in shaped.items():
            if value is not None and (
                not isinstance(value, str) or not pattern.fullmatch(value)
            ):
                errors.append(f"malformed:{name}:{description}")

        if self.runtime_image_digest is not None and (
            not isinstance(self.runtime_image_digest, str)
            or not _RUNTIME_IMAGE_RE.fullmatch(self.runtime_image_digest)
        ):
            errors.append("malformed:runtime_image_digest:sha256-prefixed")

        if self.runtime_environment_kind is not None:
            if self.runtime_environment_kind not in {"OCI_IMAGE", "HOST_NATIVE"}:
                errors.append("malformed:runtime_environment_kind")
            elif self.runtime_environment_kind == "OCI_IMAGE":
                if self.runtime_image_digest is None:
                    errors.append("missing:runtime_image_digest")
                if self.runtime_environment_digest is not None:
                    errors.append("conflict:runtime_environment_digest_for_oci")
            elif self.runtime_environment_kind == "HOST_NATIVE":
                if self.runtime_image_digest is not None:
                    errors.append("conflict:runtime_image_digest_for_host_native")
                if self.runtime_environment_digest is None:
                    errors.append("missing:runtime_environment_digest")

        return tuple(errors)
