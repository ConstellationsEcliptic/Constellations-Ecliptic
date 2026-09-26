from __future__ import annotations

from dataclasses import dataclass

from ce.foundation.identity import RuntimeIdentity
from ce.foundation.status import RuntimeAuthority


_EXPECTED_EXECUTION_PROFILE_ID = "CE-CALC-V1-EP-001"
_IDENTITY_FIELDS = (
    "source_commit",
    "source_tree_sha256_v2",
    "runtime_image_digest",
    "dependency_lock_digest",
    "timezone_bundle_digest",
    "ephemeris_bundle_digest",
)


@dataclass(frozen=True)
class RuntimeGateResult:
    authority: RuntimeAuthority
    reasons: tuple[str, ...]


def _validate_runtime_identity(identity: object) -> list[str]:
    reasons: list[str] = []

    if not isinstance(identity, RuntimeIdentity):
        return ["invalid:runtime_identity_type"]

    profile_id = identity.execution_profile_id
    if not isinstance(profile_id, str):
        reasons.append("invalid:execution_profile_id_type")
    elif not profile_id.strip():
        reasons.append("missing:execution_profile_id")
    elif profile_id != _EXPECTED_EXECUTION_PROFILE_ID:
        reasons.append("unrecognized:execution_profile_id")

    revision = identity.execution_profile_revision
    if type(revision) is not int:
        reasons.append("invalid:execution_profile_revision_type")
    elif revision < 1:
        reasons.append("invalid:execution_profile_revision")

    for name in _IDENTITY_FIELDS:
        value = getattr(identity, name)
        if value is None or (isinstance(value, str) and not value.strip()):
            reasons.append(f"missing:{name}")
        elif not isinstance(value, str):
            reasons.append(f"invalid:{name}_type")

    return reasons


def authorize_runtime(identity: RuntimeIdentity) -> RuntimeGateResult:
    """Fail-closed development boundary.

    A non-empty RuntimeIdentity is not proof of authorization. Malformed
    identity input must also terminate at the same non-authorized boundary
    rather than raising an exception that could be misinterpreted upstream.
    Production authorization requires a separately established and
    independently verified authority mechanism that is intentionally not
    implemented in this source foundation.
    """
    reasons = _validate_runtime_identity(identity)

    # Presence or shape of identity values is never sufficient for runtime
    # authority in the development foundation.
    reasons.append("source_authority_attestation_not_established")
    reasons.append("independent_runtime_identity_verification_not_established")

    return RuntimeGateResult(RuntimeAuthority.NON_AUTHORIZED, tuple(reasons))
