from __future__ import annotations

from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch

from ce.ephemeris.native_runtime import NativeRuntimeError
from tools.capture_native_runtime import _verify_source_identity


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


if __name__ == "__main__":
    unittest.main()
