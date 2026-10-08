from __future__ import annotations

import unittest

from ce.calculation.evidence import EvidencePacket
from ce.signal.engine import SignalEngine


class SignalNoRecomputationR1Tests(unittest.TestCase):
    def _packet(self) -> tuple[EvidencePacket, dict]:
        source = {
            "geometry_state": "EXACT",
            "calculation_status": "VALID",
            "ephemeris_status": "MATCH",
        }
        packet = EvidencePacket(
            evidence_packet_id="E-NORECOMP-001",
            calculation_id="C-NORECOMP-001",
            input_identity={"source": source},
            profile_version={"id": "CE-CALC-V1-EP-001", "revision": 4},
            observation_instant_or_interval={
                "start": "2026-01-01T00:00:00Z",
                "end": "2026-01-02T00:00:00Z",
            },
            timezone_context={"id": "UTC", "version": "2026d"},
            execution_profile_id="CE-CALC-V1-EP-001",
            calculation_version="CE-CALC-CORE-V1-R1-CONVERGENT",
            object_records=(),
            geometry_records=(
                {
                    "transit_object": "SUN",
                    "natal_object_or_scenario": "MOON",
                    "aspect": "CONJUNCTION",
                    "directed_branch": 0.0,
                    "signed_deviation": 0.0,
                    "absolute_deviation": 0.0,
                    "effective_orb": 2.5,
                    "qualification_state": "QUALIFIED",
                    "kinematic_state": "EXACT",
                },
            ),
            effective_orb_records=(),
            kinematics=(
                {
                    "transit_object": "SUN",
                    "aspect": "CONJUNCTION",
                    "kinematic_state": "EXACT",
                    "transit_speed": 1.0,
                },
            ),
            exact_events=(),
            window_segments=(),
            scenario_stability_state="STABLE",
            scenario_window_state="ROBUST",
            warnings=(),
            errors=(),
            numerical_tolerances={},
            solver_metadata={},
            actual_ephemeris_resolution={
                "ephemeris_resolution_status": "MATCH"
            },
            calculation_flags={
                "calculation_status": "VALID"
            },
        )
        return packet, source

    def test_mutating_original_source_after_issuance_has_no_effect(self) -> None:
        packet, source = self._packet()
        engine = SignalEngine()

        before = engine.evaluate(packet)
        source["geometry_state"] = "APPLYING"
        source["calculation_status"] = "CALCULATION_FAILURE"
        source["ephemeris_status"] = "MISMATCH"
        after = engine.evaluate(packet)

        self.assertEqual(before, after)
        self.assertEqual(after.classification, "ROBUST_EXACT_SIGNAL")
        self.assertTrue(after.canon_input_valid)

    def test_repeated_reads_are_deterministic_without_recomputation_state(self) -> None:
        packet, _ = self._packet()
        engine = SignalEngine()
        results = [engine.evaluate(packet) for _ in range(3)]
        self.assertEqual(results[0], results[1])
        self.assertEqual(results[1], results[2])


if __name__ == "__main__":
    unittest.main()
