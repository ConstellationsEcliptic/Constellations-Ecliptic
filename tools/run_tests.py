from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path
sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = os.path.join(ROOT, "src")
if src not in sys.path:
    sys.path.insert(0, src)

def _clean_generated(root: str) -> list[str]:
    base = Path(root)
    leftovers: list[str] = []
    for p in base.rglob("*"):
        rel = p.relative_to(base).as_posix()
        if "__pycache__" in p.parts or p.suffix in {".pyc", ".pyo"}:
            leftovers.append(rel)
    for rel in leftovers:
        p = base / rel
        if p.is_file() or p.is_symlink():
            p.unlink()
    for d in sorted(base.rglob("__pycache__"), reverse=True):
        if d.is_dir():
            try: d.rmdir()
            except OSError: pass
    return leftovers

def main() -> int:
    suite = unittest.defaultTestLoader.discover(os.path.join(ROOT, "tests"))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    _clean_generated(ROOT)
    if any(p.is_dir() and p.name == "__pycache__" for p in Path(ROOT).rglob("*")):
        return 1
    if any(p.is_file() and p.suffix in {".pyc", ".pyo"} for p in Path(ROOT).rglob("*")):
        return 1
    return 0 if result.wasSuccessful() else 1

if __name__ == "__main__":
    raise SystemExit(main())
