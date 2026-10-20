# CONSTELLATIONS ECLIPTIC
# PRE-A10 C3 — PURCHASE-CAP CONTRACT CANDIDATE R2

Date: 2026-10-10  
Predecessor: R1 preserved unchanged  
Classification: PRODUCT CONTRACT CANDIDATE / NON-NORMATIVE / SOURCE-BOUNDED  
Authority effect: NONE  
Normative amendment: NONE  
Official Test Register change: NONE  
Schema / code / runtime / production / SEAL effect: NONE  
Implementation authorization: NONE  
FAIL_CLOSED: TRUE

## 1. Purpose

R1 turns the C3 daily purchase-cap proposal into one state contract for product review, implementation discovery and future QA mapping. It corrects the prior source label: source/member hashes identify the Clean Current Set R3 archive, while newer applied successor records identify the characterized Product Constitution v1.6.1 and Implementation Plan v1.3.1. Global Source Authority is not established, the current full Test Register binding is unresolved, and the authorized commerce/persistence implementation was not found in the inspected scope.

Source reconciliation: [C3 Source-Lineage Reconciliation R0](https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/blob/governance/candidates/ce-autonomous-evolution-charter-r0-2026-10-09/governance/candidates/CE_PRE_A10_C3_SOURCE_LINEAGE_RECONCILIATION_R0_2026-10-10.md) plus the R1 comparison candidate in [PR #35](https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/pull/35). Source crosswalk R1 remains preserved as historical candidate; active pointer route is still open.

## 2. Settled owner baseline — not reopened

- At most one new Deep Sky purchase per authenticated account per CE service day.
- The service day is the UTC Gregorian half-open interval `[00:00:00 UTC, next date 00:00:00 UTC)`.
- One authenticated account shares its allowance across trusted devices.
- The service date is assigned using server-authoritative UTC time at the atomic reservation point after explicit confirmation; client clock and display timezone are not authoritative.

The owner-approved UTC boundary record is [Box 2515555580794](https://app.box.com/file/2515555580794). It approves the boundary/date assignment scope, not the full purchase trigger, remedy or slot state machine.

## 3. Product invariants carried forward

These candidate rules preserve rather than replace the characterized CE rules:

1. Deep Sky sells depth of synthesis, not truth, accuracy, certainty, guaranteed outcomes or psychological authority.
2. Only a valid completed observation with zero qualifying signals can be Quiet Sky; a commercial or technical failure must not be rendered as Quiet Sky or a delivered reading.
3. Commercial state cannot alter astronomy, signal qualification, Canon, uncertainty or calculation identity.
4. Credits top-up is not a new-reading purchase. Rereading an already retained/entitled reading does not create a new purchase or debit.
5. Credits restoration for an attempted reading debit and a monetary/card refund for the earlier Credits top-up are separate operations.
6. Preserve account-bound/non-expiring Credits, stable logical purchase identity, idempotent payment/fulfillment and reconciliation of unknown outcomes.
7. Applicable mandatory consumer rights remain available; this proposal does not decide jurisdiction-specific law or establish that Credits restoration alone is always sufficient.

These are source-mapped design invariants, not a claim of live implementation. See the R1 crosswalk for source identities and limits.

## 4. Separate the state dimensions

One “purchase status” is insufficient. Keep at least four logically distinct dimensions; the labels below are conceptual candidate labels, not approved enum/schema names.

### 4.1 Order and fulfillment state

`NO_ORDER`, `RESERVED`, `DEBITED_PENDING`, `RECONCILIATION_REQUIRED`, `FULFILLED`, `FAILED_PRE_DEBIT`, `TERMINAL_NON_DELIVERY`, `REMEDIED`.

### 4.2 Daily quota state for the immutable service date

`AVAILABLE`, `RESERVED_UNRESOLVED`, `COUNTED`, `RELEASED_AFTER_FULL_REVERSAL`, `CLOSED_EXPIRED_DATE`, `HISTORICAL_UNRESOLVED`.

### 4.3 Credits and monetary ledger state

Top-up/payment settlement, reading-Credits debit, exact reading-Credits restoration, monetary/card refund and other approved financial remedy are separate transactions with separate identities and idempotency. A restoration request cannot mutate an earlier top-up payment unless the separate payment remedy explicitly authorizes that operation.

### 4.4 Entitlement/output state

`NO_ENTITLEMENT`, `GENERATION_PENDING`, `VALIDATION_PENDING`, `ACCESSIBLE_FULFILLED_READING`, `NO_DELIVERY_CONFIRMED`, `REMEDY_ACCESS_REVIEW`.

No unvalidated/stale result is made accessible; no entitlement is granted to a terminal non-delivery order.

## 5. Candidate transition contract

| Trigger / evidence | Order state | Quota state for date D | Credits / entitlement consequence | Required guard |
|---|---|---|---|---|
| Preview only; no explicit confirmation | NO_ORDER | AVAILABLE | No reading debit, slot or entitlement | Never reserve or debit from a preview/click or inferred consent |
| Explicit confirmation at server UTC time on D | RESERVED | RESERVED_UNRESOLVED | Fix immutable D and stable logical order ID; no duplicate order for same account/date while unresolved | Atomic persistence-level account+date coordination is required by design; actual persistence source is not established |
| Different device, same account/date while reservation is active or counted | Competing order rejected or mapped to existing order if same logical identity | Existing reservation/count remains | No second debit or entitlement | Device identity cannot create a second allowance |
| Different authenticated account on D | Independent order may proceed through normal checks | Its own independent date-D quota | No cross-account ledger or entitlement side effects | Must not use device as account/slot key |
| Credits top-up | Top-up states only, not reading-order state | Unchanged | One top-up settlement/grant through existing idempotency | Top-up alone creates no reading slot |
| Reading debit success, fulfillment still processing | DEBITED_PENDING | COUNTED under owner-selected D1-A candidate semantics; normative application remains open | One reading debit; no accessible entitlement yet | Debit result must be authoritative and bound to same logical order and D |
| Debit/order result unknown or conflicting | RECONCILIATION_REQUIRED | RESERVED_UNRESOLVED, or HISTORICAL_UNRESOLVED after D ends | No speculative restoration, refund, duplicate debit, entitlement or terminal label | Timeout, missing callback, worker restart or midnight alone proves nothing |
| Retry of same logical order | Resume/return existing state | Unchanged | At most one reading debit, one entitlement and one application of each remedy | Same identity/date; no second order disguised as retry |
| Proven pre-debit terminal failure | FAILED_PRE_DEBIT | AVAILABLE after exact reservation release, if D is still current; otherwise close historical reservation | No debit/entitlement/restoration fabricated | Positive proof of no debit, entitlement mutation or live downstream operation |
| Recoverable post-debit failure | DEBITED_PENDING / recovery in progress | COUNTED under owner-selected D1-A candidate semantics; normative application remains open | Resume/recover under original order; no new debit or independent entitlement | Bounded retry policy; recovery remains observable and tied to D |
| Valid reading passes output validation and entitlement becomes accessible | FULFILLED | COUNTED | One delivered entitlement and the corresponding debit | Validation and accessibility for the same order both proven |
| Proven terminal non-delivery while D remains current | TERMINAL_NON_DELIVERY then REMEDIED | D2-A: historical alternative not selected; D2-B (owner-selected candidate semantics): RELEASED_AFTER_FULL_REVERSAL only after all guards | Restore exact reading debit once; no reading entitlement. Apply any separate approved money/consumer remedy. | Positive terminal evidence; exact balance/ledger identity; no downstream operation that can still deliver; restoration and operation closure complete |
| Terminal non-delivery only conclusively closed after D ends | TERMINAL_NON_DELIVERY then REMEDIED | CLOSE date D as CLOSED_EXPIRED_DATE; never transfer the old slot | Restore exact reading debit once and keep historical order/date auditable | The new date has its own allowance; do not relabel the old purchase |
| Reread of retained accessible reading | Existing FULFILLED order/entitlement | No new quota use | No new debit, order or entitlement | Same retained reading identity and valid entitlement |
| Post-delivery complaint or remedy | REMEDY review/state separate from original FULFILLED history | Preserve original date and purchase history; no automatic reset | Apply only the separately approved remedy once; mandatory consumer rights cannot be denied by quota | This C3 contract cannot invent the post-delivery remedy policy |
| Repeated known terminal fulfillment failure / unhealthy service | Candidate admission behavior under the owner-approved interlock principle, once the deterministic health contract is implemented | No reservation/consumption for rejected requests | No debit/entitlement for rejected request; clear, truthful unavailable status | Operational threshold/evidence/reset/test contract remains open; no current implementation claimed |

## 6. Decision D1 — event at which purchase counts

### D1-A — confirmed order + committed reading debit (OWNER-SELECTED; candidate semantics, normative application open)

The effective purchase event occurs when the confirmed new-reading order is durably bound to its immutable server-derived UTC service date and the one-time reading-Credits debit is authoritatively committed. Reservation is a concurrency guard before the event, not by itself a committed purchase. Valid accessible fulfillment is later.

Under this option, unknown debit outcome remains unresolved on the same logical order; a proven pre-debit failure can release the reservation once; and a committed debit holds the quota effect while fulfillment recovers or remains pending.

### D1-B — valid accessible fulfillment (alternative not selected; retained for semantic traceability)

The quota is counted only after a valid reading becomes accessible. This is a “one fulfilled reading” cap rather than the recorded “one new purchase” premise. It permits different same-day purchase attempts before valid delivery unless the contract adds another constraint. Do not treat D1-B as a stylistic paraphrase of D1-A.

**D1 boundary:** the owner selected D1-A for candidate semantics on 2026-10-10. This is not yet a normative contract amendment or authorization for production mapping. The exact source/persistence transaction, target contract and applicable adoption route must be identified before official application.

## 7. Decision D2 — terminal reversal effect on the same-date slot

D2 applies only after proven terminal non-delivery, exact reading-debit restoration once, no accessible entitlement, and closure of every relevant order/debit/generation/validation/entitlement operation. It does not apply to timeouts, unknown outcomes or recoverable failures.

- **D2-A — RETAIN_SLOT:** historical alternative, not selected by the owner on 2026-10-10; date-D quota would remain counted after restoration.
- **D2-B — RELEASE_AFTER_FULL_REVERSAL (OWNER-SELECTED; candidate semantics, normative application open):** release the date-D quota once after every guard above is satisfied and only while D is still the current date. A new independent order may then undergo the ordinary confirmation, balance and cap checks. The old order remains immutable and auditable; only its quota effect is reversed.

D1 and D2 are independent. Under D1-A + D2-B, the history of a committed purchase is not deleted, but a fully reversed, never-delivered order no longer occupies the customer's effective quota. The normative wording must express that distinction explicitly. It must not say that every committed order consumes quota unconditionally if the next clause releases quota after a reversal.

If terminal closure happens after D expires, the old date is closed and never transferred; the new date has its own quota. Midnight never proves failure. A pending order from D remains attributed to D and must not consume or be relabelled as a D+1 order merely because fulfillment occurs later.

## 8. Repeated terminal failure — additional design gap

D2-B permits a fresh same-day order after each fully reversed terminal non-delivery. The owner also approved the fulfillment-health interlock principle on 2026-10-10; the operational threshold/evidence/activation-reset contract remains open. Repeated terminal failures therefore remain a genuine implementation/reliability gap.

**Candidate recommendation:** define a deterministic service-level fulfillment-health interlock. When verified service-health evidence meets a pre-approved unavailability rule, stop accepting new paid-reading confirmations globally or for the affected service; disclose temporary unavailability; create no reading debit or quota reservation for blocked requests. Prefer this to a hidden or ad hoc user-level attempt counter, which can penalize a customer for CE's failure. The interlock principle is already owner-approved, but no production threshold, operational evidence source, activation/reset policy, current implementation or approved test exists in this candidate. The reliability/implementation contract must define deterministic health evidence, activation/reset, audit and test oracles before implementation. A hidden user-level attempt counter has not been approved; do not add one by implication.

## 9. Consumer-facing disclosure candidate

Before confirmation, supplement existing preview fields rather than duplicating them. State clearly:
- the one-new-reading daily cap and actual UTC reset instant;
- the distinction between Credits top-up, new-reading redemption and rereading an existing retained reading;
- that a pending/unknown order is being reconciled, not presumed delivered or failed;
- the expected remedy boundary for a recoverable order versus proven terminal non-delivery, without suggesting that Credits restoration necessarily extinguishes mandatory consumer rights.

No fake scarcity/countdown, purchase pressure, paid certainty, paid accuracy or promise that CE guarantees fulfillment timing.

## 10. Candidate testability / promotion boundaries

The [C3 candidate test-oracle map](https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/blob/governance/candidates/ce-autonomous-evolution-charter-r0-2026-10-09/governance/candidates/CE_PRE_A10_C3_TEST_ORACLE_MAP_CANDIDATE_R0_2026-10-10.md) contains deterministic test cases for both decision branches. They are not official IDs, not registered and not executed.

Do not modify Product Constitution, Account/Commercial specification, Implementation Plan, the official Test Register, schema, code or runtime from this document. D1-A/D2-B are already owner-selected as candidate semantics and must not be asked again. First close the exact target/source-binding and persistence-source gates, define the still-open pre-debit failure branch and operational health interlock, then prepare an exact normative delta and map only missing oracles to the official register through the verified route.

## 11. Status

Owner-originated cap premise: EVIDENCED.  
UTC boundary/date assignment: OWNER-APPROVED, LIMITED SCOPE.  
D1: OWNER-SELECTED D1-A FOR CANDIDATE SEMANTICS; NORMATIVE APPLICATION OPEN.  
D2: OWNER-SELECTED D2-B FOR CANDIDATE SEMANTICS; NORMATIVE APPLICATION OPEN.  
Fulfillment-health interlock: PRINCIPLE OWNER-APPROVED; operational threshold/evidence/activation-reset/tests NOT SPECIFIED OR IMPLEMENTED.  
Pre-debit terminal reservation failure/release: SEPARATE POLICY/CONTRACT GAP; candidate behavior is not a complete owner-approved normative policy.  
Official Test Register identity/current binding: NOT ESTABLISHED.  
Authorized commerce/persistence source: NOT ESTABLISHED IN INSPECTED SCOPE.  
Normative sources, official register, schema, code/runtime: UNCHANGED.  
SOURCE_AUTHORITY=NOT_ESTABLISHED; TRUSTED_BUILD=NOT_ESTABLISHED; PRODUCTION_RUNTIME=NOT_AUTHORIZED; SEAL=NO; AUTHORIZATION=NON_AUTHORIZED; FAIL_CLOSED=TRUE.

## 12. R2 change record

- Preserves R1 unchanged as predecessor.
- Reconciles the owner-selected D1-A, D2-B and fulfillment-health interlock principle recorded on 2026-10-10; does not ask the owner to repeat these decisions.
- Distinguishes owner-selected candidate semantics from normative adoption, official Test Register registration, code/schema, production database, runtime or release authorization.
- Marks the pre-debit failure/release branch as separate and not a complete owner-approved normative contract.
- Updates candidate oracle links/status and preserves the open official Test Register, active Technical Contracts pointer, and authorized commerce/persistence-source gates.

END OF R2 CANDIDATE
