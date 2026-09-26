from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_ARTIFACT_ID = "CE-V1-SOURCE-FOUNDATION-R1"
EXPECTED_SOURCE_LABEL = "CE_V1_SOURCE_FOUNDATION_R1"
EXPECTED_PROFILE_ID = "CE-CALC-V1-EP-001"
EXPECTED_PROFILE_REVISION = 2

REQUIRED = [
    "pyproject.toml",
    "README.md",
    "src/ce/__init__.py",
    "src/ce/calculation/contracts.py",
    "src/ce/calculation/engine.py",
    "src/ce/calculation/evidence.py",
    "src/ce/calculation/geometry.py",
    "src/ce/calculation/time.py",
    "src/ce/ephemeris/adapter.py",
    "src/ce/runtime/gates.py",
    "src/ce/signal/engine.py",
    "tests/test_geometry.py",
    "tests/test_serialization.py",
    "tests/test_runtime_gate.py",
    "tests/test_evidence.py",
    "tests/test_no_commercial_dependency.py",
    "tests/test_contract_state_integrity.py",
    "tests/test_schema_contracts.py",
    "build/build-definition.json",
    "build/dependency-lock.txt",
    "manifests/SOURCE_TREE_SHA256_V2.txt",
    "manifests/implementation_manifest.json",
    "schemas/calculation_result.schema.json",
    "schemas/evidence_packet.schema.json",
    "schemas/signal_result.schema.json",
]


def fail(msg: str) -> None:
    raise SystemExit(f"FOUNDATION_FAIL: {msg}")


def run_checked(script: str) -> None:
    cp = subprocess.run(
        [sys.executable, "-B", str(ROOT / script)],
        cwd=ROOT,
        env={
            **os.environ,
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONNOUSERSITE": "1",
        },
        text=True,
    )
    if cp.returncode != 0:
        fail(f"{script} returned non-zero")


def main() -> int:
    for rel in REQUIRED:
        if not (ROOT / rel).is_file():
            fail(f"missing required file: {rel}")

    run_checked("build/check_build_inputs.py")
    run_checked("tools/verify_source_identity.py")
    run_checked("tools/run_tests.py")
    run_checked("build/check_build_inputs.py")

    for schema_name in (
        "calculation_result.schema.json",
        "evidence_packet.schema.json",
        "signal_result.schema.json",
    ):
        try:
            json.loads((ROOT / "schemas" / schema_name).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            fail(f"invalid schema JSON: {schema_name}: {exc}")

    data = json.loads(
        (ROOT / "manifests/implementation_manifest.json").read_text(encoding="utf-8")
    )
    expected = {
        "artifact_id": EXPECTED_ARTIFACT_ID,
        "version": "0.1.0",
        "status": "DEVELOPMENT_CANDIDATE",
        "authority": "NON_AUTHORITATIVE",
        "production_source_authority": "NOT_ESTABLISHED",
        "trusted_build": "BLOCKED",
        "seal": "NO",
        "authorization": "NON_AUTHORIZED",
        "fail_closed": True,
        "canonical_profile_id": EXPECTED_PROFILE_ID,
        "canonical_profile_revision": EXPECTED_PROFILE_REVISION,
    }
    for key, value in expected.items():
        if data.get(key) != value:
            fail(f"manifest invariant mismatch: {key}")

    identity_fields = (
        (ROOT / "manifests/SOURCE_TREE_SHA256_V2.txt")
        .read_text(encoding="utf-8")
        .strip()
        .split()
    )
    if len(identity_fields) != 2 or identity_fields[1] != EXPECTED_SOURCE_LABEL:
        fail("source identity label mismatch")

    print("FOUNDATION_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
