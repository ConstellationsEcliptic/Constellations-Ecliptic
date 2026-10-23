# CONSTELLATIONS ECLIPTIC
# PRE-A10 A3 — SOURCE RECONCILIATION AND OWNER DECISION BRIEF R1

Date: 2026-10-10  
Classification: SOURCE-BOUND DECISION SUPPORT / WORKING CANDIDATE / NON-AUTHORITATIVE  
Reviewed baseline candidate head: 075be3e3ceb1c36943b43656cb672530c8ff67ae  
Authority effect: NONE  
Normative amendment: NONE  
Schema, code, editorial-data mutation: NONE  
Runtime, production, deployment, SEAL effect: NONE  
Fail-closed posture: PRESERVED

## 1. Executive finding

A3 is not ready to close. The existing owner decision resolves the narrow semantic question: a separate, optional, non-personal TODAY'S NOTE may accompany a valid QUIET_SKY result when an approved item exists; otherwise omit it, and never let it disguise a failed observation. It does not approve an editorial source/library, exact copy or UI, selection policy, locale/fallback, schema/code, runtime generation, normative amendment, official-test integration, or deployment.

Preferred candidate design: a curated, versioned, reviewed, non-personal editorial library with deterministic selection and omission whenever an item is not demonstrably eligible. No personal inputs and no free-form runtime LLM should participate in this V1 path.

A material scope question remains: may TODAY'S NOTE also accompany a valid Look Today result that has a qualifying signal, or is the first approved scope limited to valid QUIET_SKY? Implementation Plan §13.2 names TESTABLE SKY SIGNAL plus TODAY'S NOTE, but the recorded owner disposition expressly settles only the valid-QUIET_SKY case. Do not silently treat the broader display scope as approved.

Recommended area status: OWNER_DISCUSSION_REQUIRED. Keep A3 open until the remaining product-scope disposition is recorded and source/library, locale/cycle, normative and official-test dependencies are resolved through their proper routes.

## 2. VERIFIED — sources and decisions

### Product state and failure boundary
- Product Constitution v1.6.1, Box 2491704535193, §4.2: show a Testable Sky Signal only when qualification requirements are met; a valid completed observation with zero qualifying signals is QUIET_SKY.
- Product Constitution §5 prohibits loosening qualification or manufacturing a signal to fill the UI.
- Product Constitution §§8.2–8.3 keep non-VALID technical/input/integrity states separate from QUIET_SKY and prohibit stale substitution or downstream relabelling of failure.
- Product Constitution §11 prohibits presentation from altering numerical state, signal qualification, Canon meaning, uncertainty or Allowed Claim Manifest.
- Implementation Plan v1.3.1, Box 2491699264134, §13.2 describes Look Today as TESTABLE SKY SIGNAL plus TODAY'S NOTE and limits Tomorrow Check input to the testable signal.
- The archive/member audit in this branch identifies Product Constitution v1.6.1 and Implementation Plan v1.3.1 as controlled successors of the versions inside Clean Current Set R3. Their bytes are distinct from the archive members; do not claim exact byte identity with the earlier versions.

### Canon, AI and privacy
- Interpretive Canon v1.2, Box 2485337228722, §§4–6 and 17–18: semantic permission must come from source-reviewed, provenance-bound, versioned rules. Missing or unmatched Canon permission cannot be filled with a plausible interpretation.
- Evidence, AI & Output Validation v1.4, Box 2485336395859, §§3–5 and 9–12: Core uses deterministic templates; AI is not a source of facts or Canon meaning; missing/invalid evidence or semantic conformance fails closed.
- Privacy Architecture Minimal V1 v1.5, Box 2485335589220, §§12–13 and 24: persistent Personal Context, account-history reuse, raw free-text storage, hidden profiling and behavioral personalization are excluded from the current V1 path.
- Public CE editorial scope does not by itself authorize using the same material as a Personal CE result component.

### Owner disposition and bounded source discovery
- Owner Disposition — TODAY'S NOTE × Valid QUIET_SKY, Box 2515533522798: optional, separate, non-personal Note may accompany valid QUIET_SKY when an approved item exists; omit if none exists; do not present a failed observation as complete. It explicitly does not approve a library, exact copy/UI, selection algorithm, schema/code, runtime generation, normative amendment or deployment. It does not expressly settle display beside a qualifying signal.
- Source/UI Authority Discovery R1, Box 2515543958136, records that its examined Box/GitHub scope did not identify a separate approved current UI specification or TODAY'S NOTE library. This is bounded, not universal, absence.
- Product/Voice/TODAY'S NOTE Controlled Change Proposal R2, Box 2517767431094, is still a proposal; it separates hard integrity constraints from flexible style guidance and says the approved UI/product contract was not found in the inspected scope.

### Implementation and test evidence
- A9 PR #26 remains OPEN / DRAFT / DO NOT MERGE at exact HEAD c8dab3542d3d4725cf591630c07f76366f7949d0. Its inspected tree has 213 entries and no consumer-facing UI, editorial-library or TODAY'S NOTE implementation path. The inspected product-boundary tests cover backend state/fail-closed behavior, not a Note selector or rendered UI.
- A9 src/ce/product/boundary.py preserves non-VALID calculation state and denies Quiet Sky on non-VALID states. tests/test_product_boundary_fail_closed_r1.py and tests/test_product_boundary_r1.py exercise that boundary; they do not test TODAY'S NOTE.
- The candidate A3 contract is blob aaf21cf931e18b727d09f3c5cb211c8094f2f19c. Its acceptance tests are proposed, not executed product tests.
- Clean Current Set R3 archive/member audit says legacy Test Register v1.5 is excluded even though the older archive index still references it. The current characterized stack does not bind an approved full successor CE behavior-test register. Do not insert proposed A3 tests into a presumed-authoritative register.
- At baseline head 075be3e3ceb1c36943b43656cb672530c8ff67ae, Actions run 38055122534 passed register validation and 14 validator unit tests. Its separate strict completion gate correctly remained blocked at the required-completion step with A3/B1/D4 open. These are control-plane tests, not CE editorial product tests; the result applies only to that exact head.

### Cross-store search boundary
Targeted Box, ChatGPT Library, Dropbox and GitHub searches were made for an approved TODAY'S NOTE source/library/UI contract and prior disposition. Box contains the specific owner disposition and non-normative proposals cited above. Library search surfaced historical lineage/audit material but did not establish a separate approved A3 library or UI contract. Targeted Dropbox searches returned no relevant hit. GitHub inspection surfaced candidate proposals and A9 calculation/product-boundary code, not a consumer UI implementation. These bounded outcomes do not prove that no unindexed/private/local artifact exists.

## 3. INFERRED

1. The Plan's two-component description indicates design intent for a signal plus a distinct Note, but it does not fully specify content authority, eligibility, state mapping, locale, rotation, rendering or implementation.
2. The owner-approved QUIET_SKY case is settled and must not be re-asked. Extending the explicit permission to signal-present states remains unresolved unless a higher-authority record is found.
3. No implementation-completeness claim is supported by the A9 calculation-core candidate. A separate editorial data/selection/display path and dedicated tests would be required after controlled approval.
4. Omitting an unavailable Note is compatible with the approved state; it is safer than filler or an unapproved runtime-generated substitute.

## 4. PROPOSAL — preferred design

- Start with CE-authored, non-personal editorial items. External material should remain ineligible until provenance, rights/permission, attribution and review obligations are recorded.
- Use immutable item versions with stable non-personal ID, explicit approval status, exact locale, reviewed text, fixed content class, non-personal flag, accountable reviewer record, provenance/rights and effective/withdrawal window. These are candidate requirements, not an approved schema.
- Use a deterministic selector bound to an approved library digest and a versioned selection policy.
- Limit inputs to approved product state/surface, eventual supported-locale policy and an explicitly approved editorial-cycle key.
- Do not derive the cycle key from birth data, signal timing or account history. Do not assume the UTC purchase service-day boundary also governs editorial rotation.
- Do not use birth date/city, signal geometry, feedback, account identity/history, prior readings, Personal Context, credits, purchase state or inferred traits.
- Do not use a free-form runtime LLM to author, rewrite, personalize, translate or repair the Note in V1.
- If there is no approved/effective item, exact locale match, valid digest, or valid content/selector state, return OMIT_NOTE. The underlying valid personal state remains unchanged.
- Suppress the Note on non-VALID calculation, input, dependency, integrity or semantic-validation states whenever it could imply a completed personal observation.
- Keep it visibly and semantically separate. It never enters Tomorrow Check, the Qualified Signal Record, Canon, Allowed Claim Manifest, personal evidence chain or a claim-accuracy measure.

### Proposed acceptance tests, not executed
1. Valid QUIET_SKY plus approved item leaves QUIET_SKY unchanged and renders a separate Note.
2. Valid QUIET_SKY with no eligible item shows no filler.
3. If signal-present display is approved, the signal identity/qualification remains unchanged and the Note stays separate.
4. Any non-VALID state with a Note available remains failure/unavailable, never QUIET_SKY or stale output.
5. Withdrawn, expired, unapproved, malformed, wrong-version or wrong-locale items are omitted.
6. Same approved library digest, policy version and permitted inputs yield deterministic selection.
7. Variation in personal inputs, feedback, account history, Credits or purchase state does not change selection and is not passed to the selector.
8. Note never enters Tomorrow Check or compensates for missing Canon permission.
9. Removing the Note has zero effect on astronomy, qualification, evidence, Canon, uncertainty or manifest identity.
10. Truthful mismatch/limitation wording is not forced into positivity by a lexical-only rule.

## 5. HUMAN DECISION REQUIRED — bundled A3 scope

| Option | Scope | Benefits | Costs / risks | Assessment |
|---|---|---|---|---|
| A — Narrow | Note only beside valid QUIET_SKY, exactly within the explicit owner disposition; signal-present Look Today has no Note until separately approved. | Smallest extension beyond the recorded decision; lowest immediate conflation risk. | May leave the Plan's two-component description only partly realized. | Safe fallback. |
| B — Consistent valid-state component (preferred) | Optional separate Note may accompany any valid completed Look Today state, with a qualifying signal or valid QUIET_SKY, only under an approved content/locale/selection/display contract. | Best fit to the Plan's two-component description and a consistent optional editorial region. | Extends beyond the explicit Quiet Sky disposition; needs an owner decision and strict separation/consumer validation. | Preferred recommendation, NOT approved. |
| C — Remove personal Note from V1 | Keep editorial content on Public CE; Personal Look Today shows only signal or QUIET_SKY. | Simplest Personal CE surface. | Conflicts with the Plan's Note component and the already-approved optional Quiet Sky direction; requires a controlled product decision. | Not preferred without contrary evidence. |

Further dependencies: prefer a CE-authored initial corpus; exact-locale match and omit on mismatch; no implicit fallback; leave editorial cycle/rotation unset until its time basis is reconciled; name the accountable editorial review function; reconcile D4 locale policy before finalizing supported locales; establish the official Test Register and source/adoption route before normative/test integration.

## 6. HYPOTHESIS — consumer effect

A separate Note might make the surface feel more intentional or readable, especially on QUIET_SKY. No CE first-party test establishes increased appeal, trust, return rate, conversion or retention. Do not claim such a benefit as fact. The already-recorded A4 direction calls for pre-launch validation of comprehension, expectations, usability and value proposition through consented qualitative research and only already-permitted aggregate measures. Engagement must not alter astronomy, qualification, Canon or uncertainty.

## 7. UNRESOLVED risks and dependencies

- No separately approved editorial library/corpus, current UI specification, exact Note copy or Personal CE rendering contract was established in the inspected scope.
- Display scope with a qualifying signal remains unresolved.
- Supported locales, fallback, cycle/rotation key and time basis remain unresolved; D4 is still open.
- Editorial approval role/lifecycle, rights process, schema and library digest format remain proposed.
- The active official full CE behavior-test register and complete fixture-to-approved-oracle binding remain NOT_ESTABLISHED in the characterized stack.
- No TODAY'S NOTE implementation or product-specific test run was established in the inspected A9 candidate.

## 8. Next admissible action

1. Record A3 as OWNER_DISCUSSION_REQUIRED in the non-authoritative area register; keep the strict gate blocked.
2. Bring the consolidated A/B/C decision to the owner only after the packet is ready. Do not repeat the already-recorded Quiet Sky permission.
3. After the disposition, reconcile the exact contract with Product Constitution, Implementation Plan, Evidence/AI Validation, Privacy Architecture, the canonical UI/output contract and the formally identified official Test Register through controlled change management.
4. Only after source route and required tests are established may implementation be prepared.

No normative source, official Test Register, editorial corpus, schema, product code, UI, A9/A10 source, trust root, Source Authority, Trusted Build, runtime authority, production state or SEAL was changed or established by this review.

A3 status: OWNER_DISCUSSION_REQUIRED.  
Pre-A10 review: INCOMPLETE.  
A10: NOT AUTHORIZED.

---
End of R1.
