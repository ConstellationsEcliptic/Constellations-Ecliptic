from __future__ import annotations

import unittest

from ce.claim.manifest import AllowedClaimManifest
from ce.foundation.hashing import sha256_bytes
from ce.foundation.serialization import canonical_json
from ce.output.validation import validate_claim_output


class CER0A2OutputTypeStrictnessTests(unittest.TestCase):
    def _manifest(self) -> AllowedClaimManifest:
        payload = {
            "manifest_version": "CE-ALLOWED-CLAIM-MANIFEST-V1",
            "claim_id": "CLAIM-1",
            "canon_version": "CANON-1",
            "canon_registry_digest": "a" * 64,
            "canon_rule_id": "RULE-1",
            "signal_reference": "CE-SIGNAL-" + "b" * 64,
            "allowed_subject": ["reflection"],
            "allowed_scope": ["self"],
            "epistemic_layer": "ASTROLOGICAL_INTERPRETATION",
            "certainty_ceiling": "possibility",
            "allowed_modality": ["may"],
            "allowed_tense": ["present"],
            "forbidden_domains": [],
            "forbidden_claim_types": [],
            "required_evidence_refs": ["E:" + "c" * 64],
            "allowed_numeric_refs": [],
            "required_disclosures": [],
        }
        manifest_id = "CE-ACM-" + sha256_bytes(canonical_json(payload))
        return AllowedClaimManifest(manifest_id=manifest_id, **payload)

    def _payload(self, manifest: AllowedClaimManifest) -> dict:
        evidence_ref = manifest.required_evidence_refs[0]
        return {
            "manifest_id": manifest.manifest_id,
            "provenance": {
                "manifest_id": manifest.manifest_id,
                "manifest_version": manifest.manifest_version,
                "canon_version": manifest.canon_version,
                "canon_registry_digest": manifest.canon_registry_digest,
                "canon_rule_id": manifest.canon_rule_id,
                "signal_reference": manifest.signal_reference,
                "evidence_refs": [evidence_ref],
                "provenance_root_sha256": "d" * 64,
            },
            "claims": [{
                "claim_id": manifest.claim_id,
                "text": "A reflection may invite attention.",
                "subject": ["reflection"],
                "scope": ["self"],
                "modality": ["may"],
                "tense": ["present"],
                "epistemic_layer": manifest.epistemic_layer,
                "certainty": manifest.certainty_ceiling,
                "evidence_refs": [evidence_ref],
                "numeric_refs": [],
            }],
        }

    def test_integer_subject_is_rejected_without_string_coercion(self):
        manifest = self._manifest()
        payload = self._payload(manifest)
        payload["claims"][0]["subject"] = [1]
        result = validate_claim_output(
            payload,
            manifest,
            expected_signal_reference=manifest.signal_reference,
            expected_evidence_refs=manifest.required_evidence_refs,
            expected_provenance_root_sha256="d" * 64,
            semantic_conformance=lambda text, manifest: True,
        )
        self.assertFalse(result.valid)
        self.assertIn("claim_subject_item_type_invalid", result.reasons)
        self.assertIn("claim_subject_outside_manifest", result.reasons)

    def test_boolean_evidence_reference_is_rejected(self):
        manifest = self._manifest()
        payload = self._payload(manifest)
        payload["claims"][0]["evidence_refs"] = [True]
        result = validate_claim_output(
            payload,
            manifest,
            expected_signal_reference=manifest.signal_reference,
            expected_evidence_refs=manifest.required_evidence_refs,
            expected_provenance_root_sha256="d" * 64,
            semantic_conformance=lambda text, manifest: True,
        )
        self.assertFalse(result.valid)
        self.assertIn("claim_evidence_refs_item_type_invalid", result.reasons)

    def test_numeric_reference_must_be_string(self):
        manifest = self._manifest()
        payload = self._payload(manifest)
        payload["claims"][0]["numeric_refs"] = [123]
        result = validate_claim_output(
            payload,
            manifest,
            expected_signal_reference=manifest.signal_reference,
            expected_evidence_refs=manifest.required_evidence_refs,
            expected_provenance_root_sha256="d" * 64,
            semantic_conformance=lambda text, manifest: True,
        )
        self.assertFalse(result.valid)
        self.assertIn("claim_numeric_refs_item_type_invalid", result.reasons)

    def test_duplicate_manifest_fields_are_rejected(self):
        manifest = self._manifest()
        payload = self._payload(manifest)
        payload["claims"][0]["subject"] = ["reflection", "reflection"]
        result = validate_claim_output(
            payload,
            manifest,
            expected_signal_reference=manifest.signal_reference,
            expected_evidence_refs=manifest.required_evidence_refs,
            expected_provenance_root_sha256="d" * 64,
            semantic_conformance=lambda text, manifest: True,
        )
        self.assertFalse(result.valid)
        self.assertIn("claim_subject_duplicates", result.reasons)

    def test_conforming_output_remains_valid(self):
        manifest = self._manifest()
        result = validate_claim_output(
            self._payload(manifest),
            manifest,
            expected_signal_reference=manifest.signal_reference,
            expected_evidence_refs=manifest.required_evidence_refs,
            expected_provenance_root_sha256="d" * 64,
            semantic_conformance=lambda text, manifest: True,
        )
        self.assertTrue(result.valid, result.reasons)


if __name__ == "__main__":
    unittest.main()
