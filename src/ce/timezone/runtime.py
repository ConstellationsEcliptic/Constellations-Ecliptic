from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
from io import BytesIO
from typing import Mapping

from zoneinfo import ZoneInfo


class TzifRuntimeError(ValueError):
    """Timezone runtime cannot establish an authoritative resolution."""


@dataclass(frozen=True)
class TzifFileIdentity:
    path: str
    size_bytes: int
    sha256: str


@dataclass(frozen=True)
class TzifBundleIdentity:
    version: str
    files: tuple[TzifFileIdentity, ...]
    manifest_sha256: str


def compute_manifest_sha256(files: Mapping[str, bytes]) -> str:
    """Canonical identity over TZif path, size and bytes, independent of file mode."""

    digest = sha256()
    for path in sorted(files):
        encoded_path = path.encode("utf-8")
        data = files[path]
        per_file = sha256(data).hexdigest().encode("ascii")
        digest.update(len(encoded_path).to_bytes(4, "big"))
        digest.update(encoded_path)
        digest.update(len(data).to_bytes(8, "big"))
        digest.update(per_file)
    return digest.hexdigest()


class TzifRuntime:
    """Resolve local civil time exclusively from an injected TZif byte map."""

    def __init__(
        self,
        *,
        version: str,
        files: Mapping[str, bytes],
        expected_manifest_sha256: str | None,
    ) -> None:
        self.version = version
        self._files = dict(files)
        self._manifest_sha256 = compute_manifest_sha256(self._files)
        self._expected_manifest_sha256 = expected_manifest_sha256

    @property
    def identity(self) -> TzifBundleIdentity:
        entries = tuple(
            TzifFileIdentity(
                path=path,
                size_bytes=len(self._files[path]),
                sha256=sha256(self._files[path]).hexdigest(),
            )
            for path in sorted(self._files)
        )
        return TzifBundleIdentity(self.version, entries, self._manifest_sha256)

    def _zone(self, timezone_id: str) -> ZoneInfo:
        if self._expected_manifest_sha256 is None:
            raise TzifRuntimeError("tzif_bundle_identity_not_established")
        if self._manifest_sha256 != self._expected_manifest_sha256:
            raise TzifRuntimeError("tzif_bundle_identity_mismatch")
        data = self._files.get(timezone_id)
        if data is None:
            raise TzifRuntimeError(f"tzif_zone_missing:{timezone_id}")
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
        if (
            len(candidates) == 2
            and candidates[0].utcoffset() != candidates[1].utcoffset()
        ):
            raise TzifRuntimeError("ambiguous_local_time")
        return candidates[0].astimezone(timezone.utc)

    def resolve_local_interval(self, local_start: datetime, local_end: datetime, timezone_id: str) -> tuple[datetime, datetime]:
        if local_end <= local_start:
            raise TzifRuntimeError("local_interval_order_invalid")
        return (
            self.resolve_local_instant(local_start, timezone_id),
            self.resolve_local_instant(local_end, timezone_id),
        )
