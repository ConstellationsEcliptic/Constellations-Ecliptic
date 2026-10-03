from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Sequence


class EphemerisVerificationError(ValueError):
    """Expected native data identity was not established."""


@dataclass(frozen=True)
class DataFileExpectation:
    name: str
    size_bytes: int
    sha256: str


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def verify_data_files(root: Path, expected: Sequence[DataFileExpectation]) -> tuple[Path, ...]:
    verified: list[Path] = []
    for item in expected:
        path = root / item.name
        if not path.is_file():
            raise EphemerisVerificationError(f"missing_data_file:{item.name}")
        if path.stat().st_size != item.size_bytes:
            raise EphemerisVerificationError(
                f"size_mismatch:{item.name}:{path.stat().st_size}!={item.size_bytes}"
            )
        observed = sha256_file(path)
        if observed.lower() != item.sha256.lower():
            raise EphemerisVerificationError(
                f"sha256_mismatch:{item.name}:{observed}!={item.sha256}"
            )
        verified.append(path)
    return tuple(verified)
