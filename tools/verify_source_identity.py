from __future__ import annotations

from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[1]
ns = runpy.run_path(str(ROOT / "build/build_source_tree_hash.py"))
actual_hash = ns["digest"]()
manifest = (ROOT / "manifests/SOURCE_TREE_SHA256_V2.txt").read_text(encoding="utf-8").split()[0]
if actual_hash != manifest:
    raise SystemExit(f"IDENTITY_FAIL: manifest={manifest} actual={actual_hash}")
print(f"SOURCE_TREE_IDENTITY_PASS {actual_hash}")
