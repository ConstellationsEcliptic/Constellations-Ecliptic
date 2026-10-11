# CONSTELLATIONS ECLIPTIC
# ZERO-POINT FINDING 5 — DAILY DEEP SKY CAP SOURCE-CHAIN ADDENDUM R0

Date: 2026-10-11
Related crosswalk: `CE_ZERO_POINT_11_FINDINGS_3_NOTES_RECOVERED_CONTENT_CROSSWALK_R1_2026-10-11.md`, PR #38
Classification: SOURCE-BOUND EVIDENCE ADDENDUM / NON-AUTHORITATIVE
Authority effect: NONE
Normative effect: NONE
Official Test Register effect: NONE
Schema/code/runtime effect: NONE

## 1. Purpose and correction boundary

The original Finding 5 states that the initial source review did not find an explicit active normative rule limiting one purchased Deep Sky scope per account per day. That observation remains accurate for the baseline files originally checked, but the continued source-first search found a dedicated daily-cap source chain. The finding must therefore distinguish:

1. **the owner-originated product premise**, which is evidenced and must not be presented as wholly undecided;
2. **the fixed UTC Gregorian service-day boundary**, which is owner-approved in a deliberately limited scope; and
3. **the detailed normative/operational scope, order, quota, remedy and test contract**, which remains a proposal, not an active implemented or officially tested control.

This addendum refines Finding 5; it does not replace or rewrite Crosswalk R1.

## 2. Direct sources and what each establishes

- [Owner Disposition — Daily Deep Sky Service-Day Boundary R0, Box 2515555580794](https://account.box.com/file/2515555580794): approves a fixed UTC Gregorian service day from 00:00:00 UTC inclusive through the next day's 00:00:00 UTC exclusive for the existing limit of at most one new Deep Sky reading purchase per account per service day. The disposition explicitly limits itself to the day-boundary/timezone choice; it does not approve the complete reservation, quota-consumption, failure or remedy state machine.
- [Owner Disposition — U.S. Jurisdiction Investigation Direction R0, Box 2515610250498](https://account.box.com/file/2515610250498): confirms this is an owner-originated one-new-reading-per-account/service-date premise and authorizes U.S.-focused research for the workstream. It does not authorize normative amendments or implementation.
- [DR-01 Decision-Evidence Reconciliation R0, Box 2515706725948](https://account.box.com/file/2515706725948): reconciles the subsequent decision history against the older [Human Decision Register R0, Box 2514894635417](https://account.box.com/file/2514894635417). The old register literally records DR-01 as `NOT_RECORDED`; the reconciliation says preserve that historical artifact and resolve the inconsistency in a controlled successor register, without backdating or asking the owner to repeat the premise.
- [Daily Deep Sky Purchase Cap Contract Recommendation R3, Box 2515610293207](https://account.box.com/file/2515610293207) and [Proposed Normative Delta R3, Box 2515701908498](https://account.box.com/file/2515701908498): retain one new reading per authenticated account per UTC service date and propose specific order/slot/remedy semantics, while explicitly remaining NON-NORMATIVE / NOT APPROVED FOR APPLICATION.
- [State Table R0, Box 2515727457293](https://account.box.com/file/2515727457293), [Test Oracle Map R1, Box 2515723612065](https://account.box.com/file/2515723612065), and [State/Test Consistency Audit R0, Box 2515738366976](https://account.box.com/file/2515738366976): detail proposed reservation, fulfillment, service date, Credits, entitlement and remedy transitions; these records state no normative change, official register change, test execution or implementation authorization.
- [Commerce/Persistence Source Identification R1, Box 2515691567942](https://account.box.com/file/2515691567942): authoritative commerce/persistence implementation was NOT ESTABLISHED in connected/inspected scope. This is bounded evidence, not proof that no local/private worktree exists.
- [U.S. Daily Deep Sky Cap / Consumer Remedy Review R3, Box 2515625992660](https://account.box.com/file/2515625992660): U.S.-focused research is authorized, but formal paid-market jurisdiction remains `NOT_RECORDED` / not established by inspected decision records. Nationwide/state-list paid-market approval is not implied.

## 3. Reconciled Finding 5

| Subquestion | Evidence-based state |
|---|---|
| Is there an owner-originated daily cap premise? | **YES — EVIDENCED.** At most one new Deep Sky reading purchase per authenticated account per CE service day. Do not ask the owner to repeat this premise. |
| Is the day boundary settled? | **YES, LIMITED SCOPE.** Fixed UTC Gregorian date `[00:00:00 UTC, next day 00:00:00 UTC)`, shared at account level rather than tied to a particular trusted device. |
| Is the historical Human Decision Register already reconciled? | **NO.** DR-01 in R0 still says `NOT_RECORDED`; a controlled successor register should cite the later evidence and preserve R0 unchanged. |
| Does the approved boundary settle exactly when a slot is consumed? | **NO.** R3 recommends consumption only after a valid output-validated reading is accessible via entitlement, but this is not the same as the limited UTC boundary disposition. |
| Are atomic reservation, same-account/date concurrency, retry and unknown-state handling active? | **NOT ESTABLISHED.** They are proposed operational requirements; authoritative commerce/persistence source is unidentified in inspected connected scope. |
| Are Credits restoration, same-date release, expired-date closure, cash refund, replacement and post-delivery remedy fully approved? | **NO.** These are proposed contract branches; counsel-dependent mandatory rights must be preserved. Cash/card refund and Credits restoration are separate events. |
| Are cap tests already official and passed? | **NO.** US-DCAP-01–28 and cap-specific oracle-map cases are candidates, not official Test Register IDs and not executed. PAY-01/PAY-02 and existing TIME/SEC tests do not by themselves prove daily account/date scope enforcement. |
| Is a U.S. nationwide or state-list launch approved? | **NOT ESTABLISHED.** The approved U.S. workstream is a research direction, not paid-market enablement. |

## 4. Operational boundary

The proposed R3 semantics should be retained for controlled review without turning them into active policy by repetition:

- Reservation and consumption are separate states.
- A single logical reading-order identity and immutable server-derived UTC service date must survive retries and midnight rollover.
- Concurrency uniqueness needs an atomic authoritative persistence constraint; application-only check-then-insert is insufficient.
- Pending/unknown/conflicting post-debit states remain reconcilable; a timeout alone is not proof of terminal failure and must not trigger speculative restoration or silent slot release.
- If a reading is validly delivered, later remedy should retain the original order/service-date history and follow a separately approved remedy contract.
- The technical failure / Quiet Sky boundary remains governed by the existing Constitution; the cap proposal must not duplicate or weaken it.

These bullets summarize **proposed** handling, not a newly approved implementation contract.

## 5. Correct Area Register / Crosswalk implications

The Pre-A10 Area Register lineage also matters here. The PR #27 current gate targets R3 at current PR HEAD `549e53c0abccc3fb6d26f2cf0e32b7b3f7e00668`; it reports 20/23 complete with A3/B1/D4 incomplete. The file named R2 has internal `revision=R1` and the same blob as the R1-named file. Do not bind this daily-cap reconciliation to an outdated R2 summary as though it were the current strict gate.

Finding 5 remains **PARTIAL**, but for a more precise reason than before: the owner-originated premise and the UTC boundary are evidenced; active normative linkage, the complete quota/order/remedy contract, authorized persistence implementation and official test-oracle linkage remain open. The related source-chain report and the current-head correction are recorded in PR #39, sections 30 and 32:
[Zero-Point Current Evidence & Code Review R1](https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/blob/audit/ce-zero-point-current-evidence-code-review-r1-2026-10-11/governance/candidates/CE_ZERO_POINT_CURRENT_EVIDENCE_AND_CODE_REVIEW_R1_2026-10-11.md).

## 6. Explicit non-actions

- Do not reopen the already recorded daily-cap premise or UTC-boundary decision.
- Do not silently change Human Decision Register R0, active Index, Account/Commercial Specification, Business Model, Implementation Plan or official Test Register.
- Do not invent the commerce repository, schema/table/index, provider or deployed state.
- Do not describe any US-DCAP/CAND-DCAP proposal as registered, executed or passed.
- Do not infer paid-market launch authorization, Runtime Adoption, A10, production or SEAL.

Historical source identities and source authority remain separate. This addendum creates no normative or runtime authority.
