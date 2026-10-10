from __future__ import annotations

from pathlib import Path

from ce.foundation.source_tree_identity import source_tree_sha256

ROOT = Path(__file__).resolve().parents[1]
manifest = (ROOT / "manifests" / "SOURCE_TREE_SHA256_V2.txt").read_text(encoding="utf-8").split()[0]
actual_hash = source_tree_sha256(ROOT)
if actual_hash != manifest:
    raise SystemExit(f"IDENTITY_FAIL: manifest={manifest} actual={actual_hash}")
print(f"SOURCE_TREE_IDENTITY_PASS {actual_hash}")
