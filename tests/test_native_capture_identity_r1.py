from __future__ import annotations

from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from ce.ephemeris.native_runtime import NativeRuntimeError
from tools.capture_native_runtime import _resolve_runtime_environment_identity, _verify_canonical_fixture_spec, _verify_source_identity


class NativeCaptureIdentityR1Tests(unittest.TestCase):
    ROOT = Path(__file__).resolve().parents[1]

    @patch("tools.capture_native_runtime.source_tree_sha256", return_value="b" * 64)
    @patch(
        "tools.capture_native_runtime.subprocess.run",
        return_value=subprocess.CompletedProcess(
            args=["git", "rev-parse", "HEAD"],
            returncode=0,
            stdout="a" * 40 + "\n",
            stderr="",
        ),
    )
    def test_source_commit_and_tree_identity_pass(
        self,
        _run,
        _tree,
    ) -> None:
        _verify_source_identity(self.ROOT, "a" * 40, "b" * 64)

    @patch(
        "tools.capture_native_runtime.subprocess.run",
        return_value=subprocess.CompletedProcess(
            args=["git", "rev-parse", "HEAD"],
            returncode=0,
            stdout="c" * 40 + "\n",
            stderr="",
        ),
    )
    def test_source_commit_identity_mismatch_fails(self, _run) -> None:
        with self.assertRaisesRegex(NativeRuntimeError, "source_commit_identity_mismatch"):
            _verify_source_identity(self.ROOT, "a" * 40, "b" * 64)

    @patch("tools.capture_native_runtime.source_tree_sha256", return_value="c" * 64)
    @patch(
        "tools.capture_native_runtime.subprocess.run",
        return_value=subprocess.CompletedProcess(
            args=["git", "rev-parse", "HEAD"],
            returncode=0,
            stdout="a" * 40 + "\n",
            stderr="",
        ),
    )
    def test_source_tree_identity_mismatch_fails(
        self,
        _run,
        _tree,
    ) -> None:
        with self.assertRaisesRegex(NativeRuntimeError, "source_tree_identity_mismatch"):
            _verify_source_identity(self.ROOT, "a" * 40, "b" * 64)

    @patch(
        "tools.capture_native_runtime.subprocess.run",
        side_effect=subprocess.CalledProcessError(
            1, ["git", "rev-parse", "HEAD"]
        ),
    )
    def test_source_commit_identity_unavailable_fails_closed(self, _run) -> None:
        with self.assertRaisesRegex(
            NativeRuntimeError, "source_commit_identity_unavailable"
        ):
            _verify_source_identity(self.ROOT, "a" * 40, "b" * 64)


    def test_host_native_environment_digest_is_recomputed_from_manifest(self) -> None:
        import json
        from hashlib import sha256
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "environment.json"
            manifest = {
                "schema_version": "CE-V1-HOST-NATIVE-ENV-R1",
                "kind": "HOST_NATIVE",
                "os": {"system": "Windows", "release": "11", "version": "10.0", "machine": "AMD64"},
                "python": {
                    "implementation": "CPython",
                    "version": "3.13.15",
                    "platform": "Windows",
                    "executable_sha256": "a" * 64,
                    "executable_size_bytes": 1,
                },
                "components": [],
            }
            raw = json.dumps({
                "identity_manifest": manifest,
                "runtime_environment_digest": sha256(
                    json.dumps(manifest, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
                ).hexdigest(),
            })
            path.write_text(raw, encoding="utf-8")
            kind, image, environment = _resolve_runtime_environment_identity(None, path)
            self.assertEqual(kind, "HOST_NATIVE")
            self.assertIsNone(image)
            self.assertEqual(len(environment), 64)

    def test_git_blob_sha1_uses_null_byte_header(self) -> None:
        from ce.ephemeris.native_runtime import _git_blob_sha1

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "empty.bin"
            path.write_bytes(b"")
            self.assertEqual(
                _git_blob_sha1(path),
                "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391",
            )

    def test_external_fixture_path_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixture.json"
            path.write_text("{}", encoding="utf-8")
            with self.assertRaisesRegex(NativeRuntimeError, "fixture_spec_identity_mismatch"):
                _verify_canonical_fixture_spec(Path(directory), path)

    def test_mixed_runtime_identity_arguments_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "environment.json"
            path.write_text("{}", encoding="utf-8")
            with self.assertRaisesRegex(NativeRuntimeError, "runtime_identity_argument_mismatch"):
                _resolve_runtime_environment_identity("sha256:" + "a" * 64, path)


if __name__ == "__main__":
    unittest.main()
