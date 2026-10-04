from __future__ import annotations

from datetime import datetime
from pathlib import Path
import tempfile
import unittest

from ce.timezone.runtime import TzifRuntime, TzifRuntimeError, compute_manifest_sha256


class TzifRuntimeR1Tests(unittest.TestCase):
    def test_manifest_identity_is_order_independent(self) -> None:
        a = {"UTC": b"abc", "Asia/Test": b"def"}
        b = {"Asia/Test": b"def", "UTC": b"abc"}
        self.assertEqual(compute_manifest_sha256(a), compute_manifest_sha256(b))

    def test_identity_must_be_established_before_resolution(self) -> None:
        with self.assertRaisesRegex(TzifRuntimeError, "tzif_bundle_identity_not_established"):
            TzifRuntime(
                version="2026d",
                files={},
                expected_manifest_sha256=None,
            )

    def test_manifest_mismatch_fails_closed(self) -> None:
        with self.assertRaisesRegex(TzifRuntimeError, "tzif_bundle_identity_mismatch"):
            TzifRuntime(
                version="2026d",
                files={"UTC": b"not-tzif"},
                expected_manifest_sha256="0" * 64,
            )

    def test_package_manifest_binds_zone_bytes(self) -> None:
        import json
        from hashlib import sha256
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "metadata").mkdir()
            (root / "tzif").mkdir()
            zone = b"TZif2\\x00fake-zone"
            (root / "tzif" / "UTC").write_bytes(zone)
            manifest = {
                "algorithm": "SHA256_UTF8_LF_JOIN_SORTED_PATH_HASH",
                "entries": [{"path": "UTC", "size": len(zone), "sha256": sha256(zone).hexdigest()}],
            }
            raw = json.dumps(manifest).encode("utf-8")
            manifest_hash = sha256(raw).hexdigest()
            (root / "metadata" / "runtime-tzif-manifest.json").write_bytes(raw)
            runtime, identity = TzifRuntime.from_package_root(
                package_root=root,
                expected_manifest_sha256=manifest_hash,
                expected_entry_count=1,
            )
            self.assertEqual(identity.manifest.manifest_sha256, manifest_hash)
            self.assertEqual(len(identity.files), 1)

    def test_package_zone_byte_mutation_fails_closed(self) -> None:
        import json
        from hashlib import sha256
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "metadata").mkdir()
            (root / "tzif").mkdir()
            zone = b"TZif2\\x00fake-zone"
            (root / "tzif" / "UTC").write_bytes(zone)
            manifest = {
                "algorithm": "SHA256_UTF8_LF_JOIN_SORTED_PATH_HASH",
                "entries": [{"path": "UTC", "size": len(zone), "sha256": sha256(zone).hexdigest()}],
            }
            raw = json.dumps(manifest).encode("utf-8")
            manifest_hash = sha256(raw).hexdigest()
            (root / "metadata" / "runtime-tzif-manifest.json").write_bytes(raw)
            runtime, _ = TzifRuntime.from_package_root(
                package_root=root,
                expected_manifest_sha256=manifest_hash,
                expected_entry_count=1,
            )
            (root / "tzif" / "UTC").write_bytes(b"MUTATED")
            with self.assertRaisesRegex(TzifRuntimeError, "tzif_zone_size_mismatch|tzif_zone_sha256_mismatch"):
                runtime.resolve_local_instant(datetime(2026, 1, 1), "UTC")


if __name__ == "__main__":
    unittest.main()
