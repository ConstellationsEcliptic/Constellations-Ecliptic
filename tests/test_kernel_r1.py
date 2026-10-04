from __future__ import annotations

from datetime import datetime, timedelta, timezone
import unittest

from ce.calculation.contracts import ObjectRecord
from ce.calculation.kernel import (
    KernelFailure,
    calculate_aspect_window,
    calculate_zero_birth_aspect_window,
    validate_kernel_window_result,
)
from ce.foundation.status import CalculationStatus


class FakeProvider:
    """Test-only numerical source; never used by production runtime."""

    def object_state_at(self, object_id: str, instant_utc: datetime) -> ObjectRecord:
        start = datetime(2026, 1, 1, tzinfo=timezone.utc)
        seconds = (instant_utc - start).total_seconds()
        if object_id == "MOON":
            return ObjectRecord("MOON", CalculationStatus.VALID, 258, 258, 0.0, 0.0, 1.0, 0.0)
        if object_id == "SUN":
            # Test fixture: an artificial linear longitude, not astronomical data.
            return ObjectRecord("SUN", CalculationStatus.VALID, 258, 258, 59.0 + seconds / 86400.0, 0.0, 1.0, 1.0)
        return ObjectRecord(object_id, CalculationStatus.KNOWN_UNAVAILABLE, 258, None, None, None, None, None, errors=("KNOWN_UNAVAILABLE",))


class InvalidProvider(FakeProvider):
    def object_state_at(self, object_id: str, instant_utc: datetime) -> ObjectState:
        return ObjectRecord(object_id, CalculationStatus.KNOWN_UNAVAILABLE, 258, None, None, None, None, None, errors=("KNOWN_UNAVAILABLE",))


class KernelR1Tests(unittest.TestCase):
    def test_kernel_produces_event_and_window_from_provider_only(self) -> None:
        start = datetime(2026, 1, 1, tzinfo=timezone.utc)
        result = calculate_aspect_window(
            FakeProvider(),
            birth_instant_utc=start,
            target_start_utc=start,
            target_end_utc=start + timedelta(days=2),
            transit_object="SUN",
            natal_object="MOON",
            aspect="SEXTILE",
            samples=128,
        )
        validate_kernel_window_result(result)
        self.assertEqual(result.status, CalculationStatus.VALID)
        self.assertTrue(result.events)
        self.assertTrue(result.windows)
        self.assertEqual(result.events[0].instant_utc, "2026-01-02T00:00:00Z")

    def test_zero_birth_orchestrator_preserves_sampled_variable_state(self) -> None:
        start = datetime(2026, 1, 1, tzinfo=timezone.utc)
        result = calculate_zero_birth_aspect_window(
            FakeProvider(),
            birth_interval_start_utc=start,
            birth_interval_end_utc=start + timedelta(days=1),
            target_start_utc=start,
            target_end_utc=start + timedelta(days=2),
            transit_object="SUN",
            natal_object="MOON",
            aspect="SEXTILE",
            scenario_count=4,
            samples=64,
        )
        self.assertIs(result.status, CalculationStatus.NATAL_EVIDENCE_VARIABLE)
        self.assertEqual(result.scenario_state.value, "VARIABLE")
        self.assertEqual(result.scenario_count, 4)
        self.assertEqual(len(result.scenario_ids), 4)
        self.assertTrue(result.possible_segments_seconds)

    def test_zero_birth_orchestrator_rejects_bad_intervals(self) -> None:
        start = datetime(2026, 1, 1, tzinfo=timezone.utc)
        with self.assertRaisesRegex(KernelFailure, "birth_interval_order_invalid"):
            calculate_zero_birth_aspect_window(
                FakeProvider(),
                birth_interval_start_utc=start + timedelta(days=1),
                birth_interval_end_utc=start,
                target_start_utc=start,
                target_end_utc=start + timedelta(days=1),
                transit_object="SUN",
                natal_object="MOON",
                aspect="SEXTILE",
            )

    def test_invalid_provider_cannot_create_window(self) -> None:
        start = datetime(2026, 1, 1, tzinfo=timezone.utc)
        with self.assertRaisesRegex(KernelFailure, "natal_object_not_valid"):
            calculate_aspect_window(
                InvalidProvider(),
                birth_instant_utc=start,
                target_start_utc=start,
                target_end_utc=start + timedelta(days=1),
                transit_object="SUN",
                natal_object="MOON",
                aspect="SEXTILE",
                samples=32,
            )


if __name__ == "__main__":
    unittest.main()
