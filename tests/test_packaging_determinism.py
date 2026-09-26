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
        with tempfile.TemporaryDirectory(dir=ROOT / "dist") as tmp:
            temp_root = Path(tmp)
            left = temp_root / "left.txt"
            right = temp_root / "right.txt"
            payload = "CE deterministic packaging\n".encode("utf-8")
            left.write_bytes(payload)
            right.write_bytes(payload)

            os.chmod(left, 0o644)
            os.chmod(right, 0o755)

            left_zip = temp_root / "left.zip"
            right_zip = temp_root / "right.zip"

            with ZipFile(left_zip, "w") as z:
                add(z, left)
            with ZipFile(right_zip, "w") as z:
                add(z, right)

            with ZipFile(left_zip, "r") as z_left, ZipFile(right_zip, "r") as z_right:
                left_info = z_left.infolist()[0]
                right_info = z_right.infolist()[0]
                self.assertEqual(left_info.external_attr, right_info.external_attr)
