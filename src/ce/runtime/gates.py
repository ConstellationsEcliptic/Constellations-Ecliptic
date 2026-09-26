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
    """Fail-closed development boundary.

    A complete-looking RuntimeIdentity is not proof of authorization.
    Production authorization requires a separately established and
    independently verified authority mechanism that is intentionally not
    implemented in this source foundation.
    """
    reasons: list[str] = list(identity.validate_shape())

    fields = {
        "source_commit": identity.source_commit,
        "source_tree_sha256_v2": identity.source_tree_sha256_v2,
        "runtime_image_digest": identity.runtime_image_digest,
        "dependency_lock_digest": identity.dependency_lock_digest,
        "timezone_bundle_digest": identity.timezone_bundle_digest,
        "ephemeris_bundle_digest": identity.ephemeris_bundle_digest,
    }
    for name, value in fields.items():
        if not value:
            reasons.append(f"missing:{name}")

    if identity.execution_profile_id != CANONICAL_EXECUTION_PROFILE_ID:
        reasons.append("unrecognized:execution_profile_id")
    if identity.execution_profile_revision != CANONICAL_EXECUTION_PROFILE_REVISION:
        reasons.append("unrecognized:execution_profile_revision")

    reasons.append("source_authority_attestation_not_established")
    reasons.append("independent_runtime_identity_verification_not_established")
    return RuntimeGateResult(RuntimeAuthority.NON_AUTHORIZED, tuple(dict.fromkeys(reasons)))
