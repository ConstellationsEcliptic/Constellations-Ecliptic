from __future__ import annotations

import unittest

from ce.calculation.contracts import CalculationResult, ObjectState
from ce.calculation.evidence import EvidencePacket, EvidencePacketRef
from ce.foundation.identity import RuntimeIdentity
from ce.foundation.status import CalculationStatus, ScenarioState


class EvidenceContractR1Tests(unittest.TestCase):
    def packet(self) -> EvidencePacket:
        return EvidencePacket(
            evidence_packet_id="E-001",
            calculation_id="C-001",
            input_identity={"birth_date": "2000-01-01"},
            profile_version={"id": "CE-CALC-V1-EP-001", "revision": 4},
            observation_instant_or_interval={
                "start": "2026-01-01T00:00:00Z",
                "end": "2026-01-02T00:00:00Z",
            },
            timezone_context={"id": "UTC", "version": "2026d"},
            execution_profile_id="CE-CALC-V1-EP-001",
            calculation_version="CE-CALC-CORE-V1-R1-CONVERGENT",
            object_records=({"object_id": "SUN", "object_status": "VALID", "requested_flags": 258, "actual_flags": 258, "longitude": 12.5, "latitude": 0.0, "distance": 1.0, "speed": 0.9},),
            geometry_records=(),
            effective_orb_records=({"transit_object": "SUN", "natal_object_or_scenario": "MOON", "aspect": "CONJUNCTION", "effective_orb": 2.5},),
            kinematics=({"transit_object": "SUN", "aspect": "CONJUNCTION", "kinematic_state": "EXACT", "transit_speed": 0.9},),
            exact_events=(),
            window_segments=(),
            scenario_stability_state="STABLE",
            warnings=(),
            errors=(),
            numerical_tolerances={"exact_tolerance_deg": 1e-4},
            solver_metadata={"solver_revision": "CE-SOLVER-V1-R3"},
            actual_ephemeris_resolution={"status": "NOT_ESTABLISHED"},
            calculation_flags={"requested": "SWIEPH"},
        )

    def runtime_identity(self) -> RuntimeIdentity:
        return RuntimeIdentity(
            execution_profile_id="CE-CALC-V1-EP-001",
            execution_profile_revision=4,
            source_commit="a" * 40,
            source_tree_sha256_v2="b" * 64,
            runtime_image_digest="sha256:" + "c" * 64,
            dependency_lock_digest="d" * 64,
            timezone_bundle_digest="e" * 64,
            ephemeris_bundle_digest="f" * 64,
        )

    def test_packet_is_deeply_immutable(self) -> None:
        source = {"nested": {"value": "original"}}
        packet = EvidencePacket(
            evidence_packet_id="E-002",
            calculation_id="C-002",
            input_identity=source,
            profile_version={"id": "CE-CALC-V1-EP-001", "revision": 4},
            observation_instant_or_interval={"start": "2026-01-01T00:00:00Z"},
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
        source["nested"]["value"] = "external-change"
        self.assertEqual(packet.input_identity["nested"]["value"], "original")
        with self.assertRaises(TypeError):
            packet.input_identity["nested"]["value"] = "internal-change"

    def test_compound_reference_matches_packet(self) -> None:
        packet = self.packet()
        ref = EvidencePacketRef.from_packet(packet)
        self.assertTrue(ref.matches(packet))
        self.assertEqual(ref.evidence_packet_id, "E-001")
        self.assertEqual(len(ref.content_sha256), 64)

    def test_valid_result_requires_exact_evidence_binding(self) -> None:
        packet = self.packet()
        identity = self.runtime_identity()
        result = CalculationResult(
            request_id="R-001",
            status=CalculationStatus.VALID,
            calculation_id="C-001",
            observation_interval=("2026-01-01T00:00:00Z", "2026-01-01T01:00:00Z"),
            execution_profile_id="CE-CALC-V1-EP-001",
            scenario_state=ScenarioState.STABLE,
            normalized_time="2026-01-01T00:00:00Z",
            object_states=(ObjectState("SUN", 12.5, 0.9, CalculationStatus.VALID),),
            provenance={
                "source_commit": "a" * 40,
                "source_tree_sha256_v2": "b" * 64,
                "dependency_lock_digest": "d" * 64,
                "timezone_bundle_digest": "e" * 64,
                "ephemeris_bundle_digest": "f" * 64,
                "runtime_image_digest": "sha256:" + "c" * 64,
                "calculation_version": "CE-CALC-CORE-V1-R1-CONVERGENT",
            },
            _runtime_identity=identity,
            _evidence_packet=packet,
        )
        self.assertIsNotNone(result.evidence_packet_ref)
        self.assertEqual(result.evidence_packet_ref.content_sha256, packet.content_sha256())
        self.assertEqual(result.canonical_bytes(), result.canonical_bytes())

    def test_valid_result_rejects_incomplete_provenance(self) -> None:
        packet = self.packet()
        identity = self.runtime_identity()
        with self.assertRaises(ValueError):
            CalculationResult(
                request_id="R-002",
                status=CalculationStatus.VALID,
                execution_profile_id="CE-CALC-V1-EP-001",
                scenario_state=ScenarioState.STABLE,
                normalized_time="2026-01-01T00:00:00Z",
                object_states=(ObjectState("SUN", 12.5, 0.9, CalculationStatus.VALID),),
                provenance={},
                _runtime_identity=identity,
                _evidence_packet=packet,
            )

    def test_variable_result_can_publish_evidence_without_exact_natal_time(self) -> None:
        packet = self.packet()
        identity = self.runtime_identity()
        result = CalculationResult(
            request_id="R-003",
            status=CalculationStatus.NATAL_EVIDENCE_VARIABLE,
            execution_profile_id="CE-CALC-V1-EP-001",
            scenario_state=ScenarioState.VARIABLE,
            normalized_time=None,
            calculation_id="C-003",
            observation_interval=("2026-01-01T00:00:00Z", "2026-01-02T00:00:00Z"),
            object_states=(),
            provenance={
                "source_commit": "a" * 40,
                "source_tree_sha256_v2": "b" * 64,
                "dependency_lock_digest": "d" * 64,
                "timezone_bundle_digest": "e" * 64,
                "ephemeris_bundle_digest": "f" * 64,
                "runtime_image_digest": "sha256:" + "c" * 64,
                "calculation_version": "CE-CALC-CORE-V1-R1-CONVERGENT",
            },
            _runtime_identity=identity,
            _evidence_packet=packet,
        )
        self.assertEqual(result.evidence_packet_ref.content_sha256, packet.content_sha256())

    def test_invalid_stability_state_is_rejected(self) -> None:
        packet = self.packet()
        payload = {
            "evidence_packet_id": "E-INVALID",
            "calculation_id": "C-INVALID",
            "input_identity": {"birth_date": "2000-01-01"},
            "profile_version": {"id": "CE-CALC-V1-EP-001", "revision": 4},
            "observation_instant_or_interval": {"start": "2026-01-01T00:00:00Z"},
            "timezone_context": {"id": "UTC", "version": "2026d"},
            "execution_profile_id": "CE-CALC-V1-EP-001",
            "calculation_version": "v1",
            "object_records": (),
            "geometry_records": (),
            "effective_orb_records": (),
            "kinematics": (),
            "exact_events": (),
            "window_segments": (),
            "scenario_stability_state": "UNKNOWN",
            "warnings": (),
            "errors": (),
            "numerical_tolerances": {},
            "solver_metadata": {},
            "actual_ephemeris_resolution": {},
            "calculation_flags": {},
        }
        with self.assertRaises(ValueError):
            EvidencePacket(**payload)

    def test_zero_length_window_is_rejected(self) -> None:
        base = self.packet()
        with self.assertRaises(ValueError):
            EvidencePacket(
                evidence_packet_id="E-WINDOW",
                calculation_id="C-WINDOW",
                input_identity=base.input_identity,
                profile_version=base.profile_version,
                observation_instant_or_interval=base.observation_instant_or_interval,
                timezone_context=base.timezone_context,
                execution_profile_id=base.execution_profile_id,
                calculation_version=base.calculation_version,
                object_records=base.object_records,
                geometry_records=base.geometry_records,
                effective_orb_records=base.effective_orb_records,
                kinematics=base.kinematics,
                exact_events=base.exact_events,
                window_segments=(
                    {"entry_utc": "2026-01-01T00:00:00Z", "exact_events_utc": (), "exit_utc": "2026-01-01T00:00:00Z"},
                ),
                scenario_stability_state=base.scenario_stability_state,
                warnings=base.warnings,
                errors=base.errors,
                numerical_tolerances=base.numerical_tolerances,
                solver_metadata=base.solver_metadata,
                actual_ephemeris_resolution=base.actual_ephemeris_resolution,
                calculation_flags=base.calculation_flags,
            )


if __name__ == "__main__":
    unittest.main()
