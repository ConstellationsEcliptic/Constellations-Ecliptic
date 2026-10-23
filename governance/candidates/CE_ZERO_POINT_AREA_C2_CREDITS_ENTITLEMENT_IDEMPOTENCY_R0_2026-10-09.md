# CE ZERO-POINT AREA C2 — CREDITS, ENTITLEMENT AND IDEMPOTENCY
Date: 2026-10-09
Classification: SOURCE RECONCILIATION / WORKING CANDIDATE / NON-AUTHORITATIVE
Status: SOURCE_RECONCILED
Authority effect: NONE
Normative amendment: NONE
Implementation authorization: NONE
Tests executed by this review: NONE

## 1. Conclusion

The current normative contract is clear about Credit ownership, non-expiry, reread entitlement and transaction idempotency. Preserve those rules. However, the exact authorized commerce/persistence implementation source is NOT ESTABLISHED in the inspected connected scope. Normative field lists and test requirements do not justify inventing a production database schema, payment provider, live ledger or checkout code.

## 2. Normative baseline

**Account, Privacy & Commercial Specification v1.7** (Box 2485319995048):
- Credits and retained paid-reading entitlement belong to the account, not a device.
- §§10–11: Credits are account-bound, do not expire, and do not determine signal existence, aspect, transit qualification, calculation result, Canon rule, uncertainty or mismatch handling.
- §10.3: an opened reading may be reread without another Credits deduction while its retained product lifecycle permits.
- §10.4: before purchase confirmation, users see product/synthesis scope, covered period, evidence categories, output type, total mandatory price and Credits cost.
- §13: a server-issued idempotency key prevents retries from creating duplicate Credits or duplicate entitlement. Minimum transaction identity includes transaction/provider/idempotency/account/amount/currency/Credits delta/status/timestamps.
- §14: a minimal Commercial Fulfillment Record binds transaction, idempotency, account, entitlement, service, Credits granted, fulfillment status, fulfillment time, reading reference and content hash.
- §§13.1–13.3 and §20: financial records may be retained only for legitimate accounting/audit/fraud/dispute/legal purposes; unnecessary links to deleted Personal Sky must be severed; retained records must not rebuild deleted Personal Sky. Account deletion does not create a hidden permanent Credits balance; unused paid Credits are processed under the configured applicable settlement/remedy policy before closure.
- §§16–17: commercial state must stay separate from calculation/interpretation; payment success followed by synthesis failure remains deterministically reconcilable without duplicate charge, silent entitlement loss or calculation changes made to compensate.

**Business Model Minimal V1 v1.5** (Box 2485331476456):
- Credits are the only V1 monetization unit; account-owned, device-independent and non-expiring.
- The example package/price is configurable, not a USD-only policy.
- Commercial state cannot change astronomy, qualification, Canon, uncertainty or feedback meaning.
- Fulfillment records are minimal evidence of transaction/entitlement state, not a store for full Personal Sky or a mechanism to restore data after deletion.

**Implementation Plan v1.3.1** (Box 2491699264134), §7.8 and Phase 10:
- A server-authoritative transaction state machine and stable logical purchase identity/idempotency key are required.
- Provider transaction and event identifiers must be unique/deduplicated.
- Credit grant must have database-level uniqueness/atomic fulfillment; application check-then-insert alone is insufficient.
- Client callbacks cannot be the sole authority for successful fulfillment; lost responses must be recovered by status lookup/provider callback.
- Unknown/conflicting provider states go to reconciliation, not speculative grant.
- Retry of an already fulfilled logical purchase returns the existing state and cannot grant again.

**Execution Profile & Test Register v1.5** (Box 2485336117840) has the following expected cases:
- INT-02 commercial independence: same astronomy input with Credits=0 and Credits>0 keeps the same evidence identity and signal qualification; only entitlement/presentation may differ.
- PAY-01 retry idempotency: one logical request yields one transaction, one Credits grant and one entitlement.
- PAY-02 duplicate provider callback: one effective Credits grant.
- PAY-03 payment success + synthesis failure: reconcilable state, no double grant, no silent entitlement loss, calculation unchanged.
- PAY-04/05 cover deletion during fulfillment and chargeback after deletion; VERS-12 covers Credit/entitlement conservation during migration failure; SCALE-04 covers payment callback bursts.
These are expected test cases, not fresh passing test evidence from this review.

## 3. Important distinctions

| Concept | V1 contract | Do not conflate it with |
|---|---|---|
| Credits balance | Account-owned, non-expiring | Device ownership or signal eligibility |
| Logical purchase | Stable transaction identity with idempotent retry | A new purchase from every retry/webhook |
| Credit grant | Atomic, unique effective grant | Duplicate increments after duplicate callbacks |
| Reading entitlement | Access to fulfilled reading and reread within its lifecycle | Re-computation, new purchase or new AI context |
| Fulfillment | Validated reading accessible with reconcilable entitlement | Payment confirmation alone or unvalidated LLM output |
| Birth-data version change | New profile version; existing Credits/entitlement not silently erased; historical reading retains its source profile version | Rewriting an old reading under new birth data |
| Account deletion | Personal Sky/reading data follow deletion lifecycle; required financial records may remain minimally | Hidden permanent Personal Sky, profile restoration or product personalization |
| Payment/generation failure | Reconcilable state, no duplicate grant, no silent entitlement loss | Reclassifying calculation state or claiming success without evidence |

The one-new-Deep-Sky-per-service-day premise is reviewed separately in C3. Its effective purchase trigger and failure/remedy branch cannot be inferred from the general idempotency contract.

## 4. Bounded implementation-source finding

Commerce Persistence Source-Discovery Finding R0 (Box 2515659021563) records:
- The inspected GitHub main root exposed only README.md at the checked main tip.
- The inspected A9 candidate tree contains calculation/runtime/canon/claim/validation modules but no commerce/payment/checkout/Credits/entitlement/order/refund/persistence package or SQL/database migrations.
- The inspected active Box implementation folders hold calculation/runtime packages and governance/pointers, not an identified persisted Credits ledger/commerce service.
- Current normative specifications define contracts, not a specific live code path or database schema.

This is bounded to the connected repo, A9 candidate and active Box folders—not proof there is no separate private/unindexed commerce repo or local worktree. Do not infer a database/table/provider or promote historical V7/V8 commerce/affiliate code.

## 5. Recommendation

**Preserve the normative Credits/entitlement contract and do not implement against an invented persistence model.**

Establish the authorized commerce source/worktree and its exact identity, then compare its persistence/transaction behavior with these requirements. If the source has not yet been created, a candidate backend design may be prepared in an isolated non-authoritative branch, but it cannot be called the live CE commerce implementation or be activated without the relevant source/runtime gates.

No owner decision is needed to restate the settled Credits principles. Any new refund/replacement treatment or precise daily-cap trigger belongs to C3/C4.

## 6. Status and non-actions

- Account-owned / device-independent Credits: PRESERVE.
- Non-expiry: PRESERVE.
- Paid-reading reread without another Credits deduction under retained lifecycle: PRESERVE.
- Database-level uniqueness / idempotency / reconcilable unknown state: normative requirements.
- Commerce persistence source in inspected authorized scope: NOT ESTABLISHED.
- Specific database, provider, schema or live ledger: NOT INFERRED.
- Code, schema, Test Register, normative docs and runtime: unchanged.
- Tests executed by this review: NONE.
- Runtime Adoption, production, deployment and SEAL: unchanged.

## 7. Evidence references

- Account, Privacy & Commercial Specification v1.7: https://app.box.com/file/2485319995048
- Business Model Minimal V1 v1.5: https://app.box.com/file/2485331476456
- Implementation Plan v1.3.1: https://app.box.com/file/2491699264134
- Execution Profile & Test Register v1.5: https://app.box.com/file/2485336117840
- Commerce/Persistence Source-Discovery Finding R0: https://app.box.com/file/2515659021563
- Source-First Recommendation Protocol: https://app.box.com/file/2515488894918

End of C2 review.
