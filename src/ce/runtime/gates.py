from __future__ import annotations

from dataclasses import dataclass

from ce.foundation.identity import (
    CANONICAL_EXECUTION_PROFILE_ID,
    CANONICAL_EXECUTION_PROFILE_REVISION,
    RuntimeIdentity,
)
from ce.foundation.status import RuntimeAuthority


@dataclass(frozen=True)
class RuntimeGateResult:
    authority: RuntimeAuthority
    reasons: tuple[str, ...]


def authorize_runtime(identity: RuntimeIdentity) -> RuntimeGateResult:
    """Fail-closed gate; identity presence never constitutes authority."""

    reasons = list(identity.validate_shape())
    required_fields = {
        "source_commit": identity.source_commit,
        "source_tree_sha256_v2": identity.source_tree_sha256_v2,
        "runtime_environment_kind": identity.runtime_environment_kind,
        "dependency_lock_digest": identity.dependency_lock_digest,
        "timezone_bundle_digest": identity.timezone_bundle_digest,
        "ephemeris_bundle_digest": identity.ephemeris_bundle_digest,
    }
    if identity.runtime_environment_kind == "OCI_IMAGE":
        required_fields["runtime_image_digest"] = identity.runtime_image_digest
    elif identity.runtime_environment_kind == "HOST_NATIVE":
        required_fields["runtime_environment_digest"] = identity.runtime_environment_digest
    reasons.extend(
        f"missing:{name}"
        for name, value in required_fields.items()
        if value is None
    )

    if identity.execution_profile_id != CANONICAL_EXECUTION_PROFILE_ID:
        reasons.append("execution_profile_id_mismatch")
    if identity.execution_profile_revision != CANONICAL_EXECUTION_PROFILE_REVISION:
        reasons.append("execution_profile_revision_mismatch")

    reasons.append("source_authority_attestation_not_established")
    reasons.append("independent_runtime_identity_verification_not_established")
    return RuntimeGateResult(RuntimeAuthority.NON_AUTHORIZED, tuple(dict.fromkeys(reasons)))
