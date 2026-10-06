from __future__ import annotations

from collections.abc import Mapping
import re
from typing import Any

from ce.foundation.hashing import sha256_bytes
from ce.foundation.identity import RuntimeIdentity
from ce.foundation.serialization import canonical_json


PROVENANCE_ROOT_SCHEMA_VERSION = "CE-V1-PROVENANCE-ROOT-R1"
_SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")


class ProvenanceBindingError(ValueError):
    """A provenance binding is malformed or internally inconsistent."""


def runtime_identity_sha256(identity: RuntimeIdentity) -> str:
    if not isinstance(identity, RuntimeIdentity):
        raise ProvenanceBindingError("runtime_identity_required")
    errors = identity.validate_shape()
    if errors:
        raise ProvenanceBindingError("runtime_identity_invalid:" + ";".join(errors))
    return sha256_bytes(identity.canonical_bytes())


def _canonical_mapping(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ProvenanceBindingError(f"{field}_mapping_required")
    result = dict(value)
    # canonical_json performs recursive domain validation.
    canonical_json(result)
    return result


def derive_provenance_root_sha256(
    *,
    calculation_id: str,
    request_id: str,
    input_identity: Mapping[str, Any],
    profile_version: Mapping[str, Any],
    timezone_context: Mapping[str, Any],
    execution_profile_id: str,
    calculation_version: str,
    runtime_identity_digest: str,
) -> str:
    if not isinstance(calculation_id, str) or not calculation_id.strip():
        raise ProvenanceBindingError("calculation_id_required")
    if not isinstance(request_id, str) or not request_id.strip():
        raise ProvenanceBindingError("request_id_required")
    if not isinstance(execution_profile_id, str) or not execution_profile_id.strip():
        raise ProvenanceBindingError("execution_profile_id_required")
    if not isinstance(calculation_version, str) or not calculation_version.strip():
        raise ProvenanceBindingError("calculation_version_required")
    if not isinstance(runtime_identity_digest, str) or not _SHA256_RE.fullmatch(runtime_identity_digest):
        raise ProvenanceBindingError("runtime_identity_digest_invalid")

    payload = {
        "schema_version": PROVENANCE_ROOT_SCHEMA_VERSION,
        "calculation_id": calculation_id,
        "request_id": request_id,
        "input_identity": _canonical_mapping(input_identity, "input_identity"),
        "profile_version": _canonical_mapping(profile_version, "profile_version"),
        "timezone_context": _canonical_mapping(timezone_context, "timezone_context"),
        "execution_profile_id": execution_profile_id,
        "calculation_version": calculation_version,
        "runtime_identity_sha256": runtime_identity_digest,
    }
    return sha256_bytes(canonical_json(payload))
