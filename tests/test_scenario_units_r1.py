from __future__ import annotations

from datetime import datetime, timezone
import unittest

from ce.calculation.scenario_windows import (
    SCENARIO_SEGMENT_TIME_UNIT,
    build_scenario_instants,
    canonical_utc,
    normalize_segments,
)


class ScenarioUnitsR1Tests(unittest.TestCase):
    def test_segment_time_unit_is_seconds(self) -> None:
        self.assertEqual(SCENARIO_SEGMENT_TIME_UNIT, "SECONDS")

    def test_scenario_midpoint_lattice_uses_exact_integer_microseconds(self) -> None:
        start = datetime(2026, 1, 1, 0, 0, 0, 1, tzinfo=timezone.utc)
        end = datetime(2026, 1, 1, 0, 0, 10, 124, tzinfo=timezone.utc)
        values = build_scenario_instants(start, end, 4)
        total_microseconds = 10 * 1_000_000 + 123
        expected_offsets = tuple(
            ((2 * index + 1) * total_microseconds) // (2 * 4)
            for index in range(4)
        )
        actual_offsets = tuple(
            int(
                (value - start).days * 86_400_000_000
                + (value - start).seconds * 1_000_000
                + (value - start).microseconds
            )
            for value in values
        )
        self.assertEqual(actual_offsets, expected_offsets)

    def test_canonical_utc_preserves_nonzero_microseconds(self) -> None:
        value = datetime(2026, 1, 1, 12, 34, 56, 123456, tzinfo=timezone.utc)
        self.assertEqual(canonical_utc(value), "2026-01-01T12:34:56.123456Z")

    def test_gap_above_tolerance_is_not_merged(self) -> None:
        self.assertEqual(
            normalize_segments(((0.0, 10.0), (12.0, 20.0))),
            ((0.0, 10.0), (12.0, 20.0)),
        )

    def test_sub_tolerance_gap_is_merged(self) -> None:
        self.assertEqual(
            normalize_segments(((0.0, 10.0), (10.5, 20.0))),
            ((0.0, 20.0),),
        )

    def test_canonical_utc_rejects_naive_datetime(self) -> None:
        with self.assertRaisesRegex(ValueError, "datetime_must_be_timezone_aware"):
            canonical_utc(datetime(2026, 1, 1))

    def test_canonical_utc_normalizes_offset_aware_datetime(self) -> None:
        value = datetime(2026, 1, 1, 1, 0, tzinfo=timezone.utc)
        self.assertEqual(canonical_utc(value), "2026-01-01T01:00:00Z")


if __name__ == "__main__":
    unittest.main()
