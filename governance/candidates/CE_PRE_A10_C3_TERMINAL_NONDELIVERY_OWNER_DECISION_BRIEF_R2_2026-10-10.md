# CONSTELLATIONS ECLIPTIC
# PRE-A10 C3 — PURCHASE-CAP / TERMINAL NON-DELIVERY DECISION BRIEF R2

Date: 2026-10-10  
Classification: FOCUSED OWNER DECISION BRIEF / NON-NORMATIVE / SOURCE-LINEAGE QUALIFIED / TEST-REGISTER BINDING UNRESOLVED  
Authority effect: NONE  
Normative source / official Test Register change: NONE  
Implementation / runtime / production / SEAL effect: NONE

## 1. Purpose and settled baseline

This R2 is the current focused decision brief. It preserves R1 as historical candidate evidence and corrects its source-status wording and the decision framing. It does not reopen already-settled owner directions.

The owner-originated product premise remains **at most one new Deep Sky purchase per authenticated account per CE service day**. The UTC Gregorian service day is `[00:00:00 UTC, next date 00:00:00 UTC)`, assigned by server-authoritative time at the atomic reservation boundary after explicit confirmation. The same account shares the allowance across trusted devices.

Owner source: [UTC service-day disposition, Box 2515555580794](https://app.box.com/file/2515555580794). Do not ask the owner to repeat that premise or boundary.

## 2. Source correction before the product choices

The Clean Current Set R3 outer archive and six listed member hashes have been verified by operator-provided evidence within that archive. However, the archive contains Product Constitution v1.6 and Implementation Plan v1.3, while later controlled records explicitly record applied successors Product Constitution v1.6.1 and Implementation Plan v1.3.1. The successor application and post-apply verification are recorded in Box 2491700051951 and 2491702950277.

That means “archive/member bytes verified” does not mean every archive version is the sole later source, nor does it establish global Source Authority. The current candidate source map, actual unresolved pointers, Test Register gap, and bounded commerce/persistence discovery are documented here:

- [C3 Source-Lineage Reconciliation R0](https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/blob/governance/candidates/ce-autonomous-evolution-charter-r0-2026-10-09/governance/candidates/CE_PRE_A10_C3_SOURCE_LINEAGE_RECONCILIATION_R0_2026-10-10.md)
- [C3 Source-Bound Contract Crosswalk R1](https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/blob/governance/candidates/ce-autonomous-evolution-charter-r0-2026-10-09/governance/candidates/CE_PRE_A10_C3_SOURCE_BOUND_CONTRACT_CROSSWALK_R1_2026-10-10.md)
- [C3 Purchase-Cap Contract Candidate R1](https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/blob/governance/candidates/ce-autonomous-evolution-charter-r0-2026-10-09/governance/candidates/CE_PRE_A10_C3_PURCHASE_CAP_CONTRACT_CANDIDATE_R1_2026-10-10.md)
- [C3 Test Oracle Map Candidate R0](https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/blob/governance/candidates/ce-autonomous-evolution-charter-r0-2026-10-09/governance/candidates/CE_PRE_A10_C3_TEST_ORACLE_MAP_CANDIDATE_R0_2026-10-10.md)

Two independent operational blockers remain: the currently official full Test Register identity/current binding is NOT ESTABLISHED, and no authorized live commerce/persistence source was established in the inspected scope. The Technical Contracts v1.1 pointer identity also differs between the 2026-10-04 Stack Index and a later Current Decision Register. Those blockers prevent normative redline, test registration and implementation mapping; they do not require the owner to decide routine file or schema discovery.

## 3. Decision D1 — what event consumes the new-reading cap?

Reservation, effective purchase and fulfillment are different events.

| Candidate | Meaning | Consequence |
|---|---|---|
| **D1-A — confirmed order + committed reading debit (recommended)** | The effective purchase occurs when the confirmed new-reading order is durably bound to its immutable server-derived service date and its one-time reading-Credits debit is authoritatively committed. | The cap is a purchase cap, not a fulfilled-reading cap. A pending but committed order remains tied to the same slot while it recovers or is reconciled. |
| **D1-B — valid accessible fulfillment** | Count the quota only when a valid reading becomes accessible through its entitlement. | This changes the meaning toward “one successfully fulfilled reading per service date.” It is not a silent paraphrase of the owner-originated purchase cap. |

D1-A is the closer literal fit to the recorded purchase-cap premise, while distinguishing a confirmed but uncharged pre-debit failure. Under either option, an unknown outcome is reconciled on the same order, and an ordinary retry cannot create a second debit or entitlement.

## 4. Decision D2 — what happens to today's slot after proven terminal non-delivery?

D2 applies only when CE has positively established that no valid reading was made accessible, no downstream operation can still deliver one, the exact reading-Credits debit is restored exactly once, no entitlement exists, and all relevant operations are closed. A timeout, pending callback, worker restart, or midnight is not terminal failure.

| Candidate | Rule if the original UTC date is still current | Consumer and product consequence |
|---|---|---|
| **D2-A — RETAIN_SLOT** | The original date remains counted despite the exact debit restoration. | Strict count of committed purchase events, but the customer cannot make a fresh same-day purchase after CE definitively failed to deliver the reading. |
| **D2-B — RELEASE_AFTER_FULL_REVERSAL (recommended)** | Release the original-date slot once, only after every terminal/reversal/closure condition above is confirmed. | The customer can enter the ordinary confirmation, balance and cap checks again. The original purchase/failed order remains immutable and auditable; only its daily-quota effect is reversed. |

D1 and D2 are independent. **D1-A + D2-B can be coherent only if the contract explicitly separates the immutable historical purchase event from the net quota effect after a fully reversed, never-delivered order.** The contract must not claim that every committed event consumes quota unconditionally and then silently permit release on reversal.

If the terminal reversal is not completed until after the original UTC date ends, close the old date's slot without transferring it. The new date has its own allowance. Do not re-date the order or turn an unresolved transaction into a failure because midnight passed.

## 5. Additional risk and proposed safeguard

D2-B means a new same-day order could be attempted after each fully reversed terminal non-delivery. The cap policy alone does not safely handle repeated failures of a degraded fulfillment service.

Candidate recommendation: a **deterministic service-level fulfillment-health interlock** should stop new paid-reading confirmations while verified health evidence says the service is unavailable. A blocked request should create no debit or slot and should receive truthful unavailable status. Prefer a service-level interlock over a hidden, arbitrary user-level attempt limit; do not punish an account because CE repeatedly failed.

This is a proposed reliability/consumer safeguard, not an existing CE rule or implemented capability. The authorized reliability/implementation contract must later define exact health evidence, threshold, activation/reset, audit and test oracles. This does not add a third owner choice in this brief; no user-level attempt cap is implied.

## 6. Rules that remain in force under all choices

- A retry that can still safely fulfill the purchase remains linked to the original order/date and has no second debit, purchase identity or independent entitlement.
- Unknown/pending state remains observable and reconcilable; no speculative restoration, slot release, or new order that bypasses the unresolved state.
- Terminal non-delivery: restore the exact reading-debit amount once and grant no reading entitlement; apply applicable separate payment/consumer remedy.
- Credits restoration and monetary/card refund are separate ledger/payment operations. This brief does not conclude that internal Credits restoration is always the only or legally sufficient remedy.
- Post-delivery complaints preserve the original purchase/date/fulfillment history. Applicable mandatory consumer rights cannot be denied by the daily cap.
- Commercial state cannot alter astronomy, qualification, Canon, uncertainty or Quiet Sky. System failure is not Quiet Sky and is not a delivered reading.
- Checkout disclosure should supplement, not repeat, existing scope/period/evidence/output/price/Credits preview fields with the cap, real UTC reset instant, top-up vs new-reading vs reread distinction, and pending/remedy boundary.

## 7. Proposed disposition format

The two product decisions may be decided independently. No disposition is inferred from silence.

- D1 effective purchase event: **D1-A** / **D1-B** / **RECONCILE**.
- D2 same-date slot after proven terminal non-delivery and exact restoration: **D2-A** / **D2-B** / **RECONCILE**.

My recommendation is **D1-A + D2-B**, paired with the proposed service-level fulfillment-health interlock. It preserves the purchase-cap meaning at the committed order/debit point, permits a fresh same-day opportunity only after a never-delivered order is fully reversed, and avoids using an unbounded series of paid attempts against a known-broken service. These are recommendations, not approvals and not legal conclusions.

## 8. Boundary of any future approval

An owner disposition of D1/D2 would settle only the stated product semantics. It would not establish the official Test Register, authorize a normative amendment, identify live commerce/persistence, approve schema/code, establish Source Authority or Trusted Build, authorize A10/Runtime Adoption/production, or grant SEAL.

Current state:
- D1 and D2: OPEN OWNER PRODUCT DECISIONS.
- Official full Test Register current identity/binding: NOT ESTABLISHED.
- Authorized commerce/persistence source: NOT ESTABLISHED in inspected scope.
- Technical Contracts exact active pointer identity: OPEN.
- Normative sources and official Test Register: unchanged.
- Implementation/A10/Runtime Adoption/production/SEAL: NOT AUTHORIZED.
- `SOURCE_AUTHORITY=NOT_ESTABLISHED`; `TRUSTED_BUILD=NOT_ESTABLISHED`; `PRODUCTION_RUNTIME=NOT_AUTHORIZED`; `SEAL=NO`; `AUTHORIZATION=NON_AUTHORIZED`; `FAIL_CLOSED=TRUE`.

End of R2.
