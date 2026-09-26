from __future__ import annotations

from dataclasses import dataclass

from ce.foundation.identity import RuntimeIdentity
from ce.foundation.status import RuntimeAuthority


@dataclass(frozen=True)
class RuntimeGateResult:
    authority: RuntimeAuthority
    reasons: tuple[str, ...]


def authorize_runtime(identity: RuntimeIdentity) -> RuntimeGateResult:
    missing: list[str] = []
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
            missing.append(f"missing:{name}")
    if identity.execution_profile_id != "CE-CALC-V1-EP-001":
        missing.append("unrecognized:execution_profile_id")
    if identity.execution_profile_revision < 1:
        missing.append("invalid:execution_profile_revision")
    if missing:
        return RuntimeGateResult(RuntimeAuthority.NON_AUTHORIZED, tuple(missing))
    return RuntimeGateResult(RuntimeAuthority.AUTHORIZED, ())
