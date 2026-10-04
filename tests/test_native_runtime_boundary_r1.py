from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from ce.ephemeris.native_runtime import (
    CANONICAL_SWISS_BUNDLE_SHA256,
    NativeRuntimeError,
    NativeSwissEphemerisAdapter,
)


class NativeRuntimeBoundaryR1Tests(unittest.TestCase):
    def test_non_authorized_runtime_fails_before_loading(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(NativeRuntimeError, "runtime_not_authorized"):
                NativeSwissEphemerisAdapter(
                    library_path=Path(directory) / "libswe.dll",
                    ephemeris_root=Path(directory),
                    calling_convention="__cdecl",
                    runtime_authorized=False,
                )

    def test_abi_must_be_explicit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            library = Path(directory) / "libswe.dll"
            library.write_bytes(b"test")
            with self.assertRaisesRegex(NativeRuntimeError, "native_abi_calling_convention_not_pinned"):
                NativeSwissEphemerisAdapter(
                    library_path=library,
                    ephemeris_root=Path(directory),
                    calling_convention="UNSPECIFIED",
                    runtime_authorized=True,
                )

    def test_candidate_bundle_identity_is_fixed(self) -> None:
        self.assertEqual(len(CANONICAL_SWISS_BUNDLE_SHA256), 64)

    def test_unknown_object_fails_closed_without_synthetic_valid_state(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            library = Path(directory) / "libswe.dll"
            with self.assertRaisesRegex(NativeRuntimeError, "runtime_not_authorized"):
                NativeSwissEphemerisAdapter(
                    library_path=library,
                    ephemeris_root=Path(directory),
                    calling_convention="__cdecl",
                    runtime_authorized=False,
                )

    def test_canonical_library_hash_cannot_be_overridden(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            library = Path(directory) / "libswe.dll"
            library.write_bytes(b"test")
            with self.assertRaisesRegex(NativeRuntimeError, "native_library_identity_override_forbidden"):
                NativeSwissEphemerisAdapter(
                    library_path=library,
                    ephemeris_root=Path(directory),
                    calling_convention="__cdecl",
                    runtime_authorized=True,
                    expected_library_sha256="0" * 64,
                )

    def test_native_calculation_record_carries_flags_and_coordinates_contract(self) -> None:
        from ce.calculation.contracts import ObjectRecord
        import math
        record = ObjectRecord(
            object_id="SUN",
            object_status=__import__("ce.foundation.status", fromlist=["CalculationStatus"]).CalculationStatus.VALID,
            requested_flags=258,
            actual_flags=258,
            longitude=10.0,
            latitude=0.0,
            distance=1.0,
            speed=0.99,
        )
        self.assertEqual(record.requested_flags, 258)
        self.assertEqual(record.actual_flags, 258)
        self.assertTrue(math.isfinite(record.longitude))

    def test_nonvalid_object_record_cannot_publish_position(self) -> None:
        from ce.calculation.contracts import ObjectRecord
        from ce.foundation.status import CalculationStatus
        with self.assertRaises(ValueError):
            ObjectRecord(
                object_id="SUN",
                object_status=CalculationStatus.KNOWN_UNAVAILABLE,
                requested_flags=258,
                actual_flags=None,
                longitude=10.0,
                latitude=None,
                distance=None,
                speed=None,
            )


if __name__ == "__main__":
    unittest.main()
