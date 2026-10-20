# CE V1 — Trust, First-Contact Value, Credits Conversion & Controlled Evolution Standard R0

**Date:** 2026-10-20  
**Classification:** WORKING CANDIDATE / NON-NORMATIVE / RELEASE-READINESS PROPOSAL  
**Purpose:** Turn the owner's direction into one integrated, evidence-based product standard for CE V1.  
**Authority effect:** NONE. This file does not amend CE's Constitution, Calculation Constitution, Signal Engine, Interpretive Canon, Evidence/AI rules, Commercial or Privacy specifications, official Test Register, Area Register, or any source-authority/runtime/production gate. It does not authorize implementation, merge, A10, deployment, payment processing, or launch.

## 1. Product outcome

CE V1 should be compelling to discover, clear to understand, trustworthy in its claims, worthwhile to pay for, reliable after payment, and stable as the product evolves.

The intended commercial path is:

**Attraction → understanding → trust → perceived value → informed Credits purchase → fulfilled reading → satisfaction → voluntary repeat purchase.**

This is a product-design hypothesis and measurement framework, not a claim that any particular conversion or retention outcome has already been proven.

No conversion gain can justify fabricated astronomical facts, unsupported personalisation, exaggerated certainty, misleading visual context, fake urgency/social proof, hidden costs, coerced purchases, or a reading that is not supported by CE's authorized inputs and rules.

## 2. Non-negotiable invariants

1. **Epistemic integrity:** CE never makes the user believe CE knows more than it actually knows. Missing, unstable, invalid, or unauthorized inputs/rules must result in a truthful limitation or omission—not invented output.
2. **Signal / interpretation / editorial boundary:** A computed TESTABLE SKY SIGNAL must be distinguishable from its authorized interpretation and from general editorial reflection. Only the eligible signal is used for Tomorrow Check. Editorial content must never disguise a failed, incomplete, or non-VALID observation.
3. **Stable consumer promise:** Improvements may refine the product, but must not silently change the meaning, evidence basis, price/entitlement terms, privacy promise, or expected paid deliverable. Material changes require controlled review, versioning, and user-facing explanation where relevant.
4. **Honest commercial exchange:** Before purchase, users can understand the Credit package, price, the Credits required for the intended reading, and material delivery/expiry/refund/remedy terms. CE does not rely on confusion or pressure to close a sale.
5. **Minimal data:** Conversion analysis must not use birth data, reading content, or personal-context material as ordinary analytics dimensions. Collect only events necessary for documented product/commercial purposes under the approved privacy design.
6. **Fail closed:** UI copy, a marketing state, or a payment success state cannot convert a failed calculation, unqualified result, unavailable Canon rule, or failed delivery into a valid reading.
7. **Independent release evidence:** A change cannot self-certify merely because CE or the same process that generated it says it is safe. Exact inputs, candidate identity, relevant test results, source authority, and release approvals must be independently checkable.

## 3. First-contact acceptance

A prospective customer should not need to read a technical specification to understand the product's essential promise. The first-contact experience should deliver all three outcomes below.

### 3.1 Attraction

- A distinctive, polished, coherent celestial identity and clear hierarchy.
- A concise explanation of what each core experience offers: Look Back, Look Today, and Look Future.
- A clear route to explore the experience before a purchase decision.
- No fabricated celestial event, pseudo-personal sample, fake testimonial, fake user count, countdown, scarcity claim, or claim of certainty.

### 3.2 Comprehension and trust

- Users can distinguish calculation-based signal from interpretation and general reflection.
- Samples are clearly labelled as illustrative unless they are genuine readings computed from valid, authorized inputs.
- Product and marketing copy do not imply guaranteed outcomes, scientific validation of astrology, or predictive accuracy CE has not established.
- Important limitations are visible at the point where they matter. A disclaimer is not treated as a repair for an overall misleading impression.
- Account, recovery, privacy, and personal-data expectations are clear before the user commits sensitive information.

### 3.3 Minimum comprehension check

Use a small, focused first-contact check as part of release QA—not an open-ended market-research programme.

- Use representative first-contact screens and the actual proposed language for the initial target market.
- Ask participants, without prompting, what CE offers, what generated a displayed result, and what CE does not claim.
- Include at least one eligible signal-present example and one valid QUIET_SKY state. Any illustrative/simulated example must be labelled as such.
- Record misunderstandings and fix critical ones before release. In particular, a user must not reasonably be led to treat general editorial Note content as derived from their personal signal, or possibility language as a guarantee.
- Set any quantitative acceptance threshold in the test plan before the check. Do not present a small qualitative sample as statistically representative of the U.S. market, or use it as evidence that astrology is accurate.
- Re-check the changed screen after remediation. A critical misunderstanding remaining unresolved is a release blocker.

## 4. Credits purchase and value acceptance

Credits are the primary monetization model. The experience must help customers make an informed decision and must fulfil what they paid for.

### Before checkout

- State the USD price of each available package and the exact Credits supplied.
- Show the Credit cost of the intended reading before the user confirms purchase or spends Credits.
- Explain the deliverable in plain language; do not sell a reading whose essential content depends on data/rules CE does not have.
- Clearly disclose material purchase, expiry, refund/remedy, and delivery conditions according to the approved commercial policy and applicable law.
- Make one-time purchase versus recurring payment unambiguous. Do not preselect unwanted add-ons or use obstructive cancellation/checkout patterns.
- Show no unsupported claims such as “most accurate,” “proven,” “guaranteed,” or fabricated customer popularity.
- Keep the free/preview experience honest and useful; do not intentionally degrade or misrepresent it just to create pressure to pay.

### At purchase and fulfilment

- Payment, Credit balance, entitlement, reading issuance, and delivery states must be consistent and auditable.
- Follow existing owner-approved commercial semantics; do not reopen or alter them through this candidate document. In particular, preserve the existing D1-A effective-purchase decision, D2-B terminal non-delivery remedy with exactly-once reading-Credit restoration, UTC Gregorian service-day boundary, and fulfillment-health interlock.
- On timeout, duplicate callback, partial failure, or terminal non-delivery, do not double-charge, double-issue, or leave the user without the established remedy. Test retries and idempotency.
- Never fabricate a reading to conceal fulfillment failure. Do not consume a paid entitlement for a deliverable that was not successfully issued under the approved rule.
- Receipts, current balance, purchase history, and support/remedy routes should be clear.

### After fulfilment

- The delivered experience must match the description seen before payment.
- A user should be able to tell what was calculated, what is interpretation, and what is uncertain.
- Observe complaints, abandoned checkouts, refunds/remedies, fulfilment failures, and voluntary repeat purchase as product-quality evidence. Do not label repeat purchase as proof of predictive accuracy or causal efficacy.

## 5. Stable core and controlled upgrades

The product should improve continuously without making consumers feel that its promise changes on every release.

### Change classes

- **Class 1 — low semantic risk:** rendering polish, accessibility, performance, or ordinary bugs that do not change calculations, interpretation, prices, entitlement, privacy promises, or historical results. Still require relevant automated/regression tests.
- **Class 2 — material user/commerce change:** navigation/first-contact meaning, Credit prices or package terms, account/recovery, data processing, fulfilment behaviour, or changes to user-facing interpretation display. Require impact assessment, targeted regression and comprehension testing where relevant, updated version/changelog, and appropriate owner approval.
- **Class 3 — core meaning/security/authority change:** calculation algorithm, celestial source/data, signal qualification, Canon meaning, evidence/AI permissions, privacy/security boundary, official Test Register, source authority, runtime or release gate. Require the applicable formal controlled process and independent verification. These changes cannot be promoted solely by self-upgrade automation.

### Historical reproducibility and rollback

- Preserve the reading's profile version and applicable calculation, signal, Canon, template/content, and software/rule identities needed to explain how it was produced.
- Do not silently rewrite a historical reading using newer rules. A corrected reading must be separately identified and explained under approved policy.
- Each release needs a unique identity, change record, evidence trail, monitoring, and tested rollback/recovery procedure.
- Self-upgrade automation may prepare and test a candidate; it must not redefine its own acceptance rules, manufacture missing authority, or promote a failed/unauthorized candidate.

## 6. U.S.-first legal and payments gate

This section is a release-planning checklist, not legal advice or nationwide clearance.

- Review actual claims and the overall first-contact impression under applicable U.S. federal and relevant state consumer-protection rules. Explicit wording, layout, context, omissions, and implied claims all matter; a disclaimer alone may not cure a misleading design.
- Claims about accuracy, efficacy, user outcomes, popularity, personalization, or business performance must not be published without an appropriate basis.
- Determine the contracting seller, eligible customer geography/state allowlist, tax/consumer terms, dispute/refund obligations, and privacy obligations before offering paid service in that geography.
- Obtain written processor/acquirer approval for the exact product: astrology-related readings, forward-looking language, prepaid Credits/stored-value mechanics, refund/restoration flow, seller jurisdiction, and target customer geography. A provider's marketing page is not written approval of CE's offer.
- The current D4 payment-provider/seller route remains unresolved in the reviewed candidate state. Do not enable paid Credits until the exact route is approved and end-to-end transaction/fulfilment/remedy tests pass.
- Keep the initial market, USD customer-facing pricing intent, and the seller's legal jurisdiction conceptually separate; U.S. customer targeting alone does not prove a U.S. seller entity or nationwide availability.

## 7. Minimal trustworthy measurement

Measure the funnel without turning user data into a hidden personality profile.

Recommended aggregate/pseudonymous events, subject to the approved privacy design:
- first-contact visit and sample opened;
- start and completion of core experience;
- Credit package/pricing view;
- checkout started, succeeded, cancelled, or failed;
- Credits spent on a reading;
- reading fulfilled, terminally failed, or remedied;
- support/refund/remedy reason category;
- voluntary repeat purchase within a stated cohort window.

Exclude birth date/city, raw reading text, relationship details, or inferred traits from ordinary conversion analytics. Define purpose, access, retention, and deletion before instrumentation.

Review conversion together with comprehension, fulfilment reliability, complaints, refund/remedy rates, and repeat purchase. Do not optimise purchase conversion as a single isolated number. A conversion increase accompanied by increased misunderstanding, complaints, failed delivery, or coerced behaviour is a regression, not a success.

No market lift, retention, or willingness-to-pay finding is established by this document. Establish baselines from actual, appropriately obtained data when the product is ready to be used; report sample sizes and uncertainty honestly.

## 8. Proposed launch gates — all critical gates are conjunctive

A positive result in one area cannot compensate for a critical failure in another.

| Gate | Required evidence | Release-blocking examples |
|---|---|---|
| G1 — Source and rule integrity | Authorized exact source/rule identity; reproducible calculation; valid signal and Canon binding; independent verification | Missing rule/source, mismatched geometry, invented signal/meaning |
| G2 — Product boundary | All valid and non-VALID states mapped and tested; no failure disguised by UI | Failed observation shown as Quiet Sky or completed reading |
| G3 — First-contact trust | Actual launch claims reviewed; samples truth-labelled; comprehension check completed; critical misunderstandings remediated | Users reasonably infer guarantees, fake personalization, or unsupported accuracy |
| G4 — Paid value | SKU/package and per-reading Credit cost visible before commitment; deliverable matches promise | Unclear cost, misleading deliverable, pressure pattern |
| G5 — Commerce reliability | Purchase/entitlement/issuance/refund-restoration idempotency and failure paths pass end-to-end tests | Duplicate debit/credit, unresolved non-delivery, fabricated fulfilment |
| G6 — Security and privacy | Relevant account, recovery, data lifecycle, access control, incident and deletion paths verified | Unauthorized access, unclear data lifecycle, unapproved tracking |
| G7 — Legal and processor fit | Seller/market terms reviewed; relevant legal review; written exact-product payment acceptance | Unapproved processor, unreviewed target-state/legal route |
| G8 — Release and evolution | Exact build identity, full required test suite, independent gate evidence, change classification, monitoring and rollback | Untrusted runtime/source identity, missing tests, inability to recover |
| G9 — Customer value evidence | Core task can be completed and understood; no unresolved critical comprehension defect; initial metrics defined | First contact attracts by misleading users or paid value cannot be articulated |

### Gate interpretation

- **PASS:** sufficient evidence exists for that specific gate and exact candidate identity.
- **BLOCKED:** evidence is missing, conflicted, or fails; this is not waived by strong performance elsewhere.
- **NOT APPLICABLE:** allowed only with a documented, scope-consistent rationale—not as a way to hide a dependency.
- A gate result applies only to the exact build and scope examined. A later material change invalidates affected evidence and requires targeted revalidation.
- This table is a proposed candidate standard, not an active formal release gate until adopted through the applicable governance route.

## 9. Current known state and next work

As of the reviewed 2026-10-20 continuity state:

- Pre-A10 candidate PR #27 remains open/draft/not merged. Its last recorded exact candidate head was 4309a5e40dc7d3ee4e27233441104f346f65b481.
- The strict Pre-A10 gate was recorded as 20/23 areas complete with A3, B1 and D4 incomplete. Validator unit tests and R0–R3 Area Register structural checks passed; the strict gate remained blocked by design.
- A3 signal-present Today's Note scope remains unresolved as a formal owner disposition. Product recommendation for V1: do not expand Note to signal-present results by default. This candidate recommendation does not itself record an owner decision. Keep the existing limited valid-QUIET_SKY permission bounded by its pre-existing content/eligibility conditions; no eligible approved content means OMIT_NOTE.
- B1 still requires an approved current Canon/rule registry and independent semantic verification; candidate geometry tests do not themselves promote authority.
- D4 seller/payment-provider acceptance for the actual U.S.-first/USD CE Credits offer remains unresolved.
- Active full official Test Register binding remains not established/directly conflicted; do not invent official test IDs or represent this proposal as an official register.
- Source Authority / formal Trusted Build records remain scoped to their explicitly identified exact A9 candidate. Do not inherit authority to this or any other candidate by implication.

### Next actions

1. Use this standard to guide candidate-only engineering and product/commerce review; do not rewrite controlled sources by implication.
2. Map each proposed gate to existing authoritative sources and exact tests; reuse existing evidence where identity and scope match.
3. Work on B1 source/semantic closure and D4 internal seller/provider policy research in parallel. Keep A3 narrow and explicitly unresolved until recorded.
4. Add or modify formal tests only through the valid official Test Register route once its binding is resolved.
5. Re-evaluate the exact release candidate against every critical gate. Do not merge, promote runtime, enable paid Credits, or launch based on this document alone.

**Target:** CE V1 that attracts without misleading, earns trust through verifiable integrity, makes the value of Credits clear, fulfils paid readings reliably, and evolves without destabilising the consumer promise.

End of R0.
