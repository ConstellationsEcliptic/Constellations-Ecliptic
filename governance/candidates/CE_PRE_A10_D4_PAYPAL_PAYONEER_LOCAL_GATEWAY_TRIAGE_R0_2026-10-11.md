# CONSTELLATIONS ECLIPTIC
# PRE-A10 D4 — PAYPAL / PAYONEER / INDONESIAN GATEWAY TRIAGE R0

Checked: 2026-10-11
Classification: OFFICIAL-POLICY RESEARCH / NON-AUTHORITATIVE / CANDIDATE ONLY
Authority effect: NONE
Provider selection: NONE
Seller entity, launch market, currency, pricing or checkout decision: NONE
Normative / production / A10 / SEAL effect: NONE

## 1. Executive summary

No examined provider is yet confirmed eligible for the exact CE V1 offer. Current ranking is for the next *written prescreen only*, not provider selection:

1. **Xendit and Midtrans — run a truthful category prescreen in parallel** before spending on SDK integration or entity formation. Their results differ: Xendit's publicly indexed general restricted list does not explicitly name astrology, but its list and terms are non-exhaustive and eligibility is not established; Midtrans explicitly excludes materially misleading content and gives examples including products claiming supernatural knowledge / mystical services. CE's integrity constraints matter but do not automatically satisfy either provider.
2. **PayPal — do not assume availability for CE.** The Indonesia-specific PayPal Alternative Payment Methods Terms expressly list "psychic or fortune-teller services" as a prohibited merchant category for APM functionality. Because CE sells astrology-based personal interpretation and includes testable/future-oriented readings, this creates a direct material policy conflict for APM functionality. The public evidence inspected does not prove that every possible PayPal account-to-account-only path is governed identically, so that separate configuration must be classified in writing rather than presented as approved. Credits handling also needs a specific determination.
3. **Payoneer Checkout — not practical under the current CE situation.** The official page says its Checkout is provided by Stripe and/or affiliates exclusively to US and Hong Kong entities; the lead-form eligibility note requires or expects a Hong Kong entity and monthly webstore volume above US$20,000. CE has not selected a real seller jurisdiction, entity, or market and has no established sales volume. Payoneer receiving accounts/payment requests for business receipts are not the same thing as an eligible consumer checkout for CE microtransactions.

No contact has been sent to any provider. No new provider is selected or approved.

## 2. PayPal (Indonesia)

### 2.1 APM feature has a direct published astrology/fortune-telling conflict

Official Indonesia-specific source:
https://payflowlink-edgemigration.payflow.edge.paypal.com/id/legalhub/paypal/apm-tnc?country.x=ID&locale.x=en_ID

The PayPal Alternative Payment Methods Terms say they apply when APM functionality is integrated into an online checkout or an invoice/payment request so customers can use an alternative payment method. The listed prohibited categories include **"Psychic or fortune-teller services."** These terms supplement the PayPal User Agreement and applicable Acceptable Use Policy for the seller's country.

CE is an astrology-based personal interpretation product. Its future-oriented testable reading and Look Future product increase the chance of provider classification into that category. Do not assume that CE's truthfulness boundary automatically makes it exempt from the category restriction. For any flow that uses PayPal APM functionality (including the scope described by those terms), classify it as **NOT SUITABLE / DIRECT PUBLISHED POLICY CONFLICT unless PayPal itself provides a valid written determination or exception under the applicable contract**. Do not integrate that flow pending resolution.

### 2.2 Standard PayPal wallet path remains unclassified, not approved

PayPal Indonesia markets Business services for receiving payments internationally:
https://www.paypal.com/id/business?locale.x=en_ID

Its general Acceptable Use Policy describes prohibited activity and lists categories requiring approval, including payment services / e-money and stored-value cards:
https://www.paypal.com/id/legalhub/acceptableuse-full

The reviewed general AUP does not, in the text retrieved here, itself establish an across-the-board ban on every ordinary PayPal wallet payment for all astrology-related products. That does not negate the APM-specific restriction. Exact applicability depends on which PayPal product, integration methods and customer payment paths CE would actually use.

**Determination:** a conventional PayPal Business account/wallet-only checkout cannot be called approved from the evidence currently reviewed. Send PayPal Sales/Compliance the exact CE offer and ask them to distinguish (a) wallet-only PayPal account payments, (b) guest/card payment options and every APM method, and (c) invoicing/payment requests. Require an explicit statement about whether the Indonesia APM prohibition applies to the proposed integration.

### 2.3 CE Credits remain a separate classification question

The general PayPal AUP's approval-required list mentions selling stored-value cards and escrow services under payment-facilitator category, and regulated digital value can trigger additional terms. CE Credits are intended to be first-party account-bound, non-transferable, non-expiring units redeemable only for CE's own Deep Sky reading, with no cash-out. Public sources reviewed do not conclusively decide whether that model is treated as a stored-value product in PayPal's relevant Indonesian product agreement.

Include the exact Credits mechanics in the provider question. Never describe the model as having no prepaid balance or as something other than it is. Even if PayPal accepts a wallet-only payment for one-off reading, that does not automatically authorize prepaid Credits or APM.

Official sources:
- https://www.paypal.com/id/legalhub/acceptableuse-full
- https://www.paypal.com/id/legalhub/paypal/apm-tnc?country.x=ID&locale.x=en_ID
- https://www.paypal.com/id/business?locale.x=en_ID

## 3. Payoneer Checkout

Official page:
https://www.payoneer.com/checkout/

The page describes Checkout as a Stripe-powered gateway and states in its eligibility disclaimer that the service is provided by Stripe Inc. and/or affiliates exclusively to **US and Hong Kong entities**. The registration form notes eligibility requires having or being willing to set up a **Hong Kong entity** and monthly webstore volume above **US$20,000**.

CE has no approved seller entity/jurisdiction or launch market, and there is no documented monthly webstore volume close to that requirement. Creating an overseas entity just to qualify would contradict the current minimal-spend posture and would introduce real legal, banking, accounting, tax and ongoing maintenance obligations that have not been approved.

**Determination:** Payoneer Checkout = **NOT A PRACTICAL CURRENT CANDIDATE**. Do not form a Hong Kong entity or incur setup costs for this purpose. A regular Payoneer receiving account or payment request may serve certain business-to-business / marketplace receipts, but must not be represented as equivalent to a general-purpose consumer website checkout for CE microtransactions. No such alternative has been validated for this exact product.

## 4. Indonesian gateways worth written prescreening

### 4.1 Xendit

Official sources:
- Prohibited-business summary (updated 15 December 2025): https://help.xendit.co/hc/en-us/articles/360035083951-Are-there-any-businesses-that-Xendit-prohibits
- Xendit Indonesia terms, Section 11 (restricted businesses; examples are representative, not exhaustive): https://www.xendit.co/en/terms-and-conditions/
- Registered merchant documentation (updated 26 February 2026): https://help.xendit.co/hc/en-us/articles/10891368765593-ID-What-are-the-legal-documents-required-to-register-to-Xendit-for-Indonesian-Merchants
- Individual-business requirement (current help page): https://help.xendit.co/hc/en-us/articles/360035083911-Can-Individual-businesses-use-Xendit-s-services

Xendit's public summaries do not explicitly name astrology in the pages reviewed, but absence from a summary is not proof of eligibility. Section 11 states restricted categories may be representative/non-exhaustive and directs uncertain businesses to contact the provider. Xendit states it does not currently accommodate an unregistered individual business and requires a recognized legal business/entity plus documents; additional licensing documents may be requested based on industry.

**Determination:** a good candidate for a *preliminary written product classification only*, before incorporation or integration. Ask whether CE's described astrology service and prepaid first-party Credits are eligible, and exactly which seller registration type/documents and customer markets are required. Do not pay for incorporation or integrate before receiving an answer and separately deciding whether the entity cost is justified.

### 4.2 Midtrans

Official source:
https://docs.midtrans.com/docs/can-all-types-of-businesses-accept-payments-through-midtrans

Midtrans says it cannot work with goods/services containing materially dishonest, deceptive or misleading content, and gives examples including mystical/supernatural objects and products claiming supernatural knowledge. Its terms also say requirements differ by business type and payment method and directs merchants to contact it for review.

CE's prohibition on fabricated facts, fake certainty, guaranteed outcomes and claims of proven astrological truth is an important integrity control; it does **not** prove Midtrans will classify CE as eligible. The actual product remains astrology-related and contains future-oriented readings.

**Determination:** MATERIAL CATEGORY RISK / WRITTEN PRESCREEN REQUIRED. Supply the actual product description, representative output samples, disclaimers, exact Credits flow and claim boundaries. Ask for written category determination before account application or technical integration is treated as viable.

## 5. Recommended low-cost next step

Because CE has not selected a seller entity or a launch market, do not open provider accounts, form an overseas entity, buy a checkout add-on, or integrate an SDK yet.

Conduct *only written policy prescreening* in parallel:
- Xendit: exact astrology category + prepaid first-party Credits + registration/entity requirements.
- Midtrans: whether CE's qualified astrology interpretations are considered prohibited supernatural-knowledge/fortune-telling services and how Credits are classified.
- PayPal: only if PayPal remains commercially relevant, request a written distinction between wallet-only PayPal payments and the Indonesia-specific prohibited APM flow. Treat APM as blocked unless applicable contract language is validly resolved by PayPal.
- Payoneer Checkout: drop from near-term shortlist due to its published US/Hong Kong entity and >US$20,000/month requirement.

The prescreen message should disclose what CE actually sells: astrology-based interpretation based on computed celestial inputs; Look Today has a testable sky signal when qualified; Look Future describes possibilities; no claim of scientific proof or guaranteed accuracy; prepaid account-bound non-expiring Credits are used only for CE's own paid reading and cannot be transferred or cashed out. Ask for policy-section references, allowed/blocked checkout paths, geography, currency, entity requirements and written approval/limitations.

## 6. Decision boundary

Current ranking is research priority only:
- **Xendit — prescreen candidate; eligibility unestablished.**
- **Midtrans — prescreen candidate with explicit content-classification risk.**
- **PayPal APM — direct published category conflict; do not assume it can be used. PayPal wallet-only path remains unclassified.**
- **Payoneer Checkout — not practical at CE's current stage and volume.**

No provider, seller entity, market, locale, currency, pricing, SKU, checkout or consumer-remedy rule is selected. No messages have been sent. This artifact changes no normative source, official Test Register, production code, schema, runtime, A10, Source Authority, Trusted Build, release or SEAL state.

End of R0.
