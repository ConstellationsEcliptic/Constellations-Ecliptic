from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from ce.ephemeris.verification import DataFileExpectation, EphemerisVerificationError, verify_data_files


class EphemerisVerificationR1Tests(unittest.TestCase):
    def test_missing_file_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(EphemerisVerificationError, "missing_data_file"):
                verify_data_files(
                    Path(directory),
                    (DataFileExpectation("seas_18.se1", 223004, "a" * 64),),
                )

    def test_size_mismatch_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "seas_18.se1"
            path.write_bytes(b"test")
            with self.assertRaisesRegex(EphemerisVerificationError, "size_mismatch"):
                verify_data_files(
                    Path(directory),
                    (DataFileExpectation("seas_18.se1", 223004, "a" * 64),),
                )

    def test_hash_mismatch_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "seas_18.se1"
            path.write_bytes(b"test")
            with self.assertRaisesRegex(EphemerisVerificationError, "sha256_mismatch"):
                verify_data_files(
                    Path(directory),
                    (DataFileExpectation("seas_18.se1", 4, "0" * 64),),
                )


if __name__ == "__main__":
    unittest.main()
