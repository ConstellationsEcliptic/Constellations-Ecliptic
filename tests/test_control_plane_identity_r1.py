from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from ce.foundation.control_plane_identity import control_plane_sha256


class ControlPlaneIdentityR1Tests(unittest.TestCase):
    def test_same_control_plane_bytes_produce_same_identity(self) -> None:
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            for root in (Path(a), Path(b)):
                (root / ".github" / "workflows").mkdir(parents=True)
                (root / ".github" / "workflows" / "ci.yml").write_text("name: CI\n", encoding="utf-8")
                (root / "CHANGE_CONTROL.md").write_text("control\n", encoding="utf-8")
            self.assertEqual(control_plane_sha256(Path(a)), control_plane_sha256(Path(b)))

    def test_unrelated_source_bytes_do_not_change_control_plane_identity(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".github").mkdir()
            (root / ".github" / "ci.yml").write_text("name: CI\n", encoding="utf-8")
            (root / "CHANGE_CONTROL.md").write_text("control\n", encoding="utf-8")
            first = control_plane_sha256(root)
            (root / "src").mkdir()
            (root / "src" / "x.py").write_text("print('x')\n", encoding="utf-8")
            self.assertEqual(first, control_plane_sha256(root))

    def test_control_plane_changes_change_identity(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".github").mkdir()
            (root / ".github" / "ci.yml").write_text("name: CI\n", encoding="utf-8")
            (root / "CHANGE_CONTROL.md").write_text("control\n", encoding="utf-8")
            first = control_plane_sha256(root)
            (root / ".github" / "ci.yml").write_text("name: CI\non: push\n", encoding="utf-8")
            self.assertNotEqual(first, control_plane_sha256(root))


if __name__ == "__main__":
    unittest.main()
