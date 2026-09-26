from __future__ import annotations

import math
import os
import sys
import unittest
from datetime import date, time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from ce.calculation.contracts import BirthInput, CalculationRequest, CalculationResult, ObjectState
from ce.calculation.time import TimeResolution
from ce.foundation.status import BirthTimeState, CalculationStatus, ScenarioState
from ce.signal.engine import SignalResult


class ContractStateIntegrityTests(unittest.TestCase):
    def _provenance(self) -> dict[str, str]:
        return {
            "source_commit": "a" * 40,
            "source_tree_sha256_v2": "b" * 64,
            "dependency_lock_digest": "c" * 64,
            "timezone_bundle_digest": "d" * 64,
            "ephemeris_bundle_digest": "e" * 64,
            "runtime_image_digest": "sha256:" + "f" * 64,
            "calculation_version": "0.1.0",
        }

    def _valid_object(self) -> ObjectState:
        return ObjectState("sun", 12.5, 0.9, CalculationStatus.VALID)

    def test_valid_calculation_requires_evidence_state(self) -> None:
        with self.assertRaises(ValueError):
            CalculationResult("R", CalculationStatus.VALID, "CE-CALC-V1-EP-001", ScenarioState.STABLE, None)

    def test_valid_object_requires_finite_normalized_longitude(self) -> None:
        with self.assertRaises(ValueError):
            ObjectState("sun", math.nan, 0.1, CalculationStatus.VALID)
        with self.assertRaises(ValueError):
            ObjectState("sun", 361.0, 0.1, CalculationStatus.VALID)

    def test_valid_calculation_requires_complete_provenance(self) -> None:
        with self.assertRaises(ValueError):
            CalculationResult(
                "R", CalculationStatus.VALID, "CE-CALC-V1-EP-001", ScenarioState.STABLE,
                "2026-01-01T00:00:00Z", (self._valid_object(),), provenance={}
            )

    def test_valid_signal_requires_minimum_state(self) -> None:
        with self.assertRaises(ValueError):
            SignalResult(
                CalculationStatus.VALID, None, None, None, None, False
            )

    def test_birth_input_rejects_contradiction(self) -> None:
        birth = BirthInput(
            date(2000, 1, 1), None, BirthTimeState.EXACT, "Test City", "UTC", "2026d"
        )
        self.assertIn("inconsistent:birth_time_exact_requires_value", birth.validate())

    def test_request_rejects_bad_interval(self) -> None:
        birth = BirthInput(
            date(2000, 1, 1), time(12, 0), BirthTimeState.EXACT, "Test City", "UTC", "2026d"
        )
        request = CalculationRequest(
            "R", birth, "2026-01-02T00:00:00Z", "2026-01-01T00:00:00Z", "CE-CALC-V1-EP-001"
        )
        self.assertIn("invalid:target_interval_order", request.validate())

    def test_time_resolution_requires_consistent_state(self) -> None:
        with self.assertRaises(ValueError):
            TimeResolution(
                CalculationStatus.VALID, BirthTimeState.EXACT, None, "UTC", "2026d", None
            )
