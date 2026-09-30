import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GRAPH = ROOT / "provenance" / "CE_V1_NATIVE_RUNTIME_AUTHORITY_GRAPH_R1.json"
VERIFY = ROOT / "tools" / "verify_native_authority_graph.py"

def test_native_authority_graph():
    doc = json.loads(GRAPH.read_text(encoding="utf-8"))
    assert doc["status"] == "EVIDENCE_BOUND_NON_AUTHORIZED"
    assert doc["native_runtime_artifact"]["sha256"] == "04aedc75191ce7d257a20d6141ab889073a1cb6a501ecad98faa6305b24861f2"
    assert doc["canonical_data"]["revision"] == 4
    p = subprocess.run([sys.executable, str(VERIFY)], capture_output=True, text=True, cwd=ROOT)
    assert p.returncode == 0, p.stdout + p.stderr
