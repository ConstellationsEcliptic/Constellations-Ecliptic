# CE PRE-A10 — REMAINING FOUR AREA SOURCE-BOUND REVIEW AND OWNER DECISION BRIEF R0

**Date:** 2026-10-10  
**Classification:** WORKING EVIDENCE / NON-AUTHORITATIVE / DECISION SUPPORT  
**Scope:** A3 Today's Note × Quiet Sky; B1 Canon Rule Registry; C3 daily Deep Sky purchase cap; D4 launch market / locale / currency  
**Authority effect:** NONE • Normative amendment: NONE • Code/schema/runtime effect: NONE • A10/production/SEAL: NONE

## 1. Purpose and current boundary

The current 23-area register leaves four areas at `RECOMMENDATION_READY`: A3, B1, C3 and D4. This note consolidates source findings, corrects a semantic drift risk in the C3 draft summary, and identifies the narrow owner choices that cannot honestly be inferred from the current sources. It does not treat any proposed behavior as an approved contract.

The owner's current adaptive direction applies: continue autonomous investigation/candidate preparation; revise recommendations when new evidence changes the analysis; pause and discuss a new material product principle or protected decision before treating it as approved.

## 2. A3 — Today's Note × Quiet Sky

### Verified source facts
- Product Constitution v1.6.1 (Box 2491704535193) §4.2 defines Look Today as a qualified Testable Sky Signal, or valid Quiet Sky when there is no qualifying signal. Quiet Sky is not a calculation failure.
- Implementation Plan v1.3.1 (Box 2491699264134) §13.2 presents Look Today as `TESTABLE SKY SIGNAL + TODAY'S NOTE` and says only the signal may enter Tomorrow Check.
- Owner disposition (Box 2515533522798) is limited: an optional, separate, non-personal note may accompany valid Quiet Sky when an approved item exists; omit if no approved item, and never use a note to disguise technical failure. It does not approve the library/source, exact copy/UI, selection algorithm, schema/code, or runtime generation.
- Bounded source/UI discovery R1 (Box 2515543958136) did not identify an approved current editorial library or standalone UI contract in the inspected Box/GitHub paths. This is a bounded search, not proof that no external design file exists.
- Privacy Architecture Minimal V1 v1.5 (Box 2485335589220) excludes persistent user-level behavioural profiles, account-history context and persistent Personal Context from the current V1 path.

### Recommended implementation direction (NOT YET APPROVED AS A DETAILED CONTRACT)
Prepare a versioned, reviewed, non-personal editorial library with deterministic selection. It must not:
- state or imply a personal prediction or fabricate a qualified signal;
- use personal calculation details, user feedback, account history, Credits, or prior readings to select content;
- enter Tomorrow Check or alter the signal/Canon/evidence path;
- appear on a technical/invalid observation surface;
- be generated as unrestricted free-form LLM prose at runtime in V1.

If no content entry is approved for the actual locale/context, omit the note. Test the signal state and editorial note independently, and verify the note cannot change a valid Quiet Sky, turn a failed calculation into a reading, or affect the testable-signal comparison.

### Owner decision needed
Before implementing Today’s Note as a shipped surface, decide the content purpose/source and display contract: should V1 ship a curated general editorial note alongside Look Today when a reviewed item exists, or should the surface be omitted until the library and contract are approved? The current narrow Quiet Sky disposition does not settle the complete note behavior for all Look Today states, nor authorize exact content. Preferred recommendation: build and approve the content/selection contract before launch; do not generate a stand-in at runtime to fill the gap.

## 3. B1 — Canon rule registry, evidence binding, and semantic conformance

### Verified source facts
Interpretive Canon v1.2 (Box 2485337228722) requires each actual rule to be provenance-bound and versioned, with fields including Rule ID, Canon version, tradition track, source reference/scope, condition, allowed interpretation, forbidden extrapolation, confidence-language boundary and applicability scope. The versioned rule registry is the source of semantic permission. A missing rule means no interpretation; no “best guess” Canon may be invented. Conflicts that remain unresolved must be omitted.

At exact A9 candidate `c8dab3542d3d4725cf591630c07f76366f7949d0`:
- `src/ce/canon/registry.py`, blob `ae1bc1a83f712c8ca15a2d05b56310bec341332d`, defines a schema-aware registry but its module-level `get_rule()` deliberately raises `CanonRegistryNotEstablished` because the registry is not materialized.
- `src/ce/claim/manifest.py`, blob `20e64047510a98aa34c5a84abc50885b12ca76b3`, builds the Allowed Claim Manifest from a rule and binds the Canon version, registry digest, rule ID and signal reference.
- `schemas/allowed_claim_manifest.schema.json`, blob `e1b9f46cae1c584a46cf83eb1953ccd376b38028`, defines the machine-readable claim boundary.
- `src/ce/claim/authorization.py`, blob `59a88041cbf39c86faeffdef65a50dcb866b93d5`, currently matches rule conditions only against the high-level fields `classification`, `kinematic_phase`, `phase_uniformity` and `requires_uncertainty_disclaimer`.
- `src/ce/signal/record.py`, blob `b496ddc397cc28d4be18cdd468fa233e46e7c516`, derives a Qualified Signal Record from an Evidence Packet and requires exactly one unique geometry identity. The geometry identity itself contains transit object, natal object/scenario, aspect and directed branch, but these selector values are not exposed as direct fields on the current Qualified Signal Record.
- `src/ce/output/semantic.py`, blob `b33e37111770e55521c50f01ee6c7b699b5d9c61`, deliberately returns no verified semantic-conformance function until a controlled independent verifier is established. The full claim-release path consequently fails closed.

The bounded search did not establish a populated, separately approved current V1 interpretive registry. Historical V8 rulebooks and calculation-test registries are not interchangeable with Canon authority.

### Technical finding
This is not only missing data. Before source-reviewed rules are materialized, CE must reconcile whether the current rule-to-signal matcher can bind rule applicability to the geometry those rules actually describe. If a rule is about a particular transit/natal body/aspect, matching it only by broad classification/phase/uncertainty fields may not prove that the exact claimed geometry is the one authorized by the rule. The solution needs candidate engineering and independent tests; it must not be solved by weakening the schema or assuming all rules are generic.

### Recommended path (NOT A RULE APPROVAL)
1. Keep claim output fail-closed while registry or semantic verifier is unestablished.
2. Create a narrow candidate Canon corpus from primary/source-referenced materials; perform source-scope, tradition-track, ambiguity and contradiction review for every rule.
3. Choose a bounded initial V1 rule coverage and document which supported signals have approved meanings versus deliberate omission.
4. Design and test explicit evidence-to-rule binding for every applicable selector, then build/independently qualify the semantic verifier and claim-manifest path.
5. Bind registry version/digest, manifest identities and historical-reading compatibility to the exact candidate build.
6. Run adversarial language tests, output-omission tests, wrong-rule/same-phase tests and independent review before enabling interpretations.

### Owner decision needed
Once a sourced candidate rule list and condition-binding proposal are prepared, the owner must decide the initial V1 semantic scope/tradition mix. No exact astrological meaning or active Canon rule is approved by this note. Preferred recommendation: do not expand coverage by guessing; use a bounded, auditable V1 registry and omit interpretation when a rule or verified conformance is absent.

## 4. C3 — One new Deep Sky purchase per account per UTC service day

### Source-lineage correction
The established owner-originated premise is **one new Deep Sky purchase per account per CE service day**. The UTC Gregorian day boundary is separately approved (Box 2515555580794). Recent source-bound semantic analysis (Boxes 2515747060613 and 2515757204983) explicitly warns that “one purchase” and “one successfully fulfilled reading” are not semantically identical.

The existing register summary's earlier phrase “effective quota consumption is the atomic committed new-reading order + Credits debit” is a *candidate recommendation*, not a finally approved definition of the purchase event. It must not silently close this ambiguity. Earlier normative redlines also remain provisional because byte identity to the current governing archive is not established; see Box 2515745492938 and Source-Lineage Update R1, Box 2515750096004.

### Distinct events that the contract must define
1. Reservation to prevent concurrent duplicate orders.
2. Effective purchase/redemption event and its relation to the debit.
3. Validated accessible fulfillment.
4. Unknown/reconciling transaction states.
5. One-time Credits restoration, payment refund, and no-charge replacement.
6. Reread of an already-owned entitlement and post-delivery complaint/remedy.
7. UTC midnight rollover while the old transaction remains unresolved.

Timeout is not terminal non-delivery. Reservation is not necessarily purchase. Debit is not proof that the reading was delivered. A remedy must preserve order identity/history and must not grant duplicate credits/entitlements or defeat mandatory consumer rights.

### Options and recommendation
- **Option A — purchase/redemption cap:** closest literal fit to the existing owner premise. Define precisely when an effective new-reading purchase counts; do not treat a reservation as a completed purchase. If terminal non-delivery occurs after debit, its remedy must be specified separately.
- **Option B — fulfilled-reading cap:** counts only when a valid reading becomes accessible. This changes the product rule from one purchase per day to one delivered reading per day and can permit another distinct purchase after failure. Do not treat it as an implicit implementation of Option A.

Recommendation: preserve the purchase-cap premise (Option A) as the wording baseline, while keeping the exact quota event and terminal post-debit remedy branch open until the owner chooses. Do not assume that Credits restoration automatically reopens the same-day slot.

### Owner decision needed
For a confirmed terminal non-delivery after debit on the same UTC date, choose the customer remedy/slot behavior:
- **A. Reversed order releases that date's slot** only after terminal failure, exact one-time restoration/reversal and all downstream operations are confirmed; a retry is a new logical order.
- **B. The daily cap remains consumed**, but CE provides a no-charge replacement/retry linked to the original order so the user is not forced to pay again.
- **C. A different explicit remedy**, supported by product and legal review.

Preferred recommendation: do not let consumers lose access due to a CE-side technical failure; consider an original-order-linked no-charge replacement or release the slot only after proven terminal reversal. Do not finalize the product rule before examining the consequences against the purchase-cap promise and applicable consumer rights. These branches require deterministic registered tests once selected. No normative source or official Test Register has been changed.

## 5. D4 — Initial paid market, locale and currency

### Existing policy boundary
The owner-approved U.S. legal-policy disposition (Box 2515620798775) establishes a U.S. internal research baseline only; it does not establish U.S.-exclusive positioning, a U.S. launch, nationwide checkout or USD. The U.S.-focused investigation direction (Box 2515610250498) is not paid-market authorization. The illustrative `4 Credits = US$2.99` in Business Model Minimal V1 v1.5 (Box 2485331476456) is not a final price/currency decision.

### Current external provider evidence checked 2026-10-10
- Stripe's official global-availability page lists both Indonesia (Preview) and the United States as supported/preview onboarding regions: https://stripe.com/global
- Stripe's official Indonesia requirements page says Indonesia is an invite-only program and requires local-IDR bank settlement details. It also says accounts located in Indonesia do not support cross-border/international transactions: https://support.stripe.com/questions/requirements-to-open-a-stripe-account-in-indonesia?locale=en-GB and https://support.stripe.com/questions/supported-payment-methods-currencies-and-businesses-for-stripe-accounts-in-indonesia
- Stripe's official requirements for a U.S. account require a registered U.S. business or, for an unregistered business, a business owner/representative physically located in the U.S., plus verification: https://support.stripe.com/questions/requirements-for-having-a-us-stripe-account?locale=en-GB. A desired customer market alone does not establish eligibility for a merchant account there.
- Stripe's current Restricted/Prohibited Business rules state that listed restricted categories can require additional due diligence and explicit approval. They include seller-maintained stored-value/credits as potentially limited in some cases, and some jurisdiction-specific restrictions on psychic/fortune-telling services. This does not prove CE is prohibited in every market; it means eligibility for CE's exact product and Credits model must be confirmed truthfully with the provider: https://stripe.com/legal/restricted-businesses?tp=1
- Paddle's current Acceptable Use Policy states that it does not support digital services associated with pseudo-science, explicitly including horoscopes, and prohibits virtual currency or stored value including store credit, gift cards and vouchers: https://www.paddle.com/help/start/intro-to-paddle/what-am-i-not-allowed-to-sell-on-paddle. On the present CE model, Paddle should not be assumed suitable; get explicit written confirmation before considering it further.

These are provider-policy findings, not legal advice or a decision about CE's market. Payment-processor onboarding and the exact product/Credits classification remain unapproved/unverified.

### Recommended decision sequence
1. Identify the real seller/legal entity and its jurisdiction. Do not choose a fictional or convenient jurisdiction to bypass provider eligibility.
2. Prepare an accurate provider-facing product and Credits description; obtain written eligibility confirmation from any candidate processor/MoR for astrology-oriented reflective content and the internal Credits model.
3. Compare viable providers on supported customer markets, payment methods, currencies, compliance allocation, fees, refunds/chargebacks, webhook/fulfillment support, and operational requirements.
4. Select the initial paid customer market/allowlist based on actual provider eligibility and legal/business feasibility.
5. Choose UI locale separately from seller jurisdiction; choose currency and SKU price only after the market/provider configuration is selected.
6. Do not enable paid checkout or claim market readiness until the configured path and applicable disclosures/legal requirements are verified.

### Owner decision needed
A real seller-entity jurisdiction and intended initial customer market must be chosen once the feasibility evidence is ready. That choice precedes final locale/currency selection. Preferred recommendation: do not infer U.S.-first, Indonesia-only, English-only or USD-only; first establish seller jurisdiction and provider eligibility, then recommend the initial market using a sourced comparison. No checkout, payment-provider, pricing, locale or normative change is authorized by this note.

## 6. Cross-area consequence

A3, B1 and C3 concern semantics/consumer promises; D4 concerns commercial infrastructure/market eligibility. These areas can be researched in parallel, but none should be represented as resolved by general autonomy approval. Any selected owner decisions must be written as specific scoped dispositions and then reflected in the candidate register. Technical implementation/tests, formal normative changes and production/runtimes remain separate gates.

## 7. State

- A3: RECOMMENDATION_READY; specific Today’s Note source/content/display choice remains open.
- B1: RECOMMENDATION_READY; approved rule coverage, evidence binding and verified semantic checker remain unestablished.
- C3: RECOMMENDATION_READY; purchase-versus-fulfillment semantics and terminal failure remedy/slot release remain open.
- D4: RECOMMENDATION_READY; seller entity, provider eligibility, initial customer market, locale, currency and pricing remain unselected.
- Current Pre-A10 gate remains blocked until the required area reviews are completed and separate Runtime Adoption governance is addressed.
- Normative files changed: NO.
- Official Test Register changed: NO.
- Code/schema/runtime/checkout changed: NO.
- IANA 2026e adopted: NO.
- A10/production/SEAL authorized: NO.

---
End of source-bound remaining-four review.
