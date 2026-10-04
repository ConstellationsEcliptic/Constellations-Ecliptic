from __future__ import annotations

import ctypes
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any

from ce.calculation.contracts import ObjectRecord
from ce.calculation.registry import EXPECTED_OBJECTS
from ce.foundation.status import CalculationStatus


SEFLG_SWIEPH = 2
SEFLG_SPEED = 256
CANONICAL_SWISS_RUNTIME_VERSION = "2.10.03"
CANONICAL_SWISS_RELEASE = "v2.10.3bfinal"
CANONICAL_SWISS_SOURCE_COMMIT = "f4dcd18e8005dde95fd8a8d2312ed12f9accd1b0"

CANONICAL_SWISS_FILES = {
    "seas_18.se1": {
        "size_bytes": 223004,
        "sha256": "a2cd8fc33807c78ca9a700c91c2e042258b12fc4796519e00781440b5ad8b2e2",
        "git_blob_sha1": "8f900cab7e557e4c41f758a6bf3a3c3967e7e3db",
    },
    "semo_18.se1": {
        "size_bytes": 1304771,
        "sha256": "1ca07bd67c24374d77226180c20a4f9996cba013697894810518e7eb582ca4f7",
        "git_blob_sha1": "5427d9f885fd6cb9489584ade37e52c6abb4d407",
    },
    "sepl_18.se1": {
        "size_bytes": 484061,
        "sha256": "ca1393ceab3a44fbc895887cf789c68819ae6a1cbc9b22225872dbe4ccd99a66",
        "git_blob_sha1": "786702cd04506371ee6223af1ebac02d54c848b8",
    },
}
CANONICAL_SWISS_BUNDLE_SHA256 = "0cfc76a9dc51296f2241492e3376f1e71d13dd4f36b476253d4b82df57dfc990"
CANDIDATE_NATIVE_DLL_SHA256 = "04aedc75191ce7d257a20d6141ab889073a1cb6a501ecad98faa6305b24861f2"


class NativeRuntimeError(RuntimeError):
    """Native runtime boundary failure; never silently downgraded."""


@dataclass(frozen=True)
class NativeSwissCalculation:
    object_id: str
    swiss_object_id: int
    jd_ut: float
    longitude_deg: float
    latitude_deg: float
    distance_au: float
    speed_deg_per_day: float | None
    requested_flags: int
    actual_flags: int
    ephemeris: str
    warning_or_error: str | None

    def to_object_record(self) -> ObjectRecord:
        return ObjectRecord(
            object_id=self.object_id,
            object_status=CalculationStatus.VALID,
            requested_flags=self.requested_flags,
            actual_flags=self.actual_flags,
            longitude=self.longitude_deg % 360.0,
            latitude=self.latitude_deg,
            distance=self.distance_au,
            speed=self.speed_deg_per_day,
            warnings=(),
            errors=(),
        )


@dataclass(frozen=True)
class NativeRuntimeIdentity:
    library_sha256: str
    reported_version: str
    swiss_release: str
    swiss_source_commit: str
    data_bundle_sha256: str
    calling_convention: str


def sha256_file(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def _git_blob_sha1(path: Path) -> str:
    import hashlib
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def _canonical_swiss_bundle_aggregate_sha256(observed: dict[str, str]) -> str:
    lines = "".join(f"{name} {observed[name]}\n" for name in sorted(observed))
    return sha256(lines.encode("utf-8")).hexdigest()


def verify_canonical_swiss_bundle(root: Path) -> str:
    root = root.resolve()
    if not root.is_dir() or root.is_symlink():
        raise NativeRuntimeError("canonical_ephemeris_root_not_regular")
    files = [path for path in root.iterdir() if path.is_file()]
    if any(path.is_symlink() for path in root.iterdir()):
        raise NativeRuntimeError("canonical_ephemeris_root_contains_symlink")
    if any(path.is_dir() for path in root.iterdir()):
        raise NativeRuntimeError("canonical_ephemeris_root_contains_unexpected_directory")
    observed_names = {path.name for path in files}
    if observed_names != set(CANONICAL_SWISS_FILES):
        missing = sorted(set(CANONICAL_SWISS_FILES) - observed_names)
        extra = sorted(observed_names - set(CANONICAL_SWISS_FILES))
        raise NativeRuntimeError(f"canonical_ephemeris_file_set_mismatch:missing={missing}:extra={extra}")

    observed: dict[str, str] = {}
    for name, expected in CANONICAL_SWISS_FILES.items():
        path = root / name
        if path.stat().st_size != expected["size_bytes"]:
            raise NativeRuntimeError(f"canonical_ephemeris_size_mismatch:{name}")
        digest = sha256_file(path)
        if digest.lower() != expected["sha256"]:
            raise NativeRuntimeError(f"canonical_ephemeris_sha256_mismatch:{name}")
        blob = _git_blob_sha1(path)
        if blob.lower() != expected["git_blob_sha1"]:
            raise NativeRuntimeError(f"canonical_ephemeris_git_blob_mismatch:{name}")
        observed[name] = digest.lower()

    aggregate = _canonical_swiss_bundle_aggregate_sha256(observed)
    if aggregate != CANONICAL_SWISS_BUNDLE_SHA256:
        raise NativeRuntimeError("canonical_ephemeris_bundle_hash_mismatch")
    return aggregate


def _validate_actual_flags(actual_flags: int, with_speed: bool) -> None:
    if actual_flags < 0:
        raise NativeRuntimeError("native_calculation_failure")
    if (actual_flags & SEFLG_SWIEPH) != SEFLG_SWIEPH:
        raise NativeRuntimeError("actual_ephemeris_not_swisseph")
    if with_speed and (actual_flags & SEFLG_SPEED) != SEFLG_SPEED:
        raise NativeRuntimeError("actual_speed_flag_missing")


class NativeSwissEphemerisAdapter:
    """Strict CE native runtime adapter.

    This adapter performs no authority promotion. It is usable only when its
    caller has already passed the CE fail-closed runtime gate. No network,
    Moshier, alternate ephemeris engine, or host timezone database is involved.
    """

    def __init__(
        self,
        *,
        library_path: Path,
        ephemeris_root: Path,
        calling_convention: str,
        runtime_authorized: bool,
        expected_library_sha256: str = CANDIDATE_NATIVE_DLL_SHA256,
        expected_source_commit: str = CANONICAL_SWISS_SOURCE_COMMIT,
        swiss_release: str = CANONICAL_SWISS_RELEASE,
        loader: Any | None = None,
    ) -> None:
        if not runtime_authorized:
            raise NativeRuntimeError("runtime_not_authorized")
        if calling_convention not in {"__cdecl", "__stdcall"}:
            raise NativeRuntimeError("native_abi_calling_convention_not_pinned")
        if expected_library_sha256.lower() != CANDIDATE_NATIVE_DLL_SHA256:
            raise NativeRuntimeError("native_library_identity_override_forbidden")
        if expected_source_commit != CANONICAL_SWISS_SOURCE_COMMIT:
            raise NativeRuntimeError("swiss_source_commit_mismatch")
        if swiss_release != CANONICAL_SWISS_RELEASE:
            raise NativeRuntimeError("swiss_release_mismatch")
        if not library_path.is_file() or library_path.is_symlink():
            raise NativeRuntimeError("native_library_missing_or_nonregular")
        actual_library_hash = sha256_file(library_path)
        if actual_library_hash.lower() != expected_library_sha256.lower():
            raise NativeRuntimeError("native_library_sha256_mismatch")
        ephemeris_root = ephemeris_root.resolve()
        self._ephemeris_root = ephemeris_root
        bundle_hash = verify_canonical_swiss_bundle(ephemeris_root)

        if loader is None:
            if calling_convention == "__stdcall" and hasattr(ctypes, "WinDLL"):
                loader = ctypes.WinDLL
            else:
                loader = ctypes.CDLL
        try:
            self._lib = loader(str(library_path))
        except OSError as exc:
            raise NativeRuntimeError("native_library_load_failed") from exc

        self._configure_abi()
        self._lib.swe_set_ephe_path(str(ephemeris_root.resolve()).encode("utf-8"))
        self.runtime_identity = NativeRuntimeIdentity(
            library_sha256=actual_library_hash.lower(),
            reported_version=self._reported_version(),
            swiss_release=swiss_release,
            swiss_source_commit=expected_source_commit,
            data_bundle_sha256=bundle_hash,
            calling_convention=calling_convention,
        )
        if self.runtime_identity.reported_version not in {"2.10.03", "2.10.3"}:
            raise NativeRuntimeError("native_swiss_runtime_version_mismatch")

    def _configure_abi(self) -> None:
        try:
            self._lib.swe_set_ephe_path.argtypes = [ctypes.c_char_p]
            self._lib.swe_set_ephe_path.restype = None
            self._lib.swe_calc_ut.argtypes = [
                ctypes.c_double,
                ctypes.c_int,
                ctypes.c_int,
                ctypes.POINTER(ctypes.c_double),
                ctypes.c_char_p,
            ]
            self._lib.swe_calc_ut.restype = ctypes.c_int
            self._lib.swe_version.argtypes = [ctypes.c_char_p]
            self._lib.swe_version.restype = None
        except AttributeError as exc:
            raise NativeRuntimeError("native_swiss_abi_symbols_missing") from exc

    def _reported_version(self) -> str:
        buffer = ctypes.create_string_buffer(256)
        self._lib.swe_version(buffer)
        return buffer.value.decode("ascii", errors="strict")

    def calculate_object(
        self,
        object_id: str,
        julian_day_ut: float,
        with_speed: bool,
    ) -> ObjectRecord:
        detailed = self.calculate_object_detailed(object_id, julian_day_ut, with_speed)
        return detailed.to_object_record()

    def calculate_object_detailed(
        self,
        object_id: str,
        julian_day_ut: float,
        with_speed: bool,
    ) -> NativeSwissCalculation:
        if object_id not in EXPECTED_OBJECTS:
            raise NativeRuntimeError(f"object_not_in_current_registry:{object_id}")
        # Verify the exact canonical data immediately before using the native runtime.
        verify_canonical_swiss_bundle(self._ephemeris_root)
        requested_flags = SEFLG_SWIEPH | (SEFLG_SPEED if with_speed else 0)
        values = (ctypes.c_double * 6)()
        error_buffer = ctypes.create_string_buffer(256)
        actual_flags = int(
            self._lib.swe_calc_ut(
                float(julian_day_ut),
                int(EXPECTED_OBJECTS[object_id]),
                requested_flags,
                values,
                error_buffer,
            )
        )
        message = error_buffer.value.decode("utf-8", errors="replace") or None
        _validate_actual_flags(actual_flags, with_speed)
        numbers = [float(values[index]) for index in range(4)]
        import math
        if any(not math.isfinite(value) for value in numbers):
            raise NativeRuntimeError("native_numeric_result_not_finite")
        # Verify again after calculation so data mutation cannot be silently accepted.
        verify_canonical_swiss_bundle(self._ephemeris_root)
        if any(not __import__("math").isfinite(value) for value in numbers):
            raise NativeRuntimeError("native_numeric_result_not_finite")
        return NativeSwissCalculation(
            object_id=object_id,
            swiss_object_id=int(EXPECTED_OBJECTS[object_id]),
            jd_ut=float(julian_day_ut),
            longitude_deg=numbers[0],
            latitude_deg=numbers[1],
            distance_au=numbers[2],
            speed_deg_per_day=numbers[3] if with_speed else None,
            requested_flags=requested_flags,
            actual_flags=actual_flags,
            ephemeris="SWIEPH",
            warning_or_error=message,
        )

    def close(self) -> None:
        close = getattr(self._lib, "swe_close", None)
        if close is not None:
            close()
