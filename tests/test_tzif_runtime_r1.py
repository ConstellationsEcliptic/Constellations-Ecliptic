from __future__ import annotations

from datetime import datetime
import unittest

from ce.timezone.runtime import TzifRuntime, TzifRuntimeError, compute_manifest_sha256


class TzifRuntimeR1Tests(unittest.TestCase):
    def test_manifest_identity_is_order_independent(self) -> None:
        a = {"UTC": b"abc", "Asia/Test": b"def"}
        b = {"Asia/Test": b"def", "UTC": b"abc"}
        self.assertEqual(compute_manifest_sha256(a), compute_manifest_sha256(b))

    def test_identity_must_be_established_before_resolution(self) -> None:
        runtime = TzifRuntime(
            version="2026d",
            files={},
            expected_manifest_sha256=None,
        )
        with self.assertRaisesRegex(TzifRuntimeError, "tzif_bundle_identity_not_established"):
            runtime.resolve_local_instant(datetime(2026, 1, 1), "UTC")

    def test_manifest_mismatch_fails_closed(self) -> None:
        runtime = TzifRuntime(
            version="2026d",
            files={"UTC": b"not-tzif"},
            expected_manifest_sha256="0" * 64,
        )
        with self.assertRaisesRegex(TzifRuntimeError, "tzif_bundle_identity_mismatch"):
            runtime.resolve_local_instant(datetime(2026, 1, 1), "UTC")


if __name__ == "__main__":
    unittest.main()
