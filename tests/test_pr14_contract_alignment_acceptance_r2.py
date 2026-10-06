from __future__ import annotations

import json
from pathlib import Path
import unittest

from ce.canon.registry import CanonRegistry
from ce.claim.manifest import build_allowed_claim_manifest
from ce.output.validation import validate_claim_output


def registry() -> CanonRegistry:
    return CanonRegistry.from_records(
        "CE-CANON-RULE-REGISTRY-TEST-V1",
        [{
            "rule_id": "TEST-RULE-001",
            "canon_version": "CE-CANON-TEST-1",
            "tradition_track": "TEST_ONLY",
            "source_reference": "TEST-SOURCE",
            "source_scope": "TEST-SCOPE",
            "condition": {"classification": "TEST_SIGNAL"},
            "allowed_interpretation": {
                "claim_id": "TEST-CLAIM-001",
                "allowed_subject": ["reflection"],
                "allowed_scope": ["self-reflection"],
                "epistemic_layer": "ASTROLOGICAL_INTERPRETATION",
                "certainty_ceiling": "possibility_or_reflection",
                "allowed_modality": ["may", "might"],
                "allowed_tense": ["present"],
                "forbidden_domains": ["medical"],
                "forbidden_claim_types": ["guarantee"],
                "required_evidence_refs": ["EVIDENCE-001"],
                "allowed_numeric_refs": [],
                "required_disclosures": [],
            },
            "forbidden_extrapolation": ["guarantee"],
            "confidence_language_boundary": {"ceiling": "possibility"},
            "applicability_scope": ["self-reflection"],
        }],
    )


class PR14ContractAlignmentAcceptanceTests(unittest.TestCase):
    def test_P1_schema_requires_provenance_but_runtime_validator_rejects_it(self) -> None:
        root = Path(__file__).resolve().parents[1]
        schema = json.loads(
            (root / "schemas" / "claim_output.schema.json").read_text(encoding="utf-8")
        )
        self.assertIn("provenance", schema["required"])

        manifest = build_allowed_claim_manifest(
            registry(),
            rule_id="TEST-RULE-001",
            signal_reference="CE-SIGNAL-" + "1" * 64,
        )
        payload = {
            "manifest_id": manifest.manifest_id,
            "provenance": {
                "manifest_id": manifest.manifest_id,
                "manifest_version": manifest.manifest_version,
                "canon_version": manifest.canon_version,
                "canon_rule_id": manifest.canon_rule_id,
                "signal_reference": manifest.signal_reference,
                "evidence_refs": ["EVIDENCE-001"],
            },
            "claims": [{
                "claim_id": manifest.claim_id,
                "text": "This reflection may invite attention.",
                "subject": ["reflection"],
                "scope": ["self-reflection"],
                "modality": ["may"],
                "tense": ["present"],
                "epistemic_layer": "ASTROLOGICAL_INTERPRETATION",
                "certainty": "possibility_or_reflection",
                "evidence_refs": ["EVIDENCE-001"],
                "numeric_refs": [],
            }],
        }
        result = validate_claim_output(
            payload,
            manifest,
            semantic_conformance=lambda text, m: True,
        )
        self.assertFalse(result.valid)
        self.assertIn("output_schema_mismatch", result.reasons)

    def test_P2_reduced_non_schema_payload_can_be_accepted(self) -> None:
        manifest = build_allowed_claim_manifest(
            registry(),
            rule_id="TEST-RULE-001",
            signal_reference="CE-SIGNAL-" + "2" * 64,
        )
        reduced_payload = {
            "manifest_id": manifest.manifest_id,
            "claims": [{
                "claim_id": manifest.claim_id,
                "text": "This reflection may invite attention.",
            }],
        }
        result = validate_claim_output(
            reduced_payload,
            manifest,
            semantic_conformance=lambda text, m: True,
        )
        self.assertTrue(result.valid)

    def test_P3_manifest_structured_restrictions_need_corresponding_claim_fields(self) -> None:
        manifest = build_allowed_claim_manifest(
            registry(),
            rule_id="TEST-RULE-001",
            signal_reference="CE-SIGNAL-" + "3" * 64,
        )
        payload = {
            "manifest_id": manifest.manifest_id,
            "claims": [{
                "claim_id": manifest.claim_id,
                "text": "Any statement is accepted by this runtime shape.",
            }],
        }
        result = validate_claim_output(
            payload,
            manifest,
            semantic_conformance=lambda text, m: True,
        )
        self.assertTrue(result.valid)

    def test_P4_semantic_callback_is_not_an_authority_receipt(self) -> None:
        manifest = build_allowed_claim_manifest(
            registry(),
            rule_id="TEST-RULE-001",
            signal_reference="CE-SIGNAL-" + "4" * 64,
        )
        callback = lambda text, m: True
        result = validate_claim_output(
            {
                "manifest_id": manifest.manifest_id,
                "claims": [{
                    "claim_id": manifest.claim_id,
                    "text": "A semantically unsafe but pattern-unmatched statement.",
                }],
            },
            manifest,
            semantic_conformance=callback,
        )
        # The current implementation can only distinguish this through the
        # callback; the acceptance requirement is that the callback itself is
        # never treated as a trusted CE verifier in an authorized release path.
        self.assertTrue(result.valid)


if __name__ == "__main__":
    unittest.main()
