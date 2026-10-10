# CONSTELLATIONS ECLIPTIC
# C3 — COMMERCE IMPLEMENTATION FROM ZERO ROADMAP R0

Date: 2026-10-10  
Classification: SOURCE-BOUNDED IMPLEMENTATION ROADMAP / NON-NORMATIVE / CANDIDATE ONLY  
Authority effect: NONE  
Normative amendment: NONE  
Official Test Register change: NONE  
Schema / code / runtime change: NONE  
Implementation / A10 / Runtime Adoption / production / SEAL authorization: NONE  
FAIL_CLOSED: TRUE

## 1. Decision recorded for project planning

The owner has defined the CE source universe as exactly five places:

1. Box
2. Dropbox
3. ChatGPT Library (Pustaka)
4. GitHub
5. The owner's laptop

The surfaced records and artifacts reviewed across those sources do not identify an implementable CE V1 commerce backend or persistence service for Deep Sky purchases, Credits ledger operations, payment reconciliation, or entitlement fulfillment. The laptop review identified website starter/iteration projects whose inspected source covers astrology UI, AI reading endpoints, newsletter handling, affiliate placeholders, and/or a rule engine—not the required commerce service. The connected GitHub main root is a website README; the inspected A9 tree is the Calculation Core/runtime candidate; active Box implementation folders inspected are calculation/runtime/governance artifacts. V7/V8 website files are historical/intake candidates, not an authorized commerce source. Targeted Dropbox searches did not return a current commerce implementation.

**Operational classification for this project: COMMERCE IMPLEMENTATION = NOT IMPLEMENTED / START FROM ZERO within the owner-defined five-source universe.**

This is a project-planning determination based on the defined source boundary and reviewed evidence. It is not a claim about hypothetical systems outside CE's designated sources. No further search for a sixth source is in scope unless the owner changes the boundary.

## 2. Governing source basis and limits

This roadmap only translates existing characterized requirements into a staged work plan. It does not establish global Source Authority and does not promote historical or raw-intake documents.

- [Product Constitution v1.6.1 — Box 2491704535193](https://app.box.com/file/2491704535193): Deep Sky sells depth of synthesis, not truth, accuracy, certainty, guaranteed outcomes, or psychological authority; commercial/technical failure is not Quiet Sky or a delivered reading; commerce cannot alter astronomy, qualification, Canon, or uncertainty.
- [Implementation Plan v1.3.1 — Box 2491699264134](https://app.box.com/file/2491699264134): §7.8 defines server-authoritative payment state, stable logical purchase identity/idempotency, provider transaction/event deduplication, database-level uniqueness and reconciliation; Phase 10 defines Credits and commercial fulfillment after prerequisite product, account, and privacy phases.
- [Technical Contracts v1.1 hardened R2 — Box 2491799121573](https://app.box.com/file/2491799121573): §21 defines the minimum conceptual transaction and fulfillment records, required uniqueness, atomic fulfillment and unknown-provider-state handling; §§22–23 define financial-retention and data-class boundaries; §§26–28 define tests, change control and definition of done.
- Account/Privacy/Commercial v1.7 and Business Model v1.5 are characterized in the [C3 Source-Bound Contract Crosswalk R1](https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/blob/governance/candidates/ce-autonomous-evolution-charter-r0-2026-10-09/governance/candidates/CE_PRE_A10_C3_SOURCE_BOUND_CONTRACT_CROSSWALK_R1_2026-10-10.md). Their version/lineage limitations remain as stated there.
- [C3 Purchase-Cap Contract Candidate R1](https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/blob/governance/candidates/ce-autonomous-evolution-charter-r0-2026-10-09/governance/candidates/CE_PRE_A10_C3_PURCHASE_CAP_CONTRACT_CANDIDATE_R1_2026-10-10.md), [Decision Brief R2](https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/blob/governance/candidates/ce-autonomous-evolution-charter-r0-2026-10-09/governance/candidates/CE_PRE_A10_C3_TERMINAL_NONDELIVERY_OWNER_DECISION_BRIEF_R2_2026-10-10.md), and [Test Register Binding Reconciliation R0](https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/blob/governance/candidates/ce-autonomous-evolution-charter-r0-2026-10-09/governance/candidates/CE_PRE_A10_C3_TEST_REGISTER_BINDING_RECONCILIATION_R0_2026-10-10.md) are working candidates/evidence, not normative amendments or production authorization.

Two binding limitations remain: the exact active Technical Contracts pointer identity is open because records disagree, and the current official full Test Register identity/binding is not established. These limitations permit source-bounded design planning but not a normative redline, formal test registration, or implementation claim.

## 3. Requirements already established by characterized contracts

These are existing requirements, not new proposals:

1. Credits belong to the account, are not device-bound, and do not expire.
2. Deep Sky is the V1 paid product; payment unlocks depth of synthesis, not truth or certainty. The illustrative 4-Credit reading price/cost is a configurable commercial parameter, not a calculation or Canon rule.
3. A single payment processor handles payment credentials. CE must not retain full card number, CVV/CVC, or raw payment credentials.
4. The minimum conceptual transaction record is:
   `transaction_id`, `provider_transaction_ref`, `idempotency_key`, `account_id`, `amount`, `currency`, `credits_delta`, `transaction_status`, `created_at`, `completed_at`.
5. The minimum conceptual fulfillment record is:
   `transaction_id`, `provider_transaction_ref`, `idempotency_key`, `account_id`, `entitlement_id`, `service_type`, `credits_granted`, `fulfillment_status`, `fulfilled_at`, `reading_reference`, `reading_content_hash`. A content hash alone is not proof of delivery.
6. Logical purchase identity, provider transaction reference, provider event identity where available, and grant identity require persistence-layer uniqueness. Duplicate callbacks and concurrent retries must converge on one effective grant/entitlement; application-only check-then-insert is insufficient.
7. Unknown or conflicting provider state remains pending/reconcilable. It is not guessed to be success or failure. Client callback alone is not authoritative proof of provider success.
8. A retry reuses the same logical transaction/fulfillment state. Credits restoration for a failed reading debit and a monetary/card refund for the earlier Credits top-up are separate operations.
9. Retained paid readings can be reread while the applicable entitlement/lifecycle remains valid, without another reading debit. A Credits top-up is not a new-reading purchase.
10. Account deletion ends the active Personal CE relationship. Any financial record retained for an actual accounting, audit, fraud/security, dispute, or legal purpose must not recreate deleted Personal Sky; unnecessary personal linkage must be severed.
11. Purchase preview and digital-service disclosures must show the product/synthesis scope, covered period, evidence categories, output type, total mandatory price, Credits cost, processing timing, and applicable cancellation/refund/withdrawal treatment. The C3 proposal adds the daily cap/reset and top-up/new-reading/reread distinction without replacing these existing disclosures.
12. Commercial state must never alter astronomical calculation, geometry, qualification, Canon meaning, uncertainty, or signal identity. Failed/pending commerce must not be exposed as a valid delivered reading or normalized into Quiet Sky.

## 4. Owner-settled purchase-cap boundary

Already settled; do not ask the owner to repeat it:

- At most one **new Deep Sky purchase** per authenticated account per CE service day.
- Service day is the UTC Gregorian half-open interval `[00:00:00 UTC, next date 00:00:00 UTC)`.
- The same account shares the allowance across trusted devices.
- Server-authoritative UTC time assigns the immutable service date at the atomic reservation point after explicit confirmation. Client clock and display timezone are not authoritative.

These premises do not by themselves settle the effective-purchase event or the slot effect after terminal non-delivery.

## 5. Product decisions still requiring owner disposition

### D1 — Event that consumes the new-reading cap

- **D1-A — recommended:** the effective purchase occurs when the confirmed new-reading order is durably bound to its immutable server-derived service date and its one-time reading-Credits debit is authoritatively committed. The cap is a purchase cap; a committed order remains tied to its date while it recovers or is reconciled.
- **D1-B:** count only when a valid reading becomes accessible through its entitlement. This is a fulfilled-reading cap and changes the emphasis of the owner-settled purchase-cap premise.

Recommendation: **D1-A**, because it is the closer literal fit to “one new purchase” while still permitting a proven pre-debit terminal failure to release a reservation.

### D2 — Same-date slot after proven terminal non-delivery and exact restoration

D2 only applies after positive evidence that no valid reading became accessible, no downstream operation can still deliver it, the exact reading-Credits debit was restored exactly once, no entitlement exists, and all relevant downstream operations are closed.

- **D2-A:** keep the original service-date quota counted after that full reversal.
- **D2-B — recommended:** release the original-date quota once only after every terminal/reversal/closure guard is confirmed and only if the original UTC date is still current. Preserve the original order/date as immutable history; reverse only its quota effect.

If terminal closure occurs after date D ends, close the old date's slot without transferring it to D+1. Never re-date an unresolved order because of midnight. Timeout, a missing callback, a restart or midnight alone is not terminal evidence.

Recommendation: **D2-B** with a deterministic service-level fulfillment-health interlock. The interlock is a proposed reliability safeguard, not an existing rule or implementation; its health evidence, threshold, activation/reset and test oracle must be designed. It is not a third owner choice in the current decision brief.

## 6. From-zero implementation sequence

No provider, framework, database, table, column, migration, or API has been selected by this roadmap. The exact persistence design must be chosen and documented before concrete schema is written.

### Stage 0 — Close the semantic and binding gates
- Record owner disposition for D1 and D2, or an explicit RECONCILE outcome.
- Reconcile the active Technical Contracts pointer discrepancy through the controlled source-lineage record.
- Establish the exact current official full Test Register identity/pointer; do not promote raw-intake v1.5 copies by filename or hash alone.
- Keep candidate oracle labels local until official registration becomes admissible.

### Stage 1 — Freeze the service and order contract
Define and review separately the semantics and transition oracles for:
- Credits top-up/payment settlement;
- new-reading order and its immutable UTC service date;
- reading-Credits debit;
- retry and unknown/pending reconciliation;
- recoverable post-debit generation/validation failure;
- proven terminal non-delivery;
- one-time exact reading-debit restoration;
- optional/separate monetary or consumer remedy;
- entitlement grant and accessible validated reading;
- retained-reading reread;
- post-delivery complaint/remedy without silently erasing the original history;
- account/date reservation and release;
- deterministic service-level fulfillment-health interlock.

The model must retain separate order/fulfillment, daily quota, financial-ledger, and entitlement/output state dimensions. Do not collapse them into a single generic “purchase status”.

### Stage 2 — Select the implementation owners and dependencies
- Select one payment processor that meets the CE tokenized-payment boundary and applicable launch/jurisdiction requirements.
- Select the persistence system and document its transaction/isolation/uniqueness guarantees.
- Define the source repository/worktree, ownership boundary, build/test path and migration/change-control route within the existing approved CE source/governance path.
- Do not infer a processor from the starter websites, their Cloudflare documentation, or their newsletter webhook.

These are future implementation choices; none is selected by this artifact.

### Stage 3 — Write the persistence design before code
Use the required conceptual transaction and fulfillment records from the characterized contracts. Document:
- unique logical purchase identity;
- unique provider transaction reference;
- unique provider event identity where available;
- unique credit-grant identity;
- immutable order/service-date identity;
- account/date reservation coordination across devices;
- atomic fulfillment boundary;
- restoration/remedy identity and idempotency;
- reconciliation query and audit evidence for unknown provider states;
- retention/deletion/linkage severance rules.

Concrete table names, columns, indexes, provider fields, and migration syntax must follow the selected persistence system and exact source identity; they are not guessed here.

### Stage 4 — Implement in small, isolated vertical slices
Recommended sequence after gates:
1. Pure transition/state model with deterministic tests and no live payment calls.
2. Persistence uniqueness and atomic account/date reservation.
3. Credits transaction/grant and reading-debit/restoration identities.
4. Payment-provider adapter, webhook/event deduplication, status lookup and reconciliation.
5. Fulfillment validation/entitlement boundary, with no access until valid output is committed and accessible.
6. Checkout preview and accurate pending/unavailable/remedy UX.
7. Account deletion and necessary financial-retention/linkage handling.
8. Service-level health interlock and recovery/observability.
9. End-to-end verification with provider sandbox evidence, concurrency, duplicate delivery, network partition, restart and UTC-boundary fixtures.

The implementation plan places Commerce/Credits as Phase 10 after the Core, product, account/security and privacy prerequisites. C3 planning may proceed now; this is not permission to skip those dependencies or current governance gates.

### Stage 5 — Test only against bound oracles
The current candidate Test Oracle Map contains local candidate scenarios for top-up-not-consuming-quota, D1-A debit point, shared account/device allowance, separate-account isolation, UTC boundary, concurrent order reservation, pre-debit failure, unknown outcome across midnight, recoverable failure, D2-A/D2-B, restoration replay, close-after-date-expiry, reread, post-delivery remedy, service health, failure/Quiet Sky separation, and checkout disclosure.

These candidates are NOT official IDs, NOT registered, and NOT executed. After the current official Test Register is bound:
- map each case to existing PAY/ERR/SEC/SCALE/INT oracle coverage;
- add only the missing cap-specific assertions;
- independently review fixtures/oracles;
- execute and retain actual results against the exact candidate commit and chosen persistence/provider test setup.

### Stage 6 — Verify and release through existing governance
Require actual evidence for:
- database-level uniqueness under concurrent requests/webhook retries;
- one effective grant and entitlement;
- exact one-time restoration and quota release under the selected disposition;
- unknown-state reconciliation without guesses;
- no duplicate debit/order/entitlement on retries;
- no stale/unvalidated reading presented as delivered;
- UTC service-date behavior under client clock/timezone manipulation;
- consumer disclosure and legal review;
- deletion/financial-retention separation;
- reproducible build/test evidence and versioned source/runtime identity.

This roadmap does not authorize implementation, A10, Runtime Adoption, deployment, merge, production, dual approval, or SEAL. Those remain separate governance decisions.

## 7. Explicit non-goals

This work does not authorize or add:
- affiliate commerce, affiliate tracking, advertising, newsletter marketing, subscriptions or recurring billing;
- Share Card, referral/share rewards, public user-generated content or a social graph;
- persistent free-text journal or persistent Personal Context;
- behavioral profiling or use of Credits/payment state to influence astronomy, Canon, uncertainty, or user interpretation;
- manual/uncontrolled Credits or entitlement grants;
- payment-card storage at CE;
- promotion of V7/V8 historical code to current source authority;
- a claim that any commerce code, schema, provider integration, database, deployed runtime, or test has already passed.

## 8. Current disposition

- Commerce/persistence implementation in the owner-defined five-source universe: **NOT IMPLEMENTED / START FROM ZERO for project planning**.
- Normative specifications: exist; unchanged.
- D1: OPEN OWNER DECISION; recommend D1-A.
- D2: OPEN OWNER DECISION; recommend D2-B, subject to full reversal guards and original-date-only release.
- Official full Test Register identity/current binding: NOT ESTABLISHED.
- Exact active Technical Contracts pointer identity: OPEN.
- Payment provider and persistence system: NOT SELECTED.
- Candidate test oracles: NOT OFFICIAL / NOT REGISTERED / NOT EXECUTED.
- Normative files/Test Register/schema/code/runtime: UNCHANGED.
- Source authority: NOT ESTABLISHED.
- Trusted build: NOT ESTABLISHED.
- Runtime Adoption: NOT ESTABLISHED.
- Production runtime: NOT AUTHORIZED.
- SEAL: NO.
- Authorization: NON_AUTHORIZED.
- FAIL_CLOSED: TRUE.

End of R0.
