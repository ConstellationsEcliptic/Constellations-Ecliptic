from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "provenance" / "rev4_oracle_qualification_candidate_r2.json"

EXPECTED_IDS = frozenset({
    "GEO-01","GEO-02","KIN-01","KIN-02","KIN-03","KIN-04","ORB-01","ORB-02","STA-01",
    "WIN-01","WIN-02","WIN-03","UNC-01","UNC-02","UNC-03","UNC-04",
    "EPH-01","EPH-02","ERR-01","ERR-02","ERR-03","ERR-04","ERR-05","ERR-06",
    "TIME-01","TIME-02","TIME-03","INT-01",
})

class OracleQualificationError(ValueError):
    pass

def _git(*args: str) -> str:
    p = subprocess.run(["git", *args], cwd=ROOT, check=False, capture_output=True, text=True)
    if p.returncode:
        raise OracleQualificationError(f"git_command_failed:{' '.join(args)}:{p.stderr.strip()}")
    return p.stdout.strip()

def _sha(value: Any, length: int, field: str) -> None:
    if not isinstance(value, str) or len(value) != length or any(ch.lower() not in "0123456789abcdef" for ch in value):
        raise OracleQualificationError(f"{field}_invalid")

def _load() -> dict[str, Any]:
    if MANIFEST.is_symlink() or not MANIFEST.is_file():
        raise OracleQualificationError("manifest_missing_or_nonregular")
    raw = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise OracleQualificationError("manifest_top_level_mapping_required")
    return raw

def _check_ancestry(base_commit: str) -> None:
    current = _git("rev-parse", "HEAD")
    p = subprocess.run(
        ["git","merge-base","--is-ancestor",base_commit,current],
        cwd=ROOT, check=False, capture_output=True, text=True,
    )
    if p.returncode:
        raise OracleQualificationError(f"base_candidate_not_ancestor:base={base_commit}:head={current}")

def validate() -> None:
    m = _load()
    if m.get("status") != "CANDIDATE_NON_AUTHORITY":
        raise OracleQualificationError("manifest_status_not_non_authority")
    qs = m.get("qualification_state")
    if not isinstance(qs, dict) or qs.get("current_oracle_authority") != "NOT_ESTABLISHED" or qs.get("fail_closed") is not True:
        raise OracleQualificationError("qualification_state_not_fail_closed_non_authority")

    gov = m.get("governance")
    expected_gov = {
        "source_authority":"NOT_ESTABLISHED","trusted_build":"NOT_ESTABLISHED",
        "runtime_adoption":"NOT_ESTABLISHED","full_runtime_coverage":"NOT_ESTABLISHED",
        "tzif_runtime_identity":"NOT_ESTABLISHED","production_runtime":"NOT_AUTHORIZED",
        "dual_approval":"NOT_ESTABLISHED","seal":"NO","authorization":"NON_AUTHORIZED","fail_closed":True,
    }
    if not isinstance(gov, dict) or any(gov.get(k) != v for k,v in expected_gov.items()):
        raise OracleQualificationError("governance_mismatch")

    basis = m.get("basis")
    if not isinstance(basis, dict):
        raise OracleQualificationError("basis_missing")
    _sha(basis.get("base_candidate_head"),40,"base_candidate_head")
    _sha(basis.get("base_candidate_tree_sha256"),64,"base_candidate_tree_sha256")
    _sha(basis.get("base_source_tree_identity"),64,"base_source_tree_identity")
    _check_ancestry(basis["base_candidate_head"])

    reg = m.get("normative_register")
    if not isinstance(reg, dict):
        raise OracleQualificationError("normative_register_missing")
    _sha(reg.get("sha256"),64,"normative_register_sha256")

    bindings = m.get("test_bindings")
    if not isinstance(bindings, list):
        raise OracleQualificationError("test_bindings_missing")

    seen = []
    for row in bindings:
        if not isinstance(row, list) or len(row) != 4:
            raise OracleQualificationError("binding_shape_invalid")
        test_id, rel_path, method, expected_blob = row
        if test_id not in EXPECTED_IDS:
            raise OracleQualificationError(f"unknown_test_id:{test_id}")
        if not isinstance(rel_path, str) or rel_path.startswith("/"):
            raise OracleQualificationError(f"test_path_invalid:{test_id}")
        _sha(expected_blob,40,f"binding_blob_sha:{test_id}")
        path = ROOT / rel_path
        if path.is_symlink() or not path.is_file():
            raise OracleQualificationError(f"test_file_missing_or_nonregular:{test_id}")
        actual_blob = _git("hash-object","--",rel_path)
        if actual_blob != expected_blob:
            raise OracleQualificationError(f"test_file_blob_mismatch:{test_id}:expected={expected_blob}:actual={actual_blob}")
        if not isinstance(method, str) or "." not in method:
            raise OracleQualificationError(f"test_method_invalid:{test_id}")
        name = method.rsplit(".",1)[1]
        if f"def {name}(" not in path.read_text(encoding="utf-8"):
            raise OracleQualificationError(f"test_method_not_found:{test_id}:{method}")
        seen.append(test_id)

    if frozenset(seen) != EXPECTED_IDS:
        raise OracleQualificationError(f"coverage_id_set_mismatch:missing={sorted(EXPECTED_IDS-set(seen))}:extra={sorted(set(seen)-EXPECTED_IDS)}")

    serialized = json.dumps(m, sort_keys=True).upper()
    if "B7" in serialized and ("HISTORICAL_SUPPORTING_EVIDENCE_ONLY" not in serialized or "NOT_ESTABLISHED" not in serialized):
        raise OracleQualificationError("historical_b7_context_missing")

    print("ORACLE_QUALIFICATION_MANIFEST_VALID PASS")
    print(f"REQUIRED_IDS={len(EXPECTED_IDS)}")
    print(f"BINDING_ROWS={len(bindings)}")
    print(f"UNIQUE_IDS={len(set(seen))}")

if __name__ == "__main__":
    validate()
