from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from build import build_source_tree_hash
from tools.package_source import add, build_archive, package_identity, files


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


    def test_package_scope_and_identity_are_bound_to_source_tree_identity(self) -> None:
        expected = [
            p.relative_to(ROOT).as_posix()
            for p in build_source_tree_hash.iter_files()
        ]
        packaged = [p.relative_to(ROOT).as_posix() for p in files()]
        self.assertEqual(packaged, expected)

        with tempfile.TemporaryDirectory(dir=ROOT / "dist") as temp:
            left = Path(temp) / "left.zip"
            right = Path(temp) / "right.zip"
            build_archive(left)
            build_archive(right)

            self.assertEqual(left.read_bytes(), right.read_bytes())

            with ZipFile(left, "r") as z:
                self.assertEqual(sorted(z.namelist()), expected)
                comment = z.comment.decode("ascii")

            self.assertEqual(
                comment,
                f"CE_SOURCE_TREE_SHA256_V2={build_source_tree_hash.digest()}\n",
            )

            identity = package_identity(left)
            self.assertEqual(
                identity["source_tree_sha256_v2"],
                build_source_tree_hash.digest(),
            )
            self.assertRegex(
                identity["package_artifact_sha256"],
                r"^[0-9a-f]{64}$",
            )
