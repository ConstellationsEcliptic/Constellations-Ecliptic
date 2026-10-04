from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from ce.runtime.build_policy import scan_build_policy


ROOT = Path(__file__).resolve().parents[1]


class BuildPolicyR1Tests(unittest.TestCase):
    def test_current_build_tree_has_no_forbidden_tokens(self) -> None:
        findings = scan_build_policy(ROOT)
        self.assertEqual(findings, ())

    def test_workflow_yaml_is_scanned_for_forbidden_tokens(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workflow_dir = root / ".github" / "workflows"
            workflow_dir.mkdir(parents=True)
            (workflow_dir / "unsafe.yml").write_text(
                "run: curl http://example.invalid\nCFLAGS: -ffast-math\n",
                encoding="utf-8",
            )
            findings = scan_build_policy(root)
            observed = {(item.path, item.token, item.category) for item in findings}
            self.assertEqual(
                observed,
                {
                    (".github/workflows/unsafe.yml", "curl http", "RUNTIME_DOWNLOAD"),
                    (".github/workflows/unsafe.yml", "-ffast-math", "FLOATING_POINT"),
                },
            )


if __name__ == "__main__":
    unittest.main()
