from __future__ import annotations

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from ce.calculation.contracts import BirthInput, CalculationRequest
from ce.calculation.engine import CalculationEngine
from ce.ephemeris.adapter import UnavailableSwissEphemerisAdapter
from ce.foundation.identity import RuntimeIdentity
from ce.foundation.status import BirthTimeState, CalculationStatus, ScenarioState
from datetime import date, time


class RuntimeGateTests(unittest.TestCase):
    def test_missing_identity_fails_closed(self) -> None:
        identity = RuntimeIdentity("CE-CALC-V1-EP-001", 2, None, None, None, None, None, None)
        engine = CalculationEngine(identity, UnavailableSwissEphemerisAdapter())
        request = CalculationRequest(
            request_id="T-001",
            birth=BirthInput(date(2000, 1, 1), time(12, 0), BirthTimeState.EXACT, "Test City", "UTC", None),
            target_interval_start_utc="2000-01-01T00:00:00Z",
            target_interval_end_utc="2000-01-02T00:00:00Z",
            execution_profile_id="CE-CALC-V1-EP-001",
        )
        result = engine.calculate(request)
        self.assertEqual(result.status, CalculationStatus.NON_AUTHORIZED)
        self.assertEqual(result.scenario_state, ScenarioState.NONE)

    def test_complete_identity_still_fails_closed(self) -> None:
        identity = RuntimeIdentity(
            "CE-CALC-V1-EP-001", 2,
            "a" * 40, "b" * 64, "sha256:" + "c" * 64,
            "d" * 64, "e" * 64, "f" * 64,
        )
        engine = CalculationEngine(identity, UnavailableSwissEphemerisAdapter())
        request = CalculationRequest(
            request_id="T-002",
            birth=BirthInput(date(2000, 1, 1), None, BirthTimeState.ZERO_BIRTH_TIME, "Test City", "UTC", None),
            target_interval_start_utc="2000-01-01T00:00:00Z",
            target_interval_end_utc="2000-01-02T00:00:00Z",
            execution_profile_id="CE-CALC-V1-EP-001",
        )
        result = engine.calculate(request)
        self.assertEqual(result.status, CalculationStatus.NON_AUTHORIZED)
        self.assertEqual(result.scenario_state, ScenarioState.NONE)
        self.assertIn("source_authority_attestation_not_established", result.errors)
        self.assertIn("independent_runtime_identity_verification_not_established", result.errors)
        self.assertIsNone(result.normalized_time)
