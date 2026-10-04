from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from ce.ephemeris.verification import (
    DataFileExpectation,
    EphemerisVerificationError,
    classify_requested_actual_flags,
    verify_data_files,
)
from ce.foundation.status import CalculationStatus


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

    def test_requested_actual_flags_match(self) -> None:
        self.assertEqual(
            classify_requested_actual_flags(258, 258),
            CalculationStatus.VALID,
        )

    def test_requested_actual_flags_superset_is_valid(self) -> None:
        self.assertEqual(
            classify_requested_actual_flags(258, 770),
            CalculationStatus.VALID,
        )

    def test_requested_actual_flags_missing_is_failure(self) -> None:
        self.assertEqual(
            classify_requested_actual_flags(258, 2),
            CalculationStatus.CALCULATION_FAILURE,
        )

    def test_requested_actual_flags_missing_actual_is_failure(self) -> None:
        self.assertEqual(
            classify_requested_actual_flags(258, None),
            CalculationStatus.CALCULATION_FAILURE,
        )

    def test_requested_actual_flags_malformed_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            classify_requested_actual_flags(258, -1)

if __name__ == "__main__":
    unittest.main()
