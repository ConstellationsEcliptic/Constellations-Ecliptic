# CONSTELLATIONS ECLIPTIC
# B1 — CANON RULE GEOMETRY BINDING AND SEMANTIC RELEASE TEST PLAN R0

Date: 2026-10-11
Classification: NON-NORMATIVE CANDIDATE / SOURCE-BOUND ENGINEERING CONTRACT
Status: PROPOSED — NOT APPROVED / NOT IMPLEMENTED / NOT EXECUTED
Authority effect: NONE
Normative effect: NONE
Official Test Register effect: NONE
Runtime / production / A10 / SEAL effect: NONE

## 1. Purpose and safety statement

B1 concerns the connection between an approved Interpretive Canon rule, the exact qualified signal/evidence that satisfies the rule, the derived Allowed Claim Manifest, and independently verified semantic output.

The current A9 path is fail-closed. The inspected candidate does **not** contain an approved populated Canon rule registry, and `get_verified_semantic_conformance()` returns `None` until a controlled verifier is established. Therefore this review does not claim a known unsupported Canon interpretation has been released. It identifies a prospective binding/coverage gap that must be closed **before** any populated rule registry can be relied upon for release.

No sample Canon rules are created here. No astronomical, astrological or personal claims are authored.

## 2. Exact source identities inspected

Exact A9 candidate head: `c8dab3542d3d4725cf591630c07f76366f7949d0`, PR #26, draft/unmerged.

| Source | Blob SHA-1 | Relevant current behavior |
|---|---|---|
| `src/ce/canon/registry.py` | `ae1bc1a83f712c8ca15a2d05b56310bec341332d` | Typed `CanonRule` shape and canonical digest exist; unpopulated registry raises `CanonRegistryNotEstablished`; module-level getter deliberately fails closed. |
| `schemas/canon_rule.schema.json` | `770bfa661bdae89a569e8555155c97fe5b3ad2af` | Top-level rule fields are fixed, but `condition` is an object with `additionalProperties: true`; selector semantics/known keys are not structurally constrained there. |
| `schemas/allowed_claim_manifest.schema.json` | `e1b9f46cae1c584a46cf83eb1953ccd376b38028` | Manifest carries Canon version, registry digest, rule ID, signal reference, evidence references, epistemic layer, claim scope, modalities and disclosures. |
| `src/ce/claim/authorization.py` | `59a88041cbf39c86faeffdef65a50dcb866b93d5` | `_rule_matches_signal` recognizes only four condition keys: `classification`, `kinematic_phase`, `phase_uniformity`, `requires_uncertainty_disclaimer`; it matches only the broad `QualifiedSignalRecord`. Unknown condition fields are rejected by the current matcher. |
| `src/ce/signal/record.py` | `b496ddc397cc28d4be18cdd468fa233e46e7c516` | Signal identity is derived from evidence; the record’s selector fields are classification/phase/uniformity/disclaimer, while geometry identity is separately represented by records in the evidence packet. |
| `src/ce/calculation/evidence.py` | `933617491dfdb16f9d80f1a75131375558a40fb9` | Evidence packet validates geometry records including transit object, natal object or scenario, aspect, directed branch, deviations, effective orb, qualification and kinematic state; the packet has canonical content identity. |
| `src/ce/output/semantic.py` | `b33e37111770e55521c50f01ee6c7b699b5d9c61` | Independent semantic verifier accessor returns `None` by design until controlled verification exists. |
| `src/ce/claim/manifest.py` | `20e64047510a98aa34c5a84abc50885b12ca76b3` (the schema is a separate file) | Deterministic manifest is generated from a Canon rule and carries Canon registry digest and signal/evidence binding, but depends on the rule registry and release verifier. |
| `tests/test_registry_r1.py` | `03efb7dd4609f070473a13fe8ac7c34ccdc38175` | Validates calculation object/aspect/orb profile registries, not the Interpretive Canon rule registry. |
| `tests/test_time_signal_boundaries.py` | `414b9089ab5e47e067907acb94b1650573530ca4` | Explicitly tests that an unmaterialized Canon rule does not fall back. |
| `tests/test_runtime_gate.py` | `7f397ebb1fe8d0ab634f1db1ffb33bbafc9e7eab` | Contains calculation/time and runtime-gate tests; this review does not treat them as proof of complete Canon geometry applicability coverage. |

Normative source anchors: Interpretive Canon v1.2 (Box 2485337228722) §§4–7, 13–20; Evidence, AI & Output Validation v1.4 (Box 2485336395859) §§7–13, 19, 24–25; Product Constitution v1.6.1 (Box 2491704535193) §§2–3, 11–12. They require provenance-bound versioned Canon rules, no invented Canon, scope-bounded claims and fail-closed validation.

## 3. Confirmed observations vs risk

### Confirmed in the exact code

1. A non-empty matching Canon registry is required; otherwise the Canon release path reports binding failure and no claim is authorized.
2. The independent semantic-verifier accessor currently returns `None`; the output validation/release path cannot establish a successful verified semantic-conformance check from this module.
3. The current signal matcher only matches the four declared broad signal fields. It does not directly inspect `EvidencePacket.geometry_records`.
4. The Canon rule schema accepts arbitrary keys inside the `condition` object, but the current matcher rejects a condition key outside its four-field allowlist. This creates a schema/matcher contract mismatch: schema-valid does not necessarily mean an executable selector is supported.
5. The rule type carries `applicability_scope`, but the inspected matching function does not compare that field to evidence/signal. Do not rely on `applicability_scope` as if enforced by this matcher.
6. The candidate test most directly called `test_registry_r1.py` covers numerical calculation registries, not interpretive Canon applicability. Existing tests ensure absent/bad Canon rules do not fall back, but this review did not find executed deterministic tests proving every allowed geometry-bound Canon selector is checked against exact evidence.

### Not established / must not be overstated

- No approved populated V1 Canon registry was identified in the exact A9 tree inspected.
- No specific released misinterpretation was established from the current candidate.
- This is a forward-looking control/coverage gap under fail-closed status, not proof of an active production exploit or an incorrect astronomical value.
- `condition` flexibility does not itself release a claim today: unsupported keys currently fail the matcher and absent registry/verifier prevents release. The concern is future registry/schema evolution unless the contract remains explicitly constrained and independently tested.

## 4. Candidate binding requirements

Before any approved Canon registry is populated or a semantic verifier enabled, a controlled successor should establish all applicable requirements below.

### 4.1 Rule selectors must be typed and executable

- Replace free-form selector semantics with a versioned, typed schema of supported selector fields and permitted values. Every field must have a single documented source.
- At load time, reject unknown fields, duplicate/ambiguous selectors, unsupported enum values, incompatible type/value pairs and selector fields not implemented by the exact released matcher.
- Do not silently ignore `applicability_scope`, `source_scope`, `condition` or any selector field. Either bind each field to an enforceable invariant or exclude it from executable authorization and document its separate governance meaning.
- Treat schema validation, canonicalization and executable selector semantics as one version-bound package.

### 4.2 Bind a rule to the evidence it actually authorizes

Where a Canon claim's approved scope depends on a specific geometry, a candidate selector contract should explicitly bind at minimum the relevant dimensions that the authoritative Canon source defines, including:
- exact immutable evidence packet ID and content digest;
- qualifying signal ID/record and qualification state;
- geometry-record identity or an unambiguous selector over validated records;
- transit object, natal object or declared scenario, aspect, directed branch, qualification state, relevant phase/kinematic state, and effective orb only where the rule is authored to depend on those fields;
- the rule's intended source scope, applicable V1 domain and observation/evaluation interval;
- calculation/execution profile, Canon version, registry version/digest and manifest version/digest.

This list is a proposed binding floor to be reconciled with the Canon's actual rule semantics, not authority to make every field an astrological selector. Do not synthesize an aspect, choose an alternative geometry or change qualification to make a rule match.

### 4.3 Release invariants

Release must be denied when any of these conditions occurs:
- no registry, no rule, duplicate/ambiguous applicable rules or unresolved conflict;
- rule source/approval/provenance is missing or does not match the adopted Canon release;
- geometry/evidence selector does not match the exact packet;
- Canon/rule/registry/manifest digest, version or signal/evidence reference differs;
- a rule selector references fields the deployed matcher does not implement;
- independent semantic verifier is absent, caller-supplied, unbound to the approved verifier identity, or not independently verified;
- output breaches any allowed scope, epistemic layer, certainty ceiling, forbidden domain/type, evidence/numeric reference or disclosure.

No closest-match, fallback-to-similar-rule, default meaning, LLM-only interpretation, or narrative rescue is permitted.

## 5. Candidate test plan — NOT official IDs / NOT executed

Before these tests can become release evidence, map each to the valid active official Test Register identity through a controlled route and define exact deterministic fixtures and expected state.

| Candidate case | Mutation / input | Expected oracle |
|---|---|---|
| B1-CANON-01 | empty/unmaterialized registry | release rejected; no output stored or user-accessible |
| B1-CANON-02 | unknown rule ID | reject with typed reason; no fallback |
| B1-CANON-03 | schema-valid but matcher-unsupported condition key | registry load/build rejected before release; never silently ignore key |
| B1-CANON-04 | `applicability_scope` not satisfied by exact evidence | reject; source scope mismatch recorded |
| B1-CANON-05 | exact same broad signal fields but a different transit/natal-or-scenario/aspect/directed branch | geometry-specific rule must not match unless its approved selector explicitly allows both |
| B1-CANON-06 | matching geometry identity but different evidence packet content digest/profile/interval | reject stale or mismatched provenance |
| B1-CANON-07 | two overlapping applicable rules with different meanings/claim boundaries | reject/hold for controlled rule-conflict resolution; never choose by registry order |
| B1-CANON-08 | manifest rule ID/digest/Canon version differs from selected approved rule | reject manifest-registry binding |
| B1-CANON-09 | independent semantic verifier returns absent/unknown/unverified | reject; no release |
| B1-CANON-10 | structurally valid output adds claim outside scope or unsupported causality | semantic/output rejection |
| B1-CANON-11 | output adds unreferenced number, astronomy fact, or unsupported certainty | output rejected |
| B1-CANON-12 | failed calculation/ephemeris mismatch or invalid evidence | no Canon claim, no Quiet Sky mapping and no fallback |
| B1-CANON-13 | registry bytes change without registry/manifest digest change | identity check fails |
| B1-CANON-14 | semantic verifier executable changes without controlled version/identity/revalidation | runtime/claim release denied |

The case labels above are local candidate identifiers only, not CE official Test Register IDs. The table records expected testing intent; none of these cases is claimed as executed here.

## 6. Required evidence before B1 can close

1. Approved populated Canon source registry, full rule-to-tradition/source-scope provenance and independent interpretation review.
2. Controlled schema/selector version whose allowed fields equal fields consumed by the exact matcher.
3. Evidence/geometry-to-rule matching implementation and code review, including conflict/ambiguity behavior.
4. Independent semantic verifier implementation identity, training/configuration scope as relevant, reproducible validation harness, versioned test set and independent review.
5. Deterministic rule/geometry/manifest/semantic escape tests bound to the active official Test Register.
6. New exact source/tree identity and trusted build / runtime identity / adoption chain for a successor candidate; never rewrite pinned A9.
7. Demonstrated fail-closed production/release gate after all required evidence is complete. No source-authority or runtime status can be inferred from a unit-test pass alone.

## 7. Disposition

- Existing no-fallback / empty-registry behavior: **PRESERVE**.
- Current output release with missing semantic verifier: **FAIL-CLOSED / NOT AUTHORIZED**.
- Geometry-specific Canon applicability binding: **NOT ESTABLISHED in the current matcher/test set**; must be specified before populating rules that depend on geometry identity.
- Current production defect: **NOT PROVEN**.
- Official Test Register mapping, execution, independent semantic verification, runtime adoption: **NOT ESTABLISHED**.
- Candidate plan: **PROPOSED / NOT APPROVED / NOT EXECUTED**.

No Canon rule or manifest claim was invented, no registry was populated, and no code/schema/test register/normative document/runtime/A10/production/SEAL state was changed.


## 8. Existing B1 prototype reconciliation — PR #32

A follow-up review found that [PR #32](https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/pull/32) already implements part of this candidate plan in an isolated research branch. The current PR resource head is `1c3459836996ce4cc1a6ffb5ff76cb77e6a488d8` (not the old head copied into part of its PR description).

At that exact head:
- `src/ce/signal/record.py` blob `6aa54cf11432a731111c40d7b9a2de98535e7f35` defines the shared `signal_geometry_identities(packet)` extraction used by QSR issuance and matching.
- `src/ce/claim/authorization.py` blob `8f580f63f537fe323531c3937cdee6c9296b15f6` supports four typed geometry fields (transit object, natal object/scenario, aspect, directed branch) plus the four signal selectors, and requires exactly one canonical geometry identity when a geometry selector is present.
- `schemas/canon_rule.schema.json` blob `6c49333c18dbe312f74c2209479e5d0ff93ebfaa` sets `additionalProperties: false` under `condition` and declares typed geometry selectors.
- Dedicated workflow [#38073807670](https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/actions/runs/38073807670) passed **62 selected tests on each of Ubuntu, macOS and Windows**. The set includes exact geometry-selector match, geometry mismatch under the same broad signal, boolean directed-branch rejection, unsupported-key rejection, strict condition-schema parity and shared-identity extraction.

However, this does not complete the B1 release prerequisite:
- Full Boundary [#38073807732](https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/actions/runs/38073807732), Remediation [#38073807681](https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/actions/runs/38073807681), and Trusted Build A9 [#38073807704](https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/actions/runs/38073807704) **fail** at identity checks on this exact PR #32 head.
- Their logs compute candidate source identity `fbc77e725871147d59bf8c58a1409e34fc64c2d9c660efd63e3f99609bb2d9de`, which differs from preserved A9 `SOURCE_TREE_SHA256_V2` `1a4004ac644331964ab9d540abf6b1631aed1cbbe0cbdd55316fe5356a0c7a8b`. The Trusted Build job additionally computes control-plane identity `67717c29907c7bc88096ce4f841f016743db72aa1f533b4fb3bd49e1d92d419b`, different from preserved A9 manifest `0bc4f88dc43549a1033434a2a3653c02b46002024630b4294c22ddb8a5f7c357`.
- The identity mismatch is consistent with a changed research candidate and is not grounds to overwrite A9 manifests. It means this branch has no inherited A9 identity/trust and cannot be described as a current trusted-build successor.
- The candidate matcher still does not appear to enforce `CanonRule.applicability_scope`; that semantic field must either be bound to a tested authorization invariant or explicitly separated from executable selector semantics under controlled source review.
- These results are candidate research evidence. The exact candidate PR remains draft/unmerged, has no source authority or Runtime Adoption, and uses synthetic `TEST_ONLY` rule content only.

Consequently, the present plan is not a duplicate replacement for PR #32. It records the required authority/test gates and residual scope not yet demonstrated by that prototype. The appropriate next step is a controlled successor lineage with source/control-plane identities computed from the exact new tree, the prototype changes and tests reviewed together, all applicable full-boundary workflows rerun on the new exact head, and Source Authority/Trusted Build/Runtime Adoption kept separate. Never update the pinned A9 hash/manifest to make a research branch green.
