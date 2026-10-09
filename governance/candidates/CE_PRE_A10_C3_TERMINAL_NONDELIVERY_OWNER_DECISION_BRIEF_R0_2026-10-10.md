# CONSTELLATIONS ECLIPTIC
# PRE-A10 C3 — TERMINAL NON-DELIVERY OWNER DECISION BRIEF R0

**Date:** 2026-10-10  
**Classification:** FOCUSED OWNER DECISION BRIEF / NON-NORMATIVE / SOURCE-LINEAGE CONDITIONAL  
**Authority effect:** NONE  
**Normative source / official Test Register change:** NONE  
**Implementation / runtime / production / SEAL effect:** NONE

## 1. The owner premise already established

The owner-originated premise is **at most one new Deep Sky purchase per authenticated account per CE service day**. The owner separately approved the UTC Gregorian day boundary: 00:00:00 UTC inclusive through, but not including, 00:00:00 UTC on the following day (Box 2515555580794).

Do not silently replace “purchase” with “successfully fulfilled reading.” Existing candidate artifacts contain both phrasings, and the source-bound finding (Box 2515747060613) says they are not semantically identical. The purchase-cap phrasing remains the baseline.

This brief addresses a narrower remaining choice: what to do when Credits have been debited but the order is **proven terminally unable to deliver the reading on that same UTC date**.

## 2. Facts common to either remedy

Neither remedy is allowed to:

- infer terminal failure from a timeout or unknown/pending provider/worker/entitlement state;
- create a second debit, duplicate entitlement, fabricated fulfillment or false Quiet Sky;
- change the immutable service date of the original order when UTC midnight passes;
- turn a linked retry/replacement into a new paid purchase;
- discard the order/ledger history or apply a restoration twice;
- deny mandatory consumer, refund, conformity, privacy or dispute rights under applicable law.

Before acting on either path, the order must have one stable identity and an authoritative reconciled state. “Terminal non-delivery” requires evidence that no usable reading was delivered and no unresolved downstream operation can still deliver one. Unknown states remain reconciliable; a clock boundary does not turn an unknown order into a terminal failure.

## 3. Two mutually exclusive first-line remedies

| | **Option A — reverse purchase and free the date slot** | **Option B — keep purchase and fulfill original order** |
|---|---|---|
| Credits | Restore the reading debit exactly once. | Do not restore the reading debit as part of this remedy; it remains consideration for the original purchase. |
| Daily cap | Release the same-date slot only after terminal reversal/restoration and closure of every downstream operation; a new independent order may then be confirmed. | Keep the original purchase's date slot consumed. |
| Retry identity | A new same-day attempt is a distinct order and must pass normal confirmation/cap/idempotency checks. | Retry/replacement is linked to the original order and cannot create a second debit, purchase or entitlement. |
| Consumer outcome | Credits are returned; the consumer may choose whether to try again under the ordinary purchase flow. | The consumer retains the original paid order and receives the purchased service through a no-additional-debit retry/replacement. |
| Principal risk | A second purchase attempt can occur that day after complete reversal; the exact meaning of the cap must recognize an effectively reversed purchase. | The date slot remains occupied while the original order is repaired; the remedy must not become an endless retry or suppress further mandatory consumer remedies. |
| UTC rollover | Original order/date remains immutable; a closed, reversed order does not transfer its slot. D+1 has its independent allowance. | Original order/date remains immutable; a linked retry is still tied to the original order, not counted as a D+1 purchase. |

These are not the same as the separate policy choice “one purchase per day” versus “one successfully fulfilled reading per day.” Option B preserves the purchase-cap premise most literally; Option A interprets a fully reversed purchase as no longer occupying the cap after every reversal/ledger/fulfillment path is closed. That last interpretation cannot be inferred from the word “purchase” alone.

## 4. Recommendation

**Preferred default: Option B as the first-line remedy for a recoverable CE-side delivery failure after debit.**

Rationale:
1. It best preserves the recorded owner premise of one new purchase per account/service day without redefining the cap as a fulfilment-only limit.
2. It avoids requiring the consumer to create and confirm a second purchase to receive the service they already bought.
3. It preserves one logical order, one debit and at most one eventual entitlement, while allowing an idempotent linked retry.
4. It keeps the remedy distinguishable from payment refund, Credits restoration, a post-delivery complaint, and a second independent purchase.

This recommendation applies only where a retry/replacement can safely fulfill the original order. It is **not** a rule that CE may keep Credits indefinitely if fulfillment is impossible. If CE cannot deliver within the approved retry/reconciliation policy, the order must move into the separately approved cancellation/refund/restoration remedy and any mandatory consumer rights still apply. The cap effect after that terminal reversal must be explicitly specified and tested. No retry may run forever or conceal an unrecoverable failure.

Why not make Option A the universal default? It puts a second user-initiated paid attempt between the consumer and the service already purchased, and it assumes that reversal automatically makes another purchase eligible. That might be a legitimate policy, but it is a larger interpretation of the current purchase cap and should not be introduced implicitly.

## 5. Decision that still belongs to the owner

The source records do not settle whether the owner wants the preferred Option B as the first-line remedy or wants Option A (full reversal/restoration and same-day slot release) even when a same-order repair is possible. The owner is not being asked to redo the already approved UTC boundary or to choose again between purchase-cap and fulfilled-reading-cap wording.

Recommended owner disposition, once the source-lineage prerequisite is resolved:

- **B — LINKED NO-CHARGE RETRY UNDER ORIGINAL ORDER** as first-line remedy where safe delivery can still be achieved.
- Separate terminal inability-to-fulfill path: one-time debit restoration/refund under applicable policy, and a precisely defined slot effect after complete terminal closure. No silent quota reset.
- Timeout, pending, ambiguous reconciliation or an unclosed downstream operation: no terminal remedy decision and no second order bypass.

This is the recommendation for owner consideration, **not an owner decision**. No approval is inferred by silence or by the broad autonomous-work mandate.

## 6. Source-lineage and change-control blocker

The current source-lineage update (Box 2515750096004) explicitly says the individual normative Markdown files used by earlier redlines have not been proven byte-identical or otherwise linked to the current governing archive. Therefore:

- this brief is conceptual/product analysis only;
- do not write a normative redline, alter the governing archive, or update the official Test Register on this basis;
- resolve the exact current normative source lineage first;
- then prepare a controlled product-contract amendment and only the missing cap-specific tests;
- independent review and required governance gates still apply.

Key source records:
- Daily Deep Sky Service-Day Boundary owner disposition (Box 2515555580794): https://app.box.com/file/2515555580794
- Daily Deep Sky Cap Semantic Consistency Finding R0 (Box 2515747060613): https://app.box.com/file/2515747060613
- Cap Semantic Options & Test Consequences R0 (Box 2515757204983): https://app.box.com/file/2515757204983
- Normative Source-Lineage Boundary Update R1 (Box 2515750096004): https://app.box.com/file/2515750096004
- R2 Source and Test Disposition R1 (Box 2515695712759): https://app.box.com/file/2515695712759

### Source-lineage investigation — initial identification and 2026-10-10 follow-up

The Box folder listing for `01_CURRENT_GOVERNING` (folder ID `420832009587`) identifies `CE_V1_CLEAN_CURRENT_SET_R3-2026-09-24.zip` (Box file ID `2485715303669`, listed SHA-1 `58f8c3dcccc0ccb2e79a79ddd46ab0014c2783d6`) and pointer record `CE_CURRENT_GOVERNING_BOUNDARY_2026-09-24.md` (Box file ID `2485721889298`). Dropbox also exposes the corresponding clean-current-set archive at `/CE_V1_CLEAN_CURRENT_SET_R3_2026-09-24.zip` (2,654,872 bytes) and a separately extracted folder.

**New verified evidence:**

1. The operator ran Windows PowerShell `Get-FileHash -Algorithm SHA256` on the local `CE_V1_C1_SOURCE_AUTHORITY_CUMULATIVE_REHARDENING_AUDIT_R3-2026-09-24.zip`. The resulting SHA-256, `023dbe53216cd859ec1e5f49b2736ea0f70af568071b7b6117426d9b11c93cad`, exactly matches the sidecar `CE_V1_C1_SOURCE_AUTHORITY_CUMULATIVE_REHARDENING_AUDIT_R3-2026-09-24.zip.sha256` available in Dropbox. This verifies the local C1-R3 ZIP against its listed sidecar; it does not itself establish production authority or authenticate every historical assertion.
2. The C1-R3 archive is available in Dropbox at `/CE_V1_C1_SOURCE_AUTHORITY_CUMULATIVE_REHARDENING_AUDIT_R3-2026-09-24.zip` (124,019,414 bytes), with extracted companion files. Its `C1_STATUS.json` continues to report `SOURCE_AUTHORITY=NOT_ESTABLISHED`, `TRUSTED_BUILD=NOT_ESTABLISHED`, `AUTHORIZATION=NON_AUTHORIZED`, `SEAL=NO`, and `FAIL_CLOSED=TRUE`. The audit result remains `AUDIT_COMPLETE_WITH_HARD_BLOCKERS_AND_HARNESS_DEFECTS`.
3. Dropbox's text extraction for the 2,654,872-byte Clean Current Set R3 ZIP made its internal file text available. A full-text comparison against the separate Dropbox copies of `01_NORMATIVE/06_ACCOUNT_PRIVACY_COMMERCIAL_SPECIFICATION.md` and `01_NORMATIVE/CE_V1_TECHNICAL_CONTRACTS.md` matched after normalizing only trailing blank lines at the text-extraction boundary. The internal manifest lists these expected member SHA-256 values: Account/Commercial Specification `470efd7d95299e8e9a7002b355c967f982a3582412b5664f4c86e7cbc4a152e5`; Technical Contracts `e7dae6d0de4becf6aa748667d01758e1cc8499b724539930af9212d64b4cc117`. Those member hashes have **not** been recomputed from raw member bytes in this pass, and no outer SHA-256 sidecar for the Clean Current Set ZIP was located.

The relevant normative contracts therefore can now be reviewed on a source-grounded **content** basis, but exact current normative-member byte identity to the governing ZIP remains **NOT ESTABLISHED**. A text-extraction match is not represented as a raw-byte match. The original lineage boundary remains fail-closed.

The current Account/Commercial Specification v1.7 §§13–17 requires payment idempotency, a minimal fulfillment record, deterministic reconciliation, no duplicate Credits debit, and no silent loss of entitlement. Technical Contracts §§21.4–21.6 require uniqueness for purchase/order and provider identities, atomic Credits/entitlement fulfillment, and an explicit `UNKNOWN / RECONCILIATION_REQUIRED` state for uncertain provider outcomes; §25.1 permits retry only for classified retryable failure. These constraints support the technical integrity boundary but do **not** decide the product remedy between Option A and Option B.

No normative file or official Test Register was changed. Option B remains a recommendation only; terminal remedy and post-reversal cap semantics remain a protected owner decision.

## 7. Current state

- Purchase-cap premise: **OWNER-ORIGINATED / EVIDENCED**.
- UTC boundary: **OWNER-APPROVED, LIMITED TO THE DATE BOUNDARY**.
- Option B: **RECOMMENDED, NOT APPROVED**.
- Terminal remedy/cap mechanics: **OPEN OWNER-ONLY PRODUCT SEMANTIC**.
- Exact current normative-source lineage: **NOT ESTABLISHED**.
- Normative files, Test Register, production behavior: **UNCHANGED**.
- Implementation / A10 / Runtime Adoption / production / SEAL: **NOT AUTHORIZED**.

---

End of R0.
