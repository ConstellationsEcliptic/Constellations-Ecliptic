from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

EXCLUDED_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    "dist",
    ".mypy_cache",
    ".ruff_cache",
    "evidence",
    "provenance",
}
EXCLUDED_RELATIVE_PATHS = {
    "manifests/SOURCE_TREE_SHA256_V2.txt",
}
ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifests" / "SOURCE_TREE_SHA256_V2.txt"


def iter_files() -> list[Path]:
    files = []
    for p in ROOT.rglob("*"):
        rel = p.relative_to(ROOT)
        if any(part in EXCLUDED_DIRS for part in rel.parts):
            continue
        if p.is_symlink():
            raise RuntimeError(f"SYMLINK_PRESENT: {rel.as_posix()}")
        if not p.is_file() or rel.as_posix() in EXCLUDED_RELATIVE_PATHS:
            continue
        files.append(p)
    return sorted(files, key=lambda p: p.relative_to(ROOT).as_posix().encode())


def digest() -> str:
    h = hashlib.sha256()
    for p in iter_files():
        rel = p.relative_to(ROOT).as_posix().encode()
        data = p.read_bytes()
        mode = p.stat().st_mode & 0o7777
        h.update(
            b"file "
            + str(mode).encode()
            + b" "
            + str(len(data)).encode()
            + b"\n"
            + rel
            + b"\n"
            + data
            + b"\n"
        )
    return h.hexdigest()


def manifest_suffix() -> str:
    if MANIFEST.is_file():
        text = MANIFEST.read_text(encoding="utf-8")
        parts = text.split(maxsplit=1)
        if len(parts) == 2 and parts[1].strip():
            return parts[1].strip()
    return "CE_V1_SOURCE_FOUNDATION_R1"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--write-manifest",
        action="store_true",
        help="rewrite the manifest hash while preserving its existing label",
    )
    args = parser.parse_args()

    actual = digest()
    if args.write_manifest:
        MANIFEST.write_text(
            f"{actual}  {manifest_suffix()}\n",
            encoding="utf-8",
        )
    print(actual)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
