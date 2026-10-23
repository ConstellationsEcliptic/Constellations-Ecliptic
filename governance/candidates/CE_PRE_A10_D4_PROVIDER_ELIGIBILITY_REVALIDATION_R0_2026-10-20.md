# CE PRE-A10 D4 — Provider Eligibility Revalidation R0

**Date:** 2026-10-20  
**Classification:** SOURCE-BOUND REVIEW / NON-AUTHORITATIVE CANDIDATE  
**Authority effect:** NONE  
**Normative / schema / code / checkout effect:** NONE  
**Runtime / production / deployment / SEAL effect:** NONE  
**Area status:** D4 remains RECOMMENDATION_READY; owner disposition NOT RECORDED  
**FAIL_CLOSED:** TRUE

## 1. Executive conclusion

Do not select a launch market, seller jurisdiction, payment provider, locale, currency, or final price from the currently inspected evidence. The owner's recorded U.S. legal-policy baseline is an internal research baseline only; it is not a U.S.-first or U.S.-exclusive market decision. The sample “4 Credits = US$2.99” remains illustrative, not an approved price or USD-only policy.

Fresh official provider-policy review on 2026-10-20 strengthens the prior D4 finding:

- Stripe lists Indonesia as a **Preview** account region and lists the United States as supported. An Indonesia-based Stripe account is currently invite-only, accepts IDR only, settles in IDR, and does not support cross-border/international transactions. This constrains an Indonesia-based seller account; it does not itself choose CE's customer market.
- Stripe's restricted-business page was last updated 2026-09-22. It says seller-maintained stored value/credits may be subject to limits, and approval for restricted offers is specific to each service offer and can be modified or revoked. CE's exact astrology-oriented reflective product and account-owned Credits model therefore require accurate provider disclosure and explicit eligibility confirmation; no provider approval is established here.
- Paddle's published Acceptable Use Policy, last updated 2026-04-13, prohibits digital services associated with pseudo-science including horoscopes, and prohibits virtual currency/stored value including store credit, gift cards and vouchers. Under that published policy, Paddle should not be treated as a viable current candidate for CE's described product/Credits model absent a policy change or explicit written clarification that the exact offer is permitted.

No provider, seller entity, market, locale, currency, price, checkout or paid-readiness status is approved by this review.

## 2. VERIFIED — current governance and owner decisions

- Autonomous Operating Mandate Candidate R0 (GitHub blob `10ecf63bb5d235970bf2bd9646a7a25a09446256`) is expressly a non-authoritative working candidate; it grants no implementation, merge, release, production or A10 authority by itself.
- Pre-A10 Review Plan R0 (GitHub blob `d0a74a27a2d239da851d72f79acc1af4c2bcc527`) prohibits A10 implementation/promotion/adoption until all applicable areas have been reviewed and the relevant owner discussions/dispositions recorded.
- Area Register R3 (GitHub blob `ab6e005bed107d8b909a16af9f24fc239b138ae8`) keeps D4 at `RECOMMENDATION_READY`, `owner_decision_required=true`, with no D4 disposition recorded. `a10_authorized=false`.
- Owner Disposition — U.S. Legal Framework as Internal Policy Baseline (Box 2515620798775) directs use of U.S. federal and relevant state/territorial law as the internal policy research baseline. It explicitly does not establish U.S.-exclusive positioning, a launch jurisdiction, nationwide paid availability, a state/territory allowlist, currency, price, checkout enablement or a launch-market list.
- U.S.-focused investigation direction (Box 2515610250498) authorizes research focus, not a paid-market decision.
- Zero-Point Human Decision Register R0 (Box 2514894635417) records DR-04 initial jurisdiction, DR-05 locale and DR-06 currency/price as `NOT_RECORDED` in that working register. That is a bounded register state, not proof that no record could exist elsewhere.
- Business Model Minimal V1 v1.5 (Box 2485331476456) establishes a one-processor design and a simple Credits-based Deep Sky model; the US$2.99 / 4-Credit example is configurable/illustrative. Commercial state may not change calculation, qualification, Canon, uncertainty or truth.
- Paid Checkout Readiness Matrix R0 (Box 2515715498189) says the seller/entity, provider or merchant-of-record arrangement, final SKU, currency/price, terms and checkout copy are not established in the inspected source set. It explicitly says this does not block all CE development, but it blocks a paid-checkout readiness claim for an unspecified configuration.

## 3. VERIFIED — fresh external provider evidence

### Stripe

- Global availability: https://stripe.com/global — currently lists Indonesia as Preview and the United States as supported.
- Indonesia account requirements: https://support.stripe.com/questions/requirements-to-open-a-stripe-account-in-indonesia?locale=en-GB — invite-only onboarding and verification requirements.
- Indonesia methods/currencies/businesses: https://support.stripe.com/questions/supported-payment-methods-currencies-and-businesses-for-stripe-accounts-in-indonesia — Indonesia accounts currently accept IDR only, settle in IDR, and do not support cross-border/international transactions.
- Account in another country: https://support.stripe.com/questions/requirements-to-open-a-stripe-account-in-another-country?locale=en-GB — requires a genuine legal entity, tax ID, physical location, phone, government-issued ID, working website and supported physical bank account in that country; do not infer that choosing a desired market creates eligibility.
- Prohibited and Restricted Businesses, last updated 2026-09-22: https://stripe.com/legal/restricted-businesses — seller-maintained stored value/credits may be subject to limits; Stripe says restricted-offer approval is service-specific and may be modified or revoked. The page's jurisdiction-specific list also shows that eligibility can differ by merchant jurisdiction. This review does not infer that CE is approved or prohibited in a market from the absence of a named category alone.

### Paddle

- Acceptable Use Policy: https://www.paddle.com/help/start/intro-to-paddle/what-am-i-not-allowed-to-sell-on-paddle — last updated 2026-04-13; prohibits digital services associated with pseudo-science (including horoscopes) and virtual currency/stored value (including store credit, gift cards and vouchers). CE must not describe its model inaccurately or assume a generic SaaS merchant-of-record fit overrides the published exclusions.

These provider policies are operational eligibility evidence, not legal advice and not a substitute for the provider's review of CE's exact seller, product, Credits, marketing and transaction configuration.

## 4. VERIFIED — implementation/test boundary

The candidate commerce branch `prototypes/commerce-reference-model-r0-2026-10-10` is 76 commits ahead of `main` in the comparison performed for this review. Its README blob is `e650b61fd2565fcaae1df16f1416e99a4666b9a1`; it explicitly says the reference model is not a payment integration, approved production persistence layer, provider selection or official CE Test Register.

Inspected candidate files:
- `commerce_model.py` blob `eaae78db2b41590183ea646d82487e62a78110fc`;
- `postgres_schema_candidate.sql` blob `6d097393df68b6d99b1cffe440d836dc2763fb8f`;
- `test_commerce_model.py` blob `0b3c2aea7539d31531173b624e38dc946bb339cc`;
- `.github/workflows/commerce-reference-model-test.yml` blob `5424a1ad4f17fc12475b1cc5cbdaa989ae811575`.

The candidate SQL has configurable SKU revision, amount, currency, provider-name and provider-transaction fields. These are data-model capabilities, not an approved market/currency/provider configuration. The reference model and its tests cover commerce state/ledger/idempotency/fulfillment behavior; they do not establish merchant eligibility, provider approval, legal market readiness, supported locale, final price or a live checkout path. No tests were executed by this D4 review.

The candidate's owner disposition (blob `003157fbf53860880340549003e7037882e29714`) expressly does not approve a payment provider, seller/legal jurisdiction, live market, currency, price, refund policy or commercial integration.

## 5. INFERRED

1. The order of decisions matters: seller/legal jurisdiction and provider eligibility constrain which paid-customer markets are feasible; locale is a product/UI choice; currency and SKU price depend on the chosen provider-market configuration.
2. A U.S. internal legal research baseline does not justify US-first, USD-only or English/en-US-only claims.
3. An Indonesia-based Stripe account would not support an international launch through that account under the currently published limitations; this is not a conclusion about a seller entity actually being based in Indonesia.
4. Paddle's current published AUP is materially incompatible with the described CE astrology-oriented product and Credits model. Do not include Paddle in the viable shortlist under the current published policy.
5. A generic provider comparison or passing commerce-reference tests cannot replace written eligibility confirmation for the exact product and Credits instrument.

## 6. PROPOSAL — preferred sequence

**Preferred recommendation:** do not choose a market or currency yet. First establish the real seller/entity jurisdiction and its genuine eligibility; then seek written provider confirmation using an accurate description of CE's reflective astrology service, account-owned non-expiring Credits, redemption and refund/restoration semantics. Exclude Paddle under its current AUP. Evaluate Stripe only as an unapproved candidate, with the account-country limitations and seller-maintained Credits review made explicit. After a feasible provider path is confirmed, choose one initial paid-customer market/allowlist, then choose a launch UI locale, then approve currency/SKU/price and the corresponding disclosures.

A minimal single-market, single-locale, single-currency launch configuration is a complexity-reduction proposal, not a conclusion that any particular country, language or currency is best.

## 7. User/product consequences, risks and dependencies

- **User/product consequences:** no paid checkout or final price promise is made prematurely; the product may continue non-production/free-Core design and research without claiming paid-market readiness.
- **Commercial/provider risk:** onboarding rejection, payout/method incompatibility, or termination if CE's exact product/Credits model is not disclosed and accepted.
- **Consumer/legal risk:** currency, total price, taxes/fees, Credits terms, age controls, withdrawal/refund remedies and delivery promises must match the actual selected transaction and applicable requirements.
- **Integrity risk:** a provider/market decision must never affect astronomical calculation, qualification, Canon meaning, uncertainty or the content/identity of a reading.
- **Privacy risk:** do not add identity, telemetry or user-level profiling merely to choose a market or measure conversion.
- **Dependencies:** actual seller/entity and location; written provider eligibility; selected customer market; locale/content coverage (including A3 Today’s Note); Credits classification and remedy review; final SKU/currency/price; controlled transaction contract; authorized implementation and test binding; separate paid-checkout readiness decision.

## 8. HUMAN DECISION REQUIRED

No prior decision is being repeated. The remaining D4 owner choice is the actual seller/entity jurisdiction and intended initial paid-customer market, made after the feasibility packet is grounded in real provider eligibility. The internal U.S. legal-policy baseline is already recorded and is not the decision being reopened.

No locale, currency, price, processor or market should be inferred from language, sample prices, current user geography, or a provider's generic global marketing page.

## 9. UNRESOLVED / next admissible action

- Seller/legal entity and jurisdiction are not identified in the inspected D4 source set.
- No provider has given written eligibility confirmation for CE's exact astrology/Credits offer.
- No initial paid-customer market/allowlist, launch locale, currency, final SKU/price or checkout copy is approved.
- Credits classification and jurisdiction-specific consumer/tax/age/remedy requirements remain configuration-dependent.
- No authoritative payment integration or production checkout was established by the inspected source set; search results are bounded and do not prove universal absence.
- D4 remains `RECOMMENDATION_READY`; no owner disposition is recorded.

Next admissible action: prepare a concise provider-facing product/Credits fact sheet and a market-feasibility comparison after the actual seller/entity facts are known; preserve placeholders and keep paid checkout disabled. Do not implement a live provider, change normative sources or official Test Register, merge PR #26/#27, or authorize A10/runtime/production/deployment/SEAL.

## 10. Evidence references

- GitHub Autonomous Operating Mandate Candidate R0, blob `10ecf63bb5d235970bf2bd9646a7a25a09446256`.
- GitHub Pre-A10 Review Plan R0, blob `d0a74a27a2d239da851d72f79acc1af4c2bcc527`.
- GitHub Area Register R3, blob `ab6e005bed107d8b909a16af9f24fc239b138ae8`.
- Box 2517806798198 — owner-approved mandate direction, not by itself formal adoption of GDE-01 or a normative source.
- Box 2515620798775 — U.S. legal framework as internal policy baseline, limited scope.
- Box 2515610250498 — U.S.-focused investigation direction.
- Box 2514894635417 — Zero-Point Human Decision Register R0, DR-04/DR-05/DR-06.
- Box 2485331476456 — Business Model Minimal V1 v1.5.
- Box 2491704535193 — Product Constitution v1.6.1.
- Box 2515715498189 — Paid Checkout Readiness Matrix R0.
- Box 2515660036686 — seller/provider/transaction fact schedule referenced by readiness matrix.
- GitHub commerce prototype branch and blobs listed in §4.
- Official Stripe and Paddle sources listed in §3.

**Authority invariant:** this review and any tracking-register update are not release, runtime, market, provider or production authority. A completed review register can never itself grant Runtime Adoption, production, deployment or SEAL.
