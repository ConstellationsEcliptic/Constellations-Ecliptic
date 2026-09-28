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
    def test_observation_timezone_identity_missing_fails_closed(self) -> None:
        result = resolve_observation_civil_time(
            date(2000, 1, 1), time(12, 0), "UTC", None,
            authoritative_timezone_version=None,
        )
        self.assertEqual(result.status, CalculationStatus.NON_AUTHORIZED)
        self.assertEqual(result.observation_time_state, ObservationTimeState.EXACT)
        self.assertIsNone(result.resolved_instant_utc)

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

    def test_signal_engine_does_not_invent_signal(self) -> None:
        result = SignalEngine().evaluate(object())
        self.assertEqual(result.status, CalculationStatus.NOT_IMPLEMENTED)
        self.assertFalse(result.canon_input_valid)
        self.assertIsNone(result.classification)

    def test_bad_canon_rule_does_not_fallback(self) -> None:
        from ce.canon.registry import CanonRegistryNotEstablished, get_rule
        with self.assertRaises(CanonRegistryNotEstablished):
            get_rule("CE-UNMATERIALIZED-RULE")
