from __future__ import annotations

from typing import Callable

from ce.claim.manifest import AllowedClaimManifest

VerifiedSemanticConformance = Callable[[str, AllowedClaimManifest], bool]


class SemanticVerifierNotEstablished(RuntimeError):
    """No verified semantic conformance implementation is established."""


def get_verified_semantic_conformance() -> VerifiedSemanticConformance | None:
    # Deliberately fail closed until a controlled, non-caller-supplied semantic
    # verifier is established and independently verified.
    return None
