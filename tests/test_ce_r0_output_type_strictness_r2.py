from __future__ import annotations

import unittest

from ce.claim.manifest import AllowedClaimManifest
from ce.output.validation import validate_claim_output


class CER0OutputTypeStrictnessTests(unittest.TestCase):
    def _manifest(self) -> AllowedClaimManifest:
        payload = {
            "manifest_version": "CE-ALLOWED-CLAIM-MANIFEST-V1",
            "claim_id": "CLAIM-1",
            "canon_version": "CANON-1",
            "canon_registry_digest": "a" * 64,
            "canon_rule_id": "RULE-1",
            "signal_reference": "CE-SIGNAL-" + "b" * 64,
            "allowed_subject": ("1",),
            "allowed_scope": ("self",),
            "epistemic_layer": "ASTROLOGICAL_INTERPRETATION",
            "certainty_ceiling": "possibility",
            "allowed_modality": ("may",),
            "allowed_tense": ("present",),
            "forbidden_domains": (),
            "forbidden_claim_types": (),
            "required_evidence_refs": ("E:" + "c" * 64,),
            "allowed_numeric_refs": (),
            "required_disclosures": (),
        }
        digest = AllowedClaimManifest(
            manifest_id="CE-ACM-" + "0" * 64,
            **payload,
        )
        # Constructor should reject the forged manifest identity. Build a
        # legitimate self-consistent one by deriving its identity from the
        # canonical payload.
        canonical = digest.canonical_payload()
        from ce.foundation.hashing import sha256_bytes
        from ce.foundation.serialization import canonical_json
        return AllowedClaimManifest(
            manifest_id="CE-ACM-" + sha256_bytes(canonical_json(canonical)),
            **payload,
        )

    def test_runtime_validator_must_not_stringify_schema_invalid_values(self):
        manifest = self._manifest()
        evidence_ref = manifest.required_evidence_refs[0]
        payload = {
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
                "subject": [1],  # schema-invalid; validator must not coerce
                "scope": ["self"],
                "modality": ["may"],
                "tense": ["present"],
                "epistemic_layer": manifest.epistemic_layer,
                "certainty": manifest.certainty_ceiling,
                "evidence_refs": [evidence_ref],
                "numeric_refs": [],
            }],
        }
        result = validate_claim_output(
            payload,
            manifest,
            expected_signal_reference=manifest.signal_reference,
            expected_evidence_refs=(evidence_ref,),
            expected_provenance_root_sha256="d" * 64,
            semantic_conformance=lambda text, manifest: True,
        )
        self.assertFalse(
            result.valid,
            "SCHEMA-INVALID INTEGER SUBJECT WAS COERCED TO STRING AND ACCEPTED",
        )
        self.assertIn("claim_subject_outside_manifest", result.reasons)


if __name__ == "__main__":
    unittest.main()
