from __future__ import annotations

from dataclasses import replace
from datetime import date
import json

from ce.calculation.contracts import BirthInput, CalculationRequest, CalculationResult, CalculationResultDraft
from ce.calculation.evidence import EvidencePacket
from ce.calculation.evidence_builder import issue_evidence_packet
from ce.foundation.identity import RuntimeIdentity
from ce.foundation.status import CalculationStatus, NatalBirthState, ScenarioState, RuntimeAuthority
from ce.runtime.authority import (
    SignedProvenanceEvidence,
    SourceAuthorityEvidence,
    TrustedBuildEvidence,
    evaluate_full_authority,
)
from ce.runtime.gates import authorize_runtime
from ce.signal.engine import SignalEngine, SignalResult
from ce.signal.record import QualifiedSignalRecord
from ce.signal.daily import aggregate_qualified_signal_records


def runtime_identity() -> RuntimeIdentity:
    return RuntimeIdentity(
        "CE-CALC-V1-EP-001",
        4,
        "a" * 40,
        "b" * 64,
        "sha256:" + "c" * 64,
        "d" * 64,
        "e" * 64,
        "f" * 64,
    )


def provenance() -> dict[str, object]:
    return {
        "source_commit": "a" * 40,
        "source_tree_sha256_v2": "b" * 64,
        "dependency_lock_digest": "d" * 64,
        "timezone_bundle_digest": "e" * 64,
        "ephemeris_bundle_digest": "f" * 64,
        "runtime_image_digest": "sha256:" + "c" * 64,
        "calculation_version": "CE-CALC-CORE-V1-R1-CONVERGENT",
    }


def packet(*, warning: str = "A") -> EvidencePacket:
    return EvidencePacket.issue(
        calculation_id="C-PROBE",
        input_identity={"birth_date": "2000-01-01", "source": warning},
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
        warnings=(warning,),
        errors=(),
        numerical_tolerances={},
        solver_metadata={},
        actual_ephemeris_resolution={"ephemeris_resolution_status": "MATCH"},
        calculation_flags={"calculation_status": "VALID"},
    )


def probe() -> dict[str, object]:
    findings: dict[str, object] = {}

    # B1: caller-supplied provenance/context is accepted by issuance.
    draft = CalculationResultDraft(
        request_id="R-B1",
        status=CalculationStatus.NATAL_EVIDENCE_VARIABLE,
        execution_profile_id="CE-CALC-V1-EP-001",
        scenario_state=ScenarioState.VARIABLE,
        normalized_time=None,
        calculation_id="C-B1",
        observation_interval=("2026-01-01T00:00:00Z", "2026-01-02T00:00:00Z"),
    )
    issued = issue_evidence_packet(
        draft,
        input_identity={"fabricated": True},
        profile_version={"id": "CE-CALC-V1-EP-001", "revision": 4, "fabricated": True},
        timezone_context={"id": "FABRICATED", "version": "2026d"},
    )
    findings["B1_caller_supplied_evidence_context_accepted"] = (
        issued.input_identity.get("fabricated") is True
        and issued.timezone_context.get("id") == "FABRICATED"
    )

    # B2: valid-looking result/runtime can carry a packet with unrelated provenance context.
    p = packet(warning="FOREIGN")
    result = CalculationResult(
        request_id="R-B2",
        status=CalculationStatus.NATAL_EVIDENCE_VARIABLE,
        execution_profile_id="CE-CALC-V1-EP-001",
        scenario_state=ScenarioState.VARIABLE,
        normalized_time=None,
        calculation_id="C-PROBE",
        observation_interval=("2026-01-01T00:00:00Z", "2026-01-02T00:00:00Z"),
        object_states=(),
        provenance=provenance(),
        _runtime_identity=runtime_identity(),
        _evidence_packet=p,
    )
    findings["B2_result_accepts_unrelated_packet_provenance"] = result.evidence_packet_ref is not None and result.evidence_packet_ref.matches(p)

    # B3: SignalResult is directly constructible.
    forged_signal = SignalResult(
        status=CalculationStatus.VALID,
        classification="ROBUST_EXACT_SIGNAL",
        phase="EXACT",
        uncertainty_state="ROBUST",
        evidence_packet_ref=f"{p.evidence_packet_id}:{p.content_sha256()}",
        canon_input_valid=True,
    )
    findings["B3_direct_signal_result_forgery_possible"] = forged_signal.canon_input_valid

    # B4: QualifiedSignalRecord is directly constructible and accepted by aggregation.
    forged_record = QualifiedSignalRecord(
        schema_version="CE-QUALIFIED-SIGNAL-RECORD-V1",
        signal_id="CE-SIGNAL-FORGED",
        evidence_packet_ref="FORGED:" + "0" * 64,
        timestamp_observation_utc="2026-01-01T00:00:00Z",
        qualification_status="VALID",
        classification="ROBUST_EXACT_SIGNAL",
        kinematic_phase="EXACT",
        phase_uniformity="UNIFORM",
        canon_input_valid=True,
        requires_uncertainty_disclaimer=False,
        environment_pin="sha256:" + "0" * 64,
    )
    aggregate = aggregate_qualified_signal_records([forged_record], observation_completed=True)
    findings["B4_direct_qsr_forgery_reaches_daily_aggregation"] = (
        aggregate.qualifying_signal_refs == ("CE-SIGNAL-FORGED",)
    )

    # B5/B6: materially different packets can share signal_id/environment_pin
    # because the identity payload is only a subset of packet content.
    p_a = packet(warning="A")
    p_b = packet(warning="B")
    sa = SignalEngine().evaluate(p_a)
    sb = SignalEngine().evaluate(p_b)
    from ce.signal.record import issue_qualified_signal_record
    qa = issue_qualified_signal_record(p_a, sa)
    qb = issue_qualified_signal_record(p_b, sb)
    findings["B5_distinct_packets_same_signal_id"] = (
        p_a.content_sha256() != p_b.content_sha256()
        and qa.signal_id == qb.signal_id
    )
    findings["B6_distinct_packets_same_environment_pin"] = (
        qa.environment_pin == qb.environment_pin
    )

    # B7: authority evaluator can authorize internally consistent synthetic evidence.
    source_digest = "1" * 64
    build_digest = "2" * 64
    signed_digest = "3" * 64
    fingerprint = "AB" * 20
    auth = evaluate_full_authority(
        RuntimeIdentity(
            "CE-CALC-V1-EP-001",
            4,
            "a" * 40,
            "b" * 64,
            "sha256:" + "c" * 64,
            "d" * 64,
            "e" * 64,
            "f" * 64,
            source_digest,
            build_digest,
            signed_digest,
        ),
        source=SourceAuthorityEvidence(
            "https://example.invalid/ce",
            "a" * 40,
            "b" * 64,
            source_digest,
            fingerprint,
        ),
        build=TrustedBuildEvidence(
            build_digest,
            "a" * 40,
            "b" * 64,
            "d" * 64,
            "sha256:" + "c" * 64,
            "4" * 64,
            "e" * 64,
            "f" * 64,
        ),
        signed=SignedProvenanceEvidence(
            signed_digest,
            fingerprint,
            source_digest,
            build_digest,
        ),
    )
    findings["B7_synthetic_authority_chain_can_evaluate_authorized"] = auth.authorized

    # Positive control: current runtime gate remains fail-closed.
    gate = authorize_runtime(runtime_identity())
    findings["CURRENT_RUNTIME_GATE_FAIL_CLOSED"] = (
        gate.authority is RuntimeAuthority.NON_AUTHORIZED
    )

    # Additional identity issuance weakness: arbitrary packet ID is accepted by
    # the public constructor, even when it does not equal the content-derived ID.
    clean = packet(warning="ID")
    arbitrary_id = replace(clean, evidence_packet_id="ARBITRARY-ID")
    findings["B10_direct_packet_id_not_content_address_enforced"] = (
        arbitrary_id.evidence_packet_id == "ARBITRARY-ID"
        and arbitrary_id.content_sha256() != clean.content_sha256()
    )

    return findings


if __name__ == "__main__":
    findings = probe()
    print(json.dumps(findings, indent=2, sort_keys=True))
    failed = [name for name, value in findings.items() if not value]
    if failed:
        raise SystemExit("AUDIT_PROBE_UNEXPECTED_RESULT:" + ",".join(failed))
    print("CE_R0_BOUNDARY_PROBE_STATUS=FINDINGS_CONFIRMED")
