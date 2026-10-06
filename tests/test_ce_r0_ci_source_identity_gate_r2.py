from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class CER0CISourceIdentityGateTests(unittest.TestCase):
    def _text(self, path: str) -> str:
        return (ROOT / path).read_text(encoding="utf-8")

    def test_remediation_ci_must_fail_on_identity_mismatch(self):
        text = self._text(".github/workflows/ce-r0-remediation-ci-r1.yml")
        self.assertNotIn(
            "set +e",
            text,
            "REMEDIATION CI DISABLES ERROR PROPAGATION AROUND SOURCE IDENTITY",
        )
        self.assertRegex(
            text,
            r"SOURCE_TREE_IDENTITY_MATCH=FALSE[\s\S]{0,500}exit\s+1",
            "SOURCE IDENTITY MISMATCH IS REPORTED BUT NOT A HARD CI FAILURE",
        )

    def test_full_boundary_ci_must_compare_computed_identity_to_manifest(self):
        text = self._text(".github/workflows/ce-r0-full-boundary-ci-r1.yml")
        self.assertIn(
            "SOURCE_TREE_MANIFEST",
            text,
            "FULL BOUNDARY CI COMPUTES IDENTITY BUT DOES NOT READ THE MANIFEST",
        )
        self.assertRegex(
            text,
            r"(SOURCE_TREE_ACTUAL.{0,400}SOURCE_TREE_MANIFEST|SOURCE_TREE_MANIFEST.{0,400}SOURCE_TREE_ACTUAL)",
            "FULL BOUNDARY CI HAS NO EXPLICIT COMPUTED-vs-MANIFEST COMPARISON",
        )


if __name__ == "__main__":
    unittest.main()
