from __future__ import annotations

import unittest

from ce.calculation.evidence import EvidencePacket
from ce.signal.engine import SignalEngine
from ce.signal.record import (
    QUALIFIED_SIGNAL_RECORD_SCHEMA_VERSION,
    issue_qualified_signal_record,
)


class QualifiedSignalRecordR1Tests(unittest.TestCase):
    def _packet(
        self,
        *,
        scenario_stability_state: str = "STABLE",
        scenario_window_state: str = "ROBUST",
        kinematic_states: tuple[str, ...] = ("EXACT",),
        exact_event: str | None = None,
    ) -> EvidencePacket:
        geometry = tuple(
            {
                "transit_object": "SUN",
                "natal_object_or_scenario": "MOON",
                "aspect": "CONJUNCTION",
                "directed_branch": 0.0,
                "signed_deviation": 0.0,
                "absolute_deviation": 0.0,
                "effective_orb": 2.5,
                "qualification_state": "QUALIFIED",
                "kinematic_state": state,
            }
            for state in kinematic_states
        )
        events = (
            {"event_time_utc": exact_event, "residual": 0.0},
        ) if exact_event is not None else ()
        return EvidencePacket(
            evidence_packet_id="E-QSR-001",
            calculation_id="C-QSR-001",
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
            geometry_records=geometry,
            effective_orb_records=(),
            kinematics=tuple(
                {
                    "transit_object": "SUN",
                    "aspect": "CONJUNCTION",
                    "kinematic_state": state,
                    "transit_speed": 1.0,
                }
                for state in kinematic_states
            ),
            exact_events=events,
            window_segments=(),
            scenario_stability_state=scenario_stability_state,
            scenario_window_state=scenario_window_state,
            warnings=(),
            errors=(),
            numerical_tolerances={"exact_epsilon": 1.0e-4},
            solver_metadata={"solver": "r1"},
            actual_ephemeris_resolution={"ephemeris_resolution_status": "MATCH"},
            calculation_flags={"calculation_status": "VALID"},
        )

    def test_robust_exact_record_is_materialized_from_evidence(self) -> None:
        packet = self._packet()
        result = SignalEngine().evaluate(packet)
        record = issue_qualified_signal_record(packet, result)

        self.assertEqual(record.schema_version, QUALIFIED_SIGNAL_RECORD_SCHEMA_VERSION)
        self.assertTrue(record.signal_id.startswith("CE-SIGNAL-"))
        self.assertEqual(record.evidence_packet_ref, result.evidence_packet_ref)
        self.assertEqual(record.timestamp_observation_utc, "2026-01-01T00:00:00Z")
        self.assertEqual(record.qualification_status, "VALID")
        self.assertEqual(record.classification, "ROBUST_EXACT_SIGNAL")
        self.assertEqual(record.kinematic_phase, "EXACT")
        self.assertEqual(record.phase_uniformity, "UNIFORM")
        self.assertTrue(record.canon_input_valid)
        self.assertFalse(record.requires_uncertainty_disclaimer)
        self.assertRegex(record.environment_pin, r"^sha256:[0-9a-f]{64}$")

    def test_possible_applying_record_requires_disclaimer(self) -> None:
        packet = self._packet(
            scenario_stability_state="VARIABLE",
            scenario_window_state="POSSIBLE",
            kinematic_states=("APPLYING",),
            exact_event="2026-01-01T12:00:00Z",
        )
        result = SignalEngine().evaluate(packet)
        self.assertEqual(result.classification, "POSSIBLE_APPROACHING_SIGNAL")
        record = issue_qualified_signal_record(packet, result)
        self.assertEqual(record.kinematic_phase, "APPLYING")
        self.assertEqual(record.phase_uniformity, "UNIFORM")
        self.assertTrue(record.requires_uncertainty_disclaimer)
        self.assertTrue(record.canon_input_valid)

    def test_possible_mixed_record_requires_disclaimer_and_marks_phase_mixed(self) -> None:
        packet = self._packet(
            scenario_stability_state="VARIABLE",
            scenario_window_state="POSSIBLE",
            kinematic_states=("APPLYING", "SEPARATING"),
            exact_event="2026-01-01T12:00:00Z",
        )
        result = SignalEngine().evaluate(packet)
        self.assertEqual(result.classification, "POSSIBLE_MIXED_SIGNAL")

        record = issue_qualified_signal_record(packet, result)
        self.assertEqual(record.classification, "POSSIBLE_MIXED_SIGNAL")
        self.assertEqual(record.kinematic_phase, "MIXED")
        self.assertEqual(record.phase_uniformity, "MIXED")
        self.assertTrue(record.requires_uncertainty_disclaimer)

    def test_signal_id_is_deterministic_for_identical_evidence(self) -> None:
        packet = self._packet()
        result = SignalEngine().evaluate(packet)
        a = issue_qualified_signal_record(packet, result)
        b = issue_qualified_signal_record(packet, result)
        self.assertEqual(a, b)

    def test_non_valid_upstream_status_is_preserved_at_signal_boundary(self) -> None:
        packet = self._packet()
        from dataclasses import replace
        unavailable = replace(
            packet,
            calculation_flags={"calculation_status": "KNOWN_UNAVAILABLE"},
        )
        result = SignalEngine().evaluate(unavailable)
        self.assertEqual(result.status.value, "KNOWN_UNAVAILABLE")
        self.assertFalse(result.canon_input_valid)
        self.assertEqual(result.classification, "DISQUALIFIED_CALCULATION_FAILURE")

    def test_unrecognized_upstream_status_fails_closed_as_calculation_failure(self) -> None:
        packet = self._packet()
        from dataclasses import replace
        malformed = replace(
            packet,
            calculation_flags={"calculation_status": "MADE_UP_STATUS"},
        )
        result = SignalEngine().evaluate(malformed)
        self.assertEqual(result.status.value, "CALCULATION_FAILURE")
        self.assertFalse(result.canon_input_valid)

    def test_non_qualifying_result_cannot_be_materialized_as_qualified_record(self) -> None:
        packet = self._packet(
            scenario_window_state="NONE",
            kinematic_states=(),
        )
        result = SignalEngine().evaluate(packet)
        with self.assertRaisesRegex(ValueError, "qualified_signal_result_not_eligible"):
            issue_qualified_signal_record(packet, result)

    def test_mixed_phase_uniformity_is_derived_from_evidence(self) -> None:
        packet = self._packet(
            scenario_stability_state="VARIABLE",
            scenario_window_state="POSSIBLE",
            kinematic_states=("APPLYING", "SEPARATING"),
            exact_event="2026-01-01T12:00:00Z",
        )
        result = SignalEngine().evaluate(packet)
        self.assertEqual(result.phase, "MIXED")
        self.assertEqual(
            issue_qualified_signal_record(packet, result).phase_uniformity,
            "MIXED",
        )

    def test_ambiguous_multi_signal_packet_is_rejected(self) -> None:
        base = self._packet()
        geometry = tuple(base.geometry_records) + (
            {
                "transit_object": "JUPITER",
                "natal_object_or_scenario": "VENUS",
                "aspect": "TRINE",
                "directed_branch": 120.0,
                "signed_deviation": 0.0,
                "absolute_deviation": 0.0,
                "effective_orb": 2.0,
                "qualification_state": "QUALIFIED",
                "kinematic_state": "EXACT",
            },
        )
        from dataclasses import replace
        packet = replace(base, geometry_records=geometry)
        result = SignalEngine().evaluate(packet)
        with self.assertRaisesRegex(ValueError, "qualified_signal_identity_ambiguous"):
            issue_qualified_signal_record(packet, result)

    def test_cross_packet_signal_result_reference_is_rejected(self) -> None:
        packet = self._packet()
        result = SignalEngine().evaluate(packet)
        other = self._packet()
        other_result = SignalEngine().evaluate(other)
        self.assertEqual(result.evidence_packet_ref, other_result.evidence_packet_ref)
        with self.assertRaisesRegex(ValueError, "qualified_signal_evidence_reference_mismatch"):
            from dataclasses import replace
            issue_qualified_signal_record(
                packet,
                replace(result, evidence_packet_ref="E-OTHER:" + "0" * 64),
            )


if __name__ == "__main__":
    unittest.main()
