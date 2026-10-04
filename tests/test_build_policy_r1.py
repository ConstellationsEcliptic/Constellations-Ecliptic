from __future__ import annotations

from pathlib import Path
import unittest

from ce.runtime.build_policy import scan_build_policy


ROOT = Path(__file__).resolve().parents[1]


class BuildPolicyR1Tests(unittest.TestCase):
    def test_current_build_tree_has_no_forbidden_tokens(self) -> None:
        findings = scan_build_policy(ROOT)
        self.assertEqual(findings, ())


if __name__ == "__main__":
    unittest.main()
