from __future__ import annotations

import unittest

from ce.canon.registry import CanonRegistry
from ce.claim.authorization import evaluate_claim_release
from ce.claim.manifest import build_allowed_claim_manifest
from ce.foundation.identity import RuntimeIdentity
from ce.foundation.status import CalculationStatus
from ce.product.boundary import preserve_calculation_truth
from ce.signal.record import QualifiedSignalRecord


def registry() -> CanonRegistry:
    return CanonRegistry.from_records(
        "CE-CANON-RULE-REGISTRY-TEST-V1",
        [{
            "rule_id":"TEST-RULE-001",
            "canon_version":"CE-CANON-TEST-1",
            "tradition_track":"TEST_ONLY",
            "source_reference":"TEST-SOURCE",
            "source_scope":"TEST-SCOPE",
            "condition":{"classification":"TEST_SIGNAL"},
            "allowed_interpretation":{
                "claim_id":"TEST-CLAIM-001",
                "allowed_subject":["reflection"],
                "allowed_scope":["self-reflection"],
                "epistemic_layer":"ASTROLOGICAL_INTERPRETATION",
                "certainty_ceiling":"possibility_or_reflection",
                "allowed_modality":["may"],
                "allowed_tense":["present"],
                "forbidden_domains":["medical"],
                "forbidden_claim_types":["guarantee"],
                "required_evidence_refs":["EVIDENCE-001"],
                "allowed_numeric_refs":[],
                "required_disclosures":[],
            },
            "forbidden_extrapolation":["guarantee"],
            "confidence_language_boundary":{"ceiling":"possibility"},
            "applicability_scope":["self-reflection"],
        }],
    )


def signal() -> QualifiedSignalRecord:
    return QualifiedSignalRecord(
        schema_version="CE-QUALIFIED-SIGNAL-RECORD-V1",
        signal_id="CE-SIGNAL-001",
        evidence_packet_ref="EVIDENCE-001",
        timestamp_observation_utc="2026-01-01T00:00:00Z",
        qualification_status="VALID",
        classification="TEST_SIGNAL",
        kinematic_phase="EXACT",
        phase_uniformity="UNIFORM",
        canon_input_valid=True,
        requires_uncertainty_disclaimer=False,
        environment_pin="sha256:" + "0" * 64,
    )


def runtime_identity() -> RuntimeIdentity:
    return RuntimeIdentity(
        execution_profile_id="INVALID",
        execution_profile_revision=0,
        source_commit=None,
        source_tree_sha256_v2=None,
        runtime_image_digest=None,
        dependency_lock_digest=None,
        timezone_bundle_digest=None,
        ephemeris_bundle_digest=None,
        runtime_environment_kind=None,
    )


class ClaimAuthorizationR1Tests(unittest.TestCase):

    def test_canon_rule_signal_condition_mismatch_blocks_release(self) -> None:
        s = signal()
        reg = registry()
        m = build_allowed_claim_manifest(
            reg, rule_id="TEST-RULE-001", signal_reference=s.signal_id
        )
        mismatched = type(s)(
            **{**s.__dict__, "classification":"OTHER_SIGNAL"}
        )
        decision = evaluate_claim_release(
            preserve_calculation_truth(CalculationStatus.VALID),
            mismatched,
            m,
            {"manifest_id":m.manifest_id,"claims":[{"claim_id":m.claim_id,"text":"This reflection may invite attention."}]},
            runtime_identity(),
            reg,
            semantic_conformance=lambda text, manifest: True,
        )
        self.assertFalse(decision.authorized)
        self.assertIn("canon_rule_signal_condition_mismatch", decision.reasons)

    def test_runtime_gate_is_derived_and_currently_blocks_release(self) -> None:
        s = signal()
        reg = registry()
        m = build_allowed_claim_manifest(reg, rule_id="TEST-RULE-001", signal_reference=s.signal_id)
        decision = evaluate_claim_release(
            preserve_calculation_truth(CalculationStatus.VALID),
            s,
            m,
            {"manifest_id":m.manifest_id,"claims":[{"claim_id":m.claim_id,"text":"This reflection may invite attention."}]},
            runtime_identity(),
            reg,
            semantic_conformance=lambda text, manifest: True,
        )
        self.assertFalse(decision.authorized)
        self.assertIn("runtime_not_authorized", decision.reasons)

    def test_output_payload_is_validated_inside_release_evaluator(self) -> None:
        s = signal()
        reg = registry()
        m = build_allowed_claim_manifest(reg, rule_id="TEST-RULE-001", signal_reference=s.signal_id)
        decision = evaluate_claim_release(
            preserve_calculation_truth(CalculationStatus.VALID),
            s,
            m,
            {"manifest_id":m.manifest_id,"claims":[{"claim_id":m.claim_id,"text":"This will definitely happen."}]},
            runtime_identity(),
            reg,
            semantic_conformance=lambda text, manifest: True,
        )
        self.assertFalse(decision.authorized)
        self.assertIn("forbidden_guarantee_language", decision.reasons)

    def test_boundary_boolean_contract_is_enforced(self) -> None:
        s = signal()
        reg = registry()
        m = build_allowed_claim_manifest(reg, rule_id="TEST-RULE-001", signal_reference=s.signal_id)
        forged_boundary = type(preserve_calculation_truth(CalculationStatus.VALID))(
            status=CalculationStatus.VALID,
            signal_processing_allowed=True,
            canon_claim_allowed=True,
            ai_release_allowed=False,
            quiet_sky_allowed=False,
            reason="forged",
        )
        decision = evaluate_claim_release(
            forged_boundary,
            s,
            m,
            {"manifest_id":m.manifest_id,"claims":[{"claim_id":m.claim_id,"text":"This reflection may invite attention."}]},
            runtime_identity(),
            reg,
            semantic_conformance=lambda text, manifest: True,
        )
        self.assertFalse(decision.authorized)
        self.assertIn("product_boundary_contract_mismatch", decision.reasons)

    def test_non_valid_calculation_blocks(self) -> None:
        s = signal()
        reg = registry()
        m = build_allowed_claim_manifest(reg, rule_id="TEST-RULE-001", signal_reference=s.signal_id)
        decision = evaluate_claim_release(
            preserve_calculation_truth(CalculationStatus.CALCULATION_FAILURE),
            s,
            m,
            {"manifest_id":m.manifest_id,"claims":[{"claim_id":m.claim_id,"text":"This reflection may invite attention."}]},
            runtime_identity(),
            reg,
            semantic_conformance=lambda text, manifest: True,
        )
        self.assertFalse(decision.authorized)
        self.assertIn("calculation_not_valid", decision.reasons)

    def test_registry_binding_blocks_forged_manifest(self) -> None:
        s = signal()
        reg = registry()
        m = build_allowed_claim_manifest(reg, rule_id="TEST-RULE-001", signal_reference=s.signal_id)
        forged = type(m)(**{**m.__dict__, "claim_id":"FORGED-CLAIM-001"})
        decision = evaluate_claim_release(
            preserve_calculation_truth(CalculationStatus.VALID),
            s,
            forged,
            {"manifest_id":forged.manifest_id,"claims":[{"claim_id":forged.claim_id,"text":"This reflection may invite attention."}]},
            runtime_identity(),
            reg,
            semantic_conformance=lambda text, manifest: True,
        )
        self.assertFalse(decision.authorized)
        self.assertIn("manifest_registry_binding_mismatch", decision.reasons)

    def test_signal_evidence_binding_is_required(self) -> None:
        s = signal()
        reg = registry()
        m = build_allowed_claim_manifest(reg, rule_id="TEST-RULE-001", signal_reference=s.signal_id)
        forged = type(m)(**{**m.__dict__, "required_evidence_refs":("OTHER-EVIDENCE",)})
        decision = evaluate_claim_release(
            preserve_calculation_truth(CalculationStatus.VALID),
            s,
            forged,
            {"manifest_id":forged.manifest_id,"claims":[{"claim_id":forged.claim_id,"text":"This reflection may invite attention."}]},
            runtime_identity(),
            reg,
            semantic_conformance=lambda text, manifest: True,
        )
        self.assertFalse(decision.authorized)
        self.assertIn("manifest_registry_binding_mismatch", decision.reasons)


if __name__ == "__main__":
    unittest.main()
