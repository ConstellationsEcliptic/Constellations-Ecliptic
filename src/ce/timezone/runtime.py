from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
import json
from io import BytesIO
from pathlib import Path
from typing import Mapping

from zoneinfo import ZoneInfo


CANONICAL_IANA_VERSION = "2026d"
CANONICAL_RUNTIME_MANIFEST_SHA256 = "a12881024bee3b801d63b0d9cb74118b6329512f63020f36c42412de1e0a6205"
CANONICAL_VALIDATION_METADATA_SHA256 = "4f4699f51f52470937006e359612c099a15a72ea0f9eb2c0fd7876ad546e58bf"
CANONICAL_SOURCE_ARCHIVE_SHA256 = "0cb2aa8e333c3dc049badc42a0c61f21987b8cd44e107fa900bad764aacc7767"
CANONICAL_TZIF_ENTRY_COUNT = 597
CANONICAL_MANIFEST_ALGORITHM = "SHA256_UTF8_LF_JOIN_SORTED_PATH_HASH"


class TzifRuntimeError(ValueError):
    """Timezone runtime cannot establish an authoritative resolution."""


@dataclass(frozen=True)
class TzifManifestIdentity:
    manifest_sha256: str
    declared_source_manifest_sha256: str | None
    entry_count: int
    algorithm: str


@dataclass(frozen=True)
class TzifFileIdentity:
    path: str
    size_bytes: int
    sha256: str


@dataclass(frozen=True)
class TzifBundleIdentity:
    version: str
    manifest: TzifManifestIdentity
    files: tuple[TzifFileIdentity, ...]


def sha256_bytes(data: bytes) -> str:
    return sha256(data).hexdigest()


def _validate_rel_path(value: object) -> str:
    if not isinstance(value, str) or not value or value.startswith(("/", "\\")):
        raise TzifRuntimeError("tzif_manifest_path_invalid")
    path = value.replace("\\", "/")
    if path.startswith("../") or "/../" in path or path == "..":
        raise TzifRuntimeError("tzif_manifest_path_traversal")
    return path


def verify_tzif_manifest_file(
    manifest_path: Path,
    tzif_root: Path,
    *,
    expected_manifest_sha256: str = CANONICAL_RUNTIME_MANIFEST_SHA256,
    expected_entry_count: int = CANONICAL_TZIF_ENTRY_COUNT,
) -> TzifBundleIdentity:
    if manifest_path.is_symlink() or not manifest_path.is_file():
        raise TzifRuntimeError("tzif_manifest_missing_or_nonregular")
    if tzif_root.is_symlink() or not tzif_root.is_dir():
        raise TzifRuntimeError("tzif_root_missing_or_nonregular")

    raw = manifest_path.read_bytes()
    observed_manifest_sha256 = sha256_bytes(raw)
    if observed_manifest_sha256.lower() != expected_manifest_sha256.lower():
        raise TzifRuntimeError("tzif_manifest_sha256_mismatch")

    try:
        manifest = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise TzifRuntimeError("tzif_manifest_parse_failed") from exc

    if manifest.get("algorithm") != CANONICAL_MANIFEST_ALGORITHM:
        raise TzifRuntimeError("tzif_manifest_algorithm_mismatch")

    entries = manifest.get("entries")
    if not isinstance(entries, list) or len(entries) != expected_entry_count:
        raise TzifRuntimeError("tzif_manifest_entry_count_mismatch")

    expected: dict[str, tuple[int, str]] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            raise TzifRuntimeError("tzif_manifest_entry_invalid")
        rel = _validate_rel_path(entry.get("path"))
        size = entry.get("size")
        digest = entry.get("sha256")
        if type(size) is not int or size < 0:
            raise TzifRuntimeError("tzif_manifest_size_invalid")
        if not isinstance(digest, str) or len(digest) != 64:
            raise TzifRuntimeError("tzif_manifest_sha256_invalid")
        key = rel.casefold()
        if key in expected:
            raise TzifRuntimeError("tzif_manifest_duplicate_path")
        expected[key] = (size, digest.lower())

    actual_files: dict[str, Path] = {}
    for path in tzif_root.rglob("*"):
        if path.is_symlink():
            raise TzifRuntimeError("tzif_root_contains_symlink")
        if not path.is_file():
            continue
        rel = path.relative_to(tzif_root).as_posix()
        key = rel.casefold()
        if key in actual_files:
            raise TzifRuntimeError("tzif_filesystem_duplicate_path")
        actual_files[key] = path

    if len(actual_files) != expected_entry_count:
        raise TzifRuntimeError("tzif_filesystem_entry_count_mismatch")
    if set(actual_files) != set(expected):
        missing = sorted(set(expected) - set(actual_files))
        extra = sorted(set(actual_files) - set(expected))
        raise TzifRuntimeError(
            f"tzif_manifest_fileset_mismatch:missing={missing}:extra={extra}"
        )

    identities: list[TzifFileIdentity] = []
    for key in sorted(expected):
        size, digest = expected[key]
        path = actual_files[key]
        if path.stat().st_size != size:
            raise TzifRuntimeError(f"tzif_file_size_mismatch:{path}")
        observed = sha256_bytes(path.read_bytes())
        if observed != digest:
            raise TzifRuntimeError(f"tzif_file_sha256_mismatch:{path}")
        identities.append(
            TzifFileIdentity(
                path=path.relative_to(tzif_root).as_posix(),
                size_bytes=size,
                sha256=observed,
            )
        )

    declared_source_manifest_sha256 = manifest.get("manifest_sha256")
    if declared_source_manifest_sha256 is not None and not (
        isinstance(declared_source_manifest_sha256, str)
        and len(declared_source_manifest_sha256) == 64
    ):
        raise TzifRuntimeError("tzif_manifest_declared_source_hash_invalid")

    return TzifBundleIdentity(
        version=CANONICAL_IANA_VERSION,
        manifest=TzifManifestIdentity(
            manifest_sha256=observed_manifest_sha256,
            declared_source_manifest_sha256=declared_source_manifest_sha256,
            entry_count=len(identities),
            algorithm=CANONICAL_MANIFEST_ALGORITHM,
        ),
        files=tuple(identities),
    )


class TzifRuntime:
    """Resolve civil time only from an exact policy-owned TZif package."""

    def __init__(
        self,
        *,
        version: str,
        files: Mapping[str, bytes],
        expected_manifest_sha256: str | None,
    ) -> None:
        if version != CANONICAL_IANA_VERSION:
            raise TzifRuntimeError("tzif_version_mismatch")
        self.version = version
        self._files = dict(files)
        self._manifest_sha256 = self._content_identity()
        if expected_manifest_sha256 is None:
            raise TzifRuntimeError("tzif_bundle_identity_not_established")
        if self._manifest_sha256 != expected_manifest_sha256.lower():
            raise TzifRuntimeError("tzif_bundle_identity_mismatch")
        self._package_tzif_root: Path | None = None
        self._identity = TzifBundleIdentity(
            version=version,
            manifest=TzifManifestIdentity(
                manifest_sha256=expected_manifest_sha256.lower(),
                declared_source_manifest_sha256=None,
                entry_count=len(self._files),
                algorithm="INJECTED_TEST_FIXTURE",
            ),
            files=tuple(
                TzifFileIdentity(
                    path=path,
                    size_bytes=len(data),
                    sha256=sha256_bytes(data),
                )
                for path, data in sorted(self._files.items())
            ),
        )

    def _content_identity(self) -> str:
        digest = sha256()
        for path in sorted(self._files):
            encoded = path.encode("utf-8")
            data = self._files[path]
            digest.update(len(encoded).to_bytes(4, "big"))
            digest.update(encoded)
            digest.update(len(data).to_bytes(8, "big"))
            digest.update(sha256(data).digest())
        return digest.hexdigest()

    @classmethod
    def from_package_root(
        cls,
        *,
        package_root: Path,
        expected_manifest_sha256: str = CANONICAL_RUNTIME_MANIFEST_SHA256,
        expected_version: str = CANONICAL_IANA_VERSION,
        expected_entry_count: int = CANONICAL_TZIF_ENTRY_COUNT,
    ) -> tuple["TzifRuntime", TzifBundleIdentity]:
        if expected_version != CANONICAL_IANA_VERSION:
            raise TzifRuntimeError("tzif_version_mismatch")
        manifest_path = package_root / "metadata" / "runtime-tzif-manifest.json"
        tzif_root = package_root / "tzif"
        identity = verify_tzif_manifest_file(
            manifest_path,
            tzif_root,
            expected_manifest_sha256=expected_manifest_sha256,
            expected_entry_count=expected_entry_count,
        )
        runtime = cls.__new__(cls)
        runtime.version = expected_version
        runtime._files = {}
        runtime._manifest_sha256 = identity.manifest.manifest_sha256
        runtime._identity = identity
        runtime._package_tzif_root = tzif_root.resolve()
        return runtime, identity

    @property
    def identity(self) -> TzifBundleIdentity:
        return self._identity

    def _zone(self, timezone_id: str) -> ZoneInfo:
        if not timezone_id or timezone_id.startswith(("/", "\\")) or ".." in Path(timezone_id).parts:
            raise TzifRuntimeError("tzif_zone_id_invalid")

        if self._files:
            data = self._files.get(timezone_id)
            if data is None:
                raise TzifRuntimeError(f"tzif_zone_missing:{timezone_id}")
        else:
            root = getattr(self, "_package_tzif_root", None)
            if root is None:
                raise TzifRuntimeError("tzif_runtime_identity_missing")
            candidate = (root / timezone_id).resolve()
            if root != candidate and root not in candidate.parents:
                raise TzifRuntimeError("tzif_zone_path_escape")
            expected_by_path = {item.path.casefold(): item for item in self._identity.files}
            expected = expected_by_path.get(Path(timezone_id).as_posix().casefold())
            if expected is None:
                raise TzifRuntimeError(f"tzif_zone_missing:{timezone_id}")
            if candidate.is_symlink() or not candidate.is_file():
                raise TzifRuntimeError(f"tzif_zone_nonregular:{timezone_id}")
            data = candidate.read_bytes()
            if len(data) != expected.size_bytes:
                raise TzifRuntimeError(f"tzif_zone_size_mismatch:{timezone_id}")
            observed = sha256_bytes(data)
            if observed != expected.sha256:
                raise TzifRuntimeError(f"tzif_zone_sha256_mismatch:{timezone_id}")

        try:
            return ZoneInfo.from_file(BytesIO(data), key=timezone_id)
        except Exception as exc:
            raise TzifRuntimeError(f"tzif_parse_failed:{timezone_id}") from exc

    def resolve_local_instant(self, local_naive: datetime, timezone_id: str) -> datetime:
        if local_naive.tzinfo is not None:
            raise TzifRuntimeError("local_datetime_must_be_naive")
        zone = self._zone(timezone_id)
        candidates = []
        for fold in (0, 1):
            aware = local_naive.replace(tzinfo=zone, fold=fold)
            roundtrip = aware.astimezone(timezone.utc).astimezone(zone).replace(tzinfo=None)
            if roundtrip == local_naive:
                candidates.append(aware)

        if not candidates:
            raise TzifRuntimeError("nonexistent_local_time")
        if len(candidates) == 2 and candidates[0].utcoffset() != candidates[1].utcoffset():
            raise TzifRuntimeError("ambiguous_local_time")
        return candidates[0].astimezone(timezone.utc)
