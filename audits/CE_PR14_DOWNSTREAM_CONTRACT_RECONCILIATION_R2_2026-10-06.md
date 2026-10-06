# PR14 DOWNSTREAM CONTRACT RECONCILIATION R2
Date: 2026-10-06
Base audited head: 185a4393eac99f6214bf7ecb5e43a21b7e2a9c88
Disposition: RECONCILE — DO NOT MERGE

## Findings

P1 — Claim output schema and runtime validator disagree.
The JSON schema requires top-level "provenance" and claim fields:
subject, scope, modality, tense, epistemic_layer, certainty, evidence_refs, numeric_refs.
The Python validator requires the payload to contain exactly {"manifest_id","claims"} and each claim exactly {"claim_id","text"}.
Consequence: schema-valid output is rejected by runtime; a schema-invalid reduced output can be accepted.

P2 — Provenance fields are therefore not actually validated at the release boundary.
The runtime validator does not consume the schema-required provenance object.

P3 — Allowed claim constraints are not enforced as structured fields.
allowed_subject, allowed_scope, allowed_modality, allowed_tense, epistemic_layer and certainty_ceiling exist in the manifest, but the current output validator does not accept corresponding structured claim fields at all.

P4 — Semantic conformance remains caller-supplied.
validate_claim_output() accepts an arbitrary SemanticConformanceCheck callback. A future release boundary must use a CE-owned verifier/engine, not a caller-selected predicate.

P5 — Manifest/registry authenticity remains external to the object itself.
AllowedClaimManifest and CanonRule are direct data objects. The release evaluator derives an expected manifest from the supplied registry, but the registry itself is caller-provided and not a verified authority receipt.

P6 — Canon registry remains empty in the shipped PR14 candidate.
This is safe and fail-closed today; it must remain so until Canon rules are separately approved and bound.

## Required closure
1. Define one canonical claim-output contract shared by JSON schema and Python.
2. Require and validate provenance in the release object.
3. Enforce structured subject/scope/modality/tense/epistemic/certainty fields against the manifest.
4. Replace caller-supplied semantic callbacks with CE-owned semantic verification or fail closed.
5. Bind manifest and registry identity to verified upstream records.
6. Keep the registry empty until semantic authority is explicitly established.
7. Re-run downstream adversarial tests after CE-R0 provenance closure.

No source authority, trusted build, production runtime, dual approval, or SEAL is established.
