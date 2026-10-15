# CONSTELLATIONS ECLIPTIC
# PRE-A10 D4 — DODO PAYMENTS ELIGIBILITY ADDENDUM R0

Checked: 2026-10-11
Parent research snapshot: `CE_PRE_A10_D4_PAYMENT_PROVIDER_ELIGIBILITY_SNAPSHOT_R2_2026-10-11.md` (preserved unchanged)
Classification: OFFICIAL-POLICY RESEARCH / NON-AUTHORITATIVE / CANDIDATE ONLY
Authority effect: NONE
Provider selection: NONE
Seller entity / launch market / currency / checkout decision: NONE
Normative, implementation, production, A10 or SEAL effect: NONE

## 1. Executive determination

**Dodo Payments is not approved and should not be treated as the V1 default. Under the currently described CE product model, classify it as HOLD — MATERIAL PRODUCT-POLICY FIT RISK; written compliance prescreen required before further integration work.**

The key point is not that Dodo lacks digital billing features. Its public docs support digital-first products, one-time payments and usage/credit-based billing. The obstacle is whether Dodo's policy permits CE's exact product: Dodo says Spiritual & Astrology services require review, with the condition "Entertainment only; no claims or predictions"; it separately prohibits products involving stored value. CE's current model contains a testable present-day sky signal, Look Future possibilities, and prepaid account-bound non-expiring Credits. Public documentation does not resolve whether these exact semantics are permitted.

Do not disguise the product category, imply that CE does not provide predictions if its authorized product still makes future-oriented claims, or redesign CE's constitutional/product meaning merely to pass a payment processor's policy. Ask Dodo to classify the exact truthful product. If Dodo requires removal of core CE functionality or the written answer remains ambiguous, retain Dodo as unsuitable for the present V1 model.

## 2. Findings from Dodo's official sources

### 2.1 Indonesia appears on the merchant-acceptance list, subject to identity and onboarding rules

Dodo's "Countries Eligible for Merchant Acceptance" page lists Indonesia among accepted merchant-account and payout countries. However, eligibility depends on the country that issued the identity document used for verification:
- Individual account: the individual's government-issued ID.
- Registered entity: the country of incorporation and identity documents for each director and beneficial owner.

The page explicitly cautions that incorporating in an accepted country does not itself make a merchant eligible if a director or beneficial owner cannot meet identity-country requirements. Therefore, Indonesia being listed is a positive jurisdictional screening result, not a guarantee that CE, any not-yet-selected legal seller, or a particular account will be approved.

Official source: https://docs.dodopayments.com/miscellaneous/accepted-countries-and-territories

### 2.2 Spiritual & Astrology is a review category with a no-claims/no-predictions condition

Dodo's Merchant Acceptance Policy says some types are not outright prohibited but need extra review, and approval is not guaranteed. Under "Categories That Often Require Review" it expressly names:

> Spiritual & Astrology services — Entertainment only; no claims or predictions.

Official source: https://docs.dodopayments.com/miscellaneous/merchant-acceptance

Application to CE:
- CE's epistemic Constitution is unusually explicit: it prohibits fabricated celestial facts, invented interpretations, certainty inflation and false accuracy claims. This alignment with honesty is relevant but is **not equivalent to Dodo approval**.
- CE's defined product also includes TESTABLE SKY SIGNAL and Look Future readings about future possibilities. The fact that CE frames future statements as possibilities rather than guarantees may reduce deception risk, but it does not establish that those statements satisfy Dodo's published "no claims or predictions" condition.
- Dodo's policy separately lists certain spiritual products/services as unsupported when they involve paid spiritual guidance or access to spiritual authority. This provides another classification boundary to clarify, rather than a basis to label CE automatically prohibited or automatically accepted.

Result: **material product-policy fit risk / written category classification required**. Dodo should be given the actual descriptions and sample outputs of Look Today, Look Future and Deep Sky, including the distinction between computed astronomy, interpretive reflection and future-oriented language. No marketing rewrite intended to conceal the service category is acceptable.

### 2.3 Credits: platform feature support does not settle the stored-value prohibition

Dodo advertises credit-based billing, metered usage and customer credits/tokens for digital services. Its Merchant Acceptance Policy also states that Dodo cannot support products involving "stored value" within its financial-products restriction.

Official sources:
- Credit-based billing / usage examples: https://docs.dodopayments.com/guides/login
- Merchant Acceptance Policy: https://docs.dodopayments.com/miscellaneous/merchant-acceptance
- Public pricing / usage-based billing: https://dodopayments.com/id/pricing

CE's design is not a transferable wallet or cash balance. Credits are account-bound, non-expiring units consumed only to open CE's own paid reading; they are not cashable out or transferable to other users or merchants. Nevertheless, they are purchased in advance and held on an account before redemption. Public Dodo docs do not define whether that exact arrangement falls within its "stored value" prohibition or is accepted as first-party service-usage credits.

Result: **unresolved policy classification; written answer required**. Do not infer acceptance solely from Dodo supporting customer credits for API, token or usage billing, and do not infer automatic rejection without Dodo's interpretation of the exact CE structure.

The pre-screen should accurately disclose:
- advance purchase; account binding; non-transferability; no cash-out;
- no expiration under the current CE policy;
- eligible redemption only for CE's own Deep Sky reading service;
- one-time debit behavior, reread entitlement, duplicate-request idempotency;
- cancellation/refund handling and exactly-once credit restoration on proven terminal non-delivery;
- account deletion and unspent-credit treatment, which still require a source-bound consumer-remedy decision.

### 2.4 Digital delivery / billing / public pricing

Dodo generally welcomes digital goods, SaaS and AI products, and provides one-time payment and usage/credit billing capabilities. The public pricing page lists a Standard Plan headline of 4% + 40¢ per transaction; its detailed table also identifies additional payment-method / international-payment pricing. Actual fees, tax treatment, settlement currency, refund/dispute charges and method availability must be confirmed for the approved account and target transaction; headline pricing alone is not a total-cost model.

Sources:
- https://docs.dodopayments.com/guides/login
- https://dodopayments.com/id/pricing

These capabilities are functional fit evidence only. They are not proof that a regulated or restricted product category is eligible.

## 3. Current CE-policy compatibility table

| Dimension | Dodo's published position | CE's current position | Determination |
|---|---|---|---|
| Merchant jurisdiction | Indonesia is listed, subject to identity and onboarding rules | Legal seller/entity not selected | Positive country-list result; account eligibility NOT ESTABLISHED |
| Digital delivery | Digital-first goods and services generally welcomed | Automated digital readings | Generally compatible in delivery form |
| Astrology / spiritual category | Additional review; entertainment only, no claims or predictions | Astrology interpretation; Look Today testable signal and Look Future possibilities | MATERIAL PRODUCT-POLICY FIT RISK; written prescreen required |
| Claims and honesty | No misleading/unverifiable claims; high-risk categories reviewed | CE Constitution prohibits fabricated facts and certainty/accuracy inflation | Values align in honesty, but does not settle the no-predictions condition |
| Purchased Credits | Usage/credit billing supported; stored-value models restricted | Account-bound, non-expiring prepaid service Credits | UNRESOLVED; Dodo must classify the exact design |
| Checkout and fees | MoR, one-time payments, published transaction-based pricing | No provider, market, price, currency or checkout selected | Research only; no implementation authorization |
| Release / governance | No authority is conferred by public product capabilities | Pre-A10 remains gated | No authority effect |

## 4. Required written prescreen — before integration or shortlist elevation

Contact Dodo's published compliance address, `compliance@dodopayments.com`, using a truthful packet containing:
1. Actual product category: astrology-based interpretation of computed celestial inputs, with example Look Today, Look Future and Deep Sky wording—not only a generic SaaS description.
2. The explicit CE limitations: no scientifically-proven-astrology claims, no guarantees, no invented astronomical facts, no certainty claims; also explicitly disclose the existence and purpose of future-oriented/testable readings rather than asserting there are no predictions.
3. The full Credits mechanics described in §2.3, including non-expiry, account binding, exclusive service redemption, refund/non-delivery treatment and unspent balance on account deletion.
4. The genuine intended seller entity and its identity/incorporation/beneficial-owner countries, when determined; planned customer countries and payment/settlement currencies, when determined.
5. A request for a written determination of (a) whether the current product category and sample outputs are eligible under the Spiritual & Astrology policy, specifically the no-claims/no-predictions limitation; (b) whether prepaid non-transferable service-usage Credits with the stated mechanics fall within the stored-value prohibition; (c) any required restrictions, disclosures, licences, settlement limitations, fee schedule, refunds and monitoring.

Ask for the policy sections and conditions supporting the decision. Keep the provider's written answer as dated evidence. This addendum records no contact sent and no provider response; the request remains a recommended next step, not a completed action.

## 5. Recommendation and boundary

- Do **not** choose Dodo as CE's payment provider yet.
- Do **not** implement Dodo checkout or bind its SDK into production while product-category and Credits eligibility remain unresolved.
- Do not change CE's product integrity or future-reading semantics merely to fit Dodo. If the written eligibility requires changes to CE's core product, return that conflict to the CE product/governance process instead of quietly changing product claims.
- Dodo may be considered further only if it explicitly confirms in writing that the exact disclosed CE experience and Credits model can be supported under its policies, without requiring an impermissible compromise of CE's Constitution.
- If the answer is adverse or materially ambiguous, retain Dodo as not suitable for the present V1 model and continue research across other providers.

This determination is based on publicly available official policy and documentation checked on 2026-10-11. It is not a provider approval, legal conclusion, account eligibility decision, or guarantee of continued policy terms.

End of R0.
