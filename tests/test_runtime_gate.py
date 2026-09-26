from __future__ import annotations

import os
import sys
import unittest
from datetime import date, time
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from ce.calculation.contracts import BirthInput, CalculationRequest
from ce.calculation.engine import CalculationEngine
from ce.ephemeris.adapter import UnavailableSwissEphemerisAdapter
from ce.foundation.identity import RuntimeIdentity
from ce.foundation.status import BirthTimeState, CalculationStatus, RuntimeAuthority, ScenarioState
from ce.runtime.gates import RuntimeGateResult


class RuntimeGateTests(unittest.TestCase):
    def _request(self, request_id: str, profile_id: str = "CE-CALC-V1-EP-001") -> CalculationRequest:
        return CalculationRequest(
            request_id=request_id,
            birth=BirthInput(
                date(2000, 1, 1),
                time(12, 0),
                BirthTimeState.EXACT,
                "Test City",
                "UTC",
                None,
            ),
            target_interval_start_utc="2000-01-01T00:00:00Z",
            target_interval_end_utc="2000-01-02T00:00:00Z",
            execution_profile_id=profile_id,
        )

    def test_missing_identity_fails_closed(self) -> None:
        identity = RuntimeIdentity("CE-CALC-V1-EP-001", 2, None, None, None, None, None, None)
        engine = CalculationEngine(identity, UnavailableSwissEphemerisAdapter())
        result = engine.calculate(self._request("T-001"))
        self.assertEqual(result.status, CalculationStatus.NON_AUTHORIZED)
        self.assertEqual(result.scenario_state, ScenarioState.NONE)

    def test_complete_identity_still_fails_closed(self) -> None:
        identity = RuntimeIdentity(
            "CE-CALC-V1-EP-001", 2,
            "a" * 40, "b" * 64, "sha256:" + "c" * 64,
            "d" * 64, "e" * 64, "f" * 64,
        )
        engine = CalculationEngine(identity, UnavailableSwissEphemerisAdapter())
        request = self._request("T-002")
        result = engine.calculate(request)
        self.assertEqual(result.status, CalculationStatus.NON_AUTHORIZED)
        self.assertEqual(result.scenario_state, ScenarioState.NONE)
        self.assertIn("source_authority_attestation_not_established", result.errors)
        self.assertIn("independent_runtime_identity_verification_not_established", result.errors)
        self.assertIsNone(result.normalized_time)

    def test_malformed_identity_is_reported(self) -> None:
        identity = RuntimeIdentity(
            "CE-CALC-V1-EP-001", 2,
            "not-a-commit", "not-a-sha", "not-a-digest",
            None, None, None,
        )
        engine = CalculationEngine(identity, UnavailableSwissEphemerisAdapter())
        result = engine.calculate(self._request("T-003"))
        self.assertEqual(result.status, CalculationStatus.NON_AUTHORIZED)
        self.assertIn("malformed:source_commit:40-hex", result.errors)
        self.assertIn("malformed:source_tree_sha256_v2:64-hex", result.errors)
        self.assertIn("malformed:runtime_image_digest:sha256-prefixed", result.errors)

    def test_noncanonical_profile_revision_fails_closed(self) -> None:
        identity = RuntimeIdentity("CE-CALC-V1-EP-001", 3, None, None, None, None, None, None)
        engine = CalculationEngine(identity, UnavailableSwissEphemerisAdapter())
        result = engine.calculate(self._request("T-004"))
        self.assertEqual(result.status, CalculationStatus.NON_AUTHORIZED)
        self.assertIn("unrecognized:execution_profile_revision", result.errors)

    def test_authorized_path_rejects_request_profile_mismatch(self) -> None:
        identity = RuntimeIdentity(
            "CE-CALC-V1-EP-001", 2,
            "a" * 40, "b" * 64, "sha256:" + "c" * 64,
            "d" * 64, "e" * 64, "f" * 64,
        )
        engine = CalculationEngine(identity, UnavailableSwissEphemerisAdapter())
        authorized = RuntimeGateResult(RuntimeAuthority.AUTHORIZED, ())
        with patch("ce.calculation.engine.authorize_runtime", return_value=authorized):
            result = engine.calculate(self._request("T-005", profile_id="OTHER-PROFILE"))
        self.assertEqual(result.status, CalculationStatus.INVALID_INPUT)
        self.assertEqual(result.errors, ("request_execution_profile_mismatch",))
