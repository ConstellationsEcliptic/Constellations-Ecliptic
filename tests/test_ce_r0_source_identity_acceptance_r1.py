from __future__ import annotations

"""CE-R0 source identity acceptance test.

This is a hard gate candidate: the digest recorded by the repository must be
the digest computed from the exact checked-out source tree using the repository
algorithm. A mismatch is a provenance failure, not a value to be hand-edited
until it happens to match.
"""

from pathlib import Path
import unittest

from ce.foundation.source_tree_identity import source_tree_sha256


class CER0SourceIdentityAcceptanceTests(unittest.TestCase):
    def test_B8_manifest_matches_exact_candidate_tree(self) -> None:
        root = Path(__file__).resolve().parents[1]
        manifest = (root / "manifests" / "SOURCE_TREE_SHA256_V2.txt").read_text(
            encoding="utf-8"
        ).split()[0]
        actual = source_tree_sha256(root)
        self.assertEqual(
            actual,
            manifest,
            "source identity is a hard provenance gate; reconcile the algorithm/tree/ref before updating the manifest",
        )


if __name__ == "__main__":
    unittest.main()
