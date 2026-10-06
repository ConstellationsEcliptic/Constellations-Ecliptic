from __future__ import annotations

import json
import unittest
from pathlib import Path

from ce.canon.registry import CanonRegistry, CanonRegistryNotEstablished, CanonRule
from ce.claim.manifest import ManifestInvalid, build_allowed_claim_manifest
from ce.output.validation import validate_claim_output

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
                "allowed_modality":["may","might"],
                "allowed_tense":["present"],
                "forbidden_domains":["medical","diagnosis"],
                "forbidden_claim_types":["guarantee","unsupported-causality"],
                "required_evidence_refs":["EVIDENCE-001"],
                "allowed_numeric_refs":[],
                "required_disclosures":[],
            },
            "forbidden_extrapolation":["guarantee"],
            "confidence_language_boundary":{"ceiling":"possibility"},
            "applicability_scope":["self-reflection"],
        }],
    )

class CanonClaimOutputGatesR1Tests(unittest.TestCase):
    def test_unknown_canon_rule_fields_fail_closed(self) -> None:
        reg = {
            "rule_id":"TEST-RULE-001",
            "canon_version":"CE-CANON-TEST-1",
            "tradition_track":"TEST_ONLY",
            "source_reference":"TEST-SOURCE",
            "source_scope":"TEST-SCOPE",
            "condition":{},
            "allowed_interpretation":{},
            "forbidden_extrapolation":[],
            "confidence_language_boundary":{},
            "applicability_scope":[],
            "unexpected":"reject",
        }
        with self.assertRaisesRegex(ValueError, "unknown_fields"):
            CanonRegistry.from_records("CE-CANON-RULE-REGISTRY-TEST-V1", [reg])

    def test_empty_registry_fails_closed(self) -> None:
        with self.assertRaisesRegex(CanonRegistryNotEstablished, "unpopulated"):
            CanonRegistry.empty("CE-CANON-RULE-REGISTRY-V1").get_rule("ANY")

    def test_manifest_is_registry_derived_and_deterministic(self) -> None:
        reg = registry()
        a = build_allowed_claim_manifest(reg, rule_id="TEST-RULE-001", signal_reference="CE-SIGNAL-001")
        b = build_allowed_claim_manifest(reg, rule_id="TEST-RULE-001", signal_reference="CE-SIGNAL-001")
        self.assertEqual(a.manifest_id, b.manifest_id)
        self.assertEqual(a.digest(), b.digest())
        self.assertEqual(a.claim_id, "TEST-CLAIM-001")
        self.assertEqual(a.canon_rule_id, "TEST-RULE-001")

    def test_manifest_cannot_be_built_from_empty_registry(self) -> None:
        with self.assertRaisesRegex(CanonRegistryNotEstablished, "unpopulated"):
            build_allowed_claim_manifest(
                CanonRegistry.empty("CE-CANON-RULE-REGISTRY-V1"),
                rule_id="TEST-RULE-001",
                signal_reference="CE-SIGNAL-001",
            )

    def test_manifest_unknown_fields_fail_closed(self) -> None:
        reg = registry()
        m = build_allowed_claim_manifest(reg, rule_id="TEST-RULE-001", signal_reference="CE-SIGNAL-001")
        raw = m.canonical_payload()
        raw["manifest_id"] = m.manifest_id
        raw["unexpected"] = "reject"
        from ce.claim.manifest import AllowedClaimManifest
        with self.assertRaisesRegex(ManifestInvalid, "unknown_fields"):
            AllowedClaimManifest.from_mapping(raw)

    def test_manifest_digest_mismatch_fails_closed(self) -> None:
        reg = registry()
        m = build_allowed_claim_manifest(reg, rule_id="TEST-RULE-001", signal_reference="CE-SIGNAL-001")
        raw = m.canonical_payload()
        raw["manifest_id"] = "CE-ACM-WRONG"
        with self.assertRaisesRegex(ManifestInvalid, "identity"):
            from ce.claim.manifest import AllowedClaimManifest
            AllowedClaimManifest.from_mapping(raw)

    def test_output_rejects_forged_manifest_identity(self) -> None:
        reg = registry()
        m = build_allowed_claim_manifest(
            reg, rule_id="TEST-RULE-001", signal_reference="CE-SIGNAL-001"
        )
        from ce.claim.manifest import AllowedClaimManifest
        forged = AllowedClaimManifest(
            **{**m.__dict__, "claim_id": "FORGED-CLAIM-001"}
        )
        result = validate_claim_output(
            {
                "manifest_id": forged.manifest_id,
                "claims": [
                    {"claim_id": forged.claim_id, "text": "This reflection may invite attention."}
                ],
            },
            forged,
            semantic_conformance=lambda text, manifest: True,
        )
        self.assertFalse(result.valid)
        self.assertIn("manifest_identity_digest_mismatch", result.reasons)

    def test_output_requires_semantic_conformance(self) -> None:
        reg = registry()
        m = build_allowed_claim_manifest(reg, rule_id="TEST-RULE-001", signal_reference="CE-SIGNAL-001")
        result = validate_claim_output(
            {"manifest_id":m.manifest_id,"claims":[{"claim_id":m.claim_id,"text":"This reflection may invite attention."}]},
            m,
        )
        self.assertFalse(result.valid)
        self.assertIn("semantic_conformance_unavailable", result.reasons)

    def test_forbidden_output_is_rejected_even_when_semantic_check_says_true(self) -> None:
        reg = registry()
        m = build_allowed_claim_manifest(reg, rule_id="TEST-RULE-001", signal_reference="CE-SIGNAL-001")
        result = validate_claim_output(
            {"manifest_id":m.manifest_id,"claims":[{"claim_id":m.claim_id,"text":"This will definitely happen."}]},
            m,
            semantic_conformance=lambda text, manifest: True,
        )
        self.assertFalse(result.valid)
        self.assertIn("forbidden_guarantee_language", result.reasons)

    def test_semantic_pass_requires_structural_pass(self) -> None:
        reg = registry()
        m = build_allowed_claim_manifest(reg, rule_id="TEST-RULE-001", signal_reference="CE-SIGNAL-001")
        result = validate_claim_output(
            {"manifest_id":m.manifest_id,"claims":[{"claim_id":m.claim_id,"text":"This reflection may invite attention."}]},
            m,
            semantic_conformance=lambda text, manifest: True,
        )
        self.assertTrue(result.valid)

    def test_registry_artifact_is_empty_until_approved_rules_exist(self) -> None:
        payload=json.loads(
            (Path(__file__).parents[1]/"manifests"/"canon_rule_registry_v1.json")
            .read_text(encoding="utf-8")
        )
        self.assertEqual(payload, {"registry_version":"CE-CANON-RULE-REGISTRY-V1","rules":[]})

if __name__ == "__main__":
    unittest.main()
