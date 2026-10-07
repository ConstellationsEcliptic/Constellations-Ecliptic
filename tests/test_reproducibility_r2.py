from __future__ import annotations

import unittest

from ce.runtime.reproducibility import ReproducibilityCaptureError, RuntimeCapture, compare_capture_outputs


class ReproducibilityR2EnvironmentTests(unittest.TestCase):
    def _capture(self, capture_id: str, *, kind: str = "HOST_NATIVE", env_digest: str | None = "1" * 64, image_digest: str | None = None) -> RuntimeCapture:
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
            runtime_environment_kind=kind,
            runtime_image_digest=image_digest,
            runtime_environment_digest=env_digest,
            timezone_bundle_digest="e" * 64,
            ephemeris_bundle_digest="f" * 64,
            native_library_sha256="1" * 64,
            native_runtime_version="2.10.03",
            swiss_source_commit="2" * 40,
            calling_convention="__cdecl",
            fixtures=(
                {"fixture_id":"SYNTHETIC-001","records":{"value":10.0,"status":"VALID"}},
            ),
        )

    def test_host_native_capture_requires_environment_digest(self) -> None:
        with self.assertRaisesRegex(ReproducibilityCaptureError, "runtime_environment_digest"):
            self._capture("A", env_digest=None)

    def test_oci_capture_requires_image_digest(self) -> None:
        capture = self._capture("A", kind="OCI_IMAGE", env_digest=None, image_digest="sha256:" + "d" * 64)
        self.assertEqual(capture.runtime_image_digest, "sha256:" + "d" * 64)

    def test_host_native_and_oci_identity_mismatch_is_detected(self) -> None:
        host = self._capture("A")
        container = self._capture("B", kind="OCI_IMAGE", env_digest=None, image_digest="sha256:" + "d" * 64)
        errors = compare_capture_outputs(host, container)
        self.assertIn("identity_mismatch:runtime_environment_kind", errors)
        self.assertIn("identity_mismatch:runtime_image_digest", errors)
        self.assertIn("identity_mismatch:runtime_environment_digest", errors)

    def test_none_of_the_environment_identities_is_rejected(self) -> None:
        with self.assertRaisesRegex(ReproducibilityCaptureError, "runtime_environment_kind|runtime_image_digest|runtime_environment_digest"):
            self._capture("A", kind="HOST_NATIVE", env_digest=None, image_digest=None)


if __name__ == "__main__":
    unittest.main()
