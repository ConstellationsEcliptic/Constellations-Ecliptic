from __future__ import annotations

from tests.evidence_test_factory_r1 import build_test_bound_evidence_packet

from datetime import date
import unittest

from ce.calculation.contracts import (
    BirthInput,
    CalculationRequest,
    CalculationResultDraft,
    ObjectState,
)
from ce.calculation.evidence import EvidencePacket, EvidencePacketRef
from ce.calculation.evidence_builder import issue_evidence_packet
from ce.foundation.identity import RuntimeIdentity
from ce.foundation.provenance import runtime_identity_sha256
from ce.foundation.status import CalculationStatus, NatalBirthState, ScenarioState


class EvidenceContractR1Tests(unittest.TestCase):
    def runtime_identity(self) -> RuntimeIdentity:
        return RuntimeIdentity(
            "CE-CALC-V1-EP-001",
            4,
            "a" * 40,
            "b" * 64,
            "sha256:" + "c" * 64,
            "d" * 64,
            "e" * 64,
            "f" * 64,
            control_plane_sha256="9" * 64,
        )

    def request(self, request_id: str = "R-001") -> CalculationRequest:
        return CalculationRequest(
            request_id=request_id,
            birth=BirthInput(
                date(2000, 1, 1),
                "Test City",
                "UTC",
                "2026d",
                NatalBirthState.ZERO_BIRTH_TIME,
            ),
            target_interval_start_utc="2026-01-01T00:00:00Z",
            target_interval_end_utc="2026-01-02T00:00:00Z",
            execution_profile_id="CE-CALC-V1-EP-001",
        )

    def draft(self, request_id: str = "R-001", calculation_id: str = "C-001") -> CalculationResultDraft:
        return CalculationResultDraft(
            request_id=request_id,
            status=CalculationStatus.NATAL_EVIDENCE_VARIABLE,
            execution_profile_id="CE-CALC-V1-EP-001",
            scenario_state=ScenarioState.VARIABLE,
            normalized_time=None,
            calculation_id=calculation_id,
            observation_interval=("2026-01-01T00:00:00Z", "2026-01-02T00:00:00Z"),
            object_states=(),
            object_records=(),
            geometry_records=(),
            event_records=(),
            window_segments=(),
            window_classification=ScenarioState.NONE,
            possible_window_segments=(),
            robust_window_segments=(),
            scenario_observations=(),
            solver_metadata={"solver_revision": "CE-SOLVER-V1-R3"},
            actual_ephemeris_resolution={"status": "NOT_ESTABLISHED"},
            calculation_flags={"calculation_status": CalculationStatus.NATAL_EVIDENCE_VARIABLE.value},
            warnings=(),
            errors=(),
            provenance={},
        )

    def packet(self, request_id: str = "R-001", calculation_id: str = "C-001") -> EvidencePacket:
        return issue_evidence_packet(
            self.draft(request_id, calculation_id),
            request=self.request(request_id),
            runtime_identity=self.runtime_identity(),
        )

    def test_packet_is_deeply_immutable(self) -> None:
        packet = self.packet()
        original = packet.input_identity["birth_city"]
        with self.assertRaises(TypeError):
            packet.input_identity["birth_city"] = "changed"
        self.assertEqual(packet.input_identity["birth_city"], original)

    def test_post_issuance_canonical_bytes_tampering_is_detected(self) -> None:
        packet = self.packet()
        object.__setattr__(packet, "_canonical_bytes", b"TAMPERED")
        self.assertIn("invalid:_canonical_bytes:content_mismatch", packet.validate())

    def test_post_issuance_tampering_cannot_produce_valid_signal(self) -> None:
        packet = self.packet()
        object.__setattr__(packet, "_canonical_bytes", b"TAMPERED")
        from ce.signal.engine import SignalEngine
        result = SignalEngine().evaluate(packet)
        self.assertEqual(result.status, CalculationStatus.CALCULATION_FAILURE)
        self.assertFalse(result.canon_input_valid)

    def test_issued_packet_is_self_content_addressed(self) -> None:
        packet = self.packet()
        self.assertEqual(packet.evidence_packet_id, packet.content_sha256())

    def test_compound_reference_matches_packet(self) -> None:
        packet = self.packet()
        ref = EvidencePacketRef.from_packet(packet)
        self.assertTrue(ref.matches(packet))
        self.assertEqual(ref.evidence_packet_id, packet.evidence_packet_id)
        self.assertEqual(ref.content_sha256, packet.content_sha256())

    def test_draft_to_final_preserves_exact_evidence_binding(self) -> None:
        draft = self.draft("R-FINAL", "C-FINAL")
        packet = issue_evidence_packet(
            draft,
            request=self.request("R-FINAL"),
            runtime_identity=self.runtime_identity(),
        )
        result = draft.to_final(
            runtime_identity=self.runtime_identity(),
            evidence_packet=packet,
        )
        self.assertEqual(result.evidence_packet_ref.content_sha256, packet.content_sha256())
        self.assertEqual(result.provenance_root_sha256, packet.provenance_root_sha256)
        self.assertEqual(result.provenance["runtime_identity_sha256"], runtime_identity_sha256(self.runtime_identity()))

    def test_result_rejects_packet_from_different_runtime_identity(self) -> None:
        draft = self.draft("R-MISMATCH", "C-MISMATCH")
        packet = issue_evidence_packet(
            draft,
            request=self.request("R-MISMATCH"),
            runtime_identity=self.runtime_identity(),
        )
        other = RuntimeIdentity(
            "CE-CALC-V1-EP-001", 4,
            "9" * 40, "8" * 64, "sha256:" + "7" * 64,
            "6" * 64, "5" * 64, "4" * 64,
            control_plane_sha256="8" * 64,
        )
        with self.assertRaisesRegex(ValueError, "runtime_identity_packet_mismatch"):
            draft.to_final(runtime_identity=other, evidence_packet=packet)

    def test_unissued_packet_is_rejected_at_normative_result_boundary(self) -> None:
        packet = EvidencePacket(
            evidence_packet_id="fixture",
            calculation_id="C-UNISSUED",
            input_identity={"request_id": "R-UNISSUED"},
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
            scenario_stability_state="VARIABLE",
            scenario_window_state="NONE",
            warnings=(),
            errors=(),
            numerical_tolerances={},
            solver_metadata={},
            actual_ephemeris_resolution={},
            calculation_flags={},
        )
        self.assertEqual(packet.validate(), ())
        self.assertIn(
            "evidence_packet_issuance_binding_missing",
            packet.validate(require_issued=True),
        )

    def test_invalid_stability_state_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            EvidencePacket(
                evidence_packet_id="E-INVALID",
                calculation_id="C-INVALID",
                input_identity={"request_id": "R-INVALID"},
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
                scenario_stability_state="UNKNOWN",
                warnings=(),
                errors=(),
                numerical_tolerances={},
                solver_metadata={},
                actual_ephemeris_resolution={},
                calculation_flags={},
            )

    def test_zero_length_window_is_rejected(self) -> None:
        base = self.packet()
        with self.assertRaises(ValueError):
            build_test_bound_evidence_packet(
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
                scenario_window_state=base.scenario_window_state,
                warnings=base.warnings,
                errors=base.errors,
                numerical_tolerances=base.numerical_tolerances,
                solver_metadata=base.solver_metadata,
                actual_ephemeris_resolution=base.actual_ephemeris_resolution,
                calculation_flags=base.calculation_flags,
                runtime_identity_sha256=base.runtime_identity_sha256,
                provenance_root_sha256=base.provenance_root_sha256,
            )


if __name__ == "__main__":
    unittest.main()
