from __future__ import annotations

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from ce.calculation.contracts import BirthInput, CalculationRequest
from ce.calculation.engine import CalculationEngine
from ce.ephemeris.adapter import UnavailableSwissEphemerisAdapter
from ce.foundation.identity import RuntimeIdentity
from ce.foundation.status import CalculationStatus, NatalBirthState, ScenarioState
from datetime import date


class RuntimeGateTests(unittest.TestCase):
    def test_v1_birth_input_has_no_exact_birth_time_field(self) -> None:
        birth = BirthInput(
            birth_date=date(2000, 1, 1),
            birth_city="Test City",
            timezone_id="UTC",
            timezone_version="2026d",
        )
        self.assertEqual(birth.natal_birth_state, NatalBirthState.ZERO_BIRTH_TIME)
        self.assertFalse(hasattr(birth, "birth_time"))

    def test_contract_statuses_are_materialized(self) -> None:
        self.assertEqual(CalculationStatus.KNOWN_UNAVAILABLE.value, "KNOWN_UNAVAILABLE")
        self.assertEqual(
            CalculationStatus.NATAL_EVIDENCE_VARIABLE.value,
            "NATAL_EVIDENCE_VARIABLE",
        )

    def test_unsupported_calendar_policy_fails_before_runtime_gate(self) -> None:
        identity = RuntimeIdentity("CE-CALC-V1-EP-001", 4, None, None, None, None, None, None)
        engine = CalculationEngine(identity, UnavailableSwissEphemerisAdapter())
        request = CalculationRequest(
            request_id="T-CALENDAR-001",
            birth=BirthInput(date(2000, 1, 1), "Test City", "UTC", None),
            target_interval_start_utc="2000-01-01T00:00:00Z",
            target_interval_end_utc="2000-01-02T00:00:00Z",
            execution_profile_id="CE-CALC-V1-EP-001",
            calendar_policy_id="CE-V1-CALENDAR-UNSUPPORTED",
        )
        result = engine.calculate(request)
        self.assertEqual(result.status, CalculationStatus.INPUT_UNSUPPORTED)
        self.assertEqual(result.scenario_state, ScenarioState.NONE)
        self.assertIn("unsupported_calendar_policy", result.errors)
        self.assertIsNone(result.normalized_time)

    def test_calendar_policy_precedes_invalid_natal_state(self) -> None:
        identity = RuntimeIdentity("CE-CALC-V1-EP-001", 4, None, None, None, None, None, None)
        engine = CalculationEngine(identity, UnavailableSwissEphemerisAdapter())
        request = CalculationRequest(
            request_id="T-CALENDAR-PRECEDENCE-001",
            birth=BirthInput(
                date(2000, 1, 1),
                "Test City",
                "UTC",
                None,
                NatalBirthState.INVALID,
            ),
            target_interval_start_utc="2000-01-01T00:00:00Z",
            target_interval_end_utc="2000-01-02T00:00:00Z",
            execution_profile_id="CE-CALC-V1-EP-001",
            calendar_policy_id="CE-V1-CALENDAR-UNSUPPORTED",
        )
        result = engine.calculate(request)
        self.assertEqual(result.status, CalculationStatus.INPUT_UNSUPPORTED)
        self.assertIn("unsupported_calendar_policy", result.errors)

    def test_supported_calendar_policy_reaches_runtime_gate(self) -> None:
        identity = RuntimeIdentity("CE-CALC-V1-EP-001", 4, None, None, None, None, None, None)
        engine = CalculationEngine(identity, UnavailableSwissEphemerisAdapter())
        request = CalculationRequest(
            request_id="T-CALENDAR-SUPPORTED-001",
            birth=BirthInput(date(2000, 1, 1), "Test City", "UTC", None),
            target_interval_start_utc="2000-01-01T00:00:00Z",
            target_interval_end_utc="2000-01-02T00:00:00Z",
            execution_profile_id="CE-CALC-V1-EP-001",
        )
        result = engine.calculate(request)
        self.assertEqual(result.status, CalculationStatus.NON_AUTHORIZED)
        self.assertNotIn("unsupported_calendar_policy", result.errors)

    def test_invalid_natal_state_fails_before_runtime_gate(self) -> None:
        identity = RuntimeIdentity("CE-CALC-V1-EP-001", 4, None, None, None, None, None, None)
        engine = CalculationEngine(identity, UnavailableSwissEphemerisAdapter())
        request = CalculationRequest(
            request_id="T-NATAL-INVALID-001",
            birth=BirthInput(
                date(2000, 1, 1),
                "Test City",
                "UTC",
                None,
                NatalBirthState.INVALID,
            ),
            target_interval_start_utc="2000-01-01T00:00:00Z",
            target_interval_end_utc="2000-01-02T00:00:00Z",
            execution_profile_id="CE-CALC-V1-EP-001",
        )
        result = engine.calculate(request)
        self.assertEqual(result.status, CalculationStatus.INVALID_INPUT)
        self.assertEqual(result.scenario_state, ScenarioState.NONE)
        self.assertIn("invalid_natal_birth_state", result.errors)
        self.assertIsNone(result.normalized_time)

    def test_missing_identity_fails_closed(self) -> None:
        identity = RuntimeIdentity("CE-CALC-V1-EP-001", 4, None, None, None, None, None, None)
        engine = CalculationEngine(identity, UnavailableSwissEphemerisAdapter())
        request = CalculationRequest(
            request_id="T-001",
            birth=BirthInput(date(2000, 1, 1), "Test City", "UTC", None),
            target_interval_start_utc="2000-01-01T00:00:00Z",
            target_interval_end_utc="2000-01-02T00:00:00Z",
            execution_profile_id="CE-CALC-V1-EP-001",
        )
        result = engine.calculate(request)
        self.assertEqual(result.status, CalculationStatus.NON_AUTHORIZED)
        self.assertEqual(result.scenario_state, ScenarioState.NONE)

    def test_complete_identity_still_fails_closed(self) -> None:
        identity = RuntimeIdentity(
            "CE-CALC-V1-EP-001", 4,
            "a" * 40, "b" * 64, "sha256:" + "c" * 64,
            "d" * 64, "e" * 64, "f" * 64,
        )
        engine = CalculationEngine(identity, UnavailableSwissEphemerisAdapter())
        request = CalculationRequest(
            request_id="T-002",
            birth=BirthInput(date(2000, 1, 1), "Test City", "UTC", None),
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
