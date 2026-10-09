# CE ZERO-POINT AREA D4 — LOCALE, CURRENCY AND MARKET ASSUMPTIONS
Date: 2026-10-09
Classification: SOURCE RECONCILIATION / RECOMMENDATION / WORKING CANDIDATE / NON-AUTHORITATIVE
Status: RECOMMENDATION_READY
Authority effect: NONE
Normative amendment: NONE
Market / checkout authorization: NONE

## 1. Conclusion

An English-only or en-US-only product policy, a USD-only pricing policy, and a formal U.S.-first paid-launch decision are NOT ESTABLISHED in the inspected current decision/scope records. Do not infer them from the language of CE specifications, an illustrative USD price, or the owner's internal U.S. legal-policy baseline.

## 2. Owner decisions and registers

### U.S. legal-policy baseline — limited scope
Owner Disposition (Box 2515620798775) directs use of U.S. federal law and relevant U.S. state/territorial law as the internal legal-policy baseline. It specifically says CE need not prominently declare itself designed exclusively for the U.S. and does not establish a U.S.-exclusive target market, governing law for every transaction, nationwide paid checkout, state allowlist, currency or launch-market list.

### Initial market and locale/currency remain explicit decision items
The Zero-Point Human Decision Register R0 (Box 2514894635417), a non-authoritative working draft, tracks:
- DR-04 initial jurisdiction: NOT_RECORDED;
- DR-05 locale: NOT_RECORDED; recommended default is one initial launch locale chosen after the initial jurisdiction;
- DR-06 currency/price: NOT_RECORDED; the US$2.99 / 4 Credits example remains illustrative until approved;
- the register itself explicitly notes Share Card is already closed outside the register and does not reopen it.

Because the register is explicitly a working draft, its NOT_RECORDED fields are evidence of the present planning gap—not a normative amendment or proof that no disposition exists in every possible source. The U.S. legal baseline is a separate owner disposition and must not be overextended to resolve DR-04–DR-06.

## 3. Normative commercial/product facts

Business Model Minimal V1 v1.5 (Box 2485331476456) provides a configurable example of 4 Credits = US$2.99 and 4 Credits per Deep Sky reading. It expressly treats the monetary value as a configurable commercial parameter, not a calculation or Canon rule. That example cannot be used to infer USD-only prices, an approved launch market or the final legal denomination/classification of Credits.

Product/Privacy/Account specs include language/copy and jurisdiction-specific feature gates but do not, within the inspected characterized source set, establish English-only/en-US-only, USD-only, or a U.S.-exclusive public-positioning requirement. Technical calendar policy (e.g. Gregorian-only) is a separate calculation input boundary and does not determine UI language, pricing currency, or market strategy.

## 4. Recommendation

**Keep locale, currency and launch market as independent decisions, ordered by dependency—not assumed from each other.**

1. First choose and document the intended initial paid-enabled jurisdiction/market through a genuine owner decision after feasibility analysis. The U.S. internal research baseline can inform that analysis but does not itself select U.S. as the launch market.
2. For that intended scope, identify the laws/control requirements and the selected seller, provider/MoR, payment methods and actual SKU/credits configuration. Paid checkout must remain closed until a readiness disposition exists for the selected configuration.
3. Choose a single initial product locale for the launch scope if simplicity is desired, then explicitly record the locale; do not silently convert the document language into an English-only promise or infer en-US copy from USD pricing.
4. Choose currency, package pricing and Credits denomination as explicit commercial configuration; verify conversion/denomination presentation and applicable disclosures rather than treating the sample 4 Credits / US$2.99 as binding.
5. Keep region-specific age assurance, privacy and legal requirements under the existing regional feature gate. Do not claim that one internal legal baseline creates global compliance or eliminates mandatory non-U.S. requirements that could apply based on transaction facts.

This is an area where a focused owner decision will eventually be required to select actual launch market, initial locale and currency/price. No decision is needed now just to preserve the correct classification and continue the other Zero-Point reviews.

## 5. Status and non-actions

- English-only / en-US-only policy: NOT ESTABLISHED in inspected source set.
- USD-only policy: NOT ESTABLISHED.
- U.S.-first or nationwide paid launch: NOT ESTABLISHED; owner U.S. baseline is internal guidance, not a launch decision.
- One initial locale after jurisdiction selection: RECOMMENDATION, not approved policy.
- US$2.99 / 4 Credits: illustrative/configurable parameter only.
- Code, checkout, pricing, locale, normative documents and Test Register: unchanged.
- Tests executed: NONE.
- A10, Runtime Adoption, production/deployment and SEAL: unaffected.

## 6. Evidence

- Owner Disposition — U.S. Legal Framework as Internal Policy Baseline: https://app.box.com/file/2515620798775
- Zero-Point Human Decision Register R0 (DR-04, DR-05, DR-06): https://app.box.com/file/2514894635417
- Business Model Minimal V1 v1.5: https://app.box.com/file/2485331476456
- Product Constitution v1.6.1: https://app.box.com/file/2491704535193
- Paid Checkout Readiness Matrix R0: https://app.box.com/file/2515715498189
- Source-Bound Matrix R0: https://app.box.com/file/2515023681086

End of D4 review.