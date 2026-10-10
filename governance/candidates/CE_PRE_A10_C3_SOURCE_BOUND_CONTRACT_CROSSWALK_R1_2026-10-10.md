# CONSTELLATIONS ECLIPTIC
# PRE-A10 C3 — SOURCE-BOUND CONTRACT CROSSWALK R1

Date: 2026-10-10  
Classification: CANDIDATE SOURCE CROSSWALK / NON-NORMATIVE / AUTHORITY NOT ESTABLISHED  
Authority effect: NONE  
Normative amendment / official Test Register change: NONE  
Schema / code / runtime / production / SEAL effect: NONE  
Implementation authorization: NONE  
FAIL_CLOSED: TRUE

## 1. Purpose

This R1 supersedes the R0 crosswalk **for active candidate analysis only**. R0 remains preserved as a record of the earlier method and source-version labels. R1 corrects an overbroad reading of “source-bytes verified”: the hashes establish scoped Clean Current Set R3 archive/member identity, while later applied successor records establish some newer document versions and separate current identity/test/persistence issues remain.

The detailed source-lineage findings are in [C3 Source-Lineage Reconciliation R0](https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/blob/governance/candidates/ce-autonomous-evolution-charter-r0-2026-10-09/governance/candidates/CE_PRE_A10_C3_SOURCE_LINEAGE_RECONCILIATION_R0_2026-10-10.md).

## 2. Source object and versions used

| Source object | Exact identity / lineage evidence | Rule used for C3 | Limit |
|---|---|---|---|
| Clean Current Set R3 archive | Box 2485715303669; 2,654,872 bytes; SHA-1 `58f8c3dcccc0ccb2e79a79ddd46ab0014c2783d6`; SHA-256 `d9c2f4abbe0a482e982488d5d2e332202c0c0dc8fceca3b5faaceb3d2c4a8abc` | Historical governing-chain package/member container | Does not establish global Source Authority or make older member versions the sole later source |
| Product Constitution v1.6.1 | Box 2491704535193; SHA-1 `1fde1d44736e45614e8050769e60be6a875d964e`; successor/application record Box 2491700051951; post-apply verification Box 2491702950277 | Deep Sky sells depth of synthesis, not truth/accuracy/certainty; technical failure cannot be transformed into Quiet Sky/valid reading; commercial state cannot change astronomy, qualification, Canon or uncertainty | Successor materialization has limited harmonization scope and does not establish global Source Authority |
| Account/Privacy/Commercial v1.7 | Clean Current Set R3 member SHA-256 `470efd7d95299e8e9a7002b355c967f982a3582412b5664f4c86e7cbc4a152e5`; text reviewed against characterized Box source 2485319995048 | Account-bound/non-expiring Credits; retained entitlement can be reread without another debit; idempotent purchase request; minimal transaction/fulfillment records; deterministic failure reconciliation; consumer rights remain applicable | Member identity is verified within the archive; a raw-intake Box copy is not thereby promoted |
| Business Model v1.5 | Clean Current Set R3 member SHA-256 `b6a51ea4b40cf08715ca64843278e8ca6400572c67a39a1f1f34804c26133bd6`; characterized Box source 2485331476456 | Direct Credits model; Deep Sky is the paid core product; preserve anti-dark-pattern boundaries; no paid certainty or fake scarcity | Historical archive member identity, not a global authority declaration |
| Implementation Plan v1.3.1 | Box 2491699264134; SHA-1 `684a1266287ca278ff0e68b0d4c991cca7e9098b`; applied successor recorded by Box 2491700051951 and verified by Box 2491702950277 | §7.8 generic transaction state, stable logical purchase identity, database-level uniqueness, provider-event deduplication, reconciliation of unknown state, one effective grant; Phase 10 commercial fulfillment boundaries | Implementation/persistence requirements do not prove a live commerce source exists |
| Technical Contracts | Archived member is v1.0; harmonized v1.1 Box 2491699792103 / SHA-1 `4ab2177f5a2cba26d8025399509378fb821e4349`; later v1.1 hardened R2 at Box 2491799121573 / SHA-1 `b4b9ade7bc716a89132b8e0f2314467b8b5a96dc` is listed in Current Decision Register R6 | Context only; do not rely on a clause that depends solely on the unsettled artifact identity | Exact active Technical Contracts pointer lineage is OPEN |
| Official Test Register | Absent from Clean Current Set R3; archived Document Index lists v1.5; raw-intake copies have no current binding | Existing PAY/ERR coverage can be mapped conceptually | Official identity/current binding NOT ESTABLISHED; candidates are unregistered and unexecuted |
| Commerce/persistence source | Box 2515659021563 records no source found in inspected authorized scope | Implementation mapping stays generic | Do not invent tables, columns, database constraints, provider or live behavior |

## 3. Owner-originated product constraints — already settled

The following are not open questions to ask again:

- At most one new Deep Sky purchase per authenticated account per CE service day.
- The service day is the UTC Gregorian half-open interval `[00:00:00 UTC, next date 00:00:00 UTC)`.
- The allowance is shared across trusted devices for the same account.
- The date is server-derived at the atomic reservation boundary after explicit confirmation; client clock and display timezone do not govern it.

Owner boundary evidence: [Box 2515555580794](https://app.box.com/file/2515555580794). Related evidence: [Box 2515706725948](https://app.box.com/file/2515706725948), [Box 2515747060613](https://app.box.com/file/2515747060613), [Box 2515757204983](https://app.box.com/file/2515757204983).

These facts establish the cap premise and service-day boundary, not the full effective-purchase, remedy, reservation, terminal-failure or slot-release state machine.

## 4. Crosswalk of existing rule versus actual C3 gap

| Subject | Existing source coverage | C3 gap to address (proposal only) |
|---|---|---|
| Deep Sky meaning / integrity | Product Constitution v1.6.1 §4.5; §§8.2–8.3: synthesis depth only; technical failure distinct from Quiet Sky and valid output | Ensure failed/pending commerce does not create, expose, or mislabel a reading; do not duplicate Quiet Sky rules |
| Credits ownership and reread | Account/Commercial v1.7 §§11–14 as represented in the archive: account-owned/non-expiring Credits, retained entitlement reread without new debit, purchase identity and fulfillment records | Distinguish Credits top-up, new-reading order/debit, reread, linked retry, restoration, monetary refund and replacement |
| General payment idempotency | Account/Commercial §§13–14 and Implementation Plan v1.3.1 §7.8 / Phase 10 | Add account + immutable UTC service-date slot/order interaction; do not restate all generic idempotency |
| Payment success / generation failure | Account/Commercial §17 and Implementation Plan state reconciliation: deterministically reconcile, no double debit, silent entitlement loss or calculation change | Define recoverable post-debit path versus unknown state versus proven terminal non-delivery, and cap-specific slot effect |
| Purchase cap | Owner-originated one new purchase/account/service day; no complete current state machine was located | Define reservation vs effective purchase vs fulfillment; separate cap trigger (D1) from slot state after terminal reversal (D2) |
| Remedy | Applicable consumer-rights preservation in characterized Account/Commercial/Business sources | Define exact reading-Credits restoration once; preserve possible separate monetary refund/other remedies; do not make Credits restoration an exclusive legal conclusion |
| Checkout | Existing preview fields include scope, covered period, evidence categories, output type, total mandatory price and Credits cost | Supplement with daily limit, actual UTC reset instant, top-up/read/reread distinction and visible pending/remedy boundary without duplicating existing disclosures |
| Test registration | PAY-01–05 and ERR/INT tests exist in characterized historical Test Register v1.5 | Identify official current register first; register only missing cap/slot/remedy oracles through controlled revision |
| Persistence implementation | Plan specifies general uniqueness/idempotency but no authorized live commerce/persistence source found in bounded search | Do not map to schema/code until source of record is identified |

## 5. Semantics kept separate

### D1 — effective purchase event

- **D1-A (candidate recommendation):** the confirmed new-reading order becomes an effective purchase when it is durably bound to the immutable server-derived service date and its one-time reading-Credits debit is authoritatively committed. Reservation guards concurrency before this point; fulfillment is later.
- **D1-B (alternative, not silently interchangeable):** the slot is counted only when a valid reading becomes accessible. This is a fulfilled-reading cap, which changes the emphasis of the owner-originated purchase-cap premise.

### Recovery / terminal states

- Recoverable post-debit failure: continue under the original order with no second debit or independent entitlement; retain the original date and the order's cap effect.
- Unknown/pending outcome: reconcile the same order; timeout, missing callback, worker restart or UTC midnight cannot establish terminal non-delivery.
- Proven terminal non-delivery: positively establish no accessible valid reading and no remaining operation that could deliver one. Restore the exact reading debit once, grant no entitlement, apply approved consumer/payment remedies, and only then apply the selected cap rule.

### D2 — slot after terminal reversal

- **D2-A:** keep the slot occupied for the original date after exact restoration and downstream closure.
- **D2-B (candidate recommendation):** release the current-date slot once after terminal non-delivery is proven, the exact reading debit is restored exactly once, no entitlement exists, and all relevant operations are closed. The historical order/purchase event stays auditable; only the date's quota effect is reversed.

D1 and D2 are independent choices. D1-A + D2-B is internally consistent only if the final product contract explicitly distinguishes the immutable historical purchase event from the **net quota effect after a fully reversed, never-delivered order**. It must not claim both “every committed purchase always consumes the daily limit no matter what” and “fully reversed failure releases that limit.”

## 6. Additional gap identified before an owner disposition

D2-B would allow a new same-day order after each fully reversed terminal non-delivery. By itself, it does not define what happens if the service suffers repeated terminal failures. Do not silently impose a user-level attempt limit or repeatedly invite paid attempts against a known-broken fulfillment path.

Candidate recommendation for later review: use a deterministic service-level availability interlock to stop new paid-reading confirmations when a defined delivery-health condition establishes that fulfillment is unavailable; disclose temporary unavailability; do not debit Credits or create a slot for orders rejected by that interlock. Thresholds and operational evidence must be defined by the authorized implementation/reliability contract, not guessed in this product brief. This is a proposed safeguard, not an existing CE rule, owner decision, test or implemented capability.

## 7. Current conclusion

The source map is now more accurate and supports further **candidate product-contract design**, but it does not yet authorize an exact normative redline, official test registration or implementation mapping. Remaining blockers are: Technical Contracts identity/pointer reconciliation where needed; official Test Register identity/current binding; and authorized commerce/persistence source identification.

- D1 effective purchase trigger: RECOMMENDATION ONLY / NOT OWNER-APPROVED.
- D2 terminal-reversal slot effect: RECOMMENDATION ONLY / NOT OWNER-APPROVED.
- Service-level fulfillment interlock: PROPOSED GAP / NOT SPECIFIED OR IMPLEMENTED.
- Official Test Register: NOT ESTABLISHED.
- Normative sources and official register: unchanged.
- Runtime / production / SEAL: not authorized.
- FAIL_CLOSED: TRUE.

End of crosswalk.
