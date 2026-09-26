from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def run(*args: str) -> str:
    cp = subprocess.run(args, cwd=ROOT, check=True, capture_output=True, text=True)
    return cp.stdout.strip()

def main() -> int:
    record = json.loads((ROOT / "provenance/dev_source_identity.json").read_text(encoding="utf-8"))
    commit = record["source_snapshot_commit"]
    tree_expected = record["source_snapshot_tree_oid"]
    tree_actual = run("git", "rev-parse", f"{commit}^{{tree}}")
    if tree_expected != tree_actual:
        raise SystemExit(f"IDENTITY_FAIL: source snapshot tree record={tree_expected} actual={tree_actual}")
    sys.path.insert(0, str(ROOT))
    import runpy
    ns = runpy.run_path(str(ROOT / "build/build_source_tree_hash.py"))
    actual_hash = ns["digest"]()
    if record["ce_source_tree_sha256_v2"] != actual_hash:
        raise SystemExit(f"IDENTITY_FAIL: source tree digest record={record['ce_source_tree_sha256_v2']} actual={actual_hash}")
    manifest = (ROOT / "manifests/SOURCE_TREE_SHA256_V2.txt").read_text(encoding="utf-8").split()[0]
    if manifest != actual_hash:
        raise SystemExit("IDENTITY_FAIL: source digest manifest mismatch")
    print("SOURCE_IDENTITY_PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
