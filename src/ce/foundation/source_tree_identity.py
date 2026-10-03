from __future__ import annotations

from hashlib import sha256
from pathlib import Path
from typing import Iterable


DEFAULT_EXCLUDES = frozenset({".git", "__pycache__", ".pytest_cache"})
IDENTITY_EXCLUDED_PATHS = frozenset({
    "manifests/SOURCE_TREE_SHA256_V2.txt",
})


def source_tree_sha256(
    root: Path,
    *,
    include_roots: Iterable[str] = (
        "configs",
        "src",
        "tests",
        "schemas",
        "profiles",
        "manifests",
        "build",
        "tools",
    ),
    include_files: Iterable[str] = ("pyproject.toml",),
) -> str:
    """Hash identity-bearing bytes and canonical relative paths.

    The published source-tree digest manifest is excluded because including a
    file that records the digest would create a self-referential identity.
    Filesystem metadata/mode bits are deliberately not identity-bearing.
    """

    root = root.resolve()
    records: list[tuple[str, int, bytes]] = []

    for include_file in include_files:
        path = root / include_file
        if path.is_file():
            relative = path.relative_to(root).as_posix()
            if relative not in IDENTITY_EXCLUDED_PATHS:
                records.append((relative, path.stat().st_size, path.read_bytes()))

    for include_root in include_roots:
        base = root / include_root
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file():
                continue
            relative = path.relative_to(root).as_posix()
            if relative in IDENTITY_EXCLUDED_PATHS:
                continue
            if any(part in DEFAULT_EXCLUDES for part in path.parts):
                continue
            records.append((relative, path.stat().st_size, path.read_bytes()))

    digest = sha256()
    for relative, size, data in sorted(records, key=lambda item: item[0].encode("utf-8")):
        path_bytes = relative.encode("utf-8")
        digest.update(path_bytes)
        digest.update(b"\0")
        digest.update(str(size).encode("ascii"))
        digest.update(b"\0")
        digest.update(sha256(data).digest())
        digest.update(b"\n")
    return digest.hexdigest()
