from __future__ import annotations

import math
import os
import sys
import unittest
from datetime import date, datetime, time

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

    def test_valid_calculation_rejects_malformed_provenance_identity(self) -> None:
        provenance = self._provenance()
        provenance["source_commit"] = "not-a-commit"
        with self.assertRaises(ValueError):
            CalculationResult(
                "R", CalculationStatus.VALID, "CE-CALC-V1-EP-001", ScenarioState.STABLE,
                "2026-01-01T00:00:00Z", (self._valid_object(),), provenance=provenance
            )

    def test_valid_calculation_requires_complete_provenance(self) -> None:
        with self.assertRaises(ValueError):
            CalculationResult(
                "R", CalculationStatus.VALID, "CE-CALC-V1-EP-001", ScenarioState.STABLE,
                "2026-01-01T00:00:00Z", (self._valid_object(),), provenance={}
            )

    def test_nonvalid_calculation_rejects_invalid_request_id(self) -> None:
        with self.assertRaisesRegex(ValueError, "invalid:request_id"):
            CalculationResult(
                "", CalculationStatus.NON_AUTHORIZED, "CE-CALC-V1-EP-001",
                ScenarioState.NONE, None
            )

    def test_nonvalid_calculation_rejects_noncanonical_execution_profile(self) -> None:
        with self.assertRaisesRegex(ValueError, "invalid:execution_profile_id:canonical_required"):
            CalculationResult(
                "R", CalculationStatus.NON_AUTHORIZED, "OTHER-PROFILE",
                ScenarioState.NONE, None
            )

    def test_nonvalid_calculation_rejects_malformed_normalized_time(self) -> None:
        with self.assertRaisesRegex(ValueError, "invalid:normalized_time"):
            CalculationResult(
                "R", CalculationStatus.NON_AUTHORIZED, "CE-CALC-V1-EP-001",
                ScenarioState.NONE, "2026-01-01T00:00:00+00:00"
            )

    def test_nonvalid_calculation_rejects_valid_object_state(self) -> None:
        with self.assertRaisesRegex(
            ValueError, "nonvalid_result_cannot_contain_valid_object_state"
        ):
            CalculationResult(
                "R", CalculationStatus.NON_AUTHORIZED, "CE-CALC-V1-EP-001",
                ScenarioState.NONE, None, (self._valid_object(),)
            )

    def test_valid_signal_requires_minimum_state(self) -> None:
        with self.assertRaises(ValueError):
            SignalResult(
                CalculationStatus.VALID, None, None, None, None, False
            )

    def test_nonvalid_object_constructor_closes_invalid_object_id(self) -> None:
        with self.assertRaisesRegex(ValueError, "invalid:object_id"):
            ObjectState("", None, None, CalculationStatus.NON_AUTHORIZED)

    def test_nonvalid_object_constructor_closes_invalid_numeric_shape(self) -> None:
        with self.assertRaisesRegex(
            ValueError, "nonvalid_object_longitude_must_be_finite_or_none"
        ):
            ObjectState("sun", math.nan, None, CalculationStatus.NON_AUTHORIZED)

    def test_valid_object_rejects_bool_as_numeric(self) -> None:
        with self.assertRaises(ValueError):
            ObjectState("sun", True, 0.1, CalculationStatus.VALID)
        with self.assertRaises(ValueError):
            ObjectState("sun", 12.5, True, CalculationStatus.VALID)

    def test_birth_input_constructor_closes_invalid_state(self) -> None:
        with self.assertRaisesRegex(ValueError, "invalid:birth_date"):
            BirthInput(
                datetime(2000, 1, 1, 0, 0), time(12, 0), BirthTimeState.EXACT,
                "Test City", "UTC", "2026d"
            )

    def test_birth_input_constructor_closes_contradiction(self) -> None:
        with self.assertRaisesRegex(
            ValueError, "inconsistent:birth_time_exact_requires_value"
        ):
            BirthInput(
                date(2000, 1, 1), None, BirthTimeState.EXACT, "Test City", "UTC", "2026d"
            )

    def test_request_constructor_closes_bad_interval(self) -> None:
        birth = BirthInput(
            date(2000, 1, 1), time(12, 0), BirthTimeState.EXACT, "Test City", "UTC", "2026d"
        )
        with self.assertRaisesRegex(ValueError, "invalid:target_interval_order"):
            CalculationRequest(
                "R", birth, "2026-01-02T00:00:00Z", "2026-01-01T00:00:00Z",
                "CE-CALC-V1-EP-001"
            )

    def test_nonvalid_signal_rejects_semantic_payload(self) -> None:
        with self.assertRaises(ValueError):
            SignalResult(
                CalculationStatus.NON_AUTHORIZED, "classification", None, None, None, False
            )

    def test_valid_time_resolution_requires_canonical_utc(self) -> None:
        with self.assertRaises(ValueError):
            TimeResolution(
                CalculationStatus.VALID, BirthTimeState.EXACT,
                "2026-01-01T00:00:00+00:00", "UTC", "2026d", None
            )
        TimeResolution(
            CalculationStatus.VALID, BirthTimeState.EXACT,
            "2026-01-01T00:00:00Z", "UTC", "2026d", None
        )

    def test_time_resolution_requires_consistent_state(self) -> None:
        with self.assertRaises(ValueError):
            TimeResolution(
                CalculationStatus.VALID, BirthTimeState.EXACT, None, "UTC", "2026d", None
            )

    def test_calculation_engine_rejects_wrong_runtime_identity_type(self) -> None:
        from ce.calculation.engine import CalculationEngine
        from ce.ephemeris.adapter import UnavailableSwissEphemerisAdapter

        with self.assertRaisesRegex(ValueError, "invalid:runtime_identity:type_required"):
            CalculationEngine(object(), UnavailableSwissEphemerisAdapter())  # type: ignore[arg-type]

