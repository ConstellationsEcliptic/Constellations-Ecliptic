from __future__ import annotations

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from ce.calculation.contracts import CalculationResult, ObjectState
from ce.foundation.status import CalculationStatus, ScenarioState


class CalculationResultNormalizedTimeTests(unittest.TestCase):
    def _valid_result(self, normalized_time: str) -> CalculationResult:
        return CalculationResult(
            request_id="R-NORM-001",
            status=CalculationStatus.VALID,
            execution_profile_id="CE-CALC-V1-EP-001",
            scenario_state=ScenarioState.STABLE,
            normalized_time=normalized_time,
            object_states=(
                ObjectState(
                    object_id="TEST-OBJECT",
                    longitude_deg=120.0,
                    speed_deg_per_day=1.0,
                    status=CalculationStatus.VALID,
                ),
            ),
            warnings=(),
            errors=(),
            provenance={
                "source_commit": "a" * 40,
                "source_tree_sha256_v2": "b" * 64,
                "dependency_lock_digest": "c" * 64,
                "timezone_bundle_digest": "d" * 64,
                "ephemeris_bundle_digest": "e" * 64,
                "runtime_image_digest": "sha256:" + "f" * 64,
                "calculation_version": "0.1.0",
            },
        )

    def test_canonical_utc_without_fraction_is_accepted(self) -> None:
        result = self._valid_result("2026-01-01T00:00:00Z")
        self.assertEqual(result.normalized_time, "2026-01-01T00:00:00Z")

    def test_canonical_utc_with_six_fraction_digits_is_accepted(self) -> None:
        result = self._valid_result("2026-01-01T00:00:00.123456Z")
        self.assertEqual(result.normalized_time, "2026-01-01T00:00:00.123456Z")

    def test_noncanonical_utc_forms_are_rejected(self) -> None:
        invalid_values = (
            "2026-01-01 00:00:00Z",
            "2026-01-01t00:00:00Z",
            "2026-01-01T00:00Z",
            "2026-01-01T00:00:00.1234567Z",
            "2026-01-01T00:00:00+00:00",
        )
        for value in invalid_values:
            with self.subTest(value=value):
                with self.assertRaisesRegex(
                    ValueError, r"invalid:normalized_time:utc_canonical_z_required"
                ):
                    self._valid_result(value)

    def test_invalid_calendar_date_is_rejected(self) -> None:
        with self.assertRaisesRegex(
            ValueError, r"invalid:normalized_time:utc_iso8601_invalid"
        ):
            self._valid_result("2026-02-29T00:00:00Z")

    def test_direct_validation_reports_canonical_utc_requirement(self) -> None:
        result = CalculationResult(
            request_id="R-NORM-002",
            status=CalculationStatus.INVALID_INPUT,
            execution_profile_id="CE-CALC-V1-EP-001",
            scenario_state=ScenarioState.NONE,
            normalized_time="2026-01-01T00:00:00+00:00",
            errors=("invalid input",),
        )
        errors = result.validate()
        self.assertIn(
            "invalid:normalized_time:utc_canonical_z_required",
            errors,
        )


if __name__ == "__main__":
    unittest.main()
