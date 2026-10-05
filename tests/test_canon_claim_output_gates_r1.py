from __future__ import annotations

import unittest
from pathlib import Path

from ce.canon.registry import CanonRegistry, CanonRegistryNotEstablished, CanonRule
from ce.claim.manifest import CanonApprovedInterpretation, ManifestInvalid, build_allowed_claim_manifest
from ce.output.validation import validate_claim_output


def rule() -> CanonRule:
    return CanonRule.from_mapping({
        "rule_id":"TEST-RULE-001",
        "canon_version":"CE-CANON-TEST-1",
        "tradition_track":"TEST_ONLY",
        "source_reference":"TEST-SOURCE",
        "source_scope":"TEST-SCOPE",
        "condition":{"classification":"TEST_SIGNAL"},
        "allowed_interpretation":{"placeholder":True},
        "forbidden_extrapolation":["guarantee"],
        "confidence_language_boundary":{"ceiling":"possibility"},
        "applicability_scope":["self-reflection"],
    })


def interpretation() -> CanonApprovedInterpretation:
    return CanonApprovedInterpretation.from_mapping({
        "claim_id":"TEST-CLAIM-001",
        "allowed_subject":["reflection"],
        "allowed_scope":["self-reflection"],
        "epistemic_layer":"ASTROLOGICAL_INTERPRETATION",
        "certainty_ceiling":"possibility_or_reflection",
        "allowed_modality":["may","might"],
        "allowed_tense":["present"],
        "forbidden_domains":["medical","diagnosis"],
        "forbidden_claim_types":["guarantee","unsupported-causality"],
        "required_evidence_refs":["EVIDENCE-001"],
        "allowed_numeric_refs":[],
        "required_disclosures":[],
    })


class CanonClaimOutputGatesR1Tests(unittest.TestCase):
    def test_empty_registry_fails_closed(self) -> None:
        with self.assertRaisesRegex(CanonRegistryNotEstablished, "unpopulated"):
            CanonRegistry.empty("CE-CANON-RULE-REGISTRY-V1").get_rule("ANY")

    def test_manifest_is_deterministic(self) -> None:
        a = build_allowed_claim_manifest(rule(), signal_reference="CE-SIGNAL-001", interpretation=interpretation())
        b = build_allowed_claim_manifest(rule(), signal_reference="CE-SIGNAL-001", interpretation=interpretation())
        self.assertEqual(a.manifest_id, b.manifest_id)
        self.assertEqual(a.digest(), b.digest())

    def test_manifest_digest_mismatch_fails_closed(self) -> None:
        m = build_allowed_claim_manifest(rule(), signal_reference="CE-SIGNAL-001", interpretation=interpretation())
        raw = m.canonical_payload()
        raw.update({"manifest_version":m.manifest_version,"manifest_id":"CE-ACM-WRONG"})
        with self.assertRaisesRegex(ManifestInvalid, "identity"):
            from ce.claim.manifest import AllowedClaimManifest
            AllowedClaimManifest.from_mapping(raw)

    def test_output_requires_semantic_conformance(self) -> None:
        m = build_allowed_claim_manifest(rule(), signal_reference="CE-SIGNAL-001", interpretation=interpretation())
        result = validate_claim_output(
            {"manifest_id":m.manifest_id,"claims":[{"claim_id":m.claim_id,"text":"This reflection may invite attention."}]},
            m,
        )
        self.assertFalse(result.valid)
        self.assertIn("semantic_conformance_unavailable", result.reasons)

    def test_forbidden_output_is_rejected_even_when_semantic_check_says_true(self) -> None:
        m = build_allowed_claim_manifest(rule(), signal_reference="CE-SIGNAL-001", interpretation=interpretation())
        result = validate_claim_output(
            {"manifest_id":m.manifest_id,"claims":[{"claim_id":m.claim_id,"text":"This will definitely happen."}]},
            m,
            semantic_conformance=lambda text, manifest: True,
        )
        self.assertFalse(result.valid)
        self.assertIn("forbidden_guarantee_language", result.reasons)

    def test_semantic_pass_requires_structural_pass(self) -> None:
        m = build_allowed_claim_manifest(rule(), signal_reference="CE-SIGNAL-001", interpretation=interpretation())
        result = validate_claim_output(
            {"manifest_id":m.manifest_id,"claims":[{"claim_id":m.claim_id,"text":"This reflection may invite attention."}]},
            m,
            semantic_conformance=lambda text, manifest: True,
        )
        self.assertTrue(result.valid)

    def test_registry_artifact_is_empty_until_approved_rules_exist(self) -> None:
        import json
        payload=json.loads((Path(__file__).parents[1]/"manifests"/"canon_rule_registry_v1.json").read_text(encoding="utf-8"))
        self.assertEqual(payload, {"registry_version":"CE-CANON-RULE-REGISTRY-V1","rules":[]})


if __name__ == "__main__":
    unittest.main()
