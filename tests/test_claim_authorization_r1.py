from __future__ import annotations

import unittest

from ce.canon.registry import CanonRegistry
from ce.claim.authorization import evaluate_claim_release
from ce.claim.manifest import build_allowed_claim_manifest
from ce.foundation.status import CalculationStatus, RuntimeAuthority
from ce.output.validation import OutputValidationResult
from ce.product.boundary import preserve_calculation_truth
from ce.runtime.gates import RuntimeGateResult
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

class ClaimAuthorizationR1Tests(unittest.TestCase):
    def test_runtime_gate_blocks_current_release(self) -> None:
        s=signal(); reg=registry()
        m=build_allowed_claim_manifest(reg, rule_id="TEST-RULE-001", signal_reference=s.signal_id)
        decision=evaluate_claim_release(
            preserve_calculation_truth(CalculationStatus.VALID),
            s, m, OutputValidationResult(True, ()),
            RuntimeGateResult(RuntimeAuthority.NON_AUTHORIZED, ()), reg,
        )
        self.assertFalse(decision.authorized)
        self.assertIn("runtime_not_authorized", decision.reasons)

    def test_non_valid_calculation_blocks(self) -> None:
        s=signal(); reg=registry()
        m=build_allowed_claim_manifest(reg, rule_id="TEST-RULE-001", signal_reference=s.signal_id)
        decision=evaluate_claim_release(
            preserve_calculation_truth(CalculationStatus.CALCULATION_FAILURE),
            s, m, OutputValidationResult(True, ()),
            RuntimeGateResult(RuntimeAuthority.AUTHORIZED, ()), reg,
        )
        self.assertFalse(decision.authorized)
        self.assertIn("calculation_not_valid", decision.reasons)

    def test_registry_binding_blocks_forged_manifest(self) -> None:
        s=signal(); reg=registry()
        m=build_allowed_claim_manifest(reg, rule_id="TEST-RULE-001", signal_reference=s.signal_id)
        forged = type(m)(**{**m.__dict__, "claim_id":"FORGED-CLAIM-001"})
        decision=evaluate_claim_release(
            preserve_calculation_truth(CalculationStatus.VALID),
            s, forged, OutputValidationResult(True, ()),
            RuntimeGateResult(RuntimeAuthority.AUTHORIZED, ()), reg,
        )
        self.assertFalse(decision.authorized)
        self.assertIn("manifest_registry_binding_mismatch", decision.reasons)

    def test_signal_evidence_binding_is_required(self) -> None:
        s=signal(); reg=registry()
        m=build_allowed_claim_manifest(reg, rule_id="TEST-RULE-001", signal_reference=s.signal_id)
        forged = type(m)(**{**m.__dict__, "required_evidence_refs":("OTHER-EVIDENCE",)})
        decision=evaluate_claim_release(
            preserve_calculation_truth(CalculationStatus.VALID),
            s, forged, OutputValidationResult(True, ()),
            RuntimeGateResult(RuntimeAuthority.AUTHORIZED, ()), reg,
        )
        self.assertFalse(decision.authorized)
        self.assertIn("manifest_registry_binding_mismatch", decision.reasons)

if __name__ == "__main__":
    unittest.main()
