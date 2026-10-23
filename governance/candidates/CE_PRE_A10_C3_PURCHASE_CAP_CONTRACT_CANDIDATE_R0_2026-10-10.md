# CONSTELLATIONS ECLIPTIC
# PRE-A10 C3 — PURCHASE-CAP CONTRACT CANDIDATE R0

Date: 2026-10-10  
Classification: SOURCE-BOUND PRODUCT CONTRACT PROPOSAL / NON-NORMATIVE  
Authority effect: NONE  
Normative amendment: NONE  
Official Test Register change: NONE  
Schema / code / runtime / production / SEAL effect: NONE  
Implementation authorization: NONE  
Fail-closed posture: PRESERVED

## 1. Purpose and limits

This is a proposed contract shape for one new Deep Sky purchase per authenticated account per CE service day. It is grounded in the byte-verified Clean Current Set R3 source members listed in Section 8 and the owner-direction records linked below. It supersedes no historical artifact and does not apply any existing proposal to a normative source.

The goal is to preserve the owner-originated **purchase-cap** premise without quietly turning it into a fulfillment-only cap; distinguish reservations from effective purchases; preserve existing payment/idempotency and Quiet Sky protections; and separate a recoverable order from a proven terminal non-delivery.

## 2. Established baseline versus proposal

### Established by owner direction

- The product premise is at most one new Deep Sky purchase per authenticated account per CE service day.
- The service day uses the UTC Gregorian half-open interval [00:00:00 UTC, next date 00:00:00 UTC).
- The service-date assignment is based on a server-authoritative timestamp at the atomic daily-slot reservation point after the user confirms a new order.
- The same account shares the allowance across its trusted devices.
- Those directions establish the premise and date boundary only; they do not approve the complete reservation, purchase-commit, fulfillment, restoration, refund, or slot-release state machine.

Source: Owner Disposition — Daily Deep Sky Service-Day Boundary R0 (Box 2515555580794), https://app.box.com/file/2515555580794. The older Human Decision Register R0 remains historically unchanged; DR-01 evidence reconciliation is separate.

### Candidate recommendation — not approved

The effective purchase-cap event should be the durable commitment of one confirmed new-reading order with its one-time reading-Credits debit authoritatively committed, bound to the server-derived immutable service date. The reservation is the concurrency guard; it is not by itself proof that a paid purchase committed. Valid accessible fulfillment is a later state; it must not be substituted for the purchase event without an explicit change to the product premise.

This is a recommendation for owner review, not a retrospective claim that the complete event definition has already been approved.

## 3. Keep three event boundaries separate

| Event | Meaning | Daily-cap effect in this candidate |
|---|---|---|
| Reservation | After explicit user confirmation, establish one durable account/date/order guard using the server UTC timestamp. | Blocks concurrent duplicate orders while active or unresolved; it is not by itself a permanently consumed purchase. |
| Effective purchase commit | The confirmed order is durably bound to its service date and the exact reading-Credits debit is authoritatively committed once. | Counts as the one new purchase for that account/date under the proposed purchase-cap trigger. |
| Fulfillment | A valid reading passes the existing output-validation path and becomes accessible through its entitlement. | Completes delivery; it does not retroactively define when the purchase occurred. |

A confirmed purchase and a delivered reading are different facts. The product cap therefore must not be described as “one successfully fulfilled reading per UTC date” unless that alternative is explicitly selected through governance.

## 4. Proposed order state model

State names below are conceptual labels only. They are not approved enum names or a schema design.

| State / transition | Candidate invariant |
|---|---|
| Before confirmation | No slot, no reading debit, no new entitlement. |
| RESERVED | The original server-derived service date and stable logical order identity are fixed. The reservation prevents concurrent same-account/date orders while the transaction is active or unresolved. |
| PURCHASE_COMMITTED | The authoritative order/debit result confirms one effective new-reading purchase. It consumes the proposed purchase-cap allowance for the immutable service date. |
| FULFILLMENT_PENDING / recoverable error | Continue the same order. No second reading debit, independent purchase, or duplicate entitlement. |
| UNKNOWN / RECONCILIATION_REQUIRED | Keep the original order and date visible and reconcilable. Do not guess success or failure; do not restore Credits or release the guard because a timeout elapsed. |
| Conclusive pre-debit failure | Release the reservation exactly once only after confirming that no reading debit, entitlement mutation, or downstream commercial operation committed or remains unresolved. No effective purchase was committed. |
| Valid fulfillment | Bind one valid reading and one entitlement to the original order; preserve the required provenance. |
| Proven post-debit terminal non-delivery | No valid reading was delivered, no entitlement was made usable, and every downstream order/debit/generation/validation/entitlement operation is conclusively closed. Apply the approved one-time restoration/refund remedy. The same-day slot effect is a separate product choice in Section 6. |
| Post-delivery complaint or remedy | Preserve original purchase, service date, and fulfillment history. Apply the approved remedy and applicable mandatory rights; do not silently rewrite the historical purchase or automatically reset the cap. |

The actual database transaction, locking, outbox/saga, reconciliation and uniqueness design must be established against the authorized commerce/persistence source. Do not infer table/column/index names from this candidate. Application-level check-then-insert is not an acceptable substitute for an authorized persistence-level concurrency control.

## 5. Recovery follows recoverability, not the cap axis

These are distinct branches, not mutually exclusive alternatives for one state:

**A. Recoverable post-debit failure — proposed default: PATH-LINKED-RECOVERY.** If the original purchase can still be safely fulfilled, retain its original order identity, debit and immutable service date; perform a linked no-charge retry/replacement under the approved bounded recovery policy. It does not create a second paid purchase, new debit, independent entitlement or new-date purchase. It must not retry forever or disguise technical failure as QUIET_SKY.

**B. Unknown or pending outcome.** Do not decide that the order is recoverable or terminal merely because a timeout elapsed. Reconcile the same logical order. No speculative restoration, new independent same-date order, duplicate debit or duplicate entitlement is permitted while its relevant downstream outcome is unresolved.

**C. Proven terminal non-delivery.** A linked retry is no longer a valid remedy once CE has established that the original order cannot safely produce a usable reading. Restore the exact reading-Credits debit once, grant no reading entitlement, and apply any required payment-level refund or other consumer remedy under the separately approved policy. Credits restoration and a monetary/card refund are not interchangeable: a reading-Credits debit is not the same transaction as the earlier payment that may have loaded those Credits.

The term “terminal non-delivery” requires positive reconciled evidence; it must never mean simply delayed, unresponsive, timed out, or inconvenient to retry.

## 6. One remaining owner-level remedy choice

After **proven terminal non-delivery**, once the exact reading-Credits debit has been restored once and all related operations are closed, choose one same-day slot rule:

| Choice | Rule if the original UTC service date is still current | Benefit | Trade-off |
|---|---|---|---|
| **A — RETAIN_SLOT** | The original effective purchase remains counted for that date even though Credits are restored. No new independent reading order is eligible until the next service date. | Closest to a strict count of committed purchase events. | The user may have Credits restored yet be unable to purchase a reading again that day despite receiving no reading. |
| **B — RELEASE_AFTER_FULL_REVERSAL** | Release the original-date slot exactly once, only after terminal non-delivery is proven, the exact reading-Credits debit is restored, and every relevant downstream operation is closed. A new independent same-day order may then be evaluated under the ordinary cap, confirmation, balance and idempotency checks. | Treats a fully reversed, never-delivered order as no longer occupying the consumer's effective same-day purchase opportunity. | Allows more than one attempted order that day, although the earlier one must be fully reversed and must not have delivered a reading. |

These choices concern the effect of a **completed terminal reversal**, not whether ordinary quota use waits until fulfillment. Under either choice, the candidate trigger for an ordinary successful purchase remains order-plus-debit commitment, not accessible fulfillment.

**Recommended for owner consideration: Choice B — RELEASE_AFTER_FULL_REVERSAL.** It avoids leaving the customer unable to make another same-day purchase after CE conclusively failed to supply the service and restored the exact reading debit. This is a product fairness recommendation, not a legal conclusion or owner approval. A mandatory consumer right cannot be withheld because the slot is occupied.

If terminal closure and restoration occur only after the original service date has ended, close the historical date's slot without transferring it to a later date. A new UTC date has its own allowance. Do not rewrite the immutable service date or use midnight to convert an unknown state into a terminal failure.

## 7. Consumer and product integrity invariants

- Credits top-up, new-reading order/debit, reread of an existing retained entitlement, reading-Credits restoration, monetary/card refund, and linked no-charge replacement are distinct commercial events.
- Top-up alone does not consume a new-reading slot. Rereading the same retained/entitled reading does not create a new purchase or debit.
- Preserve existing account-bound/non-expiring Credits and retained-reading entitlement rules; do not duplicate general idempotency policy.
- One logical order may result in at most one effective reading debit, one delivered reading entitlement, and one application of each approved remedy.
- Cap/payment/recovery state cannot create a celestial signal, alter astronomical calculations or qualification, change Canon or uncertainty, or turn a technical failure into QUIET_SKY.
- Do not use fake scarcity, fake countdowns, purchase pressure, guaranteed-event claims, paid certainty, paid accuracy, or an inaccurate description of the reset instant.
- Disclose the one-new-reading purchase cap, actual UTC reset instant, reading scope, total mandatory price/Credits cost, and relevant status/remedy boundaries before confirmation, supplementing rather than duplicating existing disclosures.
- Preserve applicable mandatory consumer rights; this candidate does not determine jurisdiction-specific legal outcomes.

## 8. Source-bound basis and lineage limit

The following six files have direct SHA-256 member-stream checks reported by the operator as matching their manifest values in Clean Current Set R3:

| Current-set member | Verified SHA-256 |
|---|---|
| 00_DOCUMENT_INDEX.md (Document Index v1.9) | a6a2d482d27777bae21f78ae11593eef62a35f19ee899d0a69ab83e3ccb8025f |
| 01_PRODUCT_CONSTITUTION_MASTER_PRODUCT_SPECIFICATION.md (Product Constitution v1.6) | fb646bebd1b2e3e4f8f63f486e5b12a0f50ead59704464100bcd38d9b36b73d7 |
| 06_ACCOUNT_PRIVACY_COMMERCIAL_SPECIFICATION.md (Account/Privacy/Commercial Specification v1.7) | 470efd7d95299e8e9a7002b355c967f982a3582412b5664f4c86e7cbc4a152e5 |
| 08_BUSINESS_MODEL_MINIMAL_V1_FINAL.md (Business Model v1.5) | b6a51ea4b40cf08715ca64843278e8ca6400572c67a39a1f1f34804c26133bd6 |
| CE_V1_IMPLEMENTATION_PLAN.md (Implementation Plan v1.3) | ca385b00a77bff963c91bdf76fa9dea54c72c4fff4de63def473b28f5e847df4 |
| CE_V1_TECHNICAL_CONTRACTS.md (Technical Contracts v1.0) | e7dae6d0de4becf6aa748667d01758e1cc8499b724539930af9212d64b4cc117 |

The local Clean Current Set R3 outer ZIP identity matches its Box-listed SHA-1 and the SHA-256 in the governing-boundary pointer. See the [C3 Source-Bound Contract Crosswalk R0](https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/blob/governance/candidates/ce-autonomous-evolution-charter-r0-2026-10-09/governance/candidates/CE_PRE_A10_C3_SOURCE_BOUND_CONTRACT_CROSSWALK_R0_2026-10-10.md), the [daily cap semantic finding](https://app.box.com/file/2515747060613), the [cap semantic options/test consequences](https://app.box.com/file/2515757204983), and the [owner UTC boundary disposition](https://app.box.com/file/2515555580794).

Important limitation: the official Execution Profile & Test Register member was reported ABSENT_FROM_CLEAN_CURRENT_SET, while the older Document Index still lists it. The exact official full-register identity/current binding remains NOT ESTABLISHED (R3-PKG-INDEX-001); absence from this archive does not prove no tests exist. Candidate scenarios below remain unregistered.

## 9. Candidate acceptance-oracle matrix — not registered or executed

| Candidate scenario | Required oracle | Status |
|---|---|---|
| First new-reading purchase | Confirmed order plus one debit binds one immutable UTC date and consumes one proposed purchase allowance. | Candidate only |
| Two concurrent confirmations across devices for one account/date | At most one effective purchase; losing request has no second debit or entitlement. | Candidate only |
| Separate accounts on same service date | One account's slot does not block another account. | Candidate only |
| UTC boundary and client clock changes | Server UTC timestamp at reservation assigns immutable date; device clock/timezone cannot alter it. | Candidate only |
| Credits top-up versus new-reading purchase; reread versus new order | Top-up does not consume slot; reread adds no debit or slot; only a new-reading order follows the cap. | Candidate only |
| Conclusive pre-debit failure | Release only after proof of no committed debit/entitlement and no unresolved downstream operation. | Candidate only |
| Retry of one logical order | Existing state is returned/resumed; no duplicate debit, purchase event, entitlement or service date. | Candidate only |
| Pending/unknown state, including rollover | Keep same order/date reconcilable; no timeout-based terminal decision, speculative restoration, or slot transfer. | Candidate only |
| Recoverable post-debit failure | Linked retry retains the original purchase/order and debit; no new paid order or duplicate entitlement. | Candidate only |
| Proven terminal non-delivery after debit | No valid delivered entitlement; exact reading debit restored once; slot oracle follows Choice A or B after owner disposition. | Conditional |
| Terminal restoration after service date ends | Close old date; do not transfer the historical slot. | Candidate only |
| Post-delivery complaint/remedy | Preserve historical purchase/delivery; apply approved remedy and mandatory rights without silent quota reset. | Candidate only |
| Commercial state versus interpretation | Technical/commercial failure does not create a reading, signal, or QUIET_SKY. | Candidate only |

These are scenario oracles, not official Test Register IDs and not executed results. Map them to the authorized register and existing PAY/TIME/SEC/PRIV/ERR coverage only after the register binding and relevant semantic disposition are reconciled. Preserve existing generic payment/idempotency coverage; do not duplicate it.

## 10. Status and next controlled step

- Purchase-cap premise: OWNER-ORIGINATED / EVIDENCED.
- UTC Gregorian service-date boundary: OWNER-APPROVED, LIMITED SCOPE.
- Effective purchase event (committed order plus committed one-time reading debit): RECOMMENDED / NOT APPROVED AS A COMPLETE CONTRACT.
- PATH-LINKED-RECOVERY for recoverable orders: RECOMMENDED / NOT APPROVED.
- Terminal restoration and Choice A versus Choice B same-day slot effect: OPEN OWNER PRODUCT DECISION.
- Six scoped source-member identities plus outer archive identity: VERIFIED PER OPERATOR EVIDENCE.
- Official Test Register identity/current binding: NOT ESTABLISHED; no candidate IDs registered.
- Normative sources, official Test Register, schemas, code and runtime: UNCHANGED.
- Implementation / A10 / Runtime Adoption / production / SEAL: NOT AUTHORIZED.
- SOURCE_AUTHORITY=NOT_ESTABLISHED; TRUSTED_BUILD=NOT_ESTABLISHED; PRODUCTION_RUNTIME=NOT_AUTHORIZED; SEAL=NO; AUTHORIZATION=NON_AUTHORIZED; FAIL_CLOSED=TRUE.

The next useful owner action, when ready, is a narrow disposition of Choice A or Choice B after reading the accompanying corrected C3 decision brief. No current file change authorizes that choice by silence.
