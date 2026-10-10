from __future__ import annotations

from hashlib import sha256
from pathlib import Path
from typing import Iterable


DEFAULT_INCLUDE_ROOTS = (".github",)
DEFAULT_INCLUDE_FILES = ("CHANGE_CONTROL.md",)
DEFAULT_EXCLUDES = frozenset({".git", "__pycache__", ".pytest_cache"})
IDENTITY_EXCLUDED_PATHS = frozenset()


def control_plane_sha256(
    root: Path,
    *,
    include_roots: Iterable[str] = DEFAULT_INCLUDE_ROOTS,
    include_files: Iterable[str] = DEFAULT_INCLUDE_FILES,
) -> str:
    """Hash repository-controlled governance/control-plane bytes.

    This identity is intentionally separate from source-tree identity. It
    covers workflow/governance bytes that may affect build or release control
    without redefining the numerical source identity.
    """
    root = root.resolve()
    records: list[tuple[str, int, bytes]] = []

    for include_file in include_files:
        path = root / include_file
        if path.is_file() and not path.is_symlink():
            relative = path.relative_to(root).as_posix()
            if relative not in IDENTITY_EXCLUDED_PATHS:
                data = path.read_bytes()
                records.append((relative, len(data), data))

    for include_root in include_roots:
        base = root / include_root
        if not base.exists() or base.is_symlink():
            continue
        for path in base.rglob("*"):
            if not path.is_file() or path.is_symlink():
                continue
            relative = path.relative_to(root).as_posix()
            if relative in IDENTITY_EXCLUDED_PATHS:
                continue
            if any(part in DEFAULT_EXCLUDES for part in path.parts):
                continue
            data = path.read_bytes()
            records.append((relative, len(data), data))

    if not records:
        raise ValueError("control_plane_has_no_identity_bearing_files")

    digest = sha256()
    for relative, size, data in sorted(records, key=lambda item: item[0].encode("utf-8")):
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(str(size).encode("ascii"))
        digest.update(b"\0")
        digest.update(sha256(data).digest())
        digest.update(b"\n")
    return digest.hexdigest()
