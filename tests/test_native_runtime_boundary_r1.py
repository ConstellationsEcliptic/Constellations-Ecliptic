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


if __name__ == "__main__":
    unittest.main()
