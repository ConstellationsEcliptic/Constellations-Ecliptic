from __future__ import annotations

from hashlib import sha256
from pathlib import Path
import sys
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from build.build_source_tree_hash import (  # noqa: E402
    EXCLUDED_DIRS,
    EXCLUDED_NAMES as SOURCE_EXCLUDED_NAMES,
    digest as source_tree_digest,
    iter_files as source_tree_files,
)

OUT = ROOT.parent / "CE_V1_SOURCE_FOUNDATION_R1_FINAL.zip"
EXCLUDED_NAMES = set(SOURCE_EXCLUDED_NAMES) | {OUT.name}
DETERMINISTIC_FILE_MODE = 0o100644
PACKAGE_COMMENT_PREFIX = "CE_SOURCE_TREE_SHA256_V2="


def files() -> list[Path]:
    return list(source_tree_files())


def add(z: ZipFile, p: Path, *, root: Path = ROOT) -> None:
    rel = p.relative_to(root).as_posix()
    data = p.read_bytes()
    zi = ZipInfo(rel, (2026, 1, 1, 0, 0, 0))
    zi.compress_type = ZIP_DEFLATED
    zi.create_system = 3
    zi.external_attr = (DETERMINISTIC_FILE_MODE << 16)
    zi.flag_bits = 0x800
    z.writestr(zi, data)


def build_archive(output: Path = OUT) -> Path:
    tree_identity = source_tree_digest()
    with ZipFile(
        output,
        "w",
        compression=ZIP_DEFLATED,
        compresslevel=9,
        allowZip64=True,
    ) as z:
        for p in files():
            add(z, p)
        z.comment = f"{PACKAGE_COMMENT_PREFIX}{tree_identity}\n".encode("ascii")
    return output


def package_artifact_sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def package_identity(path: Path) -> dict[str, str]:
    with ZipFile(path, "r") as z:
        comment = z.comment.decode("ascii")

    prefix = PACKAGE_COMMENT_PREFIX
    if not comment.startswith(prefix) or not comment.endswith("\\n"):
        raise ValueError("package_source_identity_comment_invalid")

    return {
        "source_tree_sha256_v2": comment[len(prefix):-1],
        "package_artifact_sha256": package_artifact_sha256(path),
    }


if __name__ == "__main__":
    output = build_archive()
    identity = package_identity(output)
    print(output)
    print(f"SOURCE_TREE_SHA256_V2={identity['source_tree_sha256_v2']}")
    print(f"PACKAGE_ARTIFACT_SHA256={identity['package_artifact_sha256']}")
