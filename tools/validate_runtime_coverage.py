from __future__ import annotations

import argparse
from datetime import datetime
import json
from math import isfinite
from pathlib import Path

from ce.calculation.registry import EXPECTED_OBJECTS
from ce.ephemeris.native_runtime import (
    CANONICAL_SWISS_BUNDLE_SHA256,
    CANONICAL_SWISS_SOURCE_COMMIT,
    CANDIDATE_NATIVE_DLL_SHA256,
    SEFLG_SPEED,
    SEFLG_SWIEPH,
)
from ce.runtime.reproducibility import RuntimeCapture, ReproducibilityCaptureError, compare_capture_outputs
from ce.timezone.runtime import CANONICAL_IANA_VERSION, CANONICAL_TZIF_BUNDLE_SHA256


class CoverageValidationError(ValueError):
    pass


def _parse_capture(path: Path) -> tuple[RuntimeCapture, dict[str, object]]:
    if path.is_symlink() or not path.is_file():
        raise CoverageValidationError(f"capture_missing_or_nonregular:{path}")
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise CoverageValidationError(f"capture_parse_failed:{path}") from exc
    if not isinstance(raw, dict):
        raise CoverageValidationError("capture_top_level_mapping_required")
    payload = raw.get("capture", raw)
    if not isinstance(payload, dict):
        raise CoverageValidationError("capture_payload_mapping_required")
    required = (
        "capture_id", "captured_at_utc", "platform", "python_version",
        "execution_profile_id", "execution_profile_revision", "source_commit",
        "source_tree_sha256_v2", "dependency_lock_digest",
        "runtime_environment_kind", "runtime_image_digest",
        "runtime_environment_digest", "timezone_bundle_digest",
        "ephemeris_bundle_digest", "native_library_sha256",
        "native_runtime_version", "swiss_source_commit", "calling_convention",
        "fixtures",
    )
    missing = [key for key in required if key not in payload]
    if missing:
        raise CoverageValidationError(f"capture_missing_keys:{','.join(missing)}")
    try:
        capture = RuntimeCapture(
        capture_id=payload["capture_id"],
        captured_at_utc=payload["captured_at_utc"],
        platform=payload["platform"],
        python_version=payload["python_version"],
        execution_profile_id=payload["execution_profile_id"],
        execution_profile_revision=payload["execution_profile_revision"],
        source_commit=payload["source_commit"],
        source_tree_sha256_v2=payload["source_tree_sha256_v2"],
        dependency_lock_digest=payload["dependency_lock_digest"],
        runtime_environment_kind=payload["runtime_environment_kind"],
        runtime_image_digest=payload["runtime_image_digest"],
        runtime_environment_digest=payload["runtime_environment_digest"],
        timezone_bundle_digest=payload["timezone_bundle_digest"],
        ephemeris_bundle_digest=payload["ephemeris_bundle_digest"],
        native_library_sha256=payload["native_library_sha256"],
        native_runtime_version=payload["native_runtime_version"],
        swiss_source_commit=payload["swiss_source_commit"],
        calling_convention=payload["calling_convention"],
            fixtures=tuple(payload["fixtures"]),
        )
    except ReproducibilityCaptureError as exc:
        raise CoverageValidationError(f"capture_invalid:{exc}") from exc
    return capture, raw


def _load_fixture_spec(path: Path) -> tuple[dict[str, object], ...]:
    if path.is_symlink() or not path.is_file():
        raise CoverageValidationError("fixture_spec_missing_or_nonregular")
    raw = json.loads(path.read_text(encoding="utf-8"))
    fixtures = raw.get("fixtures")
    if not isinstance(fixtures, list) or not fixtures:
        raise CoverageValidationError("fixture_spec_nonempty_required")
    normalized = []
    for item in fixtures:
        if not isinstance(item, dict):
            raise CoverageValidationError("fixture_spec_fixture_mapping_required")
        fixture_id = item.get("fixture_id")
        jd_ut = item.get("julian_day_ut")
        objects = item.get("objects")
        if not isinstance(fixture_id, str) or not fixture_id.strip():
            raise CoverageValidationError("fixture_spec_fixture_id_invalid")
        if type(jd_ut) not in (int, float) or not isfinite(float(jd_ut)):
            raise CoverageValidationError(f"fixture_spec_jd_invalid:{fixture_id}")
        if not isinstance(objects, list) or not objects:
            raise CoverageValidationError(f"fixture_spec_objects_invalid:{fixture_id}")
        if tuple(objects) != tuple(dict.fromkeys(objects)):
            raise CoverageValidationError(f"fixture_spec_duplicate_object:{fixture_id}")
        if set(objects) != set(EXPECTED_OBJECTS):
            raise CoverageValidationError(f"fixture_spec_object_set_mismatch:{fixture_id}")
        normalized.append({
            "fixture_id": fixture_id,
            "julian_day_ut": float(jd_ut),
            "objects": tuple(objects),
        })
    ids = [str(item["fixture_id"]) for item in normalized]
    if len(ids) != len(set(ids)):
        raise CoverageValidationError("fixture_spec_duplicate_fixture_id")
    return tuple(normalized)


def _validate_identity(
    capture: RuntimeCapture,
    *,
    source_commit: str,
    source_tree_sha256: str,
    dependency_lock_digest: str,
    calling_convention: str,
) -> None:
    expected = {
        "source_commit": source_commit,
        "source_tree_sha256_v2": source_tree_sha256,
        "dependency_lock_digest": dependency_lock_digest,
        "timezone_bundle_digest": CANONICAL_TZIF_BUNDLE_SHA256,
        "ephemeris_bundle_digest": CANONICAL_SWISS_BUNDLE_SHA256,
        "native_library_sha256": CANDIDATE_NATIVE_DLL_SHA256,
        "swiss_source_commit": CANONICAL_SWISS_SOURCE_COMMIT,
        "calling_convention": calling_convention,
    }
    for name, value in expected.items():
        if getattr(capture, name) != value:
            raise CoverageValidationError(
                f"identity_mismatch:{name}:expected={value}:actual={getattr(capture, name)}"
            )
    if capture.timezone_bundle_digest != CANONICAL_TZIF_BUNDLE_SHA256:
        raise CoverageValidationError("timezone_version_binding_mismatch")
    if capture.execution_profile_id != "CE-CALC-V1-EP-001" or capture.execution_profile_revision != 4:
        raise CoverageValidationError("execution_profile_identity_mismatch")
    if capture.runtime_environment_kind == "HOST_NATIVE" and capture.runtime_environment_digest is None:
        raise CoverageValidationError("host_runtime_environment_digest_missing")
    if capture.runtime_environment_kind == "OCI_IMAGE" and capture.runtime_image_digest is None:
        raise CoverageValidationError("oci_runtime_image_digest_missing")


def _validate_fixture_set(
    capture: RuntimeCapture,
    expected: tuple[dict[str, object], ...],
) -> None:
    actual_ids = [str(item["fixture_id"]) for item in capture.fixtures]
    if len(actual_ids) != len(set(actual_ids)):
        raise CoverageValidationError("capture_duplicate_fixture_id")
    expected_ids = [str(item["fixture_id"]) for item in expected]
    if actual_ids != expected_ids:
        raise CoverageValidationError(
            f"fixture_id_set_or_order_mismatch:expected={expected_ids}:actual={actual_ids}"
        )

    for spec, observed in zip(expected, capture.fixtures):
        fixture_id = str(spec["fixture_id"])
        expected_jd = float(spec["julian_day_ut"])
        records = observed["records"]
        if not isinstance(records, dict):
            raise CoverageValidationError(f"fixture_records_mapping_required:{fixture_id}")
        actual_jd = records.get("julian_day_ut")
        if type(actual_jd) not in (int, float) or float(actual_jd) != expected_jd:
            raise CoverageValidationError(
                f"fixture_jd_mismatch:{fixture_id}:expected={expected_jd}:actual={actual_jd}"
            )
        objects = records.get("objects")
        if not isinstance(objects, list):
            raise CoverageValidationError(f"fixture_objects_list_required:{fixture_id}")
        expected_objects = tuple(spec["objects"])
        actual_objects = tuple(
            item.get("object_id") if isinstance(item, dict) else None
            for item in objects
        )
        if actual_objects != expected_objects:
            raise CoverageValidationError(
                f"fixture_object_set_or_order_mismatch:{fixture_id}"
            )
        if len(objects) != len(expected_objects):
            raise CoverageValidationError(f"fixture_object_count_mismatch:{fixture_id}")

        for index, record in enumerate(objects):
            if not isinstance(record, dict):
                raise CoverageValidationError(f"record_mapping_required:{fixture_id}:{index}")
            requested = record.get("requested_flags")
            actual = record.get("actual_flags")
            if requested != (SEFLG_SWIEPH | SEFLG_SPEED):
                raise CoverageValidationError(
                    f"requested_flags_mismatch:{fixture_id}:{index}:{requested}"
                )
            if not isinstance(actual, int) or actual < 0 or (actual & requested) != requested:
                raise CoverageValidationError(
                    f"actual_flags_do_not_cover_requested:{fixture_id}:{index}:{actual}"
                )
            if record.get("ephemeris") != "SWIEPH":
                raise CoverageValidationError(
                    f"non_swieph_result:{fixture_id}:{index}:{record.get('ephemeris')}"
                )
            for field in ("longitude_deg", "latitude_deg", "distance_au", "speed_deg_per_day"):
                value = record.get(field)
                if value is None or not isinstance(value, (int, float)) or isinstance(value, bool) or not isfinite(float(value)):
                    raise CoverageValidationError(
                        f"nonfinite_or_missing_numeric:{fixture_id}:{index}:{field}"
                    )


def validate_capture(
    path: Path,
    *,
    fixture_spec: tuple[dict[str, object], ...],
    source_commit: str,
    source_tree_sha256: str,
    dependency_lock_digest: str,
    calling_convention: str,
) -> RuntimeCapture:
    capture, raw = _parse_capture(path)
    errors = capture.validate()
    if errors:
        raise CoverageValidationError("capture_invalid:" + ";".join(errors))
    if raw.get("capture_role") not in (None, "EVIDENCE_ONLY_NON_AUTHORITY"):
        raise CoverageValidationError("capture_role_not_evidence_only")
    _validate_identity(
        capture,
        source_commit=source_commit,
        source_tree_sha256=source_tree_sha256,
        dependency_lock_digest=dependency_lock_digest,
        calling_convention=calling_convention,
    )
    _validate_fixture_set(capture, fixture_spec)
    return capture


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate CE 1900-2100 native runtime coverage captures.")
    parser.add_argument("captures", nargs="+", type=Path)
    parser.add_argument("--fixture-spec", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--source-tree-sha256-v2", required=True)
    parser.add_argument("--dependency-lock-digest", required=True)
    parser.add_argument("--calling-convention", choices=("__cdecl", "__stdcall"), required=True)
    parser.add_argument("--output-report", type=Path)
    args = parser.parse_args()

    if len(args.captures) > 2:
        raise CoverageValidationError("maximum_two_captures_supported")

    fixture_spec = _load_fixture_spec(args.fixture_spec)
    captures = [
        validate_capture(
            path,
            fixture_spec=fixture_spec,
            source_commit=args.source_commit,
            source_tree_sha256=args.source_tree_sha256_v2,
            dependency_lock_digest=args.dependency_lock_digest,
            calling_convention=args.calling_convention,
        )
        for path in args.captures
    ]

    parity_errors: tuple[str, ...] = ()
    if len(captures) == 2:
        parity_errors = compare_capture_outputs(captures[0], captures[1])
        if parity_errors:
            for error in parity_errors:
                print(f"PARITY_FAIL {error}")
            return 1

    report = {
        "schema": "CE-RUNTIME-COVERAGE-REPORT-V1",
        "status": "PASS",
        "authorization": "NON_AUTHORIZED",
        "fail_closed": True,
        "coverage_scope": {
            "fixture_count": len(fixture_spec),
            "objects_per_fixture": len(EXPECTED_OBJECTS),
            "required_object_records": len(fixture_spec) * len(EXPECTED_OBJECTS),
            "range_start_jd_ut": fixture_spec[0]["julian_day_ut"],
            "range_end_jd_ut": fixture_spec[-1]["julian_day_ut"],
        },
        "execution_identity": {
            "source_commit": args.source_commit,
            "source_tree_sha256_v2": args.source_tree_sha256_v2,
            "dependency_lock_digest": args.dependency_lock_digest,
            "timezone_bundle_digest": CANONICAL_TZIF_BUNDLE_SHA256,
            "timezone_version": CANONICAL_IANA_VERSION,
            "ephemeris_bundle_digest": CANONICAL_SWISS_BUNDLE_SHA256,
            "native_library_sha256": CANDIDATE_NATIVE_DLL_SHA256,
            "swiss_source_commit": CANONICAL_SWISS_SOURCE_COMMIT,
            "calling_convention": args.calling_convention,
        },
        "captures": [
            {
                "path": str(path),
                "capture_id": capture.capture_id,
                "content_sha256": capture.content_sha256(),
                "platform": capture.platform,
                "runtime_environment_kind": capture.runtime_environment_kind,
                "runtime_environment_digest": capture.runtime_environment_digest,
                "runtime_image_digest": capture.runtime_image_digest,
            }
            for path, capture in zip(args.captures, captures)
        ],
        "parity": {
            "executed": len(captures) == 2,
            "status": "PASS" if len(captures) == 2 else "NOT_APPLICABLE",
            "errors": list(parity_errors),
        },
        "production_authority": "NOT_ESTABLISHED",
        "note": "This report proves only the captured fixture scope; it does not itself establish production authority, full-date-grid coverage, or release authorization.",
    }

    if args.output_report:
        args.output_report.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    print("COVERAGE_VALID PASS")
    print(f"RANGE_PROBES={len(fixture_spec)}")
    print(f"OBJECTS_PER_PROBE={len(EXPECTED_OBJECTS)}")
    print(f"CAPTURES={len(captures)}")
    if len(captures) == 2:
        print("PARITY_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
