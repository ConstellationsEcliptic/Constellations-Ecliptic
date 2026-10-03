from __future__ import annotations

from pathlib import Path
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
