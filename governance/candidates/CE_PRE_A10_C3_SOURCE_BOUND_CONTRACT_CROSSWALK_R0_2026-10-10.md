# CONSTELLATIONS ECLIPTIC
# PRE-A10 C3 — SOURCE-BOUND CONTRACT CROSSWALK R0

**Date:** 2026-10-10  
**Classification:** CANDIDATE SOURCE-BOUND REVIEW / NON-NORMATIVE / DECISION SUPPORT  
**Authority effect:** NONE  
**Normative amendment / official Test Register change:** NONE  
**Schema / code / runtime / production / SEAL effect:** NONE  
**Implementation authorization:** NONE  
**Fail-closed posture:** PRESERVED

## 1. Purpose and boundary

This crosswalk records the C3 daily Deep Sky purchase-cap evidence after the operator's direct SHA-256 checks over the local Clean Current Set R3 ZIP members. It separates (a) established owner direction, (b) exact source-byte identity, (c) current contract coverage, and (d) proposed product/remedy semantics.

It is a candidate review, not a normative redline and not approval to register or execute tests. The Clean Current Set archive is a retained governing-chain artifact; it does not itself establish global `SOURCE_AUTHORITY`, trusted-build status, production authority, or SEAL.

## 2. Verified source-byte boundary

The operator-provided PowerShell output establishes:

- Archive: `CE_V1_CLEAN_CURRENT_SET_R3-2026-09-24.zip`, 2,654,872 bytes.
- Actual SHA-1: `58f8c3dcccc0ccb2e79a79ddd46ab0014c2783d6`, matching the Box-listed SHA-1.
- Actual SHA-256: `d9c2f4abbe0a482e982488d5d2e332202c0c0dc8fceca3b5faaceb3d2c4a8abc`, matching the SHA-256 in the governing-boundary pointer (Box file ID `2485721889298`).
- Each listed archive member below occurred exactly once in the ZIP and its computed SHA-256 matched the expected manifest value. The two Account/Commercial and Technical Contracts checks were completed in the earlier PowerShell pass; the other four passed in the latest pass.

| Exact Clean Current Set member | Declared document identity in extracted source | Expected/actual SHA-256 | Operator result |
|---|---|---|---|
| `01_NORMATIVE/00_DOCUMENT_INDEX.md` | Final Normative Document Index v1.9 | `a6a2d482d27777bae21f78ae11593eef62a35f19ee899d0a69ab83e3ccb8025f` | PASS |
| `01_NORMATIVE/01_PRODUCT_CONSTITUTION_MASTER_PRODUCT_SPECIFICATION.md` | Product Constitution & Master Product Specification v1.6 | `fb646bebd1b2e3e4f8f63f486e5b12a0f50ead59704464100bcd38d9b36b73d7` | PASS |
| `01_NORMATIVE/06_ACCOUNT_PRIVACY_COMMERCIAL_SPECIFICATION.md` | Account, Privacy & Commercial Specification v1.7 | `470efd7d95299e8e9a7002b355c967f982a3582412b5664f4c86e7cbc4a152e5` | PASS |
| `01_NORMATIVE/08_BUSINESS_MODEL_MINIMAL_V1_FINAL.md` | Business Model — Minimal Compliance v1.5 | `b6a51ea4b40cf08715ca64843278e8ca6400572c67a39a1f1f34804c26133bd6` | PASS |
| `01_NORMATIVE/CE_V1_IMPLEMENTATION_PLAN.md` | V1 Implementation Plan v1.3; declared as a controlled implementation-planning artifact, not a new constitution | `ca385b00a77bff963c91bdf76fa9dea54c72c4fff4de63def473b28f5e847df4` | PASS |
| `01_NORMATIVE/CE_V1_TECHNICAL_CONTRACTS.md` | V1 Technical Contracts v1.0; declared as an implementation contract, not a new constitution | `e7dae6d0de4becf6aa748667d01758e1cc8499b724539930af9212d64b4cc117` | PASS |

**Version-label correction:** the actual extracted archive members identify the Product Constitution as v1.6 (not v1.6.1) and the Implementation Plan as v1.3 (not v1.3.1). Candidate packet references have been aligned with those verified member headers. A directory name such as `01_NORMATIVE` does not upgrade an artifact's declared authority type.

### Test Register boundary remains separate

The ZIP check returned `EntryCount=0` and `ABSENT_FROM_CLEAN_CURRENT_SET` for `01_NORMATIVE/07_EXECUTION_PROFILE_TEST_REGISTER.md`. That proves archive absence only.

A broader current-binding check is recorded in the non-authoritative [Test Register, Golden Oracle & Current-Binding Audit R2](https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/blob/governance/candidates/ce-autonomous-evolution-charter-r0-2026-10-09/governance/candidates/CE_PRE_A10_TEST_REGISTER_ORACLE_LINEAGE_AUDIT_R2_2026-10-10.md). It identifies **R3-PKG-INDEX-001**: Clean Current Set R3 excludes legacy Test Register v1.5 as superseded while its older Document Index still lists document 07. The characterized current Stack Index/Manifest (2026-10-04) does not bind a full successor CE behavior-test register. This is a bounded package/index inconsistency, not proof that no tests exist and not permission to promote a raw-intake register or A9 candidate manifest.


The verified Document Index v1.9 nevertheless lists document 07 as Execution Profile & Test Register v1.5 and states that the register verifies the other documents rather than redefining them; it also requires a deterministic fixture-specific oracle for each registered test. The current authorized identity/location of that register remains unresolved:

- Box file IDs `2485336117840` and `2485323796025` have the same SHA-1 `973749ba88112a7b4202c807bcc7635d286a5ea9` and 27,957-byte size, but are both located beneath `99_LOCAL_INVENTORY_INTAKE_2026-09-24/00_RAW_UNSORTED/...` in excluded staging lineage.
- Box file ID `2485752397623` is a separate 9,773-byte file with SHA-1 `b254e31c5567c548a99be5fba97cb91f5dae18b1` beneath `New folder(5)`; its authority is not established either.
- The listing already reviewed for `02_IMPLEMENTATION_ACTIVE_V1` did not establish an authorized current Test Register there.

Do not treat any of those copies as current authority by filename, version, matching duplicate SHA-1, or folder proximity alone. Do not modify the official Test Register until its current authority pointer/identity is reconciled.

## 3. Owner direction already evidenced

The following is not an unresolved choice to be asked again:

- **Product premise:** at most one new Deep Sky purchase per authenticated account per CE service day.
- **Service-day boundary:** UTC Gregorian date, `[00:00:00 UTC, next date 00:00:00 UTC)`, owner-approved for the boundary only.
- **Account scope:** the allowance is shared across trusted devices of the same authenticated account.
- **Credits model:** account-owned, not device-bound; Credits do not expire under the current baseline.
- **Do not substitute a fulfillment-only cap** for the owner-originated purchase-cap premise.

Source records: [Owner UTC Service-Day Boundary Disposition R0](https://app.box.com/file/2515555580794), [DR-01 Decision-Evidence Reconciliation R0](https://app.box.com/file/2515706725948), [Daily Deep Sky Cap Semantic Consistency Finding R0](https://app.box.com/file/2515747060613).

The older Human Decision Register's DR-01 remains literally `NOT_RECORDED`; the later owner-direction evidence must be reconciled through controlled governance, not silently backdated into that historical record. The unresolved work is the detailed contract: exactly when a purchase is effective, concurrency/reservation, failure/reversal behavior, and the associated test oracles.

## 4. Current-source crosswalk

| Verified source | Rule actually established in that source | C3 consequence / boundary |
|---|---|---|
| Document Index v1.9, §§2–3 and §10 | Defines the ten-document normative stack, precedence and execution-test role; document 07 verifies rather than redefines requirements. | The daily cap needs an explicit contract in the appropriate product/commercial authority and corresponding tests. Do not let tests silently define product meaning. |
| Product Constitution v1.6, §4.5 | Deep Sky is paid synthesis of valid evidence; the purchased value is depth of synthesis, not truth, certainty, hidden knowledge or a guaranteed outcome. §§4.2/5 keep technical failure separate from Quiet Sky. | A cap/remedy cannot invent a reading, present failure as Quiet Sky, or sell certainty. Do not duplicate the existing Quiet Sky/error-state rule in the cap delta. |
| Account/Commercial Specification v1.7, §§11–14 | Credits belong to the account, not the device, do not expire; an already opened retained reading may be reread without another Credits deduction within the retention lifecycle; §12 gives 4 Credits/reading as an illustrative parameter; §§13–14 establish idempotent transaction identity and a minimal commercial fulfillment record. | Same-account multi-device enforcement must be atomic. Distinguish top-up, new-reading redemption, reread, refund, Credits restoration and replacement. The cap is about a new reading purchase, not the purchase of a Credits top-up or a reread. |
| Account/Commercial Specification v1.7, §17 | If payment succeeds but Deep Sky generation fails, state must remain deterministically reconcilable; no double Credits charge, silent loss of entitlement, or calculation alteration to compensate for failure. | This is the integrity boundary, not the complete daily-slot remedy. Extend only for order/date/slot effects; do not rewrite calculation or invent a successful reading. |
| Business Model v1.5, §§2.4, 3.1 and 9 | Direct user monetization through Credits; Deep Sky sells synthesis depth; no subscription model in V1; minimal fulfillment evidence is retained for legitimately delivered service and permitted dispute/accounting purposes. | Preserve the commercial model. Do not make the daily cap a subscription, streak, scarcity or marketing mechanism. Keep commercial evidence purpose-limited. |
| Implementation Plan v1.3, §7.8 and Phase 10 | Server-authoritative transaction states; stable logical purchase/idempotency identity; unique provider transaction and event deduplication; atomic unique Credits grant; recover after provider success/network loss; unknown/conflicting state requires reconciliation; retries of fulfilled purchases return existing state. | These are generic payment/fulfillment controls, not the account/service-date cap. The C3 change must not duplicate generic idempotency requirements or claim provider-payment identity alone prevents two different same-day reading orders. |
| Technical Contracts v1.0, §§21.4–21.6 and 25.1 | Persistence-level uniqueness for purchase/order/provider/event/grant identities; atomic Credits grant + entitlement transition; `UNKNOWN / RECONCILIATION_REQUIRED` for ambiguous provider status; retries only for classified retryable failure. | Preserve these mechanics. Add only the C3 account/date slot invariant and the necessary transitions linking an original reading order to its immutable service date and remedy. |

**Gap conclusion:** the six examined Clean Current Set source members do not define an account-plus-UTC-date Deep Sky cap slot, the precise purchase event that consumes it, or the same-day slot effect after terminal non-delivery. This is a cap-specific product/commercial contract gap. It is not a finding that generic idempotency, entitlement, reconciliation, Credits, or Quiet Sky controls are missing.

## 5. Candidate contract recommendation — not approved

The existing source evidence supports a narrow addition rather than a rewrite of commerce architecture.

### 5.1 Purchase object and cap trigger

Candidate recommendation for controlled review:

1. A **new Deep Sky reading redemption** is the capped object. Buying/top-upping Credits is a separate transaction; reopening a retained purchased reading is not a new purchase; a linked no-charge recovery of the original order is not another purchase.
2. The final explicit user confirmation must create one stable logical reading-order identity. The server assigns an immutable UTC service date from its authoritative timestamp and atomically enforces the account/date slot across devices. A click, preview, unconfirmed reservation or client clock alone is not enough to prove an effective purchase.
3. Define the effective purchase boundary explicitly in the contract. The recommended candidate is a durable confirmed reading-order commit associated with the exact Credits debit and account/date-slot transition, not the later point at which a valid reading becomes accessible. That preserves the owner-originated purchase-cap premise instead of covertly switching to a fulfilled-reading cap.
4. A duplicate request for the same logical order resolves to that order and cannot debit again. A second independent new-reading order for the same account/date cannot bypass an occupied or unresolved slot.
5. Exact persistence schema/indexes are implementation choices; the contract should first establish the invariant. A database-level uniqueness/atomicity design must prevent concurrent tabs/devices from creating two effective purchases for the same account/date.

This is a recommendation, not a settled owner-approved state machine. In particular, the owner direction does not by itself define whether a fully reversed terminal purchase restores same-day eligibility.

### 5.2 Failure and remedy must be separate from the cap definition

- **Pending/unknown/reconciliation:** not terminal non-delivery. No timeout-based slot release, speculative restoration, second independent order bypass, duplicate entitlement or false success. Preserve the original order identity and date until authoritative reconciliation.
- **Recoverable CE-side failure after debit:** recommended first-line `PATH-LINKED-RECOVERY`: preserve the original purchase/debit and use an idempotent, linked no-charge retry/replacement only when the original order can still be safely fulfilled. It cannot create another purchase, debit, service date or entitlement.
- **Proven terminal inability to fulfill:** a linked retry is no longer a substitute for an actual terminal remedy. Restore the reading debit exactly once and apply any applicable refund/consumer remedy. The same-day cap effect must be explicit: keeping the slot occupied versus releasing it only after completed terminal closure are distinct policy outcomes. Do not infer slot release merely from restoring Credits, and do not hold a consumer's mandatory rights hostage to the cap.
- **After a valid delivery:** a complaint/remedy must not silently be counted as a new paid purchase or automatically reset the cap. Keep the original commercial history and apply the separately defined remedy policy.
- **UTC rollover:** the original order/date remains immutable. Midnight does not turn an unknown state into a terminal failure and does not transfer the old slot into a new date. The interaction between an unresolved prior-date order and a new-date purchase needs an explicit test oracle.
- **Consumer display:** accurately explain that the cap/reset uses UTC, what counts (Credits top-up vs reading redemption vs reread), order/reconciliation state, and the applicable Credits-restoration/refund/replacement route. No fake scarcity, false countdown, forced purchase, false delivery or Quiet-Sky masking.

The remedy labels `PATH-LINKED-RECOVERY` and `PATH-REVERSAL-RELEASE` are not the same as Option A (purchase/redemption cap) and Option B (fulfilled-reading cap) in Box 2515757204983. Keep the cap-trigger axis and the remedy axis separate.

## 6. Candidate-only test-oracle matrix

These are proposed test oracles for review only. They are **not executed and not registered**. Map them against the eventual authorized Test Register before adding any tests; preserve existing generic payment/idempotency coverage.

| ID | Scenario | Required oracle | Disposition |
|---|---|---|---|
| C3-01 | First new-reading purchase for account/date | One stable order; exactly one committed purchase/debit under the approved trigger; date is server-assigned and immutable. | Candidate |
| C3-02 | Two simultaneous confirmations on different devices for the same account/date | At most one effective new-reading purchase; atomic account/date guard; losing request has a deterministic non-charge outcome. | Candidate |
| C3-03 | Different accounts, same date | Account A's slot does not consume or block account B's slot. | Candidate |
| C3-04 | UTC boundary immediately before/at 00:00:00 UTC | Assignment follows server UTC instant and approved half-open interval; client timezone/clock cannot change it. | Candidate |
| C3-05 | Credits top-up and reread of a retained reading | Top-up does not consume the reading slot; permitted reread adds no Credits deduction and is not a new reading purchase. | Candidate |
| C3-06 | Replay of same logical reading-order ID, duplicate client request | Existing order/state is returned; no second debit, slot consumption, or entitlement. Do not duplicate generic provider-webhook tests unless the cap-specific oracle is missing. | Candidate |
| C3-07 | Timeout, network partition, ambiguous callback or worker state | `UNKNOWN / RECONCILIATION_REQUIRED`; no guessed terminal failure, no timeout release, no speculative restoration or bypass order. | Candidate |
| C3-08 | Recoverable generation failure after debit | A linked retry/replacement uses the original order/date; no additional debit; at most one eventual entitlement; technical failure is never Quiet Sky. | Candidate |
| C3-09 | Confirmed terminal non-delivery after debit | Prove no usable reading and no remaining downstream operation; one-time restoration/refund oracle is deterministic. Same-day slot oracle is conditional on owner-approved remedy semantics. | Conditional on remedy disposition |
| C3-10 | Original order remains unresolved across UTC midnight | Preserve original date and reconciliation; do not treat midnight as failure or transfer the old slot. Test D+1 behavior after its product oracle is settled. | Conditional |
| C3-11 | Post-delivery complaint/remedy | No silent cap reset or fictitious new purchase; original order/fulfillment history remains auditable. | Candidate |

The previous R2 source/test disposition (Box 2515695712759) already warns against duplicating generic PAY-01/PAY-02/PAY-03, generic Quiet Sky/error tests, or generic time/security-clock coverage. Its existing-register findings remain useful as review evidence but should not be treated as proof of current official register identity until that source is reconciled.

## 7. Controlled change package and next steps

1. **Source identity:** the Clean Current Set archive and all six cited member hashes are now verified. The earlier Box source-lineage notes R0/R1 remain historical findings of what those earlier passes could not verify; do not rewrite them retroactively. This follow-up supplies new evidence.
2. **Current Test Register:** locate the explicit authorized pointer/current copy and verify its identity before making or registering tests. Archive absence alone does not settle this.
3. **Normative delta:** after protected remedy semantics are disposed, prepare a narrow candidate redline centered on the Account/Commercial Specification's Deep Sky / commercial-failure boundary, with targeted implementation mapping to the current Implementation Plan and Technical Contracts. Do not duplicate the general payment idempotency or Quiet Sky clauses, and do not invent database column/index names before the persistence design is authorized.
4. **Owner boundary:** the one-purchase-per-account-per-UTC-day premise and UTC boundary do not need to be asked again. The substantive unresolved product decision is the exact treatment of a proven terminal non-delivery after debit—especially whether completed reversal/restoration releases same-day eligibility. `PATH-LINKED-RECOVERY` remains the recommendation only for recoverable failures.
5. Keep PR #27 draft, no merge, no A10, no Test Register mutation, no normative change and no implementation/production/SEAL transition on this artifact.

## 8. State

- Clean Current Set outer identity: **PASS** against Box-listed SHA-1 and boundary-record SHA-256.
- Six cited current-set member identity checks: **PASS**.
- Daily cap premise: **OWNER-ORIGINATED / EVIDENCED**.
- UTC service-day boundary: **OWNER-APPROVED, LIMITED SCOPE**.
- Detailed counted-purchase event: **CANDIDATE RECOMMENDATION; NOT FORMALLY DISPOSED IN THE DETAILED CONTRACT**.
- Recoverable-failure `PATH-LINKED-RECOVERY`: **RECOMMENDED, NOT APPROVED**.
- Terminal non-delivery, exact restoration and same-day slot effect: **OPEN PRODUCT/CONSUMER-REMEDY CONTRACT**.
- Official Test Register identity/location: **NOT ESTABLISHED**.
- Normative/Test Register/source authority/runtime/production: **UNCHANGED / NOT AUTHORIZED**.
- `SOURCE_AUTHORITY=NOT_ESTABLISHED`; `TRUSTED_BUILD=NOT_ESTABLISHED`; `PRODUCTION_RUNTIME=NOT_AUTHORIZED`; `SEAL=NO`; `FAIL_CLOSED=TRUE`.

---

End of R0.
