# CONSTELLATIONS ECLIPTIC
# PRE-A10 C3 — PURCHASE-CAP / TERMINAL NON-DELIVERY DECISION BRIEF R1

Date: 2026-10-10  
Classification: FOCUSED OWNER DECISION BRIEF / NON-NORMATIVE / SOURCE-BYTES VERIFIED / TEST-REGISTER BINDING UNRESOLVED  
Authority effect: NONE  
Normative source / official Test Register change: NONE  
Implementation / runtime / production / SEAL effect: NONE

## 1. Settled baseline — do not repeat or reopen

The owner-originated product premise is **at most one new Deep Sky purchase per authenticated account per CE service day**. The owner separately approved a UTC Gregorian service day: 00:00:00 UTC inclusive to, but not including, 00:00:00 UTC on the next date. The same account shares its allowance across trusted devices. The service date is server-derived at the atomic reservation point after explicit confirmation; client clock and display timezone do not govern it.

These owner directions settle the premise and day boundary, not the full purchase-trigger, reservation, fulfillment, restoration or slot-release state machine. Do not ask the owner to repeat the one-purchase-per-account/day premise or the UTC boundary.

Source: [Owner Disposition — Daily Deep Sky Service-Day Boundary R0](https://app.box.com/file/2515555580794).

## 2. Correction to R0 — recovery and terminal remedy are different state branches

R0's presentation of PATH-LINKED-RECOVERY and PATH-REVERSAL-RELEASE as competing first-line remedies blurred two different operating conditions. This R1 preserves R0 as a historical candidate record and corrects the model.

- **Recoverable post-debit failure:** the same purchased order can still be safely fulfilled. The recommended remedy is PATH-LINKED-RECOVERY: resume or replace under the original logical order with no additional debit. It does not become a second purchase and does not reset the cap.
- **Unknown/pending outcome:** the order is not yet known to be recoverable or terminal. Reconcile the same order. Timeout, midnight, a missing callback or a worker restart cannot prove non-delivery or justify a speculative restoration/slot release.
- **Proven terminal non-delivery:** CE has positively reconciled that no valid reading was made usable and no downstream operation can still deliver one. A retry is no longer the remedy. Restore the exact reading-Credits debit once, grant no reading entitlement, and apply the applicable approved payment/consumer remedy. Only then apply the separately chosen slot rule.

Thus PATH-LINKED-RECOVERY and terminal reversal are not mutually exclusive choices for the same state. Recoverability determines the operational branch. A separate cap-policy decision determines the same-day slot effect after terminal reversal.

## 3. Decision D1 — define the purchase-cap event

The phrase “one new purchase per day” is not sufficient to identify each internal state transition. Reservation, effective purchase, and fulfillment remain separate.

| Candidate | Meaning | Assessment |
|---|---|---|
| **D1-A — confirmed order + committed reading debit (recommended)** | Count an effective purchase when the confirmed new-reading order is durably bound to its immutable server-derived UTC service date and its one-time reading-Credits debit is authoritatively committed. Reservation prevents concurrency while processing but is not alone a completed purchase. | Closest to the owner-originated purchase-cap premise while distinguishing an uncharged pre-debit failure. Requires exact implementation mapping to the authorized persistence design. |
| **D1-B — valid accessible fulfillment** | Count quota only once the validated reading becomes accessible. | This is a fulfilled-reading cap, not merely another wording for a purchase cap. Existing candidate R3 has proposed it, but the source-bound finding explicitly says it is not already owner-approved. It should not be adopted implicitly. |

**Recommendation:** retain the purchase-cap meaning and define the effective event as D1-A. In that model, an unknown debit outcome temporarily holds the same order/slot in reconciliation; it must not be guessed to be either success or failure. A conclusively failed pre-debit transaction with no unresolved operation can release the reservation. A successful debit consumes the proposed purchase allowance even while fulfillment remains pending; retries stay on the same logical order.

This is a proposed definition, not an existing owner approval. It does not imply that a slot must remain consumed after a completed terminal reversal; that is D2 below.

Sources: [Daily Deep Sky Cap Semantic Consistency Finding R0](https://app.box.com/file/2515747060613) and [Cap Semantic Options & Test Consequences R0](https://app.box.com/file/2515757204983).

## 4. Decision D2 — same-day slot after proven terminal non-delivery and exact restoration

D2 applies only after terminal failure is proven, the exact reading-Credits debit is restored exactly once, no entitlement was delivered, and all relevant downstream operations are closed. It does not apply to a timeout, unresolved transaction, or recoverable failure.

| Choice | Rule for the original service date when that date is still current | Customer consequence |
|---|---|---|
| **D2-A — RETAIN_SLOT** | The committed purchase event continues to count for that UTC date even after Credits restoration. No separate new-reading order is eligible until the next CE service date. | Strictest count of committed purchase events, but the customer can have Credits restored and still be unable to retry a purchase that day despite receiving no reading. |
| **D2-B — RELEASE_AFTER_FULL_REVERSAL (recommended)** | Release that date's slot once, only after terminal non-delivery, exact restoration and closure of every relevant operation are confirmed. A new independent order may then enter the ordinary confirmation, balance, cap and idempotency checks. | Restores the same-day purchase opportunity after CE conclusively failed to supply the service. This permits more than one attempted order, but the earlier order must be fully reversed and must never have delivered a reading. |

**Recommendation:** D2-B, for consumer fairness. The recommendation is not an assertion about what law requires; it is the proposed CE product rule. Applicable mandatory consumer rights cannot be restricted by the cap.

If terminal reversal is completed after the original service date ends, close the historical slot without transferring it to a later date. The next UTC date has its own allowance. Do not re-date the original purchase or convert a pending order into a terminal failure just because midnight passed.

## 5. Rules common to every choice

- An order may receive at most one effective reading debit, one delivered entitlement and one application of each approved remedy.
- Credits top-up is not a new-reading purchase; rereading a retained entitled reading is not a new purchase and adds no debit.
- A recoverable retry/replacement remains linked to the original order and date. It cannot create a second paid purchase, debit, or independent entitlement.
- Credit restoration for a reading debit and monetary/card refund for an earlier Credits top-up are different ledger/payment operations.
- After valid delivery, preserve the original order and fulfillment history; do not automatically reset the quota on a complaint. Apply the separately approved remedy and mandatory consumer rights.
- No technical failure may be rendered as QUIET_SKY, a valid signal, or a delivered reading. Commercial state cannot alter astronomical calculation, qualification, Canon, uncertainty or interpretive claims.
- No fake scarcity, inaccurate UTC countdown, emotional purchase pressure or paid certainty/accuracy.
- Preserve existing generic payment idempotency, provider-event deduplication, fulfillment reconciliation and rereread entitlements; add only missing cap-specific assertions.

## 6. Consumer and implementation consequences

The implementation must preserve one immutable service date chosen at the UTC reservation boundary and one stable logical order identity. Reservation/debit transitions must use the authorized persistence architecture's concurrency and reconciliation controls; this document does not name tables, columns, indexes or enum values. When debit success or failure is unknown, keep the same order reconcilable. Do not create a second same-date order that bypasses its unresolved commercial state.

Before confirmation, supplement—not duplicate—the existing disclosure of reading scope, evidence/output type, price and Credits cost with the daily limit, the actual UTC reset instant, top-up versus reading purchase versus reread distinction, and the visible pending/terminal remedy path.

Candidate tests must cover same-account multi-device concurrency; different-account isolation; just-before/at UTC midnight; top-up versus reading order; reread; debit success with recoverable generation failure; unknown state; pre-debit terminal failure; terminal restoration and D2 slot effect; date rollover; remedy replay; post-delivery complaint; and independence of commercial state from astronomical/interpretive output. These are **candidate oracles only**, not official IDs, not registered and not executed.

## 7. Source-byte identity and test-register blocker

The operator's direct member-stream SHA-256 checks report that all six cited Clean Current Set R3 source members match the archive manifest. The outer archive's SHA-1 matches the Box-listed value and its SHA-256 matches the governing-boundary pointer. The [C3 Source-Bound Contract Crosswalk R0](https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/blob/governance/candidates/ce-autonomous-evolution-charter-r0-2026-10-09/governance/candidates/CE_PRE_A10_C3_SOURCE_BOUND_CONTRACT_CROSSWALK_R0_2026-10-10.md) records the byte identities and clause coverage.

The official Execution Profile & Test Register member is absent from this ZIP even though the older Document Index lists it. The bounded package/index issue is R3-PKG-INDEX-001. The current official full-register identity/current binding remains NOT ESTABLISHED; absence from this ZIP is not evidence that CE has no tests. Do not promote a raw-intake copy or the A9 candidate manifest by filename alone.

These checks establish the scoped archive/member identities only. They do not establish global SOURCE_AUTHORITY, trusted build, official test-register binding, runtime adoption or production authority.

## 8. Suggested disposition format — not preselected or inferred

The owner may decide the two axes independently, or approve the recommended package as a whole:

- D1 purchase-cap event: D1-A (recommended) / D1-B (explicitly changes the premise toward a fulfilled-reading cap) / RECONCILE.
- D2 terminal reversal effect: D2-A / D2-B (recommended) / RECONCILE.

No choice is inferred from silence. No answer is requested until the owner is satisfied the alternatives and consequences are clear.

## 9. Current state

- One new purchase per account/UTC service day: OWNER-ORIGINATED / EVIDENCED.
- UTC boundary and service-date assignment rule: OWNER-APPROVED, LIMITED SCOPE.
- D1 effective purchase event: RECOMMENDED / NOT APPROVED AS A COMPLETE CONTRACT.
- Linked retry for recoverable post-debit failure: RECOMMENDED / NOT APPROVED.
- D2 terminal restoration/slot rule: OPEN OWNER PRODUCT DECISION.
- Six scoped source-member identities and outer archive identity: VERIFIED PER OPERATOR EVIDENCE.
- Official Test Register identity/current binding: NOT ESTABLISHED.
- Normative source, official Test Register, schema/code/runtime: UNCHANGED.
- Implementation, A10, Runtime Adoption, production and SEAL: NOT AUTHORIZED.
- SOURCE_AUTHORITY=NOT_ESTABLISHED; TRUSTED_BUILD=NOT_ESTABLISHED; PRODUCTION_RUNTIME=NOT_AUTHORIZED; SEAL=NO; AUTHORIZATION=NON_AUTHORIZED; FAIL_CLOSED=TRUE.

End of R1.
