from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from tools.package_source import add


ROOT = Path(__file__).resolve().parents[1]


class PackagingDeterminismTests(unittest.TestCase):
    def test_packaging_identity_is_independent_of_source_mode(self) -> None:
        (ROOT / "dist").mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=ROOT / "dist") as first, tempfile.TemporaryDirectory(
            dir=ROOT / "dist"
        ) as second:
            left_root = Path(first)
            right_root = Path(second)
            left = left_root / "payload.txt"
            right = right_root / "payload.txt"
            payload = b"CE deterministic packaging\n"
            left.write_bytes(payload)
            right.write_bytes(payload)

            os.chmod(left, 0o644)
            os.chmod(right, 0o755)

            left_zip = left_root / "left.zip"
            right_zip = right_root / "right.zip"

            with ZipFile(left_zip, "w") as z:
                add(z, left, root=left_root)
            with ZipFile(right_zip, "w") as z:
                add(z, right, root=right_root)

            self.assertEqual(left_zip.read_bytes(), right_zip.read_bytes())

            with ZipFile(left_zip, "r") as z:
                self.assertEqual(z.infolist()[0].external_attr, 0o100644 << 16)
