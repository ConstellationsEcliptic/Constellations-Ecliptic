from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "pyproject.toml",
    "README.md",
    "src/ce/__init__.py",
    "src/ce/calculation/contracts.py",
    "src/ce/calculation/engine.py",
    "src/ce/calculation/evidence.py",
    "src/ce/calculation/geometry.py",
    "src/ce/ephemeris/adapter.py",
    "src/ce/runtime/gates.py",
    "tests/test_geometry.py",
    "tests/test_serialization.py",
    "tests/test_runtime_gate.py",
    "tests/test_evidence.py",
    "tests/test_no_commercial_dependency.py",
    "build/build-definition.json",
    "build/dependency-lock.txt",
]

def fail(msg: str) -> None:
    raise SystemExit(f"FOUNDATION_FAIL: {msg}")

def main() -> int:
    for rel in REQUIRED:
        if not (ROOT / rel).is_file():
            fail(f"missing required file: {rel}")
    for p in ROOT.rglob("*"):
        rel=p.relative_to(ROOT)
        if p.is_symlink(): fail(f"symlink present: {rel}")
        if any(part in {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", "dist"} for part in rel.parts): fail(f"generated/cache path present: {rel}")
        if p.suffix in {".pyc",".pyo",".tmp"}: fail(f"generated file present: {rel}")
    cp=subprocess.run([sys.executable,"-B",str(ROOT/"tools/run_tests.py")],cwd=ROOT,env={**os.environ,"PYTHONDONTWRITEBYTECODE":"1","PYTHONNOUSERSITE":"1"},text=True)
    if cp.returncode != 0: fail("test runner returned non-zero")
    data=json.loads((ROOT/"manifests/implementation_manifest.json").read_text(encoding="utf-8"))
    if data.get("status") != "DEVELOPMENT_CANDIDATE": fail("implementation status changed unexpectedly")
    if data.get("production_source_authority") != "NOT_ESTABLISHED": fail("production authority must remain NOT_ESTABLISHED")
    print("FOUNDATION_PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
