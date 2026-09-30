import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "tools" / "verify_native_authority_graph.py"

class NativeAuthorityGraphTests(unittest.TestCase):
    def test_native_authority_graph(self) -> None:
        p = subprocess.run(
            [sys.executable, str(VERIFY)],
            capture_output=True,
            text=True,
            cwd=ROOT,
            check=False,
        )
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertIn("NATIVE_AUTHORITY_GRAPH_PASS", p.stdout)

if __name__ == "__main__":
    unittest.main()
