from __future__ import annotations

import tempfile
from pathlib import Path
import unittest

from ce.foundation.source_tree_identity import source_tree_sha256


class CER0ControlPlaneIdentityScopeTests(unittest.TestCase):
    """Adversarial proof for trust-bearing control-plane files."""

    def _tree(self, root: Path, workflow_text: str) -> None:
        (root / "src").mkdir(parents=True)
        (root / ".github" / "workflows").mkdir(parents=True)
        (root / "src" / "marker.txt").write_bytes(b"implementation")
        (root / ".github" / "workflows" / "critical.yml").write_bytes(
            workflow_text.encode("utf-8")
        )

    def test_workflow_change_must_change_identity(self):
        with tempfile.TemporaryDirectory() as first_dir, tempfile.TemporaryDirectory() as second_dir:
            first = Path(first_dir)
            second = Path(second_dir)
            self._tree(first, "name: one\n")
            self._tree(second, "name: two\n")
            first_digest = source_tree_sha256(first)
            second_digest = source_tree_sha256(second)
            self.assertNotEqual(
                first_digest,
                second_digest,
                "TRUST-BEARING CONTROL-PLANE DIVERGENCE IS INVISIBLE TO SOURCE IDENTITY",
            )


if __name__ == "__main__":
    unittest.main()
