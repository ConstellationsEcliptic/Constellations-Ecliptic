# CE PRE-A10 — REMAINING AREA SOURCE-BOUND REVIEW AND OWNER DECISION BRIEF R2

**Date:** 2026-10-10  
**Classification:** WORKING EVIDENCE / NON-AUTHORITATIVE / DECISION SUPPORT  
**Revision:** R2 (2026-10-10)
**Predecessor:** R1 (preserved unchanged)  
**Predecessor:** CE_PRE_A10_REMAINING_FOUR_AREA_RECONCILIATION_R0_2026-10-10.md (preserved unchanged)  
**Scope:** A3 Today's Note × Quiet Sky; B1 Canon Rule Registry; C3 daily Deep Sky purchase cap; D4 launch market / locale / currency  
**Authority effect:** NONE • Normative amendment: NONE • Code/schema/runtime effect: NONE • A10/production/SEAL: NONE

## 1. Purpose and current boundary

The original R0 register left four areas at `RECOMMENDATION_READY`: A3, B1, C3 and D4. Since then, the owner explicitly selected C3's D1-A effective-purchase rule, D2-B post-debit terminal-non-delivery remedy, and the fulfillment-health interlock principle. The preserved Pre-A10 area register R1 records that limited disposition. Current register R1 has 20/23 completed review areas and three genuinely incomplete areas: A3, B1 and D4. This R1 updates the decision crosswalk without mutating R0 or treating a candidate implementation as normative.

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

### Owner disposition already recorded; detailed product/implementation contract remains open
The owner has already approved the limited product-semantic direction in Box 2515533522798: an optional, clearly separate, non-personal editorial note may accompany a valid Quiet Sky when an approved item exists; omit it when no approved item exists; never let it imply a personal signal/prediction or disguise a non-VALID observation. Do not ask the owner to make that same yes/no Quiet Sky disposition again.

Still unapproved or unspecified: canonical editorial source/library and its authority; content provenance/rights and review/expiry; locale availability/fallback; deterministic selection; final UI label/layout/accessibility/copy; exact behavior for valid signal states beyond the recorded narrow Quiet Sky disposition; normative contract integration; official acceptance-test registration; implementation/deployment. The recommendation is to prepare the complete source/display/selection contract using a curated, versioned, reviewed non-personal library and deterministic selection, with no personal data or free-form runtime-LLM generation in V1. This remains a candidate design, not an approved implementation. The area remains incomplete because these engineering/source-contract artifacts and authorization route are not yet established—not because the owner has failed to decide whether a note may accompany valid Quiet Sky.

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

### Owner decision boundary — defer until evidence is prepared
Once a sourced candidate rule list and condition-binding proposal are prepared, present one consolidated, evidence-based owner decision on the initial V1 semantic scope/tradition mix; do not ask before that source-bound candidate exists. No exact astrological meaning or active Canon rule is approved by this note. Preferred recommendation: do not expand coverage by guessing; use a bounded, auditable V1 registry and omit interpretation when a rule or verified conformance is absent.

## 4. C3 — One new Deep Sky purchase per account per UTC service day

### Owner disposition now recorded — do not ask again

The owner's established premise remains **at most one new Deep Sky purchase per authenticated account per CE service day**, shared across trusted devices. The service day is the fixed UTC Gregorian half-open interval 00:00 UTC inclusive to next-date 00:00 UTC exclusive (Box 2515555580794).

On 2026-10-10, the owner-confirmed CE Commerce Product Policy Disposition (PR #33's `owner-disposition-2026-10-10.md`) selected:
- **D1-A:** an effective new-reading purchase is the confirmed logical order bound to its immutable server-derived UTC service date with the one-time reading-Credits debit committed. Reservation by itself is not effective purchase.
- **D2-B:** following positively evidenced terminal non-delivery—no valid accessible reading/entitlement, no operation that can still deliver, all relevant operations closed, and exact once-only restoration of the reading debit—the same-date slot may be released only while the original UTC date is current. After expiry, close without transferring the old slot.
- **Fulfillment-health interlock principle:** UNKNOWN, BLOCKED, or expired readiness fails closed for admission of new purchases/effective-purchase debit; the interlock must not cancel or terminalize an existing operation that may still fulfill.
- Credits top-up and rereading a retained entitlement do not consume a new-reading slot. Credits restoration and cash/card refund remain distinct.

Decision evidence:
- [Owner disposition file in PR #33](https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/blob/prototypes/commerce-reference-model-r0-2026-10-10/prototypes/commerce-reference-model-r0-2026-10-10/owner-disposition-2026-10-10.md)
- [Owner-approved UTC service-day disposition](https://app.box.com/file/2515555580794)
- [Daily Cap Normative Delta R5](https://app.box.com/file/2517761459116) — candidate only, not normative.
- Preserved Zero-Point Human Decision Register R0: Box 2514894635417; later evidence crosswalk R1: Box 2517828812586.

The Pre-A10 area register R1 now records the owner-choice component of C3 as `OWNER_DECISION_RECORDED`. This scope does not mean the whole commerce contract or implementation is complete. The general Pre-A10 completion gate correctly remains incomplete because A3, B1 and D4 remain open.

### Residual gaps that remain open

1. **Separate pre-debit terminal failure:** earlier cap materials propose releasing a reservation after definitive pre-debit failure when no debit and no operation capable of committing or delivering remain. The 2026-10-10 D1-A/D2-B disposition did not expressly settle this separate branch. PR #33 has a candidate implementation and tests, but that is not an approved normative policy.
2. **Normative contract / official Test Register:** R5 is a non-normative redline. The active Technical Contracts pointer and current official full Test Register identity/binding remain unresolved in the characterized source lineage. PR #33's tests are candidate tests, not official registration.
3. **Health interlock implementation:** producer/source of a READY attestation, thresholds/lease, renewal, monitoring, operator control, and recovery semantics remain engineering design items. The provisional five-minute candidate lease is not an owner-approved production SLO.
4. **Payment and consumer remedies:** Credits restoration, original-money payment/card refund, no-charge replacement, cancellation, and post-delivery complaint handling are distinct; D2-B does not settle every financial or legal remedy.
5. **Implementation state:** commerce/persistence implementation is classified as NOT IMPLEMENTED / START FROM ZERO within the owner's defined five-source universe. PR #33 remains isolated, open, draft, non-production, and DO NOT MERGE.

### Required next work

- Preserve D1-A, D2-B, UTC service-day boundary and the interlock principle as settled; do not ask the owner to repeat them.
- Prepare the source-bound normative redline, persistence contract and proposed test-oracle package once the active Technical Contracts / Test Register targets and valid adoption route are established.
- Keep pre-debit failure/release as a distinct candidate issue. Complete consequence and consumer-impact analysis before a separate owner packet, if a policy choice remains necessary.
- Continue testing the isolated reference model against explicit candidate fixtures. Passing CI does not make it normative or production-ready.

C3's owner-choice component is recorded; complete commerce specification, official Test Register application, provider, market, price, schema and production authorization remain open.
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

A3 and B1 remain product/semantic scope gaps; D4 remains a commercial infrastructure/market-eligibility gap. C3's selected owner choices are recorded and must not be re-approved, while its specific pre-debit failure branch and downstream contract/implementation work remain open. The general autonomy mandate does not close these gaps. Technical implementation/tests, normative promotion, Runtime Adoption and production remain separate gates.

## 7. State — R1

- A3: `RECOMMENDATION_READY`; the limited Today’s Note semantics have an owner disposition, but the shipped source/content/display contract and implementation choice remain open.
- B1: `RECOMMENDATION_READY`; approved populated Canon Rule Registry, exact evidence-to-rule binding and verified semantic checker remain unestablished in the inspected scope.
- C3: `OWNER_DECISION_RECORDED` for D1-A, D2-B, the fixed UTC service-day boundary and fulfillment-health interlock principle. A separate pre-debit failure/release policy, normative contract application, official Test Register binding, health-interlock operating design and commerce implementation remain open.
- D4: `RECOMMENDATION_READY`; seller entity, provider eligibility, initial customer market, locale, currency and price remain unselected.
- Current Pre-A10 gate remains blocked until A3, B1 and D4 are resolved through evidence/disposition. On register R1, CI reports 20/23 complete, three incomplete, and no register-integrity errors; the completion-gate exit 2 is the expected fail-closed result while those three areas remain open.
- Normative files changed: NO.
- Official Test Register changed: NO.
- Code/schema/runtime/checkout changed by this review: NO.
- A10/production/SEAL authorized: NO.

---
End of source-bound remaining-area review R1.


## R2 change record

- Preserves R1 and all prior records unchanged.
- Corrects A3 wording that could be read as asking the owner to make the optional Quiet Sky note decision again. The limited owner disposition already exists at Box 2515533522798.
- Separates that settled product-semantic permission from the still-open canonical content source/library, provenance, locale, selection, UI/copy, normative integration, official test registration and implementation gates.
- Reaffirms B1 stays fail-closed until a source-backed candidate rule list, explicit condition binding and independent semantic-verifier design are prepared. Only then prepare a consolidated genuine owner decision about initial semantic scope.
- Does not change the area register, close A3/B1/D4, change norms, register official tests, or authorize code/runtime/A10/production.
