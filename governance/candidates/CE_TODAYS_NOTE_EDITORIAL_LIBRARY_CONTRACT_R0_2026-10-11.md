# CONSTELLATIONS ECLIPTIC
# TODAY'S NOTE — EDITORIAL LIBRARY CONTRACT R0

Date: 2026-10-11  
Classification: NON-NORMATIVE CANDIDATE / DESIGN CONTROL ONLY  
Status: DRAFT — NOT APPROVED / NOT IMPLEMENTED  
Authority effect: NONE  
Normative effect: NONE  
Implementation / deployment / runtime authorization: NONE  
A10 / Source Authority / Trusted Build / SEAL effect: NONE

## 1. Purpose and bounded decision basis

This candidate defines the minimum source, lifecycle, validation and display controls that an editorial-item library would need before Today’s Note could be implemented. It does not provide approved text, create a library, approve a selection algorithm, amend a V1 document or authorize code/UI/schema changes.

The recorded owner direction is narrow: an optional, separate, non-personal Today’s Note may accompany a valid `QUIET_SKY` result only when an approved item is available; otherwise omit it. The note is not a personal signal, Canon interpretation, prediction or evidence that a signal exists, and may not disguise any calculation, technical, integrity or semantic-validation failure. See the owner disposition: [Box 2515533522798](https://account.box.com/file/2515533522798).

The owner disposition expressly did not approve an editorial database, copy, selection algorithm, schema/code, free-form runtime AI generation or deployment. This document does not convert those exclusions into approvals.

## 2. Current starting state

- Approved V1 editorial items in this candidate: **0**.
- Approved current V1 editorial library found in the bounded source chain: **NOT ESTABLISHED**.
- Selection algorithm / locale fallback: **NOT ESTABLISHED**.
- Normative Today’s Note contract: **NOT ADOPTED**.
- Official Test Register binding and valid Index-adoption route: **UNRESOLVED**.
- Historical CE 1.4 and 2.0 visual prototypes were found only in Box's raw-inventory intake. Their README calls the embedded text deterministic demo content and says it must not be represented as live astronomical calculation. They are not eligible source records for this library merely because their copy exists.

The companion manifest is intentionally empty. Do not fill it with prototype readings, “energy” scores, lucky attributes, generic horoscope copy or synthesized filler.

## 3. Item lifecycle — proposed, not yet adopted

Each item should be represented by one immutable content version. A material text edit creates a new version; it must not rewrite the text of a previously approved version in place.

Required item metadata:
1. Stable item ID and content version.
2. Exact plain-text content as reviewed.
3. Source identity and a source locator/provenance reference.
4. Explicit rights/use review status and reference to its supporting record.
5. Explicit approval state and approver/decision reference; approval must be traceable to a competent project approval process.
6. Explicit locale; locale fallback behavior is not yet selected and must not be guessed.
7. Last-reviewed timestamp and expiry/review deadline.
8. An affirmative non-personal classification.
9. A deterministic eligibility/selection contract established separately before runtime use.

No item is eligible merely because it is present in JSON, checked into a repository, has a source URL, or has an “approved” string. A later candidate must validate identity, rights status, content approval, locale, review/expiry and policy before display.

## 4. Selection and input boundaries

Any future selection method must be deterministic, reproducible, auditable and independent of personal context. It must not use:
- birth date, birth city, birth time or any calculated birth-chart attribute;
- personal signal, calculated personal sky or Canon interpretation;
- Look Back, Tomorrow Check, user feedback or prior reading;
- account history, raw free text, journal, persistent Personal Context or inferred traits;
- credit balance, purchase history, entitlement or conversion probability;
- behavioral profile, ad identifier, social graph or hidden engagement score.

The exact algorithm, date rotation rule and locale-fallback rule remain **NOT ESTABLISHED**. This candidate does not choose them. Until they are separately specified and accepted through the valid control route, a runtime selector must not be implemented from this document alone.

## 5. Display-state contract

| Underlying personal observation | Today’s Note handling under the recorded limited direction | Required truth |
|---|---|---|
| Valid `QUIET_SKY`, eligible and approved item exists | It may be displayed as a distinct, explicitly editorial item only after the separate item/library/display contract is approved and implemented. | The personal state remains `QUIET_SKY`; the note is not evidence of a signal. |
| Valid `QUIET_SKY`, no eligible approved item | Omit the note; no filler. | `QUIET_SKY` remains a valid complete state. |
| Non-VALID calculation, integrity, input, ephemeris or semantic-validation state | Do not display the note as part of a personal result if it could imply a completed reading. | Preserve the true failure/unavailable state. Never substitute `QUIET_SKY`. |
| Item missing, not approved, rights review unclear, expired, review overdue, invalid or wrong locale | Omit the item. | Item availability cannot change the underlying signal state. |
| Valid personal signal exists | This R0 does not authorize extending note display to this state. | Do not expand beyond the limited owner-approved disposition without a valid decision. |

Today’s Note must never enter Tomorrow Check as the testable signal. It must not qualify, explain away, replace, predict or add to an astronomical/signal/Canon result.

## 6. Fail-closed eligibility predicate — proposal

A selector may return an item only when all required checks are true:
- its stable ID and version are present and unambiguous;
- source/provenance is resolvable;
- rights review explicitly permits intended CE use;
- content approval is explicitly valid for the exact content version;
- locale exactly matches the separately configured display locale, unless a separately approved fallback rule exists;
- the current time is inside the recorded review/expiry window;
- non-personal classification is true;
- the approved deterministic policy selects it;
- the underlying personal observation is valid `QUIET_SKY`;
- no integrity, calculation, input or semantic-validation failure is present.

Missing, malformed, duplicate, unknown, stale, unapproved, expired or unverified values are **ineligible**, not “best effort”. An empty library returns “no note”; it does not fail the valid Quiet Sky state and does not trigger free-form model generation.

## 7. Minimum candidate acceptance tests

These are proposed acceptance cases, not tests already executed or official Test Register IDs:

1. Empty catalogue ⇒ no item; valid Quiet Sky remains Quiet Sky.
2. Exact approved and rights-cleared current-locale item ⇒ eligible for the approved selector only.
3. Draft / in-review / rejected / unknown approval ⇒ omitted.
4. Missing source, missing rights-review record or unclear rights state ⇒ omitted.
5. Expired item or overdue review ⇒ omitted.
6. Wrong locale and no approved fallback ⇒ omitted.
7. Duplicate item ID or ambiguous content version ⇒ catalog validation fails closed for the ambiguous item/library.
8. Content bytes/text changed without a new version and fresh approval ⇒ validation fails.
9. Personal attributes or purchase/engagement fields supplied to selector ⇒ contract violation; no output.
10. Non-VALID personal state ⇒ no Today’s Note in the personal result; failure remains visible.
11. Today's Note passed to Tomorrow Check ⇒ rejected as wrong input type/source.
12. Selection repeated with identical catalogue, policy and eligible state ⇒ reproducible selection.
13. No eligible item ⇒ no generated filler and no false “source available” message.
14. Any test/test-suite failure ⇒ contract remains unqualified; no normative or runtime promotion.

A new, authority-bound Test Register and valid adoption route must be established before treating any acceptance result as official CE V1 coverage.

## 8. Out of scope

This candidate does not approve:
- actual editorial text or reuse of historical prototype readings;
- any astronomical meaning, personal forecast, emotional/personality claim or Canon rule;
- exact UI/copy, design token or display on states other than valid Quiet Sky;
- an editorial CMS/database, API, AI-generated content or automatic publishing;
- locale fallback or an English/en-US-only policy;
- changes to Product Constitution, Implementation Plan, Canon, Allowed Claim Manifest, official Test Register, Index, runtime, A10 or source/build authority.

## 9. Immediate status and next admissible work

The next admissible step is source review and a separate item-level rights/content/locale/approval record, followed by a controlled proposal for selection and display tests. Do not mark A3 complete until an approved current item source/library and its governance/testing controls are established.

**State:** `CANDIDATE ONLY`; `ITEMS=0`; `LIBRARY_AUTHORITY=NOT_ESTABLISHED`; `SELECTOR=NOT_ESTABLISHED`; `IMPLEMENTATION=NOT_AUTHORIZED`; `NORMATIVE_MUTATION=NONE`; `A3=OPEN`; `FAIL_CLOSED=TRUE`.
