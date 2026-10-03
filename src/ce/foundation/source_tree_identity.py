from __future__ import annotations

from hashlib import sha256
from pathlib import Path
from typing import Iterable


DEFAULT_EXCLUDES = frozenset({".git", "__pycache__", ".pytest_cache"})


def source_tree_sha256(
    root: Path,
    *,
    include_roots: Iterable[str] = ("configs", "src", "tests", "schemas", "profiles", "manifests", "build", "tools"),
    include_files: Iterable[str] = ("pyproject.toml",),
) -> str:
    """Hash source content and canonical relative paths, never filesystem mode bits."""

    root = root.resolve()
    records: list[tuple[str, int, bytes]] = []

    for include_file in sorted(include_files):
        path = root / include_file
        if path.is_file():
            records.append((path.relative_to(root).as_posix(), path.stat().st_size, path.read_bytes()))

    for include_root in include_roots:
        base = root / include_root
        if not base.exists():
            continue
        for path in sorted(base.rglob("*")):
            if not path.is_file():
                continue
            if any(part in DEFAULT_EXCLUDES for part in path.parts):
                continue
            relative = path.relative_to(root).as_posix()
            data = path.read_bytes()
            records.append((relative, len(data), data))

    digest = sha256()
    for relative, size, data in records:
        path_bytes = relative.encode("utf-8")
        digest.update(len(path_bytes).to_bytes(4, "big"))
        digest.update(path_bytes)
        digest.update(size.to_bytes(8, "big"))
        digest.update(data)
    return digest.hexdigest()
