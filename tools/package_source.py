from __future__ import annotations

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT.parent / "CE_V1_SOURCE_FOUNDATION_R1_FINAL.zip"
EXCLUDED_DIRS = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", "dist"}
EXCLUDED_NAMES = {OUT.name, "SHA256SUMS.txt", "PACKAGE_ARTIFACT_MANIFEST.txt"}
DETERMINISTIC_FILE_MODE = 0o100644


def files() -> list[Path]:
    out = []
    for p in ROOT.rglob("*"):
        rel = p.relative_to(ROOT)
        if any(x in EXCLUDED_DIRS for x in rel.parts):
            continue
        if p.is_symlink():
            raise RuntimeError(f"SYMLINK_PRESENT:{rel.as_posix()}")
        if p.is_file() and p.name not in EXCLUDED_NAMES:
            out.append(p)
    return sorted(out, key=lambda x: x.relative_to(ROOT).as_posix().encode())


def add(z: ZipFile, p: Path, *, root: Path = ROOT) -> None:
    rel = p.relative_to(root).as_posix()
    data = p.read_bytes()
    zi = ZipInfo(rel, (2026, 1, 1, 0, 0, 0))
    zi.compress_type = ZIP_DEFLATED
    zi.create_system = 3
    zi.external_attr = (DETERMINISTIC_FILE_MODE << 16)
    zi.flag_bits = 0x800
    z.writestr(zi, data)


if __name__ == "__main__":
    with ZipFile(OUT, "w", compression=ZIP_DEFLATED, compresslevel=9, allowZip64=True) as z:
        for p in files():
            add(z, p)
    print(OUT)
