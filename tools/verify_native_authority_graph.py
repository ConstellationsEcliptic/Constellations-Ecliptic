from __future__ import annotations
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GRAPH = ROOT / "provenance" / "CE_V1_NATIVE_RUNTIME_AUTHORITY_GRAPH_R1.json"

EXPECTED = {
    "candidate.commit": "033e90cfd29e047578e70bbd20183e48682d7614",
    "candidate.source_tree_sha256": "da6a1d622940a4674a54d98656a940aee90aa32ec149ec9b0e8800e467a90ad9",
    "native_runtime_artifact.sha256": "04aedc75191ce7d257a20d6141ab889073a1cb6a501ecad98faa6305b24861f2",
    "native_runtime_artifact.size_bytes": 841728,
    "swiss_source.commit": "f4dcd18e8005dde95fd8a8d2312ed12f9accd1b0",
    "swiss_source.tree": "f06fbd2b4608e87f7874e67e732bbc444abccba1",
    "canonical_data.lock_id": "CE-V1-CANONICAL-DATA-2026D-SE-V2.10.3BFINAL",
    "canonical_data.revision": 4,
    "canonical_data.lock_sha256": "0309a9d9385925f2c5eda478e2a7704e8600cf10abf258a8bcc9c4bdcb7689a2",
    "canonical_data.aggregate_sha256": "0cfc76a9dc51296f2241492e3376f1e71d13dd4f36b476253d4b82df57dfc990",
    "hardened_runtime_derivative.sha256": "a1f591d64dfd01a0bc86e2bfb2aab300b4b18b5edec2ca9e38a1cbd71c843e29",
}

def get(doc: dict, path: str):
    cur = doc
    for key in path.split("."):
        cur = cur[key]
    return cur

def main() -> int:
    doc = json.loads(GRAPH.read_text(encoding="utf-8"))
    if doc.get("schema_version") != "CE-V1-NATIVE-RUNTIME-AUTHORITY-GRAPH-1":
        raise SystemExit("GRAPH_SCHEMA_MISMATCH")
    if doc.get("status") != "EVIDENCE_BOUND_NON_AUTHORIZED":
        raise SystemExit("GRAPH_STATUS_MISMATCH")
    for path, value in EXPECTED.items():
        if get(doc, path) != value:
            raise SystemExit(f"GRAPH_VALUE_MISMATCH:{path}")
    edges = {(e["from"], e["to"]) for e in doc.get("edges", [])}
    required = {
        ("candidate", "native_runtime_artifact"),
        ("native_runtime_artifact", "swiss_source"),
        ("native_runtime_artifact", "canonical_data"),
        ("native_runtime_artifact", "native_build_provenance"),
        ("native_runtime_artifact", "hardened_runtime_derivative"),
    }
    if edges != required:
        raise SystemExit("GRAPH_EDGE_SET_MISMATCH")
    auth = doc["authorization"]
    if auth != {
        "source_authority": "EVIDENCE_BOUND",
        "trusted_build": "NOT_ESTABLISHED",
        "production_runtime": "NOT_AUTHORIZED",
        "dual_approval": "NOT_ESTABLISHED",
        "seal": "NO",
        "authorization": "NON_AUTHORIZED",
        "fail_closed": True,
    }:
        raise SystemExit("GRAPH_AUTHORIZATION_STATE_MISMATCH")
    print("NATIVE_AUTHORITY_GRAPH_PASS")
    print("GRAPH_SHA256=" + hashlib.sha256(GRAPH.read_bytes()).hexdigest())
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
