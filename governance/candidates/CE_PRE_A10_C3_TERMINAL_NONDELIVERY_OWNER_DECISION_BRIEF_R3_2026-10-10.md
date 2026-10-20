# CONSTELLATIONS ECLIPTIC
# PRE-A10 C3 — PURCHASE-CAP / TERMINAL NON-DELIVERY DECISION BRIEF R3

Date: 2026-10-10  
Predecessor: R2 preserved unchanged
Classification: OWNER-DISPOSITION RECONCILIATION / NON-NORMATIVE / SOURCE-LINEAGE QUALIFIED / TEST-REGISTER BINDING UNRESOLVED  
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

The owner selected D1-A on 2026-10-10 for candidate semantics: the effective purchase is the confirmed logical order bound to its immutable server-derived UTC date when its exact-once reading-Credits debit commits. This selects the purchase-cap trigger and does not automatically approve the complete pre-debit failure/release contract, normative insertion, Test Register mapping or implementation.

## 4. Decision D2 — what happens to today's slot after proven terminal non-delivery?

D2 applies only when CE has positively established that no valid reading was made accessible, no downstream operation can still deliver one, the exact reading-Credits debit is restored exactly once, no entitlement exists, and all relevant operations are closed. A timeout, pending callback, worker restart, or midnight is not terminal failure.

| Candidate | Rule if the original UTC date is still current | Consumer and product consequence |
|---|---|---|
| **D2-A — RETAIN_SLOT** | The original date remains counted despite the exact debit restoration. | Strict count of committed purchase events, but the customer cannot make a fresh same-day purchase after CE definitively failed to deliver the reading. |
| **D2-B — RELEASE_AFTER_FULL_REVERSAL (recommended)** | Release the original-date slot once, only after every terminal/reversal/closure condition above is confirmed. | The customer can enter the ordinary confirmation, balance and cap checks again. The original purchase/failed order remains immutable and auditable; only its daily-quota effect is reversed. |

D1 and D2 remain semantically distinct. The owner selected D1-A + D2-B for candidate semantics. The final contract must explicitly separate the immutable historical purchase event from the net quota effect after a fully reversed, never-delivered order; it must not claim that every committed event consumes quota unconditionally and then silently permit release on reversal.

If the terminal reversal is not completed until after the original UTC date ends, close the old date's slot without transferring it. The new date has its own allowance. Do not re-date the order or turn an unresolved transaction into a failure because midnight passed.

## 5. Additional risk and proposed safeguard

D2-B means a new same-day order could be attempted after each fully reversed terminal non-delivery. The cap policy alone does not safely handle repeated failures of a degraded fulfillment service.

The owner approved the **principle** of a deterministic service-level fulfillment-health interlock on 2026-10-10: do not admit new paid-reading purchases unless the service is explicitly in a state that permits new purchases; unknown/blocked fails closed; do not cancel or terminalize an existing operation that may still fulfill. An interlock activation threshold, verified health-evidence source, lease/expiry, renewal, reset, monitoring, operator control, recovery and audit/test contract remain unspecified. A hidden or arbitrary user-level attempt limit is not approved and must not be introduced by implication.

This is a proposed reliability/consumer safeguard, not an existing CE rule or implemented capability. The authorized reliability/implementation contract must later define exact health evidence, threshold, activation/reset, audit and test oracles. This does not add a third owner choice in this brief; no user-level attempt cap is implied.

## 6. Rules that remain in force under all choices

- A retry that can still safely fulfill the purchase remains linked to the original order/date and has no second debit, purchase identity or independent entitlement.
- Unknown/pending state remains observable and reconcilable; no speculative restoration, slot release, or new order that bypasses the unresolved state.
- Terminal non-delivery: restore the exact reading-debit amount once and grant no reading entitlement; apply applicable separate payment/consumer remedy.
- Credits restoration and monetary/card refund are separate ledger/payment operations. This brief does not conclude that internal Credits restoration is always the only or legally sufficient remedy.
- Post-delivery complaints preserve the original purchase/date/fulfillment history. Applicable mandatory consumer rights cannot be denied by the daily cap.
- Commercial state cannot alter astronomy, qualification, Canon, uncertainty or Quiet Sky. System failure is not Quiet Sky and is not a delivered reading.
- Checkout disclosure should supplement, not repeat, existing scope/period/evidence/output/price/Credits preview fields with the cap, real UTC reset instant, top-up vs new-reading vs reread distinction, and pending/remedy boundary.

## 7. Owner disposition already recorded — no repeat approval

The owner already selected the following limited product semantics on 2026-10-10:
- D1 effective purchase event: D1-A — confirmed logical order bound to immutable server-derived UTC service date and exact-once committed reading-Credits debit.
- D2 same-date slot after proven terminal non-delivery: D2-B — release the original-date slot once only after complete terminal evidence, absence of accessible entitlement, closure of all relevant delivery-capable operations, and exact-once restoration of the reading debit; release only while the original UTC date is still current, with no next-day carry-over.
- Fulfillment-health interlock: APPROVED PRINCIPLE — fail closed for new purchases when admission is unknown/blocked/unhealthy; do not terminate an existing operation that may still fulfill.

Decision evidence:
- Isolated candidate owner-disposition file at PR #33 head: https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/blob/a0dcd466e28ca822a43ef86c172f7e1c91ea46a4/prototypes/commerce-reference-model-r0-2026-10-10/owner-disposition-2026-10-10.md
- Draft/non-production implementation reference and evidence: https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/pull/33

These decisions must not be presented again as open owner choices. Their status is **OWNER-SELECTED CANDIDATE SEMANTICS**, not formal normative amendment or production authorization.

Remaining work that is not already decided:
1. Pre-debit reservation rejection/release and whether any pre-debit attempt-limit semantics are needed. This is separate from the selected D1-A/D2-B path; current candidate implementation behavior must not be described as a complete owner-approved normative contract.
2. Exact source/persistence target and the authorized application route.
3. Operational health-interlock evidence, threshold, lease/expiry, activation/reset, monitoring, operator controls, recovery and tests.
4. Official full Test Register identity/binding, followed by non-duplicative oracle registration through the valid change process.
5. External-money refunds, cancellation/withdrawal and post-delivery remedies under an approved commercial/legal policy; Credits restoration is not automatically equivalent to a cash/card refund.

## 8. Boundary of the recorded disposition

The owner disposition settles only D1-A, D2-B, the fixed UTC service-day boundary and the fulfillment-health interlock principle within the scope recorded above. It does not:
- establish the official full Test Register or its current binding;
- authorize a normative amendment or a specific active CE source file;
- identify or authorize a live commerce/persistence implementation;
- approve a production database, payment provider, seller/legal jurisdiction, live market, currency, price or external-money refund policy;
- approve a five-minute production health SLO; the five-minute lease in PR #33 remains prototype-only;
- establish Source Authority, Trusted Build, A10/Runtime Adoption, production, merge/release or SEAL.

Current reconciled status:
- D1: OWNER-SELECTED D1-A FOR CANDIDATE SEMANTICS; NORMATIVE APPLICATION OPEN.
- D2: OWNER-SELECTED D2-B FOR CANDIDATE SEMANTICS; NORMATIVE APPLICATION OPEN.
- Fulfillment-health interlock: PRINCIPLE OWNER-APPROVED; operational contract OPEN.
- Pre-debit reservation-failure/release policy: OPEN / NOT A COMPLETE OWNER-APPROVED CONTRACT.
- Official full Test Register identity/current binding: NOT ESTABLISHED.
- Authorized commerce/persistence source: NOT ESTABLISHED in inspected scope.
- Technical Contracts active pointer: pointer conflict remains open; PR #35 compares R1/R2 text and shows Section 21 identical, but it does not establish formal target authority.
- Normative sources and official Test Register: unchanged.
- Implementation/A10/Runtime Adoption/production/SEAL: NOT AUTHORIZED.
- SOURCE_AUTHORITY=NOT_ESTABLISHED; TRUSTED_BUILD=NOT_ESTABLISHED; PRODUCTION_RUNTIME=NOT_AUTHORIZED; SEAL=NO; AUTHORIZATION=NON_AUTHORIZED; FAIL_CLOSED=TRUE.

## 9. R3 change record

- Preserves R2 unchanged.
- Removes the stale open D1/D2 question and records the owner-selected candidate semantics with the exact owner-disposition artifact.
- Keeps the approved interlock principle distinct from the still-open operational contract.
- Separates D1/D2 from unresolved pre-debit failure/release, official Test Register, active source/persistence, and consumer-money remedy questions.
- Grants no normative, implementation, runtime, merge, release, production or SEAL authority.

END OF BRIEF R3