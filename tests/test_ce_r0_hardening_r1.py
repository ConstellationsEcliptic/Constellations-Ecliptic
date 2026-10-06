from __future__ import annotations

from datetime import date
import unittest

from ce.calculation.contracts import (
    BirthInput,
    CalculationRequest,
    CalculationResult,
    CalculationResultDraft,
)
from ce.calculation.evidence import EvidencePacket
from ce.calculation.evidence_builder import issue_evidence_packet
from ce.foundation.identity import RuntimeIdentity
from ce.foundation.provenance import derive_provenance_root_sha256, runtime_identity_sha256
from ce.foundation.status import CalculationStatus, NatalBirthState, ScenarioState, RuntimeAuthority
from ce.runtime.authority import (
    SignedProvenanceEvidence,
    SourceAuthorityEvidence,
    TrustedBuildEvidence,
    evaluate_authority_consistency,
    evaluate_full_authority,
)
from ce.runtime.gates import authorize_runtime
from ce.signal.daily import (
    aggregate_daily_evidence_packets,
    aggregate_qualified_signal_records,
    aggregate_daily_signals,
)
from ce.signal.engine import SignalResult
from ce.signal.record import QualifiedSignalRecord, issue_qualified_signal_record


def _runtime(seed: str = "a") -> RuntimeIdentity:
    return RuntimeIdentity(
        "CE-CALC-V1-EP-001",
        4,
        seed * 40,
        ("b" if seed == "a" else "c") * 64,
        "sha256:" + ("d" if seed == "a" else "e") * 64,
        "f" * 64,
        "1" * 64,
        "2" * 64,
    )


def _packet(*, request_id: str = "REQ-1", runtime: RuntimeIdentity | None = None, warning: str = "A") -> EvidencePacket:
    runtime = runtime or _runtime()
    input_identity = {
        "request_id": request_id,
        "birth_date": "2000-01-01",
        "birth_city": "Test City",
        "timezone_id": "UTC",
        "timezone_version": "2026d",
        "natal_birth_state": "ZERO_BIRTH_TIME",
        "calendar_policy_id": "CE-V1-CALENDAR-GREGORIAN-ONLY",
    }
    profile = {
        "id": "CE-CALC-V1-EP-001",
        "revision": 4,
        "implementation_plan_version": "1.3.1",
        "technical_contracts_version": "1.1",
        "execution_profile_version": "1.3",
    }
    timezone_context = {"database": "IANA", "id": "UTC", "version": "2026d"}
    runtime_digest = runtime_identity_sha256(runtime)
    root = derive_provenance_root_sha256(
        calculation_id="CALC-1",
        request_id=request_id,
        input_identity=input_identity,
        profile_version=profile,
        timezone_context=timezone_context,
        execution_profile_id="CE-CALC-V1-EP-001",
        calculation_version="CE-CALC-CORE-V1-R1-CONVERGENT",
        runtime_identity_digest=runtime_digest,
    )
    return EvidencePacket.issue(
        calculation_id="CALC-1",
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
        possible_window_segments=(),
        robust_window_segments=(),
        scenario_observations=(),
        warnings=(warning,),
        errors=(),
        numerical_tolerances={},
        solver_metadata={},
        actual_ephemeris_resolution={"ephemeris_resolution_status": "MATCH"},
        calculation_flags={"calculation_status": "VALID"},
        runtime_identity_sha256=runtime_digest,
        provenance_root_sha256=root,
    )


class CER0HardeningTests(unittest.TestCase):
    def test_builder_rejects_caller_supplied_context_and_derives_request_context(self) -> None:
        request = CalculationRequest(
            request_id="REQ-1",
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
        draft = CalculationResultDraft(
            request_id="REQ-1",
            status=CalculationStatus.NATAL_EVIDENCE_VARIABLE,
            execution_profile_id="CE-CALC-V1-EP-001",
            scenario_state=ScenarioState.VARIABLE,
            normalized_time=None,
            calculation_id="CALC-1",
            observation_interval=("2026-01-01T00:00:00Z", "2026-01-02T00:00:00Z"),
        )
        with self.assertRaises(TypeError):
            issue_evidence_packet(  # type: ignore[call-arg]
                draft,
                input_identity={},
                profile_version={"id": "CE-CALC-V1-EP-001", "revision": 4},
                timezone_context={"id": "FABRICATED", "version": "2026d"},
            )
        packet = issue_evidence_packet(draft, request=request, runtime_identity=_runtime())
        self.assertEqual(packet.input_identity["birth_city"], "Test City")
        self.assertEqual(packet.timezone_context["id"], "UTC")
        self.assertEqual(packet.runtime_identity_sha256, runtime_identity_sha256(_runtime()))
        self.assertEqual(packet.evidence_packet_id, packet.content_sha256())

    def test_result_rejects_packet_with_different_runtime_identity(self) -> None:
        packet = _packet(runtime=_runtime("a"))
        runtime_b = _runtime("c")
        provenance = {
            "source_commit": runtime_b.source_commit,
            "source_tree_sha256_v2": runtime_b.source_tree_sha256_v2,
            "dependency_lock_digest": runtime_b.dependency_lock_digest,
            "timezone_bundle_digest": runtime_b.timezone_bundle_digest,
            "ephemeris_bundle_digest": runtime_b.ephemeris_bundle_digest,
            "runtime_image_digest": runtime_b.runtime_image_digest,
            "calculation_version": "CE-CALC-CORE-V1-R1-CONVERGENT",
        }
        with self.assertRaisesRegex(ValueError, "runtime_identity_packet_mismatch|provenance_root_sha256_packet_mismatch"):
            CalculationResult(
                request_id="REQ-1",
                status=CalculationStatus.NATAL_EVIDENCE_VARIABLE,
                execution_profile_id="CE-CALC-V1-EP-001",
                scenario_state=ScenarioState.VARIABLE,
                normalized_time=None,
                calculation_id="CALC-1",
                observation_interval=("2026-01-01T00:00:00Z", "2026-01-02T00:00:00Z"),
                provenance={**provenance, "runtime_identity_sha256": runtime_identity_sha256(runtime_b), "provenance_root_sha256": packet.provenance_root_sha256},
                provenance_root_sha256=packet.provenance_root_sha256,
                _runtime_identity=runtime_b,
                _evidence_packet=packet,
            )

    def test_signal_id_changes_when_packet_content_changes(self) -> None:
        a = _packet(warning="A")
        b = _packet(warning="B")
        qa = issue_qualified_signal_record(a)
        qb = issue_qualified_signal_record(b)
        self.assertNotEqual(a.content_sha256(), b.content_sha256())
        self.assertNotEqual(qa.signal_id, qb.signal_id)
        self.assertEqual(qa.environment_pin, "sha256:" + a.runtime_identity_sha256)

    def test_daily_aggregation_rederives_from_packets(self) -> None:
        packet = _packet()
        result = aggregate_daily_evidence_packets([packet], observation_completed=True)
        self.assertEqual(result.qualifying_signal_refs[0].startswith("CE-SIGNAL-"), True)

    def test_legacy_signal_and_qsr_aggregation_paths_fail_closed(self) -> None:
        fake_signal = SignalResult(
            CalculationStatus.VALID,
            "ROBUST_EXACT_SIGNAL",
            "EXACT",
            "ROBUST",
            "FORGED:" + "0" * 64,
            True,
        )
        with self.assertRaisesRegex(ValueError, "daily_signal_result_path_removed"):
            aggregate_daily_signals([fake_signal])
        fake_record = QualifiedSignalRecord(
            "CE-QUALIFIED-SIGNAL-RECORD-V1",
            "CE-SIGNAL-FORGED",
            "FORGED:" + "0" * 64,
            "2026-01-01T00:00:00Z",
            "VALID",
            "ROBUST_EXACT_SIGNAL",
            "EXACT",
            "UNIFORM",
            True,
            False,
            "sha256:" + "0" * 64,
        )
        with self.assertRaisesRegex(ValueError, "daily_qsr_path_removed"):
            aggregate_qualified_signal_records([fake_record], observation_completed=True)

    def test_full_authority_never_returns_authorized_from_descriptive_evidence(self) -> None:
        source = SourceAuthorityEvidence("https://example.invalid/ce", "a" * 40, "b" * 64, "1" * 64, "AB" * 20)
        build = TrustedBuildEvidence("2" * 64, "a" * 40, "b" * 64, "f" * 64, "sha256:" + "d" * 64, "3" * 64, "1" * 64, "2" * 64)
        signed = SignedProvenanceEvidence("3" * 64, "AB" * 20, "1" * 64, "2" * 64)
        identity = RuntimeIdentity(
            "CE-CALC-V1-EP-001", 4, "a" * 40, "b" * 64,
            "sha256:" + "d" * 64, "f" * 64, "1" * 64, "2" * 64,
            "1" * 64, "2" * 64, "3" * 64,
        )
        self.assertTrue(evaluate_authority_consistency(identity, source=source, build=build, signed=signed).authorized)
        result = evaluate_full_authority(identity, source=source, build=build, signed=signed)
        self.assertFalse(result.authorized)
        self.assertIn("verified_authority_receipt_required", result.reasons)

    def test_current_runtime_gate_remains_fail_closed(self) -> None:
        gate = authorize_runtime(_runtime())
        self.assertIs(gate.authority, RuntimeAuthority.NON_AUTHORIZED)


if __name__ == "__main__":
    unittest.main()
