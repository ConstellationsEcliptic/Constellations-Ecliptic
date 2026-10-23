# CE ZERO-POINT AREA C3 — ONE NEW DEEP SKY PURCHASE PER SERVICE DAY
Date: 2026-10-09
Classification: SOURCE RECONCILIATION / PRODUCT DECISION RECOMMENDATION / NON-AUTHORITATIVE
Status: RECOMMENDATION_READY
Authority effect: NONE
Normative amendment: NONE
Official Test Register change: NONE
Implementation authorization: NONE
FAIL_CLOSED: TRUE

## 1. Owner decisions already settled — do not reopen

1. Product premise: at most one new Deep Sky purchase per account per CE service day.
2. Service-day policy: fixed UTC Gregorian day, from 00:00:00 UTC inclusive to 00:00:00 UTC at the next date exclusive.
3. The server-authoritative time used to derive the service date is taken at the atomic daily-slot reservation point after the user confirms the new Deep Sky order.
4. The same authenticated account shares the allowance across trusted devices.
5. Top-ups of Credits and rereading a previously entitled retained reading are distinct from a new Deep Sky reading purchase.

The UTC owner disposition (Box 2515555580794) expressly limits the approval to the service-day boundary/timezone. It does not approve the full slot state machine, cap-consumption point, refund/cancellation, Credits restoration or release after terminal failure.

## 2. Source and lineage limits

The accessible Account/Privacy/Commercial v1.7 (Box 2485319995048), Business Model v1.5 (Box 2485331476456), Implementation Plan v1.3.1 (Box 2491699264134) and Test Register v1.5 (Box 2485336117840) establish general account-owned Credits, retained reading entitlement, idempotency, provider-event deduplication, database-level uniqueness, and reconciliation of payment/generation failure.

However, the individually readable normative Markdown inputs used by prior daily-cap crosswalks sit in an excluded staging/unsorted path; exact byte identity to the representative governing archive could not be inspected through the available connected-source operations. Source-Lineage Update R1 (Box 2515750096004) explicitly says the exact-source boundary remains NOT ESTABLISHED. The daily-cap redline R3, state table, test map and change-control packet remain provisional/non-normative and must not be applied to current normative files.

The current connected repository and active Box scope also do not establish a live commerce persistence implementation (Box 2515659021563). Do not infer an actual database schema, payment provider or live Credits ledger from normative field lists.

## 3. Essential semantic distinction

Keep these three events separate:
1. **Reservation:** atomically prevents concurrent duplicate new orders after explicit user confirmation. The reservation timestamp fixes the UTC service date under the approved owner direction.
2. **Effective purchase/redemption:** the contract-defined, server-atomic event at which a new reading purchase and corresponding Credits debit/order identity become committed.
3. **Fulfillment:** a valid reading passes the required validation and becomes accessible under entitlement.

The owner approved how to compute the service date at the reservation point. That does not yet approve that reservation itself consumes the daily purchase allowance.

A timeout is not proof of failure. A Credits debit does not prove a reading was delivered, and valid delivery is not the only possible definition of purchase. Do not silently substitute a fulfilled-reading cap for the purchase-cap premise.

## 4. Option comparison and preferred recommendation

**Preferred baseline: preserve a purchase/redemption cap (Option A), not a successful-fulfillment cap.** This is the closest literal fit to the settled owner premise. The quota event should be a single atomic CE-side commit of the new-reading order and its Credits debit; reservation is a temporary concurrency control and fulfillment remains a separate outcome.

| State/event | Recommended candidate behavior |
|---|---|
| Preview/click not confirmed | No reservation and no cap consumption. |
| Explicit confirmation | Atomically reserve account + UTC service-date slot; bind a stable logical order ID and server-authoritative service date. |
| Failure before effective debit/order commit, no unresolved operation | No effective purchase; release the reservation exactly once. |
| Credits/order commit succeeds | Purchase cap is consumed for that account/date. Retries of the same logical order return/reconcile the same order and cannot create a second purchase/debit. |
| Provider/order state unknown or timeout | Remain reconcilable; do not release slot or invent restoration merely because time elapsed. |
| Confirmed terminal non-delivery after debit, no reading delivered | Restore the applicable reading debit exactly once and offer a controlled remedy. Recommended default: a no-charge retry/replacement linked to the original order, not a second paid purchase. If the remedy instead fully cancels/reverses the purchase, release the same-date slot only after terminal failure and exact restoration are committed and no downstream operation remains unresolved; then a new same-date purchase may be admitted. This cancellation/release rule still requires owner disposition. |
| Valid reading delivered | Keep the purchase counted for that service date. Rereading uses the existing entitlement and no new Credits debit. |
| Failure or unresolved order crosses UTC midnight | Retain original order identity and original service date; never transfer its slot to the next date. The new date has its own allowance, but must not be used to retry the old logical order as a new purchase. Test that a separate next-date order cannot create duplicate grants/entitlements. |
| Complaint/remedy after valid delivery | Preserve original purchase/fulfillment history. Refund, replacement or other remedy is not automatically a quota reset; apply a separate approved remedy policy and mandatory consumer rights. |

### Why this is preferred

- It preserves the owner-stated purchase cap instead of silently redefining it as a delivery cap.
- It prevents concurrent confirmations, retries or webhooks from creating multiple purchases or grants.
- It does not make the user pay again for a service that was never delivered.
- It separates an idempotent retry/replacement under the original order from a second paid purchase.
- It keeps UTC date, order, debit, reading validation, entitlement and consumer remedy independently traceable.

### Remaining owner decision boundary

The exact choice in the post-debit terminal non-delivery branch—whether to keep the allowance consumed while providing a linked no-charge replacement, or restore Credits and release the same-date allowance after full reversal—is a material product/remedy choice not settled by the UTC approval or purchase-cap premise alone. Recommendation is to allow cap release only on confirmed terminal non-delivery plus an exact committed reversal/restoration and no unresolved downstream operation; a no-charge replacement remains linked to the original order and does not create a second purchase. This recommendation is not yet owner-approved.

## 5. Candidate test matrix — not registered or executed

Keep the official Test Register unchanged until the source/semantics prerequisites are met. Proposed oracles to later formalize:
- two concurrent confirmed new orders for the same account/UTC date -> at most one active reservation/effective purchase;
- same logical order retry -> same order state, no second debit/entitlement;
- pre-debit terminal failure with no unresolved operation -> release reservation exactly once;
- post-debit unknown outcome -> no speculative refund, cap release or duplicate order;
- terminal non-delivery -> exact-once restoration; slot release only under the approved reversal branch;
- no-charge replacement stays attached to original order and does not count as a second paid purchase;
- success but unreadable/invalid output never becomes successful fulfillment;
- successful valid delivery consumes the daily purchase allowance; reread does not consume it again;
- UTC boundary is decided only by the server timestamp at the approved reservation point;
- unresolved order/date is preserved across midnight; no date transfer or duplicate fulfillment;
- late success versus restoration/release race resolves deterministically;
- post-delivery remedy does not rewrite historical purchase/fulfillment provenance;
- Credits top-up is not a Deep Sky reading purchase;
- technical/calculation failure never becomes Quiet Sky.

## 6. Status and non-actions

- One new Deep Sky purchase per account per service day: owner-originated / evidenced.
- Fixed UTC Gregorian boundary and reservation-time service-date derivation: owner-approved, limited scope.
- Purchase vs fulfillment quota meaning: recommendation favors purchase/redemption; no silent semantic substitution.
- Failure/remedy/slot-release branch: HUMAN DECISION REQUIRED.
- Exact norm-source byte lineage: NOT ESTABLISHED in this pass; candidate crosswalk remains provisional.
- Current commerce persistence source/live implementation: NOT ESTABLISHED in inspected connected scope.
- Normative files, official Test Register, code, schema and runtime: unchanged.
- Tests executed: NONE.
- Implementation, Runtime Adoption, production, deployment and SEAL: not authorized.

## 7. Evidence references

- Owner Disposition — Daily Deep Sky Service-Day Boundary: https://app.box.com/file/2515555580794
- Daily Deep Sky Cap Semantic Options R0: https://app.box.com/file/2515757204983
- Purchase-vs-Fulfillment Semantic Finding R0: https://app.box.com/file/2515747060613
- Change-Control Packet R4 (provisional): https://app.box.com/file/2515730623159
- Source-Lineage Update R1: https://app.box.com/file/2515750096004
- Commerce/Persistence Source-Discovery Finding R0: https://app.box.com/file/2515659021563
- Current Handoff R30: https://app.box.com/file/2515742713865
- Source-First Recommendation Protocol: https://app.box.com/file/2515488894918

End of C3 review.
