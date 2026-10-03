from __future__ import annotations

from pathlib import Path
import os
import tempfile
import unittest

from ce.foundation.source_tree_identity import source_tree_sha256


class SourceTreeIdentityR1Tests(unittest.TestCase):
    def test_same_content_produces_same_identity(self) -> None:
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            for root in (Path(a), Path(b)):
                (root / "src").mkdir()
                (root / "src" / "x.py").write_text("print('x')\n", encoding="utf-8")
            self.assertEqual(source_tree_sha256(Path(a)), source_tree_sha256(Path(b)))

    def test_filesystem_mode_is_not_identity_bearing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "src").mkdir()
            path = root / "src" / "x.py"
            path.write_text("x\\n", encoding="utf-8")
            first = source_tree_sha256(root)
            os.chmod(path, 0o600)
            self.assertEqual(first, source_tree_sha256(root))

    def test_path_and_content_are_identity_bearing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "src").mkdir()
            first = root / "src" / "x.py"
            second = root / "src" / "y.py"
            first.write_text("x\n", encoding="utf-8")
            digest1 = source_tree_sha256(root)
            second.write_text("x\n", encoding="utf-8")
            self.assertNotEqual(digest1, source_tree_sha256(root))
            
if __name__ == "__main__":
    unittest.main()

    def test_source_digest_manifest_is_not_self_referential(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "src").mkdir()
            (root / "manifests").mkdir()
            (root / "src" / "x.py").write_text("x\n", encoding="utf-8")
            first = source_tree_sha256(root)
            (root / "manifests" / "SOURCE_TREE_SHA256_V2.txt").write_text(
                "deadbeef  self-reference\n", encoding="utf-8"
            )
            self.assertEqual(first, source_tree_sha256(root))
