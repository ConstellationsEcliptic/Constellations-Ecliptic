from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import platform
import uuid

from ce.ephemeris.native_runtime import (
    CANDIDATE_NATIVE_DLL_SHA256,
    CANONICAL_SWISS_RELEASE,
    CANONICAL_SWISS_SOURCE_COMMIT,
    NativeRuntimeError,
    SEFLG_SPEED,
    SEFLG_SWIEPH,
    sha256_file,
    verify_canonical_swiss_bundle,
)
from ce.calculation.registry import EXPECTED_OBJECTS
from ce.runtime.reproducibility import RuntimeCapture


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Capture native Swiss Ephemeris reproducibility evidence. "
            "This is an evidence harness, not CE runtime authorization."
        )
    )
    parser.add_argument("--library", type=Path, required=True)
    parser.add_argument("--ephemeris-root", type=Path, required=True)
    parser.add_argument("--fixture-spec", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--source-tree-sha256-v2", required=True)
    parser.add_argument("--dependency-lock-digest", required=True)
    parser.add_argument("--runtime-image-digest", required=True)
    parser.add_argument("--timezone-bundle-digest", required=True)
    parser.add_argument("--calling-convention", choices=("__cdecl", "__stdcall"), required=True)
    return parser


def _load_fixture_spec(path: Path) -> list[dict[str, object]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    fixtures = raw.get("fixtures")
    if not isinstance(fixtures, list) or not fixtures:
        raise ValueError("fixture_spec_requires_nonempty_fixtures")
    result: list[dict[str, object]] = []
    for index, fixture in enumerate(fixtures):
        if not isinstance(fixture, dict):
            raise ValueError(f"fixture_spec_invalid_fixture:{index}")
        fixture_id = fixture.get("fixture_id")
        jd_ut = fixture.get("julian_day_ut")
        objects = fixture.get("objects")
        if not isinstance(fixture_id, str) or not fixture_id.strip():
            raise ValueError(f"fixture_spec_invalid_fixture_id:{index}")
        if type(jd_ut) not in (int, float):
            raise ValueError(f"fixture_spec_invalid_julian_day:{fixture_id}")
        if not isinstance(objects, list) or not objects:
            raise ValueError(f"fixture_spec_requires_objects:{fixture_id}")
        normalized_objects = []
        for object_id in objects:
            if not isinstance(object_id, str) or object_id not in EXPECTED_OBJECTS:
                raise ValueError(f"fixture_spec_unknown_object:{fixture_id}:{object_id}")
            normalized_objects.append(object_id)
        result.append(
            {
                "fixture_id": fixture_id,
                "julian_day_ut": float(jd_ut),
                "objects": tuple(normalized_objects),
            }
        )
    return result


def _load_native_library(path: Path, calling_convention: str):
    import ctypes

    if path.is_symlink() or not path.is_file():
        raise NativeRuntimeError("native_library_missing_or_nonregular")
    observed = sha256_file(path)
    if observed.lower() != CANDIDATE_NATIVE_DLL_SHA256:
        raise NativeRuntimeError("native_library_sha256_mismatch")

    loader = ctypes.WinDLL if calling_convention == "__stdcall" and hasattr(ctypes, "WinDLL") else ctypes.CDLL
    try:
        library = loader(str(path))
    except OSError as exc:
        raise NativeRuntimeError("native_library_load_failed") from exc

    try:
        library.swe_set_ephe_path.argtypes = [ctypes.c_char_p]
        library.swe_set_ephe_path.restype = None
        library.swe_calc_ut.argtypes = [
            ctypes.c_double,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.POINTER(ctypes.c_double),
            ctypes.c_char_p,
        ]
        library.swe_calc_ut.restype = ctypes.c_int
        library.swe_version.argtypes = [ctypes.c_char_p]
        library.swe_version.restype = None
    except AttributeError as exc:
        raise NativeRuntimeError("native_swiss_abi_symbols_missing") from exc

    return library, observed


def _reported_version(library) -> str:
    import ctypes

    buffer = ctypes.create_string_buffer(256)
    library.swe_version(buffer)
    return buffer.value.decode("ascii", errors="strict")


def _calculate(library, object_id: str, jd_ut: float, ephemeris_root: Path, with_speed: bool) -> dict[str, object]:
    import ctypes

    values = (ctypes.c_double * 6)()
    error_buffer = ctypes.create_string_buffer(256)
    flags = SEFLG_SWIEPH | (SEFLG_SPEED if with_speed else 0)
    actual_flags = int(
        library.swe_calc_ut(
            float(jd_ut),
            int(EXPECTED_OBJECTS[object_id]),
            flags,
            values,
            error_buffer,
        )
    )
    if actual_flags < 0:
        raise NativeRuntimeError(f"native_calculation_failure:{object_id}:{actual_flags}")
    warning = error_buffer.value.decode("utf-8", errors="replace") or None
    return {
        "object_id": object_id,
        "swiss_object_id": int(EXPECTED_OBJECTS[object_id]),
        "jd_ut": float(jd_ut),
        "requested_flags": int(flags),
        "actual_flags": int(actual_flags),
        "longitude_deg": float(values[0]) % 360.0,
        "latitude_deg": float(values[1]),
        "distance_au": float(values[2]),
        "speed_deg_per_day": float(values[3]) if with_speed else None,
        "ephemeris": "SWIEPH",
        "warning_or_error": warning,
    }


def main() -> int:
    args = _parser().parse_args()
    fixtures = _load_fixture_spec(args.fixture_spec)

    ephemeris_root = args.ephemeris_root.resolve()
    bundle_hash = verify_canonical_swiss_bundle(ephemeris_root)
    library, library_hash = _load_native_library(args.library.resolve(), args.calling_convention)
    library.swe_set_ephe_path(str(ephemeris_root).encode("utf-8"))
    reported_version = _reported_version(library)
    if reported_version not in {"2.10.03", "2.10.3"}:
        raise NativeRuntimeError("native_swiss_runtime_version_mismatch")

    captured = []
    for fixture in fixtures:
        records = []
        for object_id in fixture["objects"]:
            records.append(
                _calculate(
                    library,
                    object_id,
                    float(fixture["julian_day_ut"]),
                    ephemeris_root,
                    with_speed=True,
                )
            )
        captured.append(
            {
                "fixture_id": str(fixture["fixture_id"]),
                "records": {
                    "julian_day_ut": float(fixture["julian_day_ut"]),
                    "objects": records,
                },
            }
        )

    runtime_capture = RuntimeCapture(
        capture_id="CE-RUNTIME-CAPTURE-" + uuid.uuid4().hex,
        captured_at_utc=datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        platform=platform.platform(),
        python_version=platform.python_version(),
        execution_profile_id="CE-CALC-V1-EP-001",
        execution_profile_revision=4,
        source_commit=args.source_commit,
        source_tree_sha256_v2=args.source_tree_sha256_v2,
        dependency_lock_digest=args.dependency_lock_digest,
        runtime_image_digest=args.runtime_image_digest,
        timezone_bundle_digest=args.timezone_bundle_digest,
        ephemeris_bundle_digest=bundle_hash,
        native_library_sha256=library_hash,
        native_runtime_version=reported_version,
        swiss_source_commit=CANONICAL_SWISS_SOURCE_COMMIT,
        calling_convention=args.calling_convention,
        fixtures=tuple(captured),
    )
    args.output.write_text(
        json.dumps(
            {
                "capture": json.loads(runtime_capture.canonical_bytes().decode("utf-8")),
                "capture_content_sha256": runtime_capture.content_sha256(),
                "capture_role": "EVIDENCE_ONLY_NON_AUTHORITY",
                "swiss_release": CANONICAL_SWISS_RELEASE,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(runtime_capture.content_sha256())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
