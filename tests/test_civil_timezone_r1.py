from __future__ import annotations

from datetime import date, datetime, time, timezone
import unittest

from ce.foundation.status import CALENDAR_POLICY_GREGORIAN_ONLY, CalculationStatus
from ce.timezone.civil import resolve_observation_civil_time, resolve_zero_birth_interval


class StubTzif:
    version = "2026d"

    def resolve_local_instant(self, local_naive: datetime, timezone_id: str) -> datetime:
        return local_naive.replace(tzinfo=timezone.utc)


class CivilTimezoneR1Tests(unittest.TestCase):
    def test_full_local_day_is_preserved(self) -> None:
        result = resolve_zero_birth_interval(
            birth_date=date(2026, 1, 1),
            timezone_id="UTC",
            timezone_version="2026d",
            calendar_policy_id=CALENDAR_POLICY_GREGORIAN_ONLY,
            tzif_runtime=StubTzif(),
        )
        self.assertEqual(result.status, CalculationStatus.NATAL_EVIDENCE_VARIABLE)
        self.assertEqual(result.local_interval_start, "2026-01-01T00:00:00")
        self.assertEqual(result.local_interval_end, "2026-01-02T00:00:00")
        self.assertEqual(result.resolved_utc_interval_start, "2026-01-01T00:00:00Z")
        self.assertEqual(result.resolved_utc_interval_end, "2026-01-02T00:00:00Z")

    def test_timezone_version_mismatch_fails_closed(self) -> None:
        class DifferentVersion(StubTzif):
            version = "2026c"

        result = resolve_zero_birth_interval(
            birth_date=date(2026, 1, 1),
            timezone_id="UTC",
            timezone_version="2026d",
            calendar_policy_id=CALENDAR_POLICY_GREGORIAN_ONLY,
            tzif_runtime=DifferentVersion(),
        )
        self.assertEqual(result.status, CalculationStatus.NON_AUTHORIZED)
        self.assertEqual(result.resolved_utc_interval_start, None)

    def test_unsupported_calendar_stops_before_resolution(self) -> None:
        class ForbiddenTzif(StubTzif):
            def resolve_local_instant(self, local_naive: datetime, timezone_id: str) -> datetime:
                raise AssertionError("timezone resolver must not be called")

        result = resolve_zero_birth_interval(
            birth_date=date(2026, 1, 1),
            timezone_id="UTC",
            timezone_version="2026d",
            calendar_policy_id="CE-V1-CALENDAR-UNSUPPORTED",
            tzif_runtime=ForbiddenTzif(),
        )
        self.assertEqual(result.status, CalculationStatus.INPUT_UNSUPPORTED)


    def test_observation_time_preserves_microseconds(self) -> None:
        result = resolve_observation_civil_time(
            observation_date=date(2026, 1, 1),
            observation_time=time(12, 34, 56, 123456),
            timezone_id="UTC",
            timezone_version="2026d",
            calendar_policy_id=CALENDAR_POLICY_GREGORIAN_ONLY,
            tzif_runtime=StubTzif(),
        )
        self.assertEqual(result.status, CalculationStatus.VALID)
        self.assertEqual(
            result.resolved_instant_utc,
            "2026-01-01T12:34:56.123456Z",
        )


    def test_observation_time_is_resolved_by_canonical_tzif_boundary(self) -> None:
        result = resolve_observation_civil_time(
            observation_date=date(2026, 1, 1),
            observation_time=time(12, 0),
            timezone_id="UTC",
            timezone_version="2026d",
            calendar_policy_id=CALENDAR_POLICY_GREGORIAN_ONLY,
            tzif_runtime=StubTzif(),
        )
        self.assertEqual(result.status, CalculationStatus.VALID)
        self.assertEqual(result.observation_time_state.value, "EXACT")
        self.assertEqual(result.resolved_instant_utc, "2026-01-01T12:00:00Z")


if __name__ == "__main__":
    unittest.main()
