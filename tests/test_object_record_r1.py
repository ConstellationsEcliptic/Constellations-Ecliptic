from __future__ import annotations

import unittest

from ce.calculation.contracts import ObjectRecord
from ce.foundation.status import CalculationStatus


class ObjectRecordR1Tests(unittest.TestCase):
    def test_requested_flags_must_be_covered_by_actual_flags(self) -> None:
        with self.assertRaisesRegex(ValueError, "actual_flags_do_not_cover_requested_flags"):
            ObjectRecord(
                "SUN", CalculationStatus.VALID, 258, 2,
                10.0, 0.0, 1.0, 1.0,
            )

    def test_requested_speed_flag_requires_speed(self) -> None:
        with self.assertRaisesRegex(ValueError, "requires_speed_when_speed_requested"):
            ObjectRecord(
                "SUN", CalculationStatus.VALID, 258, 258,
                10.0, 0.0, 1.0, None,
            )

    def test_latitude_and_distance_are_bounded(self) -> None:
        with self.assertRaisesRegex(ValueError, "latitude_must_be_normalized"):
            ObjectRecord(
                "SUN", CalculationStatus.VALID, 258, 258,
                10.0, 91.0, 1.0, 1.0,
            )
        with self.assertRaisesRegex(ValueError, "distance_must_be_positive"):
            ObjectRecord(
                "SUN", CalculationStatus.VALID, 258, 258,
                10.0, 0.0, 0.0, 1.0,
            )

    def test_nonvalid_object_cannot_publish_partial_numeric_state(self) -> None:
        with self.assertRaisesRegex(ValueError, "nonvalid_object_must_not_publish_numeric_state"):
            ObjectRecord(
                "SUN", CalculationStatus.KNOWN_UNAVAILABLE, 258, None,
                None, None, None, 1.0,
            )

    def test_observation_time_is_retained_in_canonical_record(self) -> None:
        record = ObjectRecord(
            "SUN", CalculationStatus.VALID, 258, 258,
            10.0, 0.0, 1.0, 1.0,
            observation_time_utc="2026-01-01T00:00:00Z",
        )
        self.assertEqual(record.as_dict()["observation_time_utc"], "2026-01-01T00:00:00Z")


if __name__ == "__main__":
    unittest.main()
