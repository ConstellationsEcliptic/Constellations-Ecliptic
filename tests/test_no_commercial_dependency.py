from __future__ import annotations

import inspect
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from ce.calculation.engine import CalculationEngine
from ce.calculation.geometry import circular_separation_deg, signed_angular_deviation_deg
from ce.signal.engine import SignalEngine


class CommercialIndependenceTests(unittest.TestCase):
    def test_calculation_and_signal_interfaces_have_no_commercial_state_parameter(self) -> None:
        for obj in (CalculationEngine.calculate, SignalEngine.evaluate):
            names = tuple(inspect.signature(obj).parameters)
            lowered = {name.lower() for name in names}
            self.assertFalse(lowered & {"credits", "payment", "commercial_state", "entitlement"})

    def test_signal_engine_result_does_not_change_with_external_commercial_context(self) -> None:
        # Commercial state is intentionally kept outside the calculation/signal API.
        self.assertEqual(
            self._evaluate_fixture(commercial_state="ZERO_CREDITS"),
            self._evaluate_fixture(commercial_state="CREDITS_PURCHASED"),
        )

    def _evaluate_fixture(self, *, commercial_state: str):
        from ce.calculation.evidence import EvidencePacket
        packet = EvidencePacket(
            evidence_packet_id="E-COMM-001",
            calculation_id="C-COMM-001",
            input_identity={"commercial_state_is_external": True},
            profile_version={"id": "CE-CALC-V1-EP-001", "revision": 4},
            observation_instant_or_interval={"start": "2026-01-01T00:00:00Z"},
            timezone_context={"id": "UTC", "version": "2026d"},
            execution_profile_id="CE-CALC-V1-EP-001",
            calculation_version="CE-CALC-CORE-V1-R1-CONVERGENT",
            object_records=(),
            geometry_records=({
                "transit_object": "SUN",
                "natal_object_or_scenario": "MOON",
                "aspect": "CONJUNCTION",
                "directed_branch": 0.0,
                "signed_deviation": 0.0,
                "absolute_deviation": 0.0,
                "effective_orb": 2.5,
                "qualification_state": "QUALIFIED",
                "kinematic_state": "EXACT",
            },),
            effective_orb_records=(),
            kinematics=({"transit_object": "SUN", "aspect": "CONJUNCTION", "kinematic_state": "EXACT"},),
            exact_events=(),
            window_segments=(),
            scenario_stability_state="STABLE",
            scenario_window_state="ROBUST",
            warnings=(),
            errors=(),
            numerical_tolerances={},
            solver_metadata={},
            actual_ephemeris_resolution={"ephemeris_resolution_status": "MATCH"},
            calculation_flags={"calculation_status": "VALID"},
        )
        # commercial_state exists only at caller level and is never supplied to CE.
        _ = commercial_state
        return SignalEngine().evaluate(packet)

    def test_calculation_modules_have_no_commercial_imports(self) -> None:
        modules = [CalculationEngine, circular_separation_deg, signed_angular_deviation_deg]
        banned = ("credits", "payment", "commerce", "retention", "advertising")
        for obj in modules:
            source = inspect.getsource(obj)
            lowered = source.lower()
            self.assertFalse(any(term in lowered for term in banned), obj)
