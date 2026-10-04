from __future__ import annotations

import argparse

from ce.foundation.source_tree_identity import source_tree_sha256

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifests" / "SOURCE_TREE_SHA256_V2.txt"


def digest() -> str:
    return source_tree_sha256(ROOT)


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
