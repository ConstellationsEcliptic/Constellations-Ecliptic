from __future__ import annotations

import os
import sys
from datetime import date, datetime, time
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from ce.calculation.time import resolve_exact_civil_time
from ce.foundation.status import BirthTimeState, CalculationStatus
from ce.signal.engine import SignalEngine


class TimeSignalBoundaryTests(unittest.TestCase):
    def test_timezone_identity_missing_fails_closed(self) -> None:
        result = resolve_exact_civil_time(
            date(2000, 1, 1), time(12, 0), "UTC", None,
            authoritative_timezone_version=None,
        )
        self.assertEqual(result.status, CalculationStatus.NON_AUTHORIZED)
        self.assertEqual(result.birth_time_state, BirthTimeState.EXACT)
        self.assertIsNone(result.resolved_instant_utc)

    def test_datetime_birth_date_is_rejected(self) -> None:
        result = resolve_exact_civil_time(
            datetime(2000, 1, 1, 0, 0), time(12, 0), "UTC", "2026d",
            authoritative_timezone_version="2026d",
        )
        self.assertEqual(result.status, CalculationStatus.INVALID_INPUT)

    def test_zero_birth_time_is_explicit(self) -> None:
        result = resolve_exact_civil_time(
            date(2000, 1, 1), None, "UTC", "2026d",
            authoritative_timezone_version="2026d",
        )
        self.assertEqual(result.status, CalculationStatus.INVALID_INPUT)
        self.assertEqual(result.birth_time_state, BirthTimeState.ZERO_BIRTH_TIME)

    def test_valid_time_resolution_accepts_only_canonical_utc(self) -> None:
        from ce.calculation.time import TimeResolution
        with self.assertRaises(ValueError):
            TimeResolution(
                CalculationStatus.VALID, BirthTimeState.EXACT,
                "2026-01-01T00:00:00+00:00", "UTC", "2026d", None
            )
        TimeResolution(
            CalculationStatus.VALID, BirthTimeState.EXACT,
            "2026-01-01T00:00:00Z", "UTC", "2026d", None
        )

    def test_bad_timezone_version_is_rejected(self) -> None:
        result = resolve_exact_civil_time(
            date(2000, 1, 1), time(12, 0), "UTC", "bad",
            authoritative_timezone_version="bad",
        )
        self.assertEqual(result.status, CalculationStatus.INVALID_INPUT)

    def test_signal_engine_does_not_invent_signal(self) -> None:
        result = SignalEngine().evaluate(object())
        self.assertEqual(result.status, CalculationStatus.NOT_IMPLEMENTED)
        self.assertFalse(result.canon_input_valid)
        self.assertIsNone(result.classification)

    def test_bad_canon_rule_does_not_fallback(self) -> None:
        from ce.canon.registry import CanonRegistryNotEstablished, get_rule
        with self.assertRaises(CanonRegistryNotEstablished):
            get_rule("CE-UNMATERIALIZED-RULE")
