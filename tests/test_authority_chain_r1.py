from __future__ import annotations

import unittest

from ce.foundation.identity import RuntimeIdentity
from ce.runtime.authority import (
    SignedProvenanceEvidence,
    SourceAuthorityEvidence,
    TrustedBuildEvidence,
    evaluate_authority_consistency,
    evaluate_full_authority,
)


class AuthorityChainR1Tests(unittest.TestCase):
    def _identity(self) -> RuntimeIdentity:
        return RuntimeIdentity(
            "CE-CALC-V1-EP-001",
            4,
            "a" * 40,
            "b" * 64,
            "sha256:" + "c" * 64,
            "d" * 64,
            "e" * 64,
            "f" * 64,
            "1" * 64,
            "2" * 64,
            "3" * 64,
        )

    def _evidence(self):
        return (
            SourceAuthorityEvidence(
                "https://github.example/ce",
                "a" * 40,
                "b" * 64,
                "1" * 64,
                "ABCDEF" * 6 + "ABCD",
            ),
            TrustedBuildEvidence(
                "2" * 64,
                "a" * 40,
                "b" * 64,
                "d" * 64,
                "sha256:" + "c" * 64,
                "4" * 64,
                "e" * 64,
                "f" * 64,
            ),
            SignedProvenanceEvidence(
                "3" * 64,
                "ABCDEF" * 6 + "ABCD",
                "1" * 64,
                "2" * 64,
            ),
        )

    def test_complete_synthetic_chain_is_consistent(self) -> None:
        source, build, signed = self._evidence()
        consistency = evaluate_authority_consistency(
            self._identity(), source=source, build=build, signed=signed
        )
        self.assertTrue(consistency.authorized)
        result = evaluate_full_authority(
            self._identity(), source=source, build=build, signed=signed
        )
        self.assertFalse(result.authorized)
        self.assertIn("verified_authority_receipt_required", result.reasons)

    def test_mismatched_tree_cannot_authorize(self) -> None:
        source, build, signed = self._evidence()
        build = TrustedBuildEvidence(
            build.build_digest,
            build.source_commit,
            "9" * 64,
            build.dependency_lock_digest,
            build.runtime_image_digest,
            build.runtime_manifest_digest,
            build.timezone_bundle_digest,
            build.ephemeris_bundle_digest,
        )
        result = evaluate_full_authority(
            self._identity(), source=source, build=build, signed=signed
        )
        self.assertFalse(result.authorized)
        self.assertIn("source_build_tree_mismatch", result.reasons)

    def test_malformed_runtime_manifest_digest_cannot_authorize(self) -> None:
        source, build, signed = self._evidence()
        build = TrustedBuildEvidence(
            build.build_digest,
            build.source_commit,
            build.source_tree_sha256_v2,
            build.dependency_lock_digest,
            build.runtime_image_digest,
            "not-a-sha256",
            build.timezone_bundle_digest,
            build.ephemeris_bundle_digest,
        )
        result = evaluate_full_authority(
            self._identity(), source=source, build=build, signed=signed
        )
        self.assertFalse(result.authorized)
        self.assertIn("malformed:build.runtime_manifest_digest", result.reasons)

    def test_runtime_identity_digest_mismatch_cannot_authorize(self) -> None:
        source, build, signed = self._evidence()
        identity = RuntimeIdentity(
            "CE-CALC-V1-EP-001",
            4,
            "a" * 40,
            "9" * 64,
            "sha256:" + "c" * 64,
            "d" * 64,
            "e" * 64,
            "f" * 64,
            "1" * 64,
            "2" * 64,
            "3" * 64,
        )
        result = evaluate_full_authority(identity, source=source, build=build, signed=signed)
        self.assertFalse(result.authorized)
        self.assertIn("runtime_identity_mismatch:source_tree_sha256_v2", result.reasons)


if __name__ == "__main__":
    unittest.main()
