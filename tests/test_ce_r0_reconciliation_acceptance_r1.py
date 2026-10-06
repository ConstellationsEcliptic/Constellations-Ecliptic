from __future__ import annotations

"""CE-R0 adversarial acceptance tests.

These tests intentionally describe invariants that the current 29239 candidate
must NOT yet be assumed to satisfy. The suite is an audit guardrail, not a
production-authority test.
"""

from dataclasses import replace
from datetime import date
import unittest

from ce.calculation.contracts import CalculationResultDraft
from ce.calculation.evidence import EvidencePacket
from ce.calculation.evidence_builder import issue_evidence_packet
from ce.foundation.identity import RuntimeIdentity
from ce.foundation.status import CalculationStatus, ScenarioState
from ce.runtime.authority import (
    SignedProvenanceEvidence,
    SourceAuthorityEvidence,
    TrustedBuildEvidence,
    evaluate_full_authority,
)
from ce.signal.engine import SignalEngine, SignalResult
from ce.signal.record import QualifiedSignalRecord, issue_qualified_signal_record


def _packet(*, warning: str | None = None, object_record: dict | None = None) -> EvidencePacket:
    return EvidencePacket(
        evidence_packet_id="E-R0-ADV-001",
        calculation_id="C-R0-ADV-001",
        input_identity={
            "birth_date": "2026-01-01",
            "source_commit": "a" * 40,
            "source_tree_sha256_v2": "b" * 64,
        },
        profile_version={"id": "CE-CALC-V1-EP-001", "revision": 4},
        observation_instant_or_interval={
            "start": "2026-01-01T00:00:00Z",
            "end": "2026-01-02T00:00:00Z",
        },
        timezone_context={"id": "UTC", "version": "2026d"},
        execution_profile_id="CE-CALC-V1-EP-001",
        calculation_version="CE-CALC-CORE-V1-R1-CONVERGENT",
        object_records=(() if object_record is None else (object_record,)),
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
        warnings=(() if warning is None else (warning,)),
        errors=(),
        numerical_tolerances={"exact_epsilon": 1e-4},
        solver_metadata={"solver": "r0-adversarial"},
        actual_ephemeris_resolution={"ephemeris_resolution_status": "MATCH"},
        calculation_flags={"calculation_status": "VALID"},
    )


class CER0AdversarialAcceptanceTests(unittest.TestCase):
    def test_B1_evidence_issuance_must_reject_caller_substituted_identity(self) -> None:
        result = CalculationResultDraft(
            request_id="R-B1",
            status=CalculationStatus.NATAL_EVIDENCE_VARIABLE,
            execution_profile_id="CE-CALC-V1-EP-001",
            scenario_state=ScenarioState.VARIABLE,
            normalized_time=None,
            calculation_id="C-B1",
            observation_interval=("2026-01-01T00:00:00Z", "2026-01-02T00:00:00Z"),
        )
        # The request/calculation provenance is not represented by caller-
        # supplied evidence mappings. Future implementation must reject this
        # substitution rather than materialize a packet from arbitrary context.
        with self.assertRaises(ValueError):
            issue_evidence_packet(
                result,
                input_identity={"birth_date": "ATTACKER-SUBSTITUTED"},
                profile_version={"id": "CE-CALC-V1-EP-001", "revision": 4},
                timezone_context={"id": "UTC", "version": "2026d"},
            )

    def test_B2_result_and_packet_must_share_one_provenance_root(self) -> None:
        packet = _packet()
        identity = RuntimeIdentity(
            "CE-CALC-V1-EP-001",
            4,
            "a" * 40,
            "b" * 64,
            "sha256:" + "c" * 64,
            "d" * 64,
            "e" * 64,
            "f" * 64,
        )
        result = CalculationResultDraft(
            request_id="R-B2",
            status=CalculationStatus.NATAL_EVIDENCE_VARIABLE,
            execution_profile_id="CE-CALC-V1-EP-001",
            scenario_state=ScenarioState.VARIABLE,
            normalized_time=None,
            calculation_id="C-R0-ADV-001",
            observation_interval=("2026-01-01T00:00:00Z", "2026-01-02T00:00:00Z"),
            provenance={
                "source_commit": "a" * 40,
                "source_tree_sha256_v2": "b" * 64,
                "dependency_lock_digest": "d" * 64,
                "timezone_bundle_digest": "e" * 64,
                "ephemeris_bundle_digest": "f" * 64,
                "runtime_image_digest": "sha256:" + "c" * 64,
                "calculation_version": "CE-CALC-CORE-V1-R1-CONVERGENT",
            },
        )
        # Packet carries a different source-root assertion.
        mismatched_packet = replace(
            packet,
            input_identity={
                "birth_date": "2026-01-01",
                "source_commit": "9" * 40,
                "source_tree_sha256_v2": "8" * 64,
            },
        )
        # The future invariant is equality of one canonical provenance root.
        with self.assertRaises(ValueError):
            result.to_final(runtime_identity=identity, evidence_packet=mismatched_packet)

    def test_B3_QSR_must_not_accept_a_caller_forged_signal_result(self) -> None:
        packet = _packet()
        forged = SignalResult(
            status=CalculationStatus.VALID,
            classification="ROBUST_EXACT_SIGNAL",
            phase="EXACT",
            uncertainty_state="ROBUST",
            evidence_packet_ref=f"{packet.evidence_packet_id}:{packet.content_sha256()}",
            canon_input_valid=True,
        )
        with self.assertRaises(ValueError):
            issue_qualified_signal_record(packet, forged)

    def test_B4_qualified_signal_record_must_validate_its_own_invariants(self) -> None:
        with self.assertRaises(ValueError):
            QualifiedSignalRecord(
                schema_version="CE-QUALIFIED-SIGNAL-RECORD-V1",
                signal_id="not-a-canonical-signal-id",
                evidence_packet_ref="forged:reference",
                timestamp_observation_utc="not-utc",
                qualification_status="VALID",
                classification="ROBUST_EXACT_SIGNAL",
                kinematic_phase="EXACT",
                phase_uniformity="UNIFORM",
                canon_input_valid=True,
                requires_uncertainty_disclaimer=False,
                environment_pin="sha256:" + "0" * 64,
            )

    def test_B5_signal_id_must_change_when_immutable_evidence_changes(self) -> None:
        first = _packet(warning="W-A")
        second = replace(first, warnings=("W-B",))
        a = issue_qualified_signal_record(first, SignalEngine().evaluate(first))
        b = issue_qualified_signal_record(second, SignalEngine().evaluate(second))
        self.assertNotEqual(a.signal_id, b.signal_id)

    def test_B6_environment_pin_must_bind_the_complete_runtime_identity(self) -> None:
        first = _packet(object_record={
            "object_id": "SUN",
            "object_status": "VALID",
            "requested_flags": 258,
            "actual_flags": 258,
            "longitude": 10.0,
            "latitude": 0.0,
            "distance": 1.0,
            "speed": 1.0,
        })
        second = replace(first, object_records=(
            {
                "object_id": "SUN",
                "object_status": "VALID",
                "requested_flags": 258,
                "actual_flags": 258,
                "longitude": 11.0,
                "latitude": 0.0,
                "distance": 1.0,
                "speed": 1.0,
            },
        ))
        a = issue_qualified_signal_record(first, SignalEngine().evaluate(first))
        b = issue_qualified_signal_record(second, SignalEngine().evaluate(second))
        self.assertNotEqual(a.environment_pin, b.environment_pin)

    def test_B7_consistency_only_authority_evidence_must_not_authorize(self) -> None:
        runtime = RuntimeIdentity(
            "CE-CALC-V1-EP-001",
            4,
            "a" * 40,
            "b" * 64,
            "sha256:" + "c" * 64,
            "d" * 64,
            "e" * 64,
            "f" * 64,
            "1" * 64,
            "2" * 64,
            "3" * 64,
        )
        fingerprint = "ABCDEF" * 6 + "ABCD"
        source = SourceAuthorityEvidence(
            "https://example.invalid/ce",
            "a" * 40,
            "b" * 64,
            "1" * 64,
            fingerprint,
        )
        build = TrustedBuildEvidence(
            "2" * 64,
            "a" * 40,
            "b" * 64,
            "d" * 64,
            "sha256:" + "c" * 64,
            "4" * 64,
            "e" * 64,
            "f" * 64,
        )
        signed = SignedProvenanceEvidence("3" * 64, fingerprint, "1" * 64, "2" * 64)
        result = evaluate_full_authority(runtime, source=source, build=build, signed=signed)
        self.assertFalse(result.authorized, "synthetic dataclass consistency must not constitute authority")


if __name__ == "__main__":
    unittest.main()
