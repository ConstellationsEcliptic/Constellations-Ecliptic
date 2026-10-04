from __future__ import annotations

from dataclasses import dataclass
import re

from ce.foundation.identity import RuntimeIdentity


_SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")
_COMMIT_RE = re.compile(r"^[0-9a-fA-F]{40}$")
_FINGERPRINT_RE = re.compile(r"^[0-9A-Fa-f]{40}$")


class AuthorityEvidenceError(ValueError):
    """Authority-chain evidence is incomplete or internally inconsistent."""


@dataclass(frozen=True)
class SourceAuthorityEvidence:
    repository_uri: str
    source_commit: str
    source_tree_sha256_v2: str
    source_authority_digest: str
    signer_fingerprint: str


@dataclass(frozen=True)
class TrustedBuildEvidence:
    build_digest: str
    source_commit: str
    source_tree_sha256_v2: str
    dependency_lock_digest: str
    runtime_image_digest: str
    runtime_manifest_digest: str
    timezone_bundle_digest: str
    ephemeris_bundle_digest: str


@dataclass(frozen=True)
class SignedProvenanceEvidence:
    provenance_signature_digest: str
    signer_fingerprint: str
    source_authority_digest: str
    trusted_build_digest: str


@dataclass(frozen=True)
class AuthorityEvaluation:
    authorized: bool
    reasons: tuple[str, ...]
    source_authority_digest: str | None
    trusted_build_digest: str | None
    provenance_signature_digest: str | None


def _require_sha(value: str, field: str) -> None:
    if not isinstance(value, str) or not _SHA256_RE.fullmatch(value):
        raise AuthorityEvidenceError(f"malformed:{field}")


def _require_commit(value: str, field: str) -> None:
    if not isinstance(value, str) or not _COMMIT_RE.fullmatch(value):
        raise AuthorityEvidenceError(f"malformed:{field}")


def _require_fingerprint(value: str, field: str) -> None:
    if not isinstance(value, str) or not _FINGERPRINT_RE.fullmatch(value):
        raise AuthorityEvidenceError(f"malformed:{field}")


def evaluate_full_authority(
    runtime_identity: RuntimeIdentity,
    *,
    source: SourceAuthorityEvidence,
    build: TrustedBuildEvidence,
    signed: SignedProvenanceEvidence,
) -> AuthorityEvaluation:
    reasons: list[str] = []

    runtime_errors = runtime_identity.validate_shape()
    reasons.extend(f"runtime_identity:{item}" for item in runtime_errors)

    try:
        _require_commit(source.source_commit, "source.source_commit")
        _require_sha(source.source_tree_sha256_v2, "source.source_tree_sha256_v2")
        _require_sha(source.source_authority_digest, "source.source_authority_digest")
        _require_fingerprint(source.signer_fingerprint, "source.signer_fingerprint")
        _require_sha(build.build_digest, "build.build_digest")
        _require_commit(build.source_commit, "build.source_commit")
        _require_sha(build.source_tree_sha256_v2, "build.source_tree_sha256_v2")
        _require_sha(build.dependency_lock_digest, "build.dependency_lock_digest")
        _require_sha(build.runtime_manifest_digest, "build.runtime_manifest_digest")
        _require_sha(build.timezone_bundle_digest, "build.timezone_bundle_digest")
        _require_sha(build.ephemeris_bundle_digest, "build.ephemeris_bundle_digest")
        _require_sha(signed.provenance_signature_digest, "signed.provenance_signature_digest")
        _require_sha(signed.source_authority_digest, "signed.source_authority_digest")
        _require_sha(signed.trusted_build_digest, "signed.trusted_build_digest")
        _require_fingerprint(signed.signer_fingerprint, "signed.signer_fingerprint")
    except AuthorityEvidenceError as exc:
        reasons.append(str(exc))

    if source.source_commit != build.source_commit:
        reasons.append("source_build_commit_mismatch")
    if source.source_tree_sha256_v2 != build.source_tree_sha256_v2:
        reasons.append("source_build_tree_mismatch")
    if signed.source_authority_digest != source.source_authority_digest:
        reasons.append("signed_source_authority_digest_mismatch")
    if signed.trusted_build_digest != build.build_digest:
        reasons.append("signed_trusted_build_digest_mismatch")
    if signed.signer_fingerprint != source.signer_fingerprint:
        reasons.append("signer_fingerprint_mismatch")

    required_runtime_matches = {
        "source_commit": source.source_commit,
        "source_tree_sha256_v2": source.source_tree_sha256_v2,
        "dependency_lock_digest": build.dependency_lock_digest,
        "runtime_image_digest": build.runtime_image_digest,
        "timezone_bundle_digest": build.timezone_bundle_digest,
        "ephemeris_bundle_digest": build.ephemeris_bundle_digest,
        "source_authority_digest": source.source_authority_digest,
        "trusted_build_digest": build.build_digest,
        "provenance_signature_digest": signed.provenance_signature_digest,
    }
    for field, expected in required_runtime_matches.items():
        actual = getattr(runtime_identity, field)
        if actual != expected:
            reasons.append(f"runtime_identity_mismatch:{field}")

    if reasons:
        return AuthorityEvaluation(
            False,
            tuple(dict.fromkeys(reasons)),
            None,
            None,
            None,
        )

    return AuthorityEvaluation(
        True,
        (),
        source.source_authority_digest,
        build.build_digest,
        signed.provenance_signature_digest,
    )
