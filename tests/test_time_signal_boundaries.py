from __future__ import annotations

import os
import sys
import unittest
from datetime import date, time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from ce.calculation.time import (
    resolve_observation_civil_time,
    resolve_zero_birth_interval,
)
from ce.foundation.status import NatalBirthState, CalculationStatus, ObservationTimeState
from ce.signal.engine import SignalEngine


class TimeSignalBoundaryTests(unittest.TestCase):
    def test_zero_birth_interval_rejects_unsupported_calendar_policy(self) -> None:
        result = resolve_zero_birth_interval(
            date(2000, 1, 1), "UTC", "2026d",
            authoritative_timezone_version="2026d",
            calendar_policy_id="CE-V1-CALENDAR-UNSUPPORTED",
        )
        self.assertEqual(result.status, CalculationStatus.INPUT_UNSUPPORTED)
        self.assertEqual(result.natal_birth_state, NatalBirthState.ZERO_BIRTH_TIME)
        self.assertIsNone(result.resolved_utc_interval_start)
        self.assertEqual(result.error, "unsupported_calendar_policy")

    def test_observation_time_rejects_unsupported_calendar_policy(self) -> None:
        result = resolve_observation_civil_time(
            date(2000, 1, 1), time(12, 0), "UTC", "2026d",
            authoritative_timezone_version="2026d",
            calendar_policy_id="CE-V1-CALENDAR-UNSUPPORTED",
        )
        self.assertEqual(result.status, CalculationStatus.INPUT_UNSUPPORTED)
        self.assertEqual(result.observation_time_state, ObservationTimeState.INVALID)
        self.assertIsNone(result.resolved_instant_utc)
        self.assertEqual(result.error, "unsupported_calendar_policy")

    def test_observation_time_missing_is_invalid_input(self) -> None:
        result = resolve_observation_civil_time(
            date(2000, 1, 1), None, "UTC", "2026d",
            authoritative_timezone_version="2026d",
        )
        self.assertEqual(result.status, CalculationStatus.INVALID_INPUT)
        self.assertEqual(result.observation_time_state, ObservationTimeState.INVALID)
        self.assertIsNone(result.resolved_instant_utc)
        self.assertEqual(result.error, "explicit_observation_time_required")

    def test_observation_timezone_version_mismatch_fails_closed(self) -> None:
        result = resolve_observation_civil_time(
            date(2000, 1, 1), time(12, 0), "UTC", "2025a",
            authoritative_timezone_version="2026d",
        )
        self.assertEqual(result.status, CalculationStatus.NON_AUTHORIZED)
        self.assertEqual(result.observation_time_state, ObservationTimeState.EXACT)
        self.assertIsNone(result.resolved_instant_utc)
        self.assertEqual(result.error, "authoritative_timezone_identity_not_established")

    def test_zero_birth_time_timezone_version_mismatch_fails_closed(self) -> None:
        result = resolve_zero_birth_interval(
            date(2000, 1, 1), "UTC", "2025a",
            authoritative_timezone_version="2026d",
        )
        self.assertEqual(result.status, CalculationStatus.NON_AUTHORIZED)
        self.assertEqual(result.natal_birth_state, NatalBirthState.ZERO_BIRTH_TIME)
        self.assertIsNone(result.resolved_utc_interval_start)
        self.assertIsNone(result.resolved_utc_interval_end)
        self.assertEqual(result.error, "authoritative_timezone_identity_not_established")

    def test_zero_birth_interval_handles_gregorian_leap_day_boundary(self) -> None:
        result = resolve_zero_birth_interval(
            date(2000, 2, 29), "UTC", "2026d",
            authoritative_timezone_version=None,
        )
        self.assertEqual(result.local_interval_start, "2000-02-29T00:00:00")
        self.assertEqual(result.local_interval_end, "2000-03-01T00:00:00")
        self.assertIsNone(result.resolved_utc_interval_start)

    def test_zero_birth_time_is_engine_interval_not_exact_time(self) -> None:
        result = resolve_zero_birth_interval(
            date(2000, 1, 1), "UTC", "2026d",
            authoritative_timezone_version="2026d",
        )
        self.assertEqual(result.status, CalculationStatus.NON_AUTHORIZED)
        self.assertEqual(result.natal_birth_state, NatalBirthState.ZERO_BIRTH_TIME)
        self.assertEqual(result.local_interval_start, "2000-01-01T00:00:00")
        self.assertEqual(result.local_interval_end, "2000-01-02T00:00:00")
        self.assertIsNone(result.resolved_utc_interval_start)
        self.assertIsNone(result.resolved_utc_interval_end)

    def _signal_packet(
        self,
        *,
        calculation_status: str = "VALID",
        ephemeris_resolution_status: str = "MATCH",
        errors: tuple[str, ...] = (),
    ) -> EvidencePacket:
        return EvidencePacket(
            evidence_packet_id="E-SIGNAL-001",
            calculation_id="C-SIGNAL-001",
            input_identity={"birth_date": "2026-01-01"},
            profile_version={"id": "CE-CALC-V1-EP-001", "revision": 4},
            observation_instant_or_interval={
                "start": "2026-01-01T00:00:00Z",
                "end": "2026-01-02T00:00:00Z",
            },
            timezone_context={"id": "UTC", "version": "2026d"},
            execution_profile_id="CE-CALC-V1-EP-001",
            calculation_version="CE-CALC-CORE-V1-R1-CONVERGENT",
            object_records=(),
            geometry_records=(),
            effective_orb_records=(),
            kinematics=(),
            exact_events=(),
            window_segments=(),
            scenario_stability_state="STABLE",
            warnings=(),
            errors=errors,
            numerical_tolerances={},
            solver_metadata={},
            actual_ephemeris_resolution={
                "ephemeris_resolution_status": ephemeris_resolution_status
            },
            calculation_flags={"calculation_status": calculation_status},
        )

    def test_signal_engine_rejects_non_evidence_input_fail_closed(self) -> None:
        result = SignalEngine().evaluate(object())
        self.assertEqual(result.status, CalculationStatus.CALCULATION_FAILURE)
        self.assertFalse(result.canon_input_valid)
        self.assertIsNone(result.classification)

    def test_signal_engine_accepts_integrity_gate_but_does_not_invent_qualification(self) -> None:
        result = SignalEngine().evaluate(self._signal_packet())
        self.assertEqual(result.status, CalculationStatus.NOT_IMPLEMENTED)
        self.assertFalse(result.canon_input_valid)
        self.assertIsNone(result.classification)
        self.assertTrue(result.evidence_packet_ref)
        self.assertIn("E-SIGNAL-001:", result.evidence_packet_ref)

    def test_signal_engine_rejects_calculation_failure(self) -> None:
        result = SignalEngine().evaluate(
            self._signal_packet(calculation_status="CALCULATION_FAILURE")
        )
        self.assertEqual(result.status, CalculationStatus.CALCULATION_FAILURE)
        self.assertFalse(result.canon_input_valid)

    def test_signal_engine_rejects_ephemeris_mismatch(self) -> None:
        result = SignalEngine().evaluate(
            self._signal_packet(ephemeris_resolution_status="MISMATCH")
        )
        self.assertEqual(result.status, CalculationStatus.CALCULATION_FAILURE)
        self.assertFalse(result.canon_input_valid)

    def test_signal_engine_rejects_packet_errors(self) -> None:
        result = SignalEngine().evaluate(
            self._signal_packet(errors=("CALCULATION_FAILURE",))
        )
        self.assertEqual(result.status, CalculationStatus.CALCULATION_FAILURE)
        self.assertFalse(result.canon_input_valid)

    def test_bad_canon_rule_does_not_fallback(self) -> None:
        from ce.canon.registry import CanonRegistryNotEstablished, get_rule
        with self.assertRaises(CanonRegistryNotEstablished):
            get_rule("CE-UNMATERIALIZED-RULE")
