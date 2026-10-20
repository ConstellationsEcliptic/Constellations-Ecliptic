# CONSTELLATIONS ECLIPTIC
# B1 APPLICABILITY SCOPE — SOURCE-BOUND SEMANTIC DECISION PACKET R0

**Date:** 2026-10-20  
**Classification:** DECISION SUPPORT / NON-NORMATIVE / NO AUTHORITY EFFECT  
**Applies to:** B1 research candidate only; inspected source identity `1c3459836996ce4cc1a6ffb5ff76cb77e6a488d8`  
**Disposition:** SCOPE SEMANTICS NOT ESTABLISHED — KEEP CLAIM RELEASE FAIL-CLOSED

## 1. Purpose

Record the source findings, separate the concepts that must not be conflated, and prepare an owner/governance decision on the V1 `applicability_scope` contract. This packet does not choose semantics on behalf of CE, amend a normative document, approve Canon rules, or authorize code/production.

## 2. Executive determination

The clean current R3 Interpretive Canon v1.2 requires `applicability_scope` as a provenance-bound Canon rule field and requires an interpretation to remain within the scope of its underlying signal. The inspected Canon does not define the field's machine-readable vocabulary, the runtime context that selects a scope, or a deterministic matching predicate.

At the inspected B1 candidate HEAD, the parser requires and serializes/hashes `applicability_scope`, but `_rule_matches_signal` evaluates `rule.condition` and derived signal/evidence geometry, not `rule.applicability_scope`. A separate semantic conformance accessor deliberately returns `None`; output validation blocks when semantic conformance is unavailable. This establishes an incomplete technical contract in the inspected candidate path, **not evidence of a production authorization bypass**.

No additional source located in the bounded current-set review closes the gap. Therefore:
- Do not invent scope-token meanings or infer them from field names.
- Do not equate rule-level `applicability_scope` with manifest-level `allowed_scope`.
- Do not derive the missing meaning from the historical V8 Rule Engine's planet/aspect selectors.
- Do not implement an evaluator until scope dimension, vocabulary, context source, matching semantics, compatibility, and approval path are explicitly controlled.
- Keep claim release fail-closed while the independently verified semantic conformance component is unavailable.

## 3. Source inventory and precedence

### 3.1 Clean current normative baseline

1. **Document Index v1.9** — Dropbox path `/CE_V1_CLEAN_CURRENT_SET_R3_2026-09-24/01_NORMATIVE/00_DOCUMENT_INDEX.md`, Dropbox item `id:siAWKEOCeiYAAAAAAAAAAQ`. It assigns interpretation to Document 04 / the versioned Rule Registry, evidence and claim authorization to Document 05, tests to Document 07, and says lower layers may not rewrite higher layers. URL: https://www.dropbox.com/scl/fi/bordcwydxzvxse37r3tqr
2. **Interpretive Canon v1.2** — clean current source `/CE_V1_CLEAN_CURRENT_SET_R3_2026-09-24/01_NORMATIVE/04_INTERPRETIVE_CANON.md`, Dropbox item `id:dezOICOFazYAAAAAAAAAAQ`, size 6,817 bytes, revision `0165d6d856d47440000000390c5d143`. URL: https://www.dropbox.com/scl/fi/cuk7agyqbe1itz4ufkrvo
3. **Evidence, AI & Output Validation Specification v1.4** — clean current source `05_EVIDENCE_AI_OUTPUT_VALIDATION_SPECIFICATION.md`, Dropbox item `id:uuf5l2xXGw8AAAAAAAAAAQ`. It defines manifest-level `allowed_scope` as a boundary for claim language/output, with examples such as self-reflection, work/structure, communication, and relationship reflection. URL: https://www.dropbox.com/scl/fi/q6fcerrhyryjlkhegc1ey
4. **CE V1 Technical Contracts v1.0** — `CE_V1_TECHNICAL_CONTRACTS.md`, Dropbox item `id:RPEwLt6E5jAAAAAAAAAAAQ`. Its own status is Controlled Implementation Artifact; it translates the normative stack and explicitly does not replace it. URL: https://www.dropbox.com/scl/fi/p6wdoog7uu7ibn9mcmebd
5. **Clean-set gate state** — R3 marks implementation as DEVELOPMENT_CANDIDATE, Source Authority and Trusted Build NOT_ESTABLISHED, production runtime NOT_AUTHORIZED, SEAL NO, AUTHORIZATION NON_AUTHORIZED, and FAIL_CLOSED TRUE. The governing R3 audit-state document also records unresolved assurance/source-identity/harness blockers.

### 3.2 Exact candidate implementation inspected

Repository: https://github.com/ConstellationsEcliptic/Constellations-Ecliptic  
Inspected B1 head: `1c3459836996ce4cc1a6ffb5ff76cb77e6a488d8`

- [`src/ce/canon/registry.py`](https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/blob/1c3459836996ce4cc1a6ffb5ff76cb77e6a488d8/src/ce/canon/registry.py) parses `applicability_scope` as a string sequence and includes it in the canonical payload/digest.
- [`src/ce/claim/authorization.py`](https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/blob/1c3459836996ce4cc1a6ffb5ff76cb77e6a488d8/src/ce/claim/authorization.py) uses `_rule_matches_signal` to inspect `rule.condition` and signal/evidence geometry; this matcher does not evaluate `rule.applicability_scope`.
- [`src/ce/output/semantic.py`](https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/blob/1c3459836996ce4cc1a6ffb5ff76cb77e6a488d8/src/ce/output/semantic.py) returns `None` from `get_verified_semantic_conformance()` until a controlled and independently verified semantic verifier exists.
- [`src/ce/output/validation.py`](https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/blob/1c3459836996ce4cc1a6ffb5ff76cb77e6a488d8/src/ce/output/validation.py) adds `semantic_conformance_unavailable` when no verifier is available.
- [`schemas/canon_rule.schema.json`](https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/blob/1c3459836996ce4cc1a6ffb5ff76cb77e6a488d8/schemas/canon_rule.schema.json) declares the field structurally; PR #42 adds a non-empty-array constraint but does not define scope semantics.

Related draft candidates:
- PR #32 — shared geometry identity research candidate; source/control-plane identity failures remain.
- PR #42 — rejects an empty scope array; structural only.
- PR #43 — INT-02/INT-03 candidate assertion/test-discovery improvement; unrelated to scope semantics.
- PRs #32, #42 and #43 remain draft / non-authoritative; their test passes do not adopt Canon meaning or authorize release.

### 3.3 Historical Rule Engine

The historical V8 `ce-rule-engine.js`, its test, and Rulebook v1.0 were inspected as lineage only. They use planet-pair/aspect matching and do not define a current V1 scope-token vocabulary, runtime context, or scope predicate. They cannot be used as the missing V1 contract.

### 3.4 Separate Test Register identity discrepancy

The clean R3 current set’s `EXCLUDED_SUPERSEDED_FILES_R3.md` explicitly excludes “the legacy Execution Profile/Test Register v1.5 and other Rev.1 implementation manifests.” However, Document Index v1.9 still lists Document 07 v1.5 in its ten-document normative stack, and the clean current `01_NORMATIVE` directory listing does not contain `07_EXECUTION_PROFILE_TEST_REGISTER.md`.

This is a source/index conflict that must be reconciled through controlled governance. Historical v1.5 IDs may be preserved as historical lineage/crosswalk entries, but their presence in raw intake does **not** itself establish an active official register. Accordingly, the prior 100-ID v1.5 crosswalk is historical reconciliation evidence only; “72 IDs not rebound” is not a count of confirmed gaps in a currently authorized register. Do not restore v1.5 in place, invent a replacement register, or assign historical IDs as active without an approved adoption decision.

## 4. Concepts that remain distinct

| Field / layer | What the inspected source establishes | What it does not establish |
|---|---|---|
| `source_scope` | Required Canon provenance/source field | Runtime context selector or equivalent of `applicability_scope` |
| `condition` | Selector fields the current candidate matcher checks against signal/evidence | Equivalent of rule applicability scope |
| Rule `applicability_scope` | Required, parsed and digest-bound by the candidate model; Canon requires signal-scope discipline | Token vocabulary, context dimension, or comparison algorithm |
| Manifest `allowed_scope` | Downstream boundary constraining what a claim may say | Rule-selection permission or a proven synonym for `applicability_scope` |
| Historical V8 planet/aspect selectors | Legacy geometry matching | Current V1 applicability semantics |

Similar names are not sufficient proof of equivalence.

## 5. Decision options

| Option | Description | Assessment |
|---|---|---|
| **A. Approve a separate typed Scope Contract** | Define the field’s semantic dimension, controlled token registry/version, trusted runtime context, predicate, mapping to downstream claim scopes, unknown/missing behavior, and migration policy. Only then implement and independently verify it. | **Preferred future path**, subject to controlled owner/governance approval. No semantics are selected by this packet. |
| **B. Alias rule `applicability_scope` to manifest `allowed_scope`** | Reuse the output claim scope list as the rule-selection field. | **Not recommended.** It conflates rule applicability with downstream language restrictions and still requires a defined runtime context/predicate. |
| **C. Derive applicability from `condition`, `source_scope`, or geometry selectors** | Treat the existing evidence or provenance selectors as the missing scope contract. | **Not supported by inspected sources.** Duplicates or substitutes different layers without a normative mapping. |
| **D. Remove the required field** | Delete `applicability_scope` from rules/schema/Canon contract. | **Not permissible without a controlled normative revision** because current Canon v1.2 lists it as required. |
| **E. Keep current fail-closed behavior pending a controlled decision** | Do not release interpretation when semantic conformance is unavailable; do not invent a scope implementation. | **Required interim operating state.** It prevents unsupported claims but does not itself complete B1 semantics. |

## 6. Proposed contract shape for review — conditional, not adopted

If Option A is chosen, the smallest implementation-ready decision must explicitly settle all of the following before any code change:

1. **Meaning / dimension:** state whether scope identifies an interpretive domain, a reading/product context, a signal boundary, or another dimension. Do not combine dimensions implicitly.
2. **Vocabulary and versioning:** enumerate canonical scope IDs, definitions, aliases/normalization rules, prohibited values, and registry/contract version. Unknown IDs must not silently degrade to a default.
3. **Trusted context:** define the structured runtime context field, its authoritative source, provenance, lifecycle, and whether a request may carry one or multiple contexts. A caller-supplied label alone must not become semantic authority.
4. **Predicate:** specify deterministic matching (including list semantics), precedence, duplicates, missing context, unknown token, conflicting contexts, and compatibility across versions. No wildcard/default-allow behavior unless explicitly defined and justified.
5. **Manifest mapping:** define a versioned, explicit mapping or derivation from an approved rule/context to manifest `allowed_scope`. Do not assume identity. A missing mapping or scope expansion must reject the claim.
6. **Change and history:** define what happens to historical reading provenance when scope registry or rule versions change. Existing history must preserve the versions used.
7. **Independent verification:** establish a controlled semantic verifier that is not caller-supplied and can be independently tested; retain release blocking until it is established.
8. **Test governance:** bind tests through a reconciled, currently approved Test Register adoption path. Do not use the excluded v1.5 historical IDs as active obligations by assumption.

### Expected negative-path examples after approval

- A rule’s geometry condition matches, but the approved runtime context is outside that rule’s approved scope → **no rule match / no claim**.
- Required context is missing, malformed, unknown, duplicated contrary to contract, or conflicting → **fail closed**.
- The rule matches, but no approved rule/context-to-manifest mapping exists → **no manifest / no claim**.
- The manifest’s `allowed_scope` exceeds the permitted mapping for the selected rule/context → **reject output**.
- A change in scope registry version changes the result without an explicit versioned release transition → **integrity failure**.

These are prospective requirements/examples, not current passing tests or approved CE semantics.

## 7. Required evidence before closure

B1 scope closure requires all of the following at the same exact candidate identity:
- an explicit, approved scope contract and controlled vocabulary/registry;
- matcher enforcement using a trusted runtime context and deterministic predicate;
- explicit mapping and validation across Canon rule scope and manifest claim scope;
- negative-path tests covering missing, unknown, mismatch, conflicting and expansion cases;
- an independently controlled semantic conformance verifier, exercised adversarially;
- exact source/build identity proof and required boundary/remediation/Trusted Build checks;
- reconciled active Test Register identity and ID binding; and
- required human review/dual control under the governing release process.

A cross-platform unit-test pass alone does not satisfy these gates.

## 8. Recommendation and disposition

**Recommendation:** Option E now, while submitting Option A as a controlled owner/governance decision. Do not implement guessed scope semantics or merge the scope-related candidate work. Reconcile the Document Index v1.9 versus excluded Test Register v1.5 conflict separately through the valid documentation-governance path. Follow the governing R3 remediation order for Source Authority, source identity, B7/B8 harness, exact-parent re-verification, and Trusted Build; this packet does not reorder or bypass those earlier gates.

**Current status:** `APPLICABILITY_SCOPE_SEMANTICS = NOT_ESTABLISHED`; `INDEPENDENT_SEMANTIC_VERIFIER = NOT_ESTABLISHED`; `OFFICIAL_ACTIVE_TEST_REGISTER_BINDING = NOT_ESTABLISHED / CONFLICTED`; `PRODUCTION_AUTHORIZATION = NOT_AUTHORIZED`; `FAIL_CLOSED = TRUE`.

No Canon rule, scope vocabulary, registry, runtime code, historical file, test ID, source manifest, authority status, payment configuration, or release gate was changed by this analysis.

**End of packet.**
