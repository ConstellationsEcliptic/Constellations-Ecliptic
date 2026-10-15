# CONSTELLATIONS ECLIPTIC
# PRE-A10 D4 — PAYMENT PROVIDER ELIGIBILITY SNAPSHOT R1

**Checked:** 2026-10-10  
**Classification:** OFFICIAL-POLICY SOURCE SNAPSHOT / DECISION SUPPORT / NON-AUTHORITATIVE  
**Authority effect:** NONE  
**Provider selection:** NONE  
**Seller-entity / market / currency / checkout decision:** NONE  
**Legal advice:** NONE  
**Implementation / production / SEAL effect:** NONE

## 1. Purpose and order of decision

This update records a fresh check of payment-provider policy pages published by the providers themselves. It does not decide where CE should be incorporated or which markets to serve.

The correct order remains:

1. Identify the **actual legal seller entity and jurisdiction** (or the genuine intended entity-formation path).
2. Determine whether that entity can onboard with a candidate processor or Merchant of Record (MoR), including exact product-category acceptance.
3. Select permitted customer markets and fulfillment geography only within that eligibility.
4. Choose base currency, additional localized display currencies, payment methods and locale.
5. Reconcile disclosures, tax/consumer rights, credits/debit/entitlement semantics and refund/chargeback handling with the selected commercial/legal model.

Do not reverse this order by selecting a country or USD checkout first and then assuming an account can be opened there. A Stripe account in another country requires genuine local eligibility/identity/business arrangements as described by Stripe; a chosen provider cannot substitute for the seller entity.

## 2. Current official evidence

### 2.1 Stripe — Indonesia account

**Checked 2026-10-10.** Stripe's own Indonesia support page currently states that the Indonesia program is invite-only. It also says that Indonesia Stripe accounts can only accept IDR and pay merchants in IDR, that cross-border/international transactions are not supported for accounts based in Indonesia, and that the currently supported payment-method set is limited (the current page lists Indonesia bank transfer/virtual account and dashboard-created transactions).

Sources:
- Requirements to open an account in Indonesia: https://support.stripe.com/questions/requirements-to-open-a-stripe-account-in-indonesia?locale=en-GB
- Supported methods/currencies/businesses for Indonesian accounts: https://support.stripe.com/questions/supported-payment-methods-currencies-and-businesses-for-stripe-accounts-in-indonesia?locale=en-GB
- Global availability: https://stripe.com/global

**Implication:** an Indonesian Stripe account cannot be assumed available for immediate onboarding or suitable for a global V1 buyer market with international card processing. Do not conclude that Indonesia must be the seller jurisdiction from the founder's physical location alone; that is a separate legal/business decision.

### 2.2 Stripe — other-country account

Stripe's current support policy says a seller opening an account in a country other than its primary business country needs a legal entity, tax ID, physical location, phone number, government-issued ID, working website and physical bank account in the relevant country (with stated exceptions). Stripe must support payment processing in that jurisdiction.

Source: https://support.stripe.com/questions/requirements-to-open-a-stripe-account-in-another-country?locale=en-GB

**Implication:** no US-first, USD-first or foreign-account plan may assume eligibility based on an online incorporation offer, a mailing address, or a nominal account location. The exact real entity and arrangements must be evaluated, including tax/legal obligations and provider approval.

### 2.3 Stripe — CE Credits and product classification

Stripe's current prohibited/restricted-business page says seller-maintained stored value/credits may be subject to limits and separately lists preloaded cards, gift cards and virtual credits/stored-value products among restricted categories. This means the actual CE Credits design must be described accurately to Stripe: source/issuer, holder, transferability, redemption scope, refund behavior, monetary representation and whether Credits can be used only to buy CE's own service.

Sources:
- Prohibited and Restricted Businesses (page shows last update 2026-09-22 on the retrieved current copy): https://stripe.com/legal/restricted-businesses?tp=1
- Restricted-business FAQ: https://support.stripe.com/questions/prohibited-and-restricted-business-list-faqs?locale=en-GB

Do **not** conclude that CE Credits are automatically allowed or automatically prohibited based only on a category label. Obtain provider classification and approval for the exact product flow before selecting Stripe as the production provider.

### 2.4 Paddle — direct policy conflict for this product model

Paddle's published Acceptable Use Policy, last updated **13 April 2026** on the page retrieved 2026-10-10, explicitly lists among prohibited categories:
- digital services associated with pseudoscience, including horoscopes/fortune-telling; and
- virtual currency or stored value, including store credit, gift cards and vouchers.

Source: https://www.paddle.com/help/start/intro-to-paddle/what-am-i-not-allowed-to-sell-on-paddle

CE's current intended product includes personal astrology readings and an account-held Credits mechanism. Those features appear to intersect two expressly listed prohibited categories. Based on the public policy presently available, **do not shortlist Paddle as an eligible V1 MoR for this product without an explicit written provider determination that the exact described CE offering is eligible**. This is a policy-suitability finding, not a claim that the product is unlawful.

## 3. What the evidence does and does not establish

| Proposition | Current status |
|---|---|
| Stripe Indonesia is currently invite-only | VERIFIED from official Stripe page checked 2026-10-10 |
| Stripe Indonesia accounts currently accept/pay in IDR only and do not support international/cross-border transactions | VERIFIED from official Stripe page checked 2026-10-10 |
| A different-country Stripe account requires real country-specific business and banking/identity arrangements | VERIFIED from official Stripe guidance; eligibility remains entity-specific |
| CE Credits classification is accepted by Stripe | **NOT ESTABLISHED**; exact flow needs prior provider review/approval |
| Paddle is a supported provider for CE V1 | **NOT ESTABLISHED; current public AUP appears to conflict with astrology/horoscope content and stored-value Credits** |
| U.S. entity or market is the best choice | **NOT ESTABLISHED**; not inferable from Stripe availability alone |
| USD is the correct base currency | **NOT ESTABLISHED** |
| Indonesia is the initial paid market | **NOT ESTABLISHED** |
| A specific other processor is suitable | **NOT ESTABLISHED** until product-category, seller-entity, market, settlement, refund and credit-ledger flow are verified |

Provider pages can change. Recheck the official page and obtain provider confirmation at the point of actual onboarding; preserve dated snapshots and responses relevant to the final product description.

## 4. Minimum provider-review packet for CE

Before a provider is selected, prepare a single accurate packet that answers:

1. What is the real legal seller entity, its jurisdiction, owners, tax registration, operating location and settlement bank?
2. Is CE primarily selling software access, a digital service, personal horoscope/astrology readings, or a combination under the provider's categories? Describe product behavior truthfully; do not disguise astrology as generic software.
3. Are Credits nontransferable, noncash, account-bound and redeemable only for CE's own digital service? What does the customer buy at top-up, what event debits Credits, and what remedies exist when fulfillment fails?
4. Which customer countries can lawfully and contractually be served? Which are excluded?
5. What are the permitted checkout/payment methods, presentment/settlement currencies, chargeback/refund paths, local tax responsibilities, and data/subprocessor terms?
6. Is explicit written prior approval required? Does the approval cover both the personal-reading service and the specific Credits/entitlement flow?

Record the submitted product description, provider response, date, service/merchant account type, scope of approval and any exclusions. A generic sales conversation is not proof that the actual Credits flow was approved.

## 5. Protected owner discussion later

A material owner choice remains: **the intended legal seller-entity jurisdiction and whether the plan is to serve Indonesian buyers first, an explicitly bounded other market, or multiple markets from a genuinely eligible entity**. That choice affects legal/tax advice, provider eligibility, currency and user-facing pricing. It should not be decided by the assistant or inferred from account location.

No immediate decision is required merely to complete this evidence snapshot. When the entity options and trade-offs are ready, present a short evidence-backed choice set for the owner and, where appropriate, qualified local counsel. If the current entity/jurisdiction is not yet established, say so rather than selecting a provider prematurely.

## 6. Next admissible work

- Continue source-bound comparison of alternative providers only after defining the genuine seller-entity scenario, so comparisons are apples-to-apples.
- Include provider confirmation of the exact astrology + stored-Credits use case, not only pricing or advertised country support.
- Preserve CE's existing no-manipulation, clear pricing, idempotency, fulfillment, dispute, deletion and mandatory consumer-rights boundaries.
- Do not change payment integration, Credits ledger semantics, market configuration, live checkout, account credentials or production settings as a result of this snapshot.

---

End of R1.
