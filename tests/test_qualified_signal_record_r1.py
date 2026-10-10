from __future__ import annotations

from tests.evidence_test_factory_r1 import build_test_bound_evidence_packet

import unittest

from ce.calculation.evidence import EvidencePacket
from ce.foundation.identity import RuntimeIdentity
from ce.foundation.provenance import derive_provenance_root_sha256, runtime_identity_sha256
from ce.signal.engine import SignalEngine
from ce.signal.record import (
    QUALIFIED_SIGNAL_RECORD_SCHEMA_VERSION,
    issue_qualified_signal_record,
    signal_geometry_identities,
)


class QualifiedSignalRecordR1Tests(unittest.TestCase):
    def _packet(
        self,
        *,
        scenario_window_state: str = "ROBUST",
        kinematic_states: tuple[str, ...] = ("EXACT",),
        exact_event: str | None = None,
        warning: str = "A",
    ) -> EvidencePacket:
        runtime = RuntimeIdentity(
            "CE-CALC-V1-EP-001", 4,
            "a" * 40, "b" * 64, "sha256:" + "c" * 64,
            "d" * 64, "e" * 64, "f" * 64,
            control_plane_sha256="9" * 64,
        )
        input_identity = {
            "request_id": "R-QSR",
            "birth_date": "2000-01-01",
            "birth_city": "Test City",
            "timezone_id": "UTC",
            "timezone_version": "2026d",
            "natal_birth_state": "ZERO_BIRTH_TIME",
            "calendar_policy_id": "CE-V1-CALENDAR-GREGORIAN-ONLY",
        }
        profile = {"id": "CE-CALC-V1-EP-001", "revision": 4}
        timezone_context = {"id": "UTC", "version": "2026d", "database": "IANA"}
        runtime_digest = runtime_identity_sha256(runtime)
        root = derive_provenance_root_sha256(
            calculation_id="C-QSR",
            request_id="R-QSR",
            input_identity=input_identity,
            profile_version=profile,
            timezone_context=timezone_context,
            execution_profile_id="CE-CALC-V1-EP-001",
            calculation_version="CE-CALC-CORE-V1-R1-CONVERGENT",
            runtime_identity_digest=runtime_digest,
        )
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
            ({"event_time_utc": exact_event, "residual": 0.0},)
            if exact_event is not None
            else ()
        )
        return build_test_bound_evidence_packet(
            calculation_id="C-QSR",
            input_identity=input_identity,
            profile_version=profile,
            observation_instant_or_interval={
                "start": "2026-01-01T00:00:00Z",
                "end": "2026-01-02T00:00:00Z",
            },
            timezone_context=timezone_context,
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
            scenario_stability_state="VARIABLE" if scenario_window_state != "ROBUST" else "STABLE",
            scenario_window_state=scenario_window_state,
            warnings=(warning,),
            errors=(),
            numerical_tolerances={},
            solver_metadata={},
            actual_ephemeris_resolution={"ephemeris_resolution_status": "MATCH"},
            calculation_flags={"calculation_status": "VALID"},
            runtime_identity_sha256=runtime_digest,
            provenance_root_sha256=root,
        )

    def test_geometry_identity_extractor_matches_qsr_identity_contract(self) -> None:
        packet = self._packet()
        self.assertEqual(
            signal_geometry_identities(packet),
            {("SUN", "MOON", "CONJUNCTION", 0.0)},
        )

    def test_robust_exact_record_is_materialized(self) -> None:
        record = issue_qualified_signal_record(self._packet())
        self.assertEqual(record.schema_version, QUALIFIED_SIGNAL_RECORD_SCHEMA_VERSION)
        self.assertTrue(record.signal_id.startswith("CE-SIGNAL-"))
        self.assertTrue(record.evidence_packet_ref.endswith(":" + record.evidence_packet_ref.split(":", 1)[1]))
        self.assertEqual(record.timestamp_observation_utc, "2026-01-01T00:00:00Z")
        self.assertEqual(record.qualification_status, "VALID")
        self.assertEqual(record.classification, "ROBUST_EXACT_SIGNAL")
        self.assertEqual(record.kinematic_phase, "EXACT")
        self.assertEqual(record.phase_uniformity, "UNIFORM")
        self.assertTrue(record.canon_input_valid)
        self.assertFalse(record.requires_uncertainty_disclaimer)

    def test_possible_applying_record_requires_disclaimer(self) -> None:
        record = issue_qualified_signal_record(
            self._packet(
                scenario_window_state="POSSIBLE",
                kinematic_states=("APPLYING",),
                exact_event="2026-01-01T12:00:00Z",
            )
        )
        self.assertEqual(record.classification, "POSSIBLE_APPROACHING_SIGNAL")
        self.assertTrue(record.requires_uncertainty_disclaimer)

    def test_possible_mixed_record_requires_disclaimer(self) -> None:
        record = issue_qualified_signal_record(
            self._packet(
                scenario_window_state="POSSIBLE",
                kinematic_states=("APPLYING", "SEPARATING"),
                exact_event="2026-01-01T12:00:00Z",
            )
        )
        self.assertEqual(record.classification, "POSSIBLE_MIXED_SIGNAL")
        self.assertEqual(record.kinematic_phase, "MIXED")
        self.assertEqual(record.phase_uniformity, "MIXED")
        self.assertTrue(record.requires_uncertainty_disclaimer)

    def test_signal_id_is_deterministic_for_identical_evidence(self) -> None:
        a = issue_qualified_signal_record(self._packet())
        b = issue_qualified_signal_record(self._packet())
        self.assertEqual(a, b)

    def test_distinct_packet_content_produces_distinct_signal_id(self) -> None:
        a = issue_qualified_signal_record(self._packet(warning="A"))
        b = issue_qualified_signal_record(self._packet(warning="B"))
        self.assertNotEqual(a.signal_id, b.signal_id)
        self.assertEqual(a.environment_pin, b.environment_pin)

    def test_non_qualifying_packet_cannot_be_materialized(self) -> None:
        packet = self._packet(
            scenario_window_state="NONE",
            kinematic_states=(),
        )
        with self.assertRaisesRegex(ValueError, "qualified_signal_result_not_eligible"):
            issue_qualified_signal_record(packet)

    def test_ambiguous_multi_signal_packet_is_rejected(self) -> None:
        from ce.foundation.identity import RuntimeIdentity
        from ce.foundation.provenance import derive_provenance_root_sha256, runtime_identity_sha256
        runtime = RuntimeIdentity(
            "CE-CALC-V1-EP-001", 4,
            "a" * 40, "b" * 64, "sha256:" + "c" * 64,
            "d" * 64, "e" * 64, "f" * 64,
            control_plane_sha256="9" * 64,
        )
        from dataclasses import replace
        base = self._packet()
        input_identity = dict(base.input_identity)
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
        profile = dict(base.profile_version)
        timezone_context = dict(base.timezone_context)
        root = derive_provenance_root_sha256(
            calculation_id=base.calculation_id,
            request_id=input_identity["request_id"],
            input_identity=input_identity,
            profile_version=profile,
            timezone_context=timezone_context,
            execution_profile_id=base.execution_profile_id,
            calculation_version=base.calculation_version,
            runtime_identity_digest=runtime_identity_sha256(runtime),
        )
        packet = build_test_bound_evidence_packet(
            calculation_id=base.calculation_id,
            input_identity=input_identity,
            profile_version=profile,
            observation_instant_or_interval=dict(base.observation_instant_or_interval),
            timezone_context=timezone_context,
            execution_profile_id=base.execution_profile_id,
            calculation_version=base.calculation_version,
            object_records=base.object_records,
            geometry_records=geometry,
            effective_orb_records=base.effective_orb_records,
            kinematics=base.kinematics,
            exact_events=base.exact_events,
            window_segments=base.window_segments,
            scenario_stability_state=base.scenario_stability_state,
            scenario_window_state=base.scenario_window_state,
            warnings=base.warnings,
            errors=base.errors,
            numerical_tolerances=base.numerical_tolerances,
            solver_metadata=base.solver_metadata,
            actual_ephemeris_resolution=base.actual_ephemeris_resolution,
            calculation_flags=base.calculation_flags,
            runtime_identity_sha256=runtime_identity_sha256(runtime),
            provenance_root_sha256=root,
        )
        self.assertEqual(len(signal_geometry_identities(packet)), 2)
        with self.assertRaisesRegex(ValueError, "qualified_signal_identity_ambiguous"):
            issue_qualified_signal_record(packet)

    def test_duplicate_geometry_records_share_one_canonical_identity(self) -> None:
        packet = self._packet(kinematic_states=("EXACT", "EXACT"))
        self.assertEqual(
            signal_geometry_identities(packet),
            {("SUN", "MOON", "CONJUNCTION", 0.0)},
        )

    def test_unissued_packet_is_rejected_before_qsr(self) -> None:
        packet = EvidencePacket(
            evidence_packet_id="fixture",
            calculation_id="C-FIX",
            input_identity={"request_id": "R-FIX"},
            profile_version={"id": "CE-CALC-V1-EP-001", "revision": 4},
            observation_instant_or_interval={
                "start": "2026-01-01T00:00:00Z",
                "end": "2026-01-02T00:00:00Z",
            },
            timezone_context={"id": "UTC", "version": "2026d"},
            execution_profile_id="CE-CALC-V1-EP-001",
            calculation_version="v1",
            object_records=(),
            geometry_records=(),
            effective_orb_records=(),
            kinematics=(),
            exact_events=(),
            window_segments=(),
            scenario_stability_state="STABLE",
            warnings=(),
            errors=(),
            numerical_tolerances={},
            solver_metadata={},
            actual_ephemeris_resolution={},
            calculation_flags={},
        )
        with self.assertRaisesRegex(ValueError, "qualified_signal_evidence"):
            issue_qualified_signal_record(packet)


if __name__ == "__main__":
    unittest.main()
