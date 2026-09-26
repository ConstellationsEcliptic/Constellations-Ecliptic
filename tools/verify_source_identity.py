from __future__ import annotations

import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SOURCE_LABEL = "CE_V1_SOURCE_FOUNDATION_R1"

ns = runpy.run_path(str(ROOT / "build/build_source_tree_hash.py"))
actual_hash = ns["digest"]()
identity_fields = (
    (ROOT / "manifests/SOURCE_TREE_SHA256_V2.txt")
    .read_text(encoding="utf-8")
    .strip()
    .split()
)

if len(identity_fields) != 2 or identity_fields[1] != EXPECTED_SOURCE_LABEL:
    raise SystemExit("IDENTITY_FAIL: invalid source identity label")

manifest_hash = identity_fields[0]
if actual_hash != manifest_hash:
    raise SystemExit(f"IDENTITY_FAIL: manifest={manifest_hash} actual={actual_hash}")

print(f"SOURCE_TREE_IDENTITY_PASS {actual_hash}")
