from __future__ import annotations

import unittest

from ce.runtime.reproducibility import ReproducibilityCaptureError, RuntimeCapture, compare_capture_outputs


class ReproducibilityR1Tests(unittest.TestCase):
    def _capture(self, capture_id: str, longitude: float = 10.0) -> RuntimeCapture:
        return RuntimeCapture(
            capture_id=capture_id,
            captured_at_utc="2026-01-01T00:00:00Z",
            platform="synthetic-test-platform",
            python_version="3.13.15",
            execution_profile_id="CE-CALC-V1-EP-001",
            execution_profile_revision=4,
            source_commit="a" * 40,
            source_tree_sha256_v2="b" * 64,
            control_plane_sha256="9" * 64,
            dependency_lock_digest="c" * 64,
            runtime_environment_kind="OCI_IMAGE",
            runtime_image_digest="sha256:" + "d" * 64,
            runtime_environment_digest=None,
            timezone_bundle_digest="e" * 64,
            ephemeris_bundle_digest="f" * 64,
            native_library_sha256="1" * 64,
            native_runtime_version="2.10.03",
            swiss_source_commit="2" * 40,
            calling_convention="__cdecl",
            fixtures=(
                {
                    "fixture_id": "SYNTHETIC-001",
                    "records": {"value": longitude, "status": "VALID"},
                },
            ),
        )

    def test_capture_is_content_addressed(self) -> None:
        self.assertEqual(self._capture("A").content_sha256(), self._capture("A").content_sha256())

    def test_identity_mismatch_is_detected(self) -> None:
        left = self._capture("A")
        right = self._capture("B")
        right = RuntimeCapture(**{**right.__dict__, "native_library_sha256": "9" * 64})
        errors = compare_capture_outputs(left, right)
        self.assertIn("identity_mismatch:native_library_sha256", errors)

    def test_numeric_tolerance_is_explicit(self) -> None:
        left = self._capture("A", 10.0)
        right = self._capture("B", 10.0001)
        self.assertIn("fixtures[SYNTHETIC-001].records.value:numeric_mismatch", compare_capture_outputs(left, right))
        self.assertEqual(
            compare_capture_outputs(left, right, numeric_tolerances={"value": 0.001}),
            (),
        )

    def test_nonfinite_fixture_is_rejected(self) -> None:
        with self.assertRaisesRegex(ReproducibilityCaptureError, "finite_number_required"):
            self._capture("A", float("nan"))


if __name__ == "__main__":
    unittest.main()
