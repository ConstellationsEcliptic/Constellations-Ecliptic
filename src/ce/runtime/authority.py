from __future__ import annotations

from dataclasses import dataclass, field
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

@dataclass(frozen=True)
class VerifiedRuntimeCapability:
    """Non-forgeable-in-practice capability produced only from verified authority.

    The public constructor is intentionally non-issuing. The issuance boundary
    is internal to this module and currently unreachable because
    evaluate_full_authority remains fail-closed until a separately verified
    authority receipt exists.
    """

    runtime_identity_sha256: str
    runtime_environment_kind: str
    source_commit: str
    source_tree_sha256_v2: str
    dependency_lock_digest: str
    timezone_bundle_digest: str
    ephemeris_bundle_digest: str
    native_library_sha256: str
    swiss_release: str
    swiss_source_commit: str
    source_authority_digest: str
    trusted_build_digest: str
    provenance_signature_digest: str
    _issued: bool = field(default=False, init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        if not self._issued:
            raise AuthorityEvidenceError("runtime_capability_must_be_issued")

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []
        if not self._issued:
            errors.append("runtime_capability_not_issued")
        for name, value in (
            ("runtime_identity_sha256", self.runtime_identity_sha256),
            ("source_tree_sha256_v2", self.source_tree_sha256_v2),
            ("dependency_lock_digest", self.dependency_lock_digest),
            ("timezone_bundle_digest", self.timezone_bundle_digest),
            ("ephemeris_bundle_digest", self.ephemeris_bundle_digest),
            ("native_library_sha256", self.native_library_sha256),
            ("source_authority_digest", self.source_authority_digest),
            ("trusted_build_digest", self.trusted_build_digest),
            ("provenance_signature_digest", self.provenance_signature_digest),
        ):
            if not isinstance(value, str) or not _SHA256_RE.fullmatch(value):
                errors.append(f"malformed:capability.{name}")
        if not isinstance(self.source_commit, str) or not _COMMIT_RE.fullmatch(self.source_commit):
            errors.append("malformed:capability.source_commit")
        if self.runtime_environment_kind != "HOST_NATIVE":
            errors.append("capability_runtime_environment_kind_must_be_host_native")
        if not isinstance(self.native_library_sha256, str) or not _SHA256_RE.fullmatch(self.native_library_sha256):
            errors.append("malformed:capability.native_library_sha256")
        if not isinstance(self.swiss_release, str) or not self.swiss_release.strip():
            errors.append("malformed:capability.swiss_release")
        if not isinstance(self.swiss_source_commit, str) or not _COMMIT_RE.fullmatch(self.swiss_source_commit):
            errors.append("malformed:capability.swiss_source_commit")
        return tuple(errors)


def issue_verified_runtime_capability(
    runtime_identity: RuntimeIdentity,
    *,
    source: SourceAuthorityEvidence,
    build: TrustedBuildEvidence,
    signed: SignedProvenanceEvidence,
    native_library_sha256: str,
    swiss_release: str,
    swiss_source_commit: str,
) -> VerifiedRuntimeCapability:
    """Issue capability only after a future verified authority receipt.

    Current CE authority is deliberately non-authorized, so this function
    fail-closes with verified_authority_receipt_required.
    """

    _require_sha(native_library_sha256, "native_library_sha256")
    _require_commit(swiss_source_commit, "swiss_source_commit")
    if not isinstance(swiss_release, str) or not swiss_release.strip():
        raise AuthorityEvidenceError("malformed:swiss_release")

    evaluation = evaluate_full_authority(
        runtime_identity,
        source=source,
        build=build,
        signed=signed,
    )
    if not evaluation.authorized:
        raise AuthorityEvidenceError("verified_authority_receipt_required")

    runtime_digest = sha256_runtime_identity = __import__(
        "ce.foundation.provenance", fromlist=["runtime_identity_sha256"]
    ).runtime_identity_sha256(runtime_identity)
    capability = object.__new__(VerifiedRuntimeCapability)
    object.__setattr__(capability, "runtime_identity_sha256", runtime_digest)
    object.__setattr__(capability, "runtime_environment_kind", runtime_identity.runtime_environment_kind or "")
    object.__setattr__(capability, "source_commit", runtime_identity.source_commit or "")
    object.__setattr__(capability, "source_tree_sha256_v2", runtime_identity.source_tree_sha256_v2 or "")
    object.__setattr__(capability, "dependency_lock_digest", runtime_identity.dependency_lock_digest or "")
    object.__setattr__(capability, "timezone_bundle_digest", runtime_identity.timezone_bundle_digest or "")
    object.__setattr__(capability, "ephemeris_bundle_digest", runtime_identity.ephemeris_bundle_digest or "")
    object.__setattr__(capability, "native_library_sha256", native_library_sha256)
    object.__setattr__(capability, "swiss_release", swiss_release)
    object.__setattr__(capability, "swiss_source_commit", swiss_source_commit)
    object.__setattr__(capability, "source_authority_digest", source.source_authority_digest)
    object.__setattr__(capability, "trusted_build_digest", build.build_digest)
    object.__setattr__(capability, "provenance_signature_digest", signed.provenance_signature_digest)
    object.__setattr__(capability, "_issued", True)
    errors = capability.validate()
    if errors:
        raise AuthorityEvidenceError("runtime_capability_invalid:" + ";".join(errors))
    return capability


def _require_sha(value: str, field: str) -> None:
    if not isinstance(value, str) or not _SHA256_RE.fullmatch(value):
        raise AuthorityEvidenceError(f"malformed:{field}")


def _require_commit(value: str, field: str) -> None:
    if not isinstance(value, str) or not _COMMIT_RE.fullmatch(value):
        raise AuthorityEvidenceError(f"malformed:{field}")


def _require_fingerprint(value: str, field: str) -> None:
    if not isinstance(value, str) or not _FINGERPRINT_RE.fullmatch(value):
        raise AuthorityEvidenceError(f"malformed:{field}")


def evaluate_authority_consistency(
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



def evaluate_full_authority(
    runtime_identity: RuntimeIdentity,
    *,
    source: SourceAuthorityEvidence,
    build: TrustedBuildEvidence,
    signed: SignedProvenanceEvidence,
) -> AuthorityEvaluation:
    """Authorization boundary: descriptive evidence is never self-authorizing.

    The legacy consistency evaluator remains available as audit evidence, but
    this function cannot produce an AUTHORIZED decision. A future production
    path must supply a separately verified authority receipt established by
    controlled governance machinery.
    """
    consistency = evaluate_authority_consistency(
        runtime_identity,
        source=source,
        build=build,
        signed=signed,
    )
    reasons = list(consistency.reasons)
    reasons.append("verified_authority_receipt_required")
    return AuthorityEvaluation(
        authorized=False,
        reasons=tuple(dict.fromkeys(reasons)),
        source_authority_digest=None,
        trusted_build_digest=None,
        provenance_signature_digest=None,
    )
