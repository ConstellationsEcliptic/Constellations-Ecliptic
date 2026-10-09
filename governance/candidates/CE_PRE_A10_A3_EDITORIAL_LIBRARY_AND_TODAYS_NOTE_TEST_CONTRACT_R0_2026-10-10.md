# CONSTELLATIONS ECLIPTIC
# PRE-A10 A3 — EDITORIAL LIBRARY & TODAY'S NOTE TEST CONTRACT R0

**Date:** 2026-10-10  
**Classification:** SOURCE-BOUND PRODUCT/TECHNICAL REQUIREMENTS PROPOSAL / WORKING CANDIDATE / NON-AUTHORITATIVE  
**Authority effect:** NONE  
**Normative amendment:** NONE  
**Schema / code / editorial-data mutation:** NONE  
**Runtime / production / SEAL effect:** NONE

## 1. Purpose

This note translates the current V1 source boundary and the owner's narrow A3 disposition into a testable candidate contract for a future editorial-library design. It does not approve final note copy, a library, a locale fallback, a date-rotation policy, a schema implementation or deployment.

## 2. Source hierarchy and verified owner decision

### Binding V1 source

1. **Product Constitution v1.6.1** (Box 2491704535193), §4.2: Look Today displays a Testable Sky Signal only when qualification requirements are met; with no qualifying signal, the personal state is Quiet Sky. §5 forbids loosening qualification or manufacturing a signal to fill the UI. §§8.2–8.3 prohibit mapping technical/non-VALID failure into Quiet Sky or presenting stale results.
2. **Implementation Plan v1.3.1** (Box 2491699264134), §13.2: Look Today consists of `TESTABLE SKY SIGNAL + TODAY'S NOTE`; only the Testable Sky Signal may enter Tomorrow Check.
3. **Interpretive Canon v1.2** (Box 2485337228722), §§4–6, 13 and 17–18: semantic permission requires reviewed, provenance-bound, versioned Canon rules. No matching rule means no Canon interpretation; runtime must not invent a best-guess meaning.
4. **Evidence, AI & Output Validation v1.4 / Release V1.6** (Box 2485336395859), §§3–5, 9–12 and 22: Core uses deterministic templates; AI has no independent authority to add claims or Canon meaning; output validation is fail-closed.
5. **Privacy Architecture — Minimal Data V1.5** (Box 2485335589220), §§12–13 and 24: the V1 language path excludes usernames, email, payment data, device identifiers, raw free text, account history and Persistent Personal Context. Core does not need an LLM.
6. **Voice Integrity / Today's Note Change-Control Packet R0** (Box 2515536757604), §§1–4: existing work proposes a curated, versioned library and states that no approved UI specification or editorial library was found in the bounded search. That is a bounded search result, not proof that no such artifact exists anywhere.

### Owner-approved product-semantic direction (limited)

**Owner Disposition — Today's Note × Valid Quiet Sky R0** (Box 2515533522798) expressly permits an optional, clearly separate, nonpersonal editorial item alongside a valid Quiet Sky result when an approved item exists. If no approved item exists, omit it. This is **not** a normative amendment or implementation authorization and does not approve a library, exact copy, selection algorithm, schema/code or runtime generation.

## 3. Required content class

Recommended candidate class identifier: `NON_PERSONAL_EDITORIAL_REFLECTION`.

An item in this class:

- is general editorial reflection, not astronomical fact, qualified signal, Canon interpretation, a user-specific prediction, a causal explanation or a psychological assessment;
- does not claim to explain the user's current personal sky, feelings, traits, relationships or future;
- is never treated as signal evidence, Canon permission, Allowed Claim Manifest input, or a substitute when no Canon rule matches;
- is not evaluated by Tomorrow Check and cannot affect signal comparison or any accuracy metric;
- must not be created or selected from birth data, personal signal geometry, account history, feedback, Personal Context, purchase/entitlement state, credit balance or a hidden profile.

If an item asserts an astronomical fact, user-specific claim, causal relationship or forecast, it is not eligible for this class. It must be omitted or handled by a different, separately authorized contract.

## 4. Minimum candidate editorial record

The following is a proposed review checklist, **not an approved schema**:

| Field | Purpose / candidate constraint |
|---|---|
| `editorial_item_id` | Stable ID that does not encode personal data. |
| `version` | Immutable content version; replacement text receives a new version. |
| `status` | Explicit lifecycle value; only `APPROVED` can be selected. Draft, rejected, expired and withdrawn items are ineligible. |
| `locale` | Exact supported language/locale key; unspecified locale must not silently be interpreted. |
| `text` | Exact reviewed content, not an LLM prompt or an editable runtime draft. |
| `content_class` | Fixed to `NON_PERSONAL_EDITORIAL_REFLECTION` for this surface. |
| `personalized` | Must be false; runtime validation rejects true, missing or unknown states. |
| `source_provenance` | CE-authored source record or exact external source reference. If there is external material, record licensing/permission, attribution obligations and reviewer decision. |
| `approval_record` | Named accountable reviewer identity/role, approval timestamp, approval version and review status. |
| `effective_window` | Optional explicit effective/withdrawal dates, with unambiguous inclusive/exclusive boundary rules. |
| `editorial_tags` | Optional fixed, nonpersonal editorial taxonomy only; never a user-trait classifier. |

The selection/display audit record should be minimal: selected item ID/version, approved library version/digest, locale match, deterministic selection-policy version, applicable product state and omission/selection result. It must not duplicate birth data, signal evidence or account history.

## 5. Candidate deterministic selection contract

Proposed constraints:

1. Input is limited to an explicitly defined product surface/state, supported locale and an approved editorial-cycle key. The exact cycle key/boundary is still open and must not be inferred from birth data or signal time.
2. The selector only considers immutable approved items whose content class is `NON_PERSONAL_EDITORIAL_REFLECTION`, whose `personalized` value is false, and whose approval/effective window is valid.
3. Locale fallback is **not implicit**. If no item satisfies the chosen locale policy, omit the Note. Any deliberate fallback ordering must be documented and approved before implementation.
4. Selection is deterministic for the same library digest, policy version and permitted input tuple. It must not rely on ambient random state, model sampling, account identity or concealed personal context.
5. No eligible item means `OMIT_NOTE`, not an error in the personal observation, not generation of filler and not a fabricated signal.
6. A runtime LLM must not author, rewrite, personalize or repair this class in V1. Existing CE constraints remain stronger than editorial preferences.
7. If any selected item fails integrity, locale, approval, content-class or semantic checks, discard the item and return `OMIT_NOTE`; do not pick an unreviewed fallback.

This note deliberately does not choose whether the cycle key is a UTC service date, local civil date or a release-pinned rotation. That choice changes user-facing behavior and needs a source-backed product decision after the canonical time/locale policy is established.

## 6. State-to-display contract candidate

| Personal observation/system result | Personal state | Editorial Note |
|---|---|---|
| `VALID` with a qualifying signal | Show only the existing qualified signal under its approved contract. | May appear only in a separate editorial region; cannot add to, explain or strengthen the signal. |
| Valid `QUIET_SKY` with zero qualifying signals | Show Quiet Sky as the real personal observation result. | May appear as a separate, nonpersonal item if approved and eligible. Omitting it is also a valid outcome. |
| Any non-VALID calculation, input, integrity, dependency or semantic-validation state | Show the appropriate failure/unavailable/recovery state; do not call it Quiet Sky and do not substitute stale output. | Suppress the Note in the personal result surface so it cannot imply that the current observation completed. |
| No approved item, item withdrawn/expired, locale unavailable, digest invalid or selector error | Preserve the underlying valid personal state if one exists. | `OMIT_NOTE`; no fabricated filler, no user-visible claim that a Note was available. |

The Note component must be independently identifiable and removable without altering the personal state, QSR, Canon rule, Allowed Claim Manifest, Tomorrow Check input or retained reading provenance.

## 7. Candidate acceptance tests

### Library integrity and approval
- A draft, rejected, expired, withdrawn, malformed, unsigned-for-review or wrong-version item is never selectable.
- Changing approved text creates a new version and changes the library digest; old selections remain traceable to their exact version.
- Unknown fields and invalid/missing content-class/personalization/locale values fail closed for the Note.
- Rights/attribution review is recorded for external material; unsupported copied material is not eligible.
- A library digest/provenance mismatch yields `OMIT_NOTE` without changing the personal observation state.

### Determinism and privacy
- Same allowed inputs + same approved library digest + same selector version produce the same output.
- Different birth dates, birth cities, signal geometries, account IDs, feedback values, credit balances, purchase state, account history or Personal Context do not affect eligibility/selection.
- No eligible locale match returns `OMIT_NOTE`; an unapproved fallback locale is never chosen.
- No random call or runtime LLM generation is reachable on this V1 path.
- Editorial audit metadata does not duplicate personal or payment data.

### State and consumer boundary
- A valid Quiet Sky remains Quiet Sky whether the Note is present, omitted, invalid or withdrawn.
- A non-VALID state cannot be converted into Quiet Sky or made to look like a completed reading by a Note.
- The Note cannot be returned by, referenced as evidence in, or alter Tomorrow Check.
- A Note cannot create a Canon claim or bypass a missing/ambiguous Canon rule.
- The Note is visually and semantically separate from the personal sky state and cannot claim personal relevance.
- Removing the Note has zero effect on astronomy, qualification, manifest, uncertainty, or user-reported data.
- Negative-sounding words are not rejected solely by a word list; review checks actual meaning, fear manipulation, fabrication and misleading personalization.

## 8. Change-control order

Recommended order:

1. Identify and check the canonical current product/UI authority location (the previous search was bounded, not universal).
2. Owner reviews the final state/display/locale-cycle option set after sources are reconciled. The narrow Quiet Sky product choice already approved is not reopened without new evidence; this review covers details not approved by it.
3. Complete editorial-source, rights, locale, versioning and deterministic selection contract.
4. Formally reconcile and approve any required normative text changes in a controlled change packet.
5. Only then implement schema/library/selector/UI, with the tests above plus full regression; keep production unauthorized until its separate gates are met.

## 9. Current status

- Core state boundaries: **PRESERVE**.
- Optional nonpersonal Note beside valid Quiet Sky when approved item exists: **OWNER-APPROVED, LIMITED SCOPE**.
- Approved editorial corpus/source: **NOT FOUND IN BOUNDED SEARCH / NOT ESTABLISHED**.
- Final locale/cycle/fallback policy, schema, exact copy, implementation and runtime generation: **NOT APPROVED**.
- This note: **NON-NORMATIVE CANDIDATE ONLY**. No V1 source, code, schema, editorial data or runtime was changed.

---

End of R0.
