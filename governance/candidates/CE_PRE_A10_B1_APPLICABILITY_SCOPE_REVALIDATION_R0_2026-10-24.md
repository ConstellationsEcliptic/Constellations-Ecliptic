# CE PRE-A10 B1 — APPLICABILITY SCOPE AND SOURCE-LINEAGE REVALIDATION R0

**Date:** 2026-10-24  
**Classification:** SOURCE-BOUND REVIEW / NON-AUTHORITATIVE CANDIDATE TRACKING  
**Authority effect:** NONE  
**Normative effect:** NONE  
**Canon approval effect:** NONE  
**Implementation / merge / release effect:** NONE  
**FAIL_CLOSED:** TRUE

## 1. Scope and exact tracking baseline

This addendum revalidates B1 only. It supplements, but does not replace, the existing B1 source review and applicability-scope decision packet.

- Mandate candidate R0: blob `10ecf63bb5d235970bf2bd9646a7a25a09446256`.
- Pre-A10 Review Plan R0: blob `d0a74a27a2d239da851d72f79acc1af4c2bcc527`.
- Area Register R4: blob `2795ce51d558c8ac9c9fa711965664868f0c09ee`.
- B1 source-reconciliation brief: blob `b0046c9a7c4532798977d482dc60e525b0ca0f2e`.
- PR #27 candidate HEAD before this addendum: `5a86053eb9954067a5d64c5a2501ec50a541ebba`.
- B1 geometry-binding PR #32 exact HEAD: `1c3459836996ce4cc1a6ffb5ff76cb77e6a488d8`.
- B1 applicability-scope decision packet R0: Box 2537825238196; reported SHA-1 `870b31f562936b05f1542e1226ed07b0e33a8f08`.

Area Register R4 records B1 as `RECOMMENDATION_READY`, `owner_decision_required=true`, with no B1 owner disposition. Its global gate remains `BLOCKED_PENDING_PRE_A10_AREA_REVIEW_AND_SEPARATE_RUNTIME_ADOPTION_GOVERNANCE`; `a10_authorized=false`.

## 2. VERIFIED — current normative source and scope contract

The clean-current-set source was fetched directly from Dropbox, not inferred from a raw-intake copy:

- Document Index v1.9: item `id:siAWKEOCeiYAAAAAAAAAAQ`, path `/CE_V1_CLEAN_CURRENT_SET_R3_2026-09-24/01_NORMATIVE/00_DOCUMENT_INDEX.md`.
- Interpretive Canon v1.2: item `id:dezOICOFazYAAAAAAAAAAQ`, path `/CE_V1_CLEAN_CURRENT_SET_R3_2026-09-24/01_NORMATIVE/04_INTERPRETIVE_CANON.md`, 6,817 bytes, revision `0165d6d856d47440000000390c5d143`.
- Excluded/superseded inventory: item `id:eXEZYv0GSBwAAAAAAAAAAQ`, path `/CE_V1_CLEAN_CURRENT_SET_R3_2026-09-24/00_START_HERE/EXCLUDED_SUPERSEDED_FILES_R3.md`.

Canon v1.2 §§4–7, 13–14, and 17–20 establish that:
- a rule must be provenance-bound and versioned, including rule ID, Canon version, tradition track, source reference/scope, condition, allowed interpretation, forbidden extrapolation, confidence-language boundary, and `applicability_scope`;
- the separately versioned Rule Registry is the source of record for semantic permission;
- missing or conflicting permission produces omission, not a best-guess interpretation; and
- interpretation must remain within the scope of the underlying signal.

The inspected normative text does **not** define a machine-readable vocabulary for rule-level `applicability_scope`, a trusted runtime context contract, or a deterministic context-to-scope predicate.

## 3. VERIFIED — exact B1 candidate source at PR #32 HEAD

The source was fetched at exact PR #32 HEAD `1c3459836996ce4cc1a6ffb5ff76cb77e6a488d8`:

| File | Blob SHA | Observed behavior |
|---|---|---|
| `src/ce/canon/registry.py` | `ae1bc1a83f712c8ca15a2d05b56310bec341332d` | Parses `applicability_scope` as a string sequence and includes it in canonical payload/digest. |
| `src/ce/claim/authorization.py` | `8f580f63f537fe323531c3937cdee6c9296b15f6` | Matches supported signal conditions and geometry selectors from the bound Evidence Packet; does not read/evaluate `rule.applicability_scope`. |
| `schemas/canon_rule.schema.json` | `6c49333c18dbe312f74c2209479e5d0ff93ebfaa` | Declares the scope array and item type; the inspected PR #32 head does not require a non-empty array. |
| `src/ce/output/semantic.py` | `b33e37111770e55521c50f01ee6c7b699b5d9c61` | `get_verified_semantic_conformance()` deliberately returns `None`. |
| `src/ce/output/validation.py` | `7474c55c7323dc446e4799b3db4f6dc16a1b75a6` | Records `semantic_conformance_unavailable` when the verifier is absent and rejects the output. |

This is an incomplete semantic contract in the inspected candidate path, **not evidence of a production authorization bypass**. The absent semantic verifier and output-validation boundary remain fail-closed.

The downstream manifest field `allowed_scope`, rule `condition`, `source_scope`, geometry selectors, and rule `applicability_scope` are distinct concepts. No inspected source establishes that any pair is interchangeable.

## 4. VERIFIED — candidate tests and identity-bound failures

The recorded exact-head GitHub runs are:

- PR #32 dedicated geometry-binding workflow, run [38073807670](https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/actions/runs/38073807670): SUCCESS on PR #32 HEAD `1c3459836996ce4cc1a6ffb5ff76cb77e6a488d8`.
- PR #32 Full Boundary, run [38073807732](https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/actions/runs/38073807732): FAILURE at source identity.
- PR #32 Remediation, run [38073807681](https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/actions/runs/38073807681): FAILURE at source identity.
- PR #32 Trusted Build A9, run [38073807704](https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/actions/runs/38073807704): FAILURE at source/control-plane identity.
- PR #41 consistency-test branch HEAD `59ce585a02f7c407af57da79873bd19cc243daa2`, run [39374391831](https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/actions/runs/39374391831): SUCCESS; reported 88 tests/platform.
- PR #42 non-empty-scope structural branch HEAD `645330589eaf17a4b506699eefc08dd013490e04`, run [39375144094](https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/actions/runs/39375144094): SUCCESS; reported 92 tests/platform.
- PR #43 INT-02/INT-03 candidate-test branch HEAD `7cdebcb5d1542b38941879aac971db62cd4b0e3a`, run [39376027149](https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/actions/runs/39376027149): SUCCESS; reported 95 tests/platform.

These are **different exact heads and separate candidate workflows**. PR #42 and PR #43 are parallel child branches based on PR #41; neither result proves that both follow-ups have been integrated and tested together. The 88/92/95 counts must not be added or described as a single combined suite. Their synthetic tests do not establish approved Canon semantics, independent semantic verification, an active official Test Register, A9 source identity, Source Authority, Trusted Build, Runtime Adoption, or release authority.

PR #32's own record reports that its research source-tree digest `fbc77e725871147d59bf8c58a1409e34fc64c2d9c660efd63e3f99609bb2d9de` differs from the preserved A9 source-tree identity `1a4004ac644331964ab9d540abf6b1631aed1cbbe0cbdd55316fe5356a0c7a8b`; the research control-plane identity `67717c29907c7bc88096ce4f841f016743db72aa1f533b4fb3bd49e1d92d419b` differs from preserved A9 `0bc4f88dc43549a1033434a2a3653c02b46002024630b4294c22ddb8a5f7c357`. These differences must not be erased by changing pinned A9 manifests.

## 5. VERIFIED — official Test Register lineage conflict

The retained Clean Current Set R3 exclusion inventory explicitly excludes the legacy Execution Profile/Test Register v1.5 and other Rev.1 implementation manifests, while its embedded Document Index v1.9 still lists Document 07 v1.5. A later, separately verified one-off documentation-governance successor is now active: Box 2537512845526, `CE_DOCUMENTATION_GOVERNANCE_INDEX_V2.0_ACTIVE_SUCCESSOR_FINAL_R0_2026-10-20.md`, SHA-256 `b4664997618e45e96fb5bfa5cc87175f25a260a35bc8dad0f9021b5ccbad35c6`; its external Post-Apply Adoption Receipt is Box 2537509430090 and records PASS for final read-back/identity verification under decision `CE-OD-GDE01-INDEX-V2.0-2026-10-20-001`. The adopted v2.0 successor explicitly labels Document 07 v1.5 as historical/excluded from R3 and states that active full-register binding remains NOT ESTABLISHED / directly conflicted. This resolves the documentation-index wording for the bounded v2.0 successor, **not** the active full Test Register identity/authority gap.

Therefore:
- historical v1.5 IDs and the 100-ID crosswalk remain lineage evidence only;
- do not reopen the already-approved one-off Index v2.0 disposition or ask for it again;
- no replacement/current official full Test Register identity or binding may be invented or inferred from a raw-intake copy; and
- passing synthetic/candidate tests does not allocate official IDs or close the full-register authority issue.

The earlier Box decision `CE_HUMAN_DECISION_A1_B1_2026-10-04_R1` (Box 2504543582233) selected B1 for **calculation-core test-registry provenance and controlled rebinding**. It is not a decision approving an astrological Canon corpus or the semantic meaning of `applicability_scope`. The overloaded label must not be misread as a Canon disposition.

The B1 applicability-scope packet (Box 2537825238196) has zero Box comments. No separate owner disposition defining scope tokens/context/predicate was established in the inspected sources.

## 6. INFERRED — unresolved semantic and assurance layers

B1 contains distinct blockers that must not be collapsed:

1. Approved, populated current V1 Canon corpus and its exact provenance/approval identity: **NOT ESTABLISHED**.
2. Rule-level `applicability_scope` vocabulary, trusted context, predicate, versioning and missing/unknown/conflict behavior: **NOT ESTABLISHED**.
3. Mapping from approved rule/context to manifest `allowed_scope`: **NOT ESTABLISHED**.
4. Independently controlled semantic-conformance verifier: **NOT ESTABLISHED**.
5. Active official full Test Register identity and binding: **NOT ESTABLISHED / CONFLICTED**.
6. Research candidate source/control-plane identity and separate A9/Trusted Build/runtime gates: **NOT ESTABLISHED / NOT AUTHORIZED**.

A structural non-empty-list check closes only a shape constraint. It cannot decide the field's semantics or make a rule authorized.

## 7. PROPOSAL — preferred disposition

**Keep Option E as the interim state: fail closed and do not implement guessed scope semantics. Prepare Option A, a separate typed Scope Contract, for controlled owner/governance disposition.**

Before any evaluator is implemented, the approved contract must define:
- the scope dimension and vocabulary/version;
- trusted runtime context and its provenance;
- deterministic matching/list/duplicate/precedence behavior;
- missing, unknown, conflicting and mismatching scope outcomes;
- explicit versioned mapping to manifest `allowed_scope`;
- historical-reading compatibility; and
- independent verifier and official Test Register adoption path.

Once authorized, synthetic tests should include identical conditions with different scopes, matching and mismatching trusted contexts, missing/unknown/conflicting scopes, manifest-scope expansion, and registry-version mismatch. These test vectors must validate the approved contract, not invent semantic meaning.

**Rationale:** this preserves the current Canon contract without silently assigning new meaning to a required field. It also avoids turning test success on a modified research branch into a claim of semantic or release readiness.

**User/product consequences:** interpretations remain omitted wherever the required approved rule, scope authorization or semantic verification is absent. This can reduce available reading content, but prevents unsupported or out-of-scope personal claims.

**Risks/dependencies:** delay to semantic coverage; need for controlled source review and a genuine semantic disposition; official Test Register/index conflict; independent verifier design and qualification; exact-source/build identity and separate release gates.

## 8. HUMAN DECISION REQUIRED

A controlled decision is still required for the V1 rule-level `applicability_scope` contract, including whether to approve a separate typed Scope Contract (Option A). The existing Box packet and draft PR #44 prepare that decision but do not record its approval.

No rule-by-rule semantic decision is requested in this addendum. No prior owner decision is reopened.

## 9. UNRESOLVED and next admissible action

Next admissible action: retain the source-bound packet, reconcile the Document Index v1.9 / excluded Test Register v1.5 conflict through its controlled governance route, and obtain the scoped owner/governance disposition for Option A before writing a scope evaluator. Keep the B1 candidate PRs isolated until their dependencies and identities are explicitly reconciled.

No test suite was run in this review. No normative source, Canon rule, registry, schema, production code, official Test Register, A9 manifest, protected candidate identity, PR #26, PR #27, Source Authority, Trusted Build, Runtime Adoption, production, deployment, or SEAL state was changed by this addendum. This register/report is not an authority transition.

**Status:** B1 remains `RECOMMENDATION_READY`; A3 remains open; D4 remains open; Pre-A10 remains blocked.
