# CE PRE-A10 — CANON / CLAIM / LANGUAGE RELEASE-BOUNDARY RECONCILIATION R0

Date: 2026-10-10  
Classification: SOURCE-TO-CODE RECONCILIATION / WORKING CANDIDATE / NON-AUTHORITATIVE  
Authority effect: NONE  
Normative amendment: NONE  
User-facing release authorization: NONE  
A10 / Runtime Adoption / production / SEAL effect: NONE

## 1. Executive result

Reading the actual V1 Product Constitution v1.6.1, Interpretive Canon v1.2, and Evidence, AI & Output Validation Specification v1.4 yields this controlling chain:

**qualified calculation evidence → signal record → approved/versioned Canon rule → derived Allowed Claim Manifest → language output → structural and semantic validation → release decision.**

The exact A9 candidate implements material parts of this control chain and intentionally fail-closes at missing authority. It does not establish that a populated approved current V1 Canon registry exists, nor does it establish a controlled independent semantic-conformance implementation that allows output release. Those are safeguards and unresolved prerequisites—not permission to bypass the boundary.

## 2. Normative source reconciliation

### 2.1 Product Constitution v1.6.1

- §4.2: Look Today shows Testable Sky Signal only when qualification requirements are met; otherwise a completed valid observation with zero qualifying signals is Quiet Sky.
- §5: Quiet Sky is a valid state, not an invitation to relax orbs, add objects, change branch/event timing/stability, or create a synthetic signal.
- §§8.2–8.3: technical/non-VALID states must not be relabeled Quiet Sky or replaced with stale results.
- §11: Product Layer can present authorized evidence, but cannot change numerical state, qualification, Canon meaning, uncertainty, or the Allowed Claim Manifest.
- §15: V1 uses Gregorian calendar and birth date/canonical location; exact birth time is NOT_USED. The calculation layer retains a half-open zero-birth interval; no substitute birth hour may be invented.

### 2.2 Interpretive Canon v1.2

- §4 requires every actual rule to bind a rule ID/version, tradition track, source reference/scope, condition, allowed interpretation, forbidden extrapolation, certainty boundary and applicability scope.
- §§5–6 establish the versioned registry as the semantic source of record and prohibit runtime-invented Canon.
- §§13–14 require unresolved conflicts to be omitted, and each interpretation to be tied to Canon version and Rule ID.
- §18 explicitly says the document is a governance/contract baseline, while semantic rules must come from a separately versioned registry after source review and approval; no approved rule means no interpretation.
- §§19–20 preserve the invariant that Canon cannot modify calculation or qualification, and missing rules mean omission rather than invention.

### 2.3 Evidence, AI & Output Validation Specification v1.4

- §§3–4: AI is Language Infrastructure only; V1 AI input is restricted to calculated evidence, Qualified Signal Record, Canon output, Allowed Claim Manifest, expressly permitted current-session categorical selection and presentation constraints. Raw free text, persistent Personal Context/history and hidden memory are absent.
- §§5–6: Core language uses deterministic templates. Deep Sky may use one LLM processor for a constrained structured payload and constrained JSON, not an open-ended final prose/HTML stream.
- §§7–8: Allowed Claim Manifest is a machine-readable authorization boundary derived from approved Canon interpretation; AI does not author the manifest. No matching rule means no manifest and no claim.
- §§10–12: output validation is fail-closed; non-VALID calculations cannot become Quiet Sky, valid signal, prior observation or stale cached output. Missing/incomplete Canon or manifest means do not generate the affected claim; semantic failure means no release.
- §11: JSON/schema checking alone does not prevent semantic jailbreak; semantic conformance is required and cannot be established by treating a classifier as the source of truth.
- §§18–24: reading provenance binds profile/Canon/manifest versions; user responses remain user-reported and cannot rescue a mismatch; commercial state cannot change truth conditions; validation cases include guarantee, diagnosis, invented fact/aspect, hidden-profile, certainty escalation, mismatched evidence, version mismatch, missing evidence, malformed JSON and failure-to-Quiet-Sky coercion.
- §25: AI cannot create facts/rules, change qualification, escalate certainty, perform narrative rescue or release semantically unvalidated output.

These are controlling boundaries. They do not authorize adding product content or loosening release validation.

## 3. Exact A9 candidate source findings

Exact A9 candidate: c8dab3542d3d4725cf591630c07f76366f7949d0.

| Source | Git blob SHA-1 | Directly established |
|---|---|---|
| src/ce/canon/registry.py | ae1bc1a83f712c8ca15a2d05b56310bec341332d | Schema validation, duplicate-ID rejection, versioned digest and empty registry representation. Empty lookup raises CanonRegistryNotEstablished; module-level get_rule deliberately raises because the registry is not materialized. |
| src/ce/claim/manifest.py | 20e64047510a98aa34c5a84abc50885b12ca76b3 | Manifest derives from a CanonRule, embeds Canon version, registry digest and rule ID, binds the signal reference and derives identity digest. |
| schemas/allowed_claim_manifest.schema.json | e1b9f46cae1c584a46cf83eb1953ccd376b38028 | Closed-object schema requiring manifest identity, Canon/registry identity, signal binding, claim scope and evidence/numeric/disclosure restrictions. |
| src/ce/output/validation.py | 7474c55c7323dc446e4799b3db4f6dc16a1b75a6 | Constrained output/provenance/manifest matching, single-claim shape, allowed subject/scope/modality/tense, certainty ceiling, evidence/numeric references and hard forbidden-language patterns. Critically, it adds semantic_conformance_unavailable when no verifier is supplied. |
| src/ce/output/semantic.py | b33e37111770e55521c50f01ee6c7b699b5d9c61 | get_verified_semantic_conformance() deliberately returns None until a controlled, non-caller-supplied semantic verifier is established and independently verified. |
| src/ce/claim/authorization.py | 59a88041cbf39c86faeffdef65a50dcb866b93d5 | Full release decision calls the verified-semantic-verifier getter and also requires runtime authorization, valid calculation/evidence, exact derived signal, rule/registry/manifest consistency and provenance. |
| tests/test_time_signal_boundaries.py | 414b9089ab5e47e067907acb94b1650573530ca4 | test_bad_canon_rule_does_not_fallback asserts that a non-materialized rule lookup raises CanonRegistryNotEstablished. |
| tests/test_ce_r0_full_boundary_r1.py | c39b2d5aa55edcc0a77fa6451b2d911dc12ab59d | Tests explicit rejection when semantic conformance is unavailable and rejection when runtime identity is not authorized. Its positive isolated validator test injects a test lambda, not the production verifier. |

The PR #26 changed-file inventory contains Canon/Manifest/Output code and JSON schemas, but no populated Canon-rule data file. This is a bounded finding about the exact inspected candidate tree and search scope, not a universal claim that no external file exists anywhere.

## 4. Correct interpretation of code and tests

Three different things must not be conflated.

1. **Schema/manifest correctness:** a candidate can validate object shapes, stable IDs, digest bindings and permitted fields.
2. **Semantic-output correctness:** the text itself must be checked against the approved meaning and boundary of the manifest. The current candidate deliberately reports the verified checker as not established; structural checks and a caller-injected lambda are not a production semantic verifier.
3. **Release authorization:** even semantically conforming candidate output is not releasable unless exact Canon registry binding, evidence binding, calculation state and runtime authority checks also succeed.

The existing tests prove useful failure behavior. They do not establish a production-ready language path. In particular, a test-only semantic_conformance=lambda text, manifest: True checks that the structural validator accepts an isolated conforming example; it cannot substitute for the deliberately absent verified release-path checker.

## 5. Implications for open Zero-Point areas

| Area | Source-grounded disposition | What remains unresolved |
|---|---|---|
| A3 — Today’s Note | The recorded owner direction is narrow: a separate non-personal note may accompany valid Quiet Sky only when an approved item exists; omit when none exists; never mask failure. Product/Canon/AI contracts prevent the Note becoming a signal, Canon claim or prediction by presentation alone. | No approved editorial library/source, selector, locale policy, exact UI/content contract or implementation is established or authorized. This note does not authorize any of them. |
| B1 — Canon registry | Preserve schema/provenance rules and fail-closed missing-rule behavior. Canon v1.2 §18 says actual semantic rules must come from a separate reviewed/approved registry. Current A9 get_rule cannot return a rule from the unmaterialized registry. | No populated, approved current V1 rule dataset and promotion lineage established in the inspected tree. Do not create semantic content merely to fill the registry. |
| B3 — Voice boundary | Enforce evidence/state/manifest/semantic constraints as hard gates; evaluate warm/clear/non-fatalistic tone only after meaning and status are preserved. Accurate limitation must not be suppressed due to negative-sounding words alone. | The verified semantic checker is absent and a complete current operative V1 Voice Constitution is not established. Do not implement a blanket lexical ban, forced positivity, or a style gate that overrides facts/state. |
| E3 — Testing/oracle | Exact A9 tests and CI exist; the 28-ID surface has been mapped in the companion crosswalk. | Complete normative cross-domain register and independently qualified semantic oracle/runtime remain not established. Passing fixed-vector tests cannot stand in for an approved semantic source or release path. |

## 6. Admissible next steps

1. Preserve fail-closed code and frozen A9 identity. Do not implement semantic meanings, free-form Today’s Note generation, or production language generation in this review branch.
2. For B1, locate an already-approved versioned Canon registry and prove its lineage, or prepare source-reviewed candidate rules with full provenance and conflict resolution, then seek explicit Canon approval before any active registry exists.
3. For language release, implement and independently validate a controlled semantic-conformance checker only through a later isolated candidate with adversarial/positive/negative regression tests; no verifier is to be wired into an authorized runtime before independent review.
4. For Today’s Note, separately prepare the owner-limited editorial contract: source/rights/approval, locale, deterministic selection, provenance, omission policy and strict separation from personal signal/failure. It remains distinct from the personal output and does not belong in the Allowed Claim Manifest unless a future approved specification explicitly defines that route.
5. Add named tests for the normative v1.4 §24 minimums and bind each to source clauses, test IDs, expected-value provenance and exact runtime profile. This is a candidate coverage plan, not proof that all those tests currently exist or passed.

## 7. Non-actions / authority boundary

- No normative document, Canon meaning, Allowed Claim Manifest definition or current A9 source file changed.
- No production semantic verifier was supplied or enabled.
- No claim about consumer demand, predictive accuracy, runtime readiness or production deployment is made.
- PR #27 remains a draft, non-authoritative candidate; do not merge.
- A10 remains unauthorized; Runtime Adoption, full runtime coverage, TZIF runtime identity, production, deployment and SEAL remain NOT ESTABLISHED / NOT AUTHORIZED.

**End of R0.**
