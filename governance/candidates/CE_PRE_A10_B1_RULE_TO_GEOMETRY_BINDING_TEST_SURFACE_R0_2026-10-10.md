# CONSTELLATIONS ECLIPTIC
# PRE-A10 B1 — CANON RULE / GEOMETRY BINDING TEST-SURFACE REVIEW R0

**Date:** 2026-10-10  
**Classification:** SOURCE-BOUND TECHNICAL REVIEW / WORKING CANDIDATE / NON-AUTHORITATIVE  
**Scope:** Exact A9 source candidate `c8dab3542d3d4725cf591630c07f76366f7949d0`; Canon rule applicability and test surface  
**Authority effect:** NONE  
**Normative amendment:** NONE  
**Canon-rule activation:** NONE  
**Code/schema/registry/runtime effect:** NONE  
**A10 / Runtime Adoption / production / SEAL effect:** NONE

## 1. Purpose

This note records a bounded review of the exact A9 Canon/claim code, related schemas, and directly relevant test files. It sharpens the technical work needed before any real V1 Canon rule corpus can be materialized. It does not author or approve a Canon meaning.

## 2. Normative anchor

Interpretive Canon v1.2 (Box 2485337228722) makes the versioned, provenance-bound Rule Registry the source of semantic permission. Each real rule needs a source reference and scope, tradition track, condition, allowed interpretation, forbidden extrapolation, confidence-language boundary and applicability scope. No matching rule means no interpretation; the runtime may not invent a best-guess rule. Canon rules cannot rewrite calculation or signal qualification.

Evidence, AI & Output Validation v1.4 (Box 2485336395859) makes the Allowed Claim Manifest a derivative of an approved rule, requires output validation and semantic conformance, and requires the claim-release path to fail closed where a rule, manifest or semantic validation is absent.

## 3. Exact A9 source observations

The following blob identities were fetched at exact A9 HEAD `c8dab3542d3d4725cf591630c07f76366f7949d0`.

| File | Blob SHA-1 | Relevant implementation fact |
|---|---|---|
| `src/ce/canon/registry.py` | `ae1bc1a83f712c8ca15a2d05b56310bec341332d` | Registry/rule schema handling, duplicate-ID rejection and canonical digest exist; module-level lookup raises `CanonRegistryNotEstablished` because no actual registry is materialized. |
| `schemas/canon_rule.schema.json` | `770bfa661bdae89a569e8555155c97fe5b3ad2af` | Rule shape is closed at the top level, but `condition` is currently an object with `additionalProperties: true`; this schema does not define the supported condition-key/value contract. |
| `src/ce/claim/authorization.py` | `59a88041cbf39c86faeffdef65a50dcb866b93d5` | `_SUPPORTED_RULE_CONDITION_FIELDS` accepts only `classification`, `kinematic_phase`, `phase_uniformity`, and `requires_uncertainty_disclaimer`. Unknown keys cause `_rule_matches_signal` to return false. |
| `src/ce/signal/record.py` | `b496ddc397cc28d4be18cdd468fa233e46e7c516` | QSR issuance derives from an issued Evidence Packet and requires exactly one unique identity tuple consisting of transit object, natal/scenario, aspect and directed branch. The QSR object itself exposes broad classification/phase/uncertainty fields, not that tuple as direct selector fields. |
| `src/ce/claim/manifest.py` | `20e64047510a98aa34c5a84abc50885b12ca76b3` | The manifest binds Canon version, registry digest, rule ID, signal reference, allowed claim scope, evidence and constraints. |
| `src/ce/output/semantic.py` | `b33e37111770e55521c50f01ee6c7b699b5d9c61` | The verified semantic-conformance function deliberately returns `None` until a controlled independent verifier is established. |
| `src/ce/output/validation.py` | `7474c55c7323dc446e4799b3db4f6dc16a1b75a6` | If semantic conformance is not provided, validation records `semantic_conformance_unavailable`. |
| `schemas/allowed_claim_manifest.schema.json` | `e1b9f46cae1c584a46cf83eb1953ccd376b38028` | Manifest has an explicit closed-field machine-readable shape and evidence/scope constraints. |

### Correct interpretation

This source does **not** prove a current geometry-mismatch exploit. Unsupported geometry conditions are rejected by the current matcher, which is fail-closed. The actual concern is narrower: the current matcher cannot evaluate a rule that declares a geometry-specific selector, while a rule using only broad supported fields does not itself demonstrate that its approved meaning is applicable to the exact transit/natal/aspect/branch in the Evidence Packet.

Because the actual approved V1 rule corpus is not materialized and the production semantic verifier is absent, the current candidate's end-to-end claim release remains blocked. The geometry binding issue is a technical prerequisite to resolve and verify before enabling such interpretations—not a reason to bypass the existing block.

## 4. Bounded test-surface review

The following relevant A9 test files were inspected directly:

| Test file | Observed coverage | Limit relevant to B1 |
|---|---|---|
| `tests/test_ce_r0_full_boundary_r1.py` (blob `c39b2d5aa55edcc0a77fa6451b2d911dc12ab59d`) | Uses synthetic `TEST_ONLY` rule `TEST-RULE-001` with condition `classification = ROBUST_EXACT_SIGNAL`; exercises constrained output, prohibited modality, release blocking without the internal semantic verifier, missing evidence binding and empty-registry behavior. The isolated output-validator success test injects a test lambda returning true. | The synthetic generic rule and test-only lambda do not qualify the production Canon or a production semantic verifier. In the reviewed tests, no explicit same-classification/same-phase fixture was observed in which a geometry-specific rule selector is checked against the exact Evidence Packet geometry. |
| `tests/test_qualified_signal_record_r1.py` (blob `10916846403d84e40deb97d0d1d57af47a82bd5e`) | Covers QSR materialization, deterministic identity, qualification, uncertainty disclaimer and ambiguous multi-signal rejection. Geometry identity is derived from the packet. | It tests QSR issuance, not geometry-specific Canon rule authorization. |
| `tests/test_time_signal_boundaries.py` (blob `414b9089ab5e47e067907acb94b1650573530ca4`) | Contains `test_bad_canon_rule_does_not_fallback` and calculation/time/signal boundary cases. | Missing/bad-rule fallback behavior is covered; exact geometry-to-rule condition matching is not established by that test. |
| `tests/test_schema_structure_r1.py` (blob `3f40c2f31647d257450691f2aee39e7c65031b2f`) | Checks key schema structures and strict record shapes for current evidence/QSR artifacts. | Schema-structure checks alone do not prove semantic equivalence between accepted Canon condition keys and runtime matcher behavior. |

This is a bounded file-level review, not a claim that every test in every repository has been inspected. The full A9 tree's existence of additional tests, calculation registries or historical oracles does not make those artifacts current Canon authority.

## 5. Candidate test matrix required before enabling a populated registry

These are proposed technical regression cases, not tests executed in this review.

| ID | Candidate case | Required result |
|---|---|---|
| B1-GEO-01 | A rule with explicit, supported geometry selectors is matched against the exact unique geometry identity bound to the issued Evidence Packet. | Match only when every declared selector matches the bound evidence and the rule's reviewed applicability scope permits it. |
| B1-GEO-02 | Change only transit object while preserving broad classification, phase, phase uniformity and disclaimer state. | Geometry-specific rule does not match; no authorized claim is released. |
| B1-GEO-03 | Change only natal object/scenario while preserving broad fields. | No geometry-specific match. |
| B1-GEO-04 | Change aspect or directed branch while preserving broad fields. | No geometry-specific match. |
| B1-GEO-05 | Rule contains a condition key or selector type not supported by the versioned condition contract. | Reject deterministically and fail closed; schema and runtime must not silently disagree. |
| B1-GEO-06 | Evidence packet/signal identity is changed after manifest creation, or the manifest points at a different signal/evidence packet. | Binding mismatch and no release. |
| B1-GEO-07 | Packet has zero, ambiguous, or conflicting geometry identities relevant to the rule. | No authorization; never choose a convenient geometry. Explicit duplicate/conflict behavior must be tested, not inferred from the set of distinct identity tuples alone. |
| B1-GEO-08 | An approved rule is intentionally broad rather than geometry-specific. | Accept only if its actual source review and applicability scope explicitly permit that breadth; the test must not silently assume all rules are either generic or geometry-specific. |
| B1-GEO-09 | Registry is absent/empty, rule ID is missing, rule provenance/version is wrong, or registry digest changes. | No manifest/release; preserve the existing fail-closed path. |
| B1-GEO-10 | The production semantic verifier is absent, unavailable, or not the controlled internally selected verifier. | No release, irrespective of structural-test success or a test-injected lambda. |
| B1-GEO-11 | A geometry-specific rule matches, but language claims exceed that rule's approved scope/certainty or evidence. | Semantic/claim validation rejects it; geometry match alone is never sufficient for release. |

## 6. Preferred technical investigation

Compare two bounded candidate approaches before choosing one:

**Option A — EvidencePacket-bound matching (preferred to prototype first):** pass the already-validated Evidence Packet into rule-matching and compare only a rule's explicitly supported selectors to the exact geometry identity already used to issue the QSR. Preserve signal/packet/manifest digest binding. Define a closed, versioned condition schema and runtime contract in lockstep. This likely avoids changing the public QSR shape, but must first test duplicate/conflicting geometry-record handling and prove the selector set is identical to the evidence that qualified the signal.

**Option B — Explicit geometry identity on a versioned QSR:** materialize the unique selector tuple on the QSR, update its schema/version and consumers, and bind the matcher to those fields. This makes the selector visible at the signal-contract boundary but increases schema/version and compatibility work.

Neither option is adopted here. Before engineering promotion, independently test the chosen contract against exact source requirements, manifest/provenance binding, ambiguous packets and historical compatibility. No real Canon rules should be fabricated to facilitate the prototype; synthetic `TEST_ONLY` rules must be unmistakably identified and never promoted as production registry data.

## 7. State and next admissible action

### Exact A9 state remains unchanged

- Exact A9 candidate HEAD: `c8dab3542d3d4725cf591630c07f76366f7949d0`; source branch/PR #26 was not modified by this prototype.
- Actual approved populated V1 Canon registry: **NOT ESTABLISHED in the inspected A9 candidate tree**.
- Production verified semantic conformance implementation: **NOT ESTABLISHED**.
- Exact A9 matcher does not support geometry selector condition fields. Its current behavior rejects those unknown keys, so the confirmed issue is inability to evaluate geometry-specific conditions—not a demonstrated current wrong-geometry release.
- Current A9 claim-release path remains fail-closed. This prototype grants no release capability.

### Isolated prototype and exact-head test evidence (added 2026-10-10)

Candidate branch: `research/b1-geometry-rule-binding-r0-2026-10-10`. Corrected prototype HEAD: `802408757e33d3d8a255d29b0d912f28b5770224`. Revalidation PR: [#31 — DRAFT / DO NOT MERGE](https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/pull/31).

The prototype uses the EvidencePacket-bound option: rule selectors are matched against the same Evidence Packet used to issue the QSR; it adds a closed condition schema and synthetic `TEST_ONLY` positive/negative regressions. It does not change the QSR public shape and does not contain or activate any real Canon rule.

- Dedicated read-only workflow, PR event [run #37978828630](https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/actions/runs/37978828630): **SUCCESS** on Ubuntu, macOS and Windows, Python 3.13.15.
- All three matrix jobs ran **59 tests each**; each reported `OK`. The source/tests AST-parse step passed, and all jobs reported `PYTHON_BYTECODE_CLEAN=TRUE`.
- The first prototype run failed its positive matching test because immutable EvidencePacket geometry records are `Mapping` objects rather than plain `dict`. The prototype now accepts the immutable mapping interface; the original failure remains visible in [run #37978660234](https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/actions/runs/37978660234) rather than being erased.
- A9-specific Full Boundary, Remediation and Trusted Build workflows for the **modified prototype** stopped at source/control-plane identity gates ([Full Boundary #37978828599](https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/actions/runs/37978828599), [Remediation #37978828550](https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/actions/runs/37978828550), [Trusted Build #37978828545](https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/actions/runs/37978828545)). That is the expected refusal to treat changed source as exact A9; those workflows did not run the full suite. They do not invalidate the previous A9 exact-head result and do not establish Trusted Build for this prototype.

### Shared geometry-identity source refinement (latest candidate, 2026-10-10)

During post-pass review, a second implementation of geometry identity extraction was found in the prototype matcher. Even after passing its targeted matrix, duplicate identity parsers could drift from the signal-issuance contract. The candidate was refined in separate PR [#32](https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/pull/32), branch `research/b1-geometry-binding-single-identity-r0-2026-10-10`, exact head `d6231e3a4d550ad7711e9a5895214c8d9b1b0aa6`.

- `src/ce/signal/record.py` now exposes `signal_geometry_identities(packet)`; QSR issuance uses the same helper.
- `src/ce/claim/authorization.py` calls that same helper and only transforms the sole unique identity into named selectors. It no longer independently parses packet geometry records. Finite selector values are still required by rule matching.
- `tests/test_qualified_signal_record_r1.py` tests the exact identity tuple on a synthetic packet and asserts the ambiguous synthetic packet exposes two identities before QSR issuance rejects it.
- Dedicated workflow [run #37979511807](https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/actions/runs/37979511807) passed on this exact head across Ubuntu, macOS and Windows, Python 3.13.15. Each platform ran **60 tests**, reported `OK`, passed source/test AST parsing, and passed bytecode/cache absence checks.
- PR #32 remains OPEN / DRAFT / NOT MERGED / DO NOT MERGE. The new result is only a targeted 60-test boundary matrix, not full-suite qualification or independent review. It grants no source authority, Trusted Build, Runtime Adoption, production authorization or SEAL.

The earlier 59-test result for PR #31 remains valid only for its earlier head. The original failure and the corrective rerun history are retained in earlier PR/run links; no failed run was removed or re-labelled as a success.

### What is established versus still required

**Established for this candidate only:** the targeted 59-test regression set passes on three operating systems; exact geometry selectors can match or mismatch the unique geometry identity in the issued Evidence Packet; unsupported selectors fail closed; semantic-verifier absence and runtime non-authorization still block release.

**Not established:** complete CE suite on the modified source; independent code review; comprehensive duplicate/conflicting geometry-record cases; normative approval of selector scope; real Canon rule corpus and provenance; production semantic verifier; source authority/trusted-build authority for the new head; Runtime Adoption or production authorization.

Next: run additional focused adversarial/compatibility tests and obtain an independent technical review of the selector contract, while separately preparing a source-reviewed Canon candidate list. Do not promote the prototype, infer source scope, create real rules from synthetic fixtures, or alter normative/product authority. No new owner decision is needed just to continue this technical validation; the owner's later choice of V1 Canon/tradition scope remains protected until a source-backed option set is ready.

---

End of R0.
