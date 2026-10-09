# CE ZERO-POINT AREA A3 — TODAY'S NOTE × QUIET SKY
Date: 2026-10-09
Classification: SOURCE-RECONCILED PRODUCT CHANGE RECOMMENDATION / WORKING CANDIDATE / NON-AUTHORITATIVE
Area status: RECOMMENDATION_READY
Authority effect: NONE
Normative amendment: NONE
Implementation authorization: NONE
Runtime / production / SEAL effect: NONE
FAIL_CLOSED: TRUE

## 1. Executive conclusion

A prior owner disposition exists and has now been retrieved and read. Do not ask the owner to repeat the decision already recorded.

The owner-approved limited semantic direction is:
- TODAY'S NOTE may appear alongside a valid QUIET_SKY result when an approved editorial item is available;
- it is optional, non-personal, and semantically separate from the personal observation state;
- it is not a personal signal, Canon interpretation, prediction, or evidence that a signal exists;
- Quiet Sky remains the true personal state whether a Note appears or is omitted;
- if no approved item exists, omit the Note instead of generating filler;
- technical, calculation, integrity, or semantic-validation failure remains a failure/unavailable state; the Note must not make the failed observation appear complete.

Source: Owner Disposition — Today's Note × Valid Quiet Sky R0, Box 2515533522798. It is expressly non-normative and does not authorize implementation.

## 2. Source and decision reconciliation

### Binding/current normative constraints

- Product Constitution v1.6.1 §4.2: display TESTABLE SKY SIGNAL only when qualification is met; otherwise a valid completed observation with zero qualifying signals is Quiet Sky.
- Product Constitution §5: do not modify qualification or create signals to fill the UI.
- Product Constitution §§8.2–8.3: a non-VALID state must not be represented as Quiet Sky or replaced with stale results.
- Product Constitution §11: presentation may format approved evidence but cannot rewrite numerical state, qualification, Canon meaning, uncertainty, or Allowed Claim Manifest.
- Implementation Plan v1.3.1 §13.2 names TESTABLE SKY SIGNAL + TODAY'S NOTE and says only the testable signal may enter Tomorrow Check.
- Interpretive Canon v1.2 requires approved provenance-bound Canon permission and prohibits invented Canon.
- Evidence/AI Output Validation v1.4 constrains AI to approved evidence, Canon and manifest with fail-closed behavior.
- Privacy Architecture excludes persistent Personal Context and personal/account history from the V1 AI path.

### Existing owner disposition — exact scope

Owner Disposition R0 (Box 2515533522798), titled “Today’s Note × Valid Quiet Sky,” states the optional-note decision above. Its scope exclusions explicitly say it does not approve an editorial database/library, exact UI copy or screen design, selection algorithm, schema or code changes, free-form runtime AI generation, deployment, normative changes, or any change to signal/Canon/uncertainty/manifest/data/entitlement boundaries.

Thus the high-level semantic choice is settled within the recorded limited scope. The full output/content contract is not yet adopted or implemented.

### Bounded UI/editorial source discovery

Source / UI Authority Discovery R1 (Box 2515543958136) records that the examined Box normative/documentation structure and connected GitHub repository did not reveal a separate approved UI specification or editorial library. The GitHub main tree was reported to contain only README.md; inspected A8/A9 candidate trees were calculation-core, product-boundary, schema, build/provenance and test materials, not consumer-facing UI.

This is a bounded result, not proof of universal non-existence. No source should be described as an approved UI authority based on these results, and the absence of a located UI source does not authorize a workaround.

## 3. Recommendation

**Adopt a curated, versioned, review-approved editorial library as the V1 candidate design; do not use free-form runtime LLM generation for TODAY'S NOTE.**

Suggested item contract, subject to controlled change:
- stable editorial_item_id and immutable item version;
- explicitly approved locale;
- reviewed text and provenance/rights metadata where applicable;
- explicit class NON_PERSONAL_EDITORIAL_REFLECTION;
- personalized = false;
- identifiable reviewer/approval record and effective state;
- optional non-personal editorial tags only.

Select deterministically from eligible approved items, with auditable provenance. The selector must not read birth data, personal signal, account history, feedback, purchase/credit state, inferred traits, or hidden profile. Locale fallback is permitted only to a separately reviewed version; otherwise omit the Note.

Reasons:
1. It preserves the owner-approved optional-note behavior while keeping the personal state truthful.
2. A source/version/approval record gives editorial material traceability and rollback.
3. Deterministic selection reduces semantic drift and does not require sending personal data to an LLM.
4. Omission is safe and explicitly permitted; there is no need for synthetic filler.
5. It does not change signal qualification, Canon meaning, forecast certainty, Tomorrow Check, or personal-data scope.

## 4. Required state contract for any later implementation

| Observation state | Personal result | TODAY'S NOTE |
|---|---|---|
| Valid completed observation with qualified Testable Sky Signal | Display only the authorized qualifying signal under its existing contract. | Optional, distinct editorial item if approved/effective and locale-valid. Must not expand or reinterpret the signal. |
| Valid completed observation with zero qualifying signals | Display QUIET_SKY as the true state. | May appear separately if approved/effective and locale-valid; absence is also valid. Never acts as a substitute signal or personal reading. |
| Any non-VALID, incomplete, technical, calculation, integrity or semantic-validation failure | Display the actual failure/unavailable/recovery state. No stale output. | Suppress in the personal reading surface if it could imply completion. A genuinely separate public editorial surface is a different contract. |
| No approved/effective item or no approved locale variant | Preserve the actual personal result state. | Omit; no filler generation. |

TODAY'S NOTE is not eligible for Tomorrow Check. Tomorrow Check only evaluates the Testable Sky Signal through its own categorical feedback contract.

## 5. Acceptance tests required before adoption

These are proposed test cases, not executed tests:
- Valid signal + Note: distinct slots/classes/provenance; Note cannot modify signal.
- Valid Quiet Sky + approved Note: state remains Quiet Sky; Note is general editorial.
- Valid Quiet Sky + no Note: Quiet Sky still completes with no filler.
- Failure + approved Note: actual failure state remains visible; Note cannot mask it.
- Change Note text/source/version: signal identity/qualification and Tomorrow Check eligibility stay unchanged.
- Vary birth data, personal signal, account history, feedback, purchases and Credits: selector does not read or depend on them.
- Locale unavailable: omit unless approved locale fallback exists.
- Unsupported celestial, personal, predictive or causal claim in Note: reject from editorial class.
- Negative-sounding word alone: no rejection solely on lexical negativity when text is accurate, non-alarmist and within the approved class.
- Missing Canon rule: Note cannot compensate by manufacturing interpretation.
- Repeated selection with same eligible source/version/input: deterministic reproducible item and provenance.

No Test Register change is authorized here, and no test is claimed to have been executed.

## 6. Change-control path and open boundary

Before implementation:
1. Reconcile the precise proposed clauses against exact current source lineage.
2. Decide through CE change-control whether and how the normative contract should be added (Product Constitution/Implementation Plan and any needed schema or data specification).
3. Establish the actual content-owner/review role and editorial item lifecycle.
4. Prepare the controlled diff, schemas and tests in an isolated candidate.
5. Validate UI rendering against valid, missing-note and failure states.
6. Independently review and verify the candidate before any later promotion/release gate.

No new owner decision is needed about the already-approved limited permission to show an optional Note alongside valid Quiet Sky. A focused owner discussion will be needed only if the recommended broader contract (content class/source/locale/display/approval lifecycle and normative amendment) is ready for controlled acceptance. No implementation or normative amendment is authorized by this brief.

## 7. Evidence references

- Owner Disposition R0: https://app.box.com/file/2515533522798
- Source/UI Authority Discovery R1: https://app.box.com/file/2515543958136
- Today's Note × Quiet Sky Contract Recommendation R0: https://app.box.com/file/2515537459111
- Voice Integrity & Today's Note Change-Control Packet R1: https://app.box.com/file/2515541872217
- Product Constitution v1.6.1: https://app.box.com/file/2491704535193
- Implementation Plan v1.3.1: https://app.box.com/file/2491699264134
- Interpretive Canon v1.2: https://app.box.com/file/2485337228722
- Evidence, AI & Output Validation v1.4: https://app.box.com/file/2485336395859

End of A3 recommendation.