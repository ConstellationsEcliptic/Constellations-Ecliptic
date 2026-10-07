from __future__ import annotations

import json
import tempfile
from pathlib import Path
import unittest

from ce.calculation.registry import EXPECTED_OBJECTS
from ce.ephemeris.native_runtime import CANONICAL_SWISS_BUNDLE_SHA256, CANDIDATE_NATIVE_DLL_SHA256, CANONICAL_SWISS_SOURCE_COMMIT
from ce.timezone.runtime import CANONICAL_TZIF_BUNDLE_SHA256
from tools.validate_runtime_coverage import CoverageValidationError, validate_capture


SOURCE_COMMIT = "5" * 40
SOURCE_TREE = "6" * 64
LOCK = "7" * 64
CONTROL_PLANE = "9" * 64


class RuntimeCoverageValidatorR1Tests(unittest.TestCase):
    def _spec(self) -> tuple[dict[str, object], ...]:
        return (
            {
                "fixture_id": "CE-NATIVE-R1-1900-001",
                "julian_day_ut": 2415021.0,
                "objects": tuple(EXPECTED_OBJECTS),
            },
            {
                "fixture_id": "CE-NATIVE-R1-2000-001",
                "julian_day_ut": 2451545.0,
                "objects": tuple(EXPECTED_OBJECTS),
            },
            {
                "fixture_id": "CE-NATIVE-R1-2100-001",
                "julian_day_ut": 2488069.0,
                "objects": tuple(EXPECTED_OBJECTS),
            },
        )

    def _capture(self) -> dict[str, object]:
        fixtures = []
        for spec in self._spec():
            fixtures.append(
                {
                    "fixture_id": spec["fixture_id"],
                    "records": {
                        "julian_day_ut": spec["julian_day_ut"],
                        "objects": [
                            {
                                "object_id": object_id,
                                "requested_flags": 258,
                                "actual_flags": 258,
                                "longitude_deg": 1.0,
                                "latitude_deg": 0.0,
                                "distance_au": 1.0,
                                "speed_deg_per_day": 1.0,
                                "ephemeris": "SWIEPH",
                            }
                            for object_id in spec["objects"]
                        ],
                    },
                }
            )
        return {
            "capture": {
                "capture_id": "CAPTURE-001",
                "captured_at_utc": "2026-10-04T00:00:00Z",
                "platform": "TEST",
                "python_version": "3.13.15",
                "execution_profile_id": "CE-CALC-V1-EP-001",
                "execution_profile_revision": 4,
                "source_commit": SOURCE_COMMIT,
                "source_tree_sha256_v2": SOURCE_TREE,
                "control_plane_sha256": CONTROL_PLANE,
                "dependency_lock_digest": LOCK,
                "runtime_environment_kind": "HOST_NATIVE",
                "runtime_image_digest": None,
                "runtime_environment_digest": "8" * 64,
                "timezone_bundle_digest": CANONICAL_TZIF_BUNDLE_SHA256,
                "ephemeris_bundle_digest": CANONICAL_SWISS_BUNDLE_SHA256,
                "native_library_sha256": CANDIDATE_NATIVE_DLL_SHA256,
                "native_runtime_version": "2.10.03",
                "swiss_source_commit": CANONICAL_SWISS_SOURCE_COMMIT,
                "calling_convention": "__cdecl",
                "fixtures": fixtures,
            },
            "capture_role": "EVIDENCE_ONLY_NON_AUTHORITY",
        }

    def _write(self, payload: dict[str, object]) -> Path:
        temp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        path = Path(temp.name)
        temp.close()
        path.write_text(json.dumps(payload), encoding="utf-8")
        self.addCleanup(lambda: path.unlink(missing_ok=True))
        return path

    def test_valid_capture_passes_strict_coverage(self) -> None:
        path = self._write(self._capture())
        capture = validate_capture(
            path,
            fixture_spec=self._spec(),
            source_commit=SOURCE_COMMIT,
            source_tree_sha256=SOURCE_TREE,
            dependency_lock_digest=LOCK,
            control_plane_sha256=CONTROL_PLANE,
            calling_convention="__cdecl",
        )
        self.assertEqual(capture.fixtures[-1]["fixture_id"], "CE-NATIVE-R1-2100-001")

    def test_duplicate_fixture_id_is_rejected(self) -> None:
        payload = self._capture()
        fixtures = payload["capture"]["fixtures"]
        fixtures[1]["fixture_id"] = fixtures[0]["fixture_id"]
        path = self._write(payload)
        with self.assertRaisesRegex(CoverageValidationError, "capture_invalid"):
            validate_capture(
                path,
                fixture_spec=self._spec(),
                source_commit=SOURCE_COMMIT,
                source_tree_sha256=SOURCE_TREE,
                dependency_lock_digest=LOCK,
                control_plane_sha256=CONTROL_PLANE,
                calling_convention="__cdecl",
            )

    def test_wrong_jd_is_rejected(self) -> None:
        payload = self._capture()
        payload["capture"]["fixtures"][0]["records"]["julian_day_ut"] = 2415020.5
        path = self._write(payload)
        with self.assertRaisesRegex(CoverageValidationError, "fixture_jd_mismatch"):
            validate_capture(
                path,
                fixture_spec=self._spec(),
                source_commit=SOURCE_COMMIT,
                source_tree_sha256=SOURCE_TREE,
                dependency_lock_digest=LOCK,
                calling_convention="__cdecl",
            )

    def test_actual_flags_must_cover_requested(self) -> None:
        payload = self._capture()
        payload["capture"]["fixtures"][0]["records"]["objects"][0]["actual_flags"] = 2
        path = self._write(payload)
        with self.assertRaisesRegex(CoverageValidationError, "actual_flags_do_not_cover_requested"):
            validate_capture(
                path,
                fixture_spec=self._spec(),
                source_commit=SOURCE_COMMIT,
                source_tree_sha256=SOURCE_TREE,
                dependency_lock_digest=LOCK,
                calling_convention="__cdecl",
            )


if __name__ == "__main__":
    unittest.main()
