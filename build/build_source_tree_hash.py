from __future__ import annotations

import hashlib
from pathlib import Path

EXCLUDED_DIRS = {".git", "__pycache__", ".pytest_cache", "dist", ".mypy_cache", ".ruff_cache", "evidence", "provenance"}
EXCLUDED_NAMES = {"SOURCE_TREE_SHA256_V2.txt"}
ROOT = Path(__file__).resolve().parents[1]

def iter_files() -> list[Path]:
    files=[]
    for p in ROOT.rglob("*"):
        rel=p.relative_to(ROOT)
        if any(part in EXCLUDED_DIRS for part in rel.parts): continue
        if p.is_symlink(): raise RuntimeError(f"SYMLINK_PRESENT: {rel.as_posix()}")
        if not p.is_file() or p.name in EXCLUDED_NAMES: continue
        files.append(p)
    return sorted(files,key=lambda p:p.relative_to(ROOT).as_posix().encode())

def digest() -> str:
    h=hashlib.sha256()
    for p in iter_files():
        rel=p.relative_to(ROOT).as_posix().encode(); data=p.read_bytes(); mode=p.stat().st_mode & 0o7777
        h.update(b"file "+str(mode).encode()+b" "+str(len(data)).encode()+b"\n"+rel+b"\n"+data+b"\n")
    return h.hexdigest()

if __name__ == "__main__":
    out=ROOT/"manifests"/"SOURCE_TREE_SHA256_V2.txt"; out.write_text(digest()+"  CE_V1_SOURCE_FOUNDATION_R1\n",encoding="utf-8"); print(digest())
