from __future__ import annotations

from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from ce.ephemeris.native_runtime import (
    CANONICAL_SWISS_BUNDLE_SHA256,
    CANDIDATE_NATIVE_DLL_SHA256,
    NativeRuntimeError,
    NativeSwissCalculation,
    NativeSwissEphemerisAdapter,
)
from ce.runtime.authority import VerifiedRuntimeCapability


def build_test_runtime_capability() -> VerifiedRuntimeCapability:
    capability = object.__new__(VerifiedRuntimeCapability)
    values = {
        "runtime_identity_sha256": "a" * 64,
        "runtime_environment_kind": "HOST_NATIVE",
        "source_commit": "b" * 40,
        "source_tree_sha256_v2": "c" * 64,
        "dependency_lock_digest": "d" * 64,
        "timezone_bundle_digest": "e" * 64,
        "ephemeris_bundle_digest": "f" * 64,
        "native_library_sha256": CANDIDATE_NATIVE_DLL_SHA256,
        "swiss_release": "v2.10.3bfinal",
        "swiss_source_commit": "f4dcd18e8005dde95fd8a8d2312ed12f9accd1b0",
        "source_authority_digest": "1" * 64,
        "trusted_build_digest": "2" * 64,
        "provenance_signature_digest": "3" * 64,
        "control_plane_sha256": "4" * 64,
        "native_calling_convention": "__cdecl",
    }
    for name, value in values.items():
        object.__setattr__(capability, name, value)
    object.__setattr__(capability, "_issued", True)
    errors = capability.validate()
    if errors:
        raise AssertionError(";".join(errors))
    return capability


class NativeRuntimeBoundaryR1Tests(unittest.TestCase):
    def test_public_constructor_cannot_create_runtime_capability(self) -> None:
        with self.assertRaisesRegex(Exception, "runtime_capability_must_be_issued"):
            VerifiedRuntimeCapability(
                runtime_identity_sha256="a"*64,
                runtime_environment_kind="HOST_NATIVE",
                source_commit="b"*40,
                source_tree_sha256_v2="c"*64,
                dependency_lock_digest="d"*64,
                timezone_bundle_digest="e"*64,
                ephemeris_bundle_digest="f"*64,
                native_library_sha256=CANDIDATE_NATIVE_DLL_SHA256,
                swiss_release="v2.10.3bfinal",
                swiss_source_commit="f4dcd18e8005dde95fd8a8d2312ed12f9accd1b0",
                source_authority_digest="1"*64,
                trusted_build_digest="2"*64,
                provenance_signature_digest="3"*64,
                control_plane_sha256="4"*64,
                native_calling_convention="__cdecl",
            )

    def test_native_adapter_rejects_missing_capability(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(NativeRuntimeError, "runtime_capability_required"):
                NativeSwissEphemerisAdapter(
                    library_path=Path(directory) / "libswe.dll",
                    ephemeris_root=Path(directory),
                    calling_convention="__cdecl",
                    runtime_capability=None,  # type: ignore[arg-type]
                )

    def test_native_adapter_has_no_boolean_authorization_parameter(self) -> None:
        import inspect
        signature = inspect.signature(NativeSwissEphemerisAdapter.__init__)
        self.assertNotIn("runtime_authorized", signature.parameters)

    def test_abi_must_be_explicit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            library = Path(directory) / "libswe.dll"
            library.write_bytes(b"test")
            with self.assertRaisesRegex(NativeRuntimeError, "native_abi_calling_convention_mismatch"):
                with patch("ce.ephemeris.native_runtime.sha256_file", return_value=CANDIDATE_NATIVE_DLL_SHA256),                      patch("ce.ephemeris.native_runtime.verify_canonical_swiss_bundle", return_value="9"*64):
                    NativeSwissEphemerisAdapter(
                        library_path=library,
                        ephemeris_root=Path(directory),
                        calling_convention="UNSPECIFIED",
                        runtime_capability=build_test_runtime_capability(),
                    )

    def test_candidate_bundle_identity_is_fixed(self) -> None:
        self.assertEqual(len(CANONICAL_SWISS_BUNDLE_SHA256), 64)

    def test_canonical_library_hash_cannot_be_overridden(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            library = Path(directory) / "libswe.dll"
            library.write_bytes(b"test")
            with self.assertRaisesRegex(NativeRuntimeError, "native_library_identity_override_forbidden"):
                NativeSwissEphemerisAdapter(
                    library_path=library,
                    ephemeris_root=Path(directory),
                    calling_convention="__cdecl",
                    runtime_capability=build_test_runtime_capability(),
                    expected_library_sha256="0" * 64,
                )

    def test_native_diagnostics_are_preserved(self) -> None:
        detailed = NativeSwissCalculation(
            object_id="SUN",
            swiss_object_id=0,
            jd_ut=2451545.0,
            longitude_deg=1.0,
            latitude_deg=0.0,
            distance_au=1.0,
            speed_deg_per_day=1.0,
            requested_flags=258,
            actual_flags=258,
            ephemeris="SWIEPH",
            warning_or_error="NATIVE-WARNING",
        )
        record = detailed.to_object_record()
        self.assertEqual(record.warnings, ("NATIVE-WARNING",))
        self.assertEqual(record.errors, ())

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
