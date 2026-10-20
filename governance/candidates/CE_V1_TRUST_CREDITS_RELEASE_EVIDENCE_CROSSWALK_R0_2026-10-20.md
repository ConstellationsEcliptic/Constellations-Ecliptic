# CE V1 — Trust / Credits Standard to Evidence Crosswalk R0

**Date:** 2026-10-20  
**Classification:** CANDIDATE EVIDENCE CROSSWALK / NON-NORMATIVE / SOURCE-BOUND  
**Parent working standard:** CE V1 Trust, First-Contact Value, Credits Conversion & Controlled Evolution Standard R0 in PR #40.  
**Authority effect:** NONE. This crosswalk does not alter any governing source, official Test Register, Area Register, code, runtime, A10, Source Authority, Trusted Build, production authorization, payment enablement, or release gate.

## 1. Purpose

Make the proposed readiness standard actionable against evidence already present in CE's repository. Reuse existing evidence only when its exact candidate identity and test scope match. Do not repeat successful tests merely to create paperwork, and do not interpret a component-level pass as full product/release readiness.

Status labels here:
- **PASS — narrow scope only:** evidence supports exactly the bounded claim noted.
- **PARTIAL:** useful evidence exists but significant integration, authority, or end-to-end coverage remains.
- **BLOCKED:** a release prerequisite is known to be missing, conflicting, failed, or not authorized.
- **NOT EVIDENCED:** the reviewed sources do not establish the requirement; this is not a universal claim that no private/local evidence exists.

## 2. Crosswalk

| Proposed gate | Evidence already verified | Current status | What's still missing / why this blocks launch | Most direct next step |
|---|---|---|---|---|
| **G1 — Source and rule integrity** | A9 exact candidate  c8dab3542d3d4725cf591630c07f76366f7949d0 has record-backed Source Authority and formal Trusted Build for that exact candidate; PR #26 full-boundary/remediation tests passed 261 per OS. B1 prototype PR #32 has a 62-test matrix passing on Ubuntu/macOS/Windows at 1c3459836996ce4cc1a6ffb5ff76cb77e6a488d8. | **BLOCKED for release; narrow candidate evidence PASS** | No populated approved current V1 Canon registry / independently verified semantic verifier is established in the inspected scope. PR #32 uses TEST_ONLY synthetic rules. Full boundary, remediation and Trusted Build workflows on PR #32 fail source-tree/control-plane identity checks against pinned A9. The A9 candidate has a source-tree test-discovery defect: an intended self-reference-exclusion test is not collected. | Preserve A9 bytes/manifests. In a separate candidate, close geometry/profile-to-runtime traceability, add the missing test correctly, bind applicability to authorization, and produce a controlled successor with a valid source/control-plane identity and re-run applicable suites. Populate/promote Canon only through an authorized source route. |
| **G2 — Product-state / fail-closed boundary** | The inspected A9 code has fail-closed behavior for invalid/non-authorized computation and rejects an empty/unmaterialized Canon registry. A9 full boundary and remediation suites passed at its exact head. | **PARTIAL / BLOCKED for launch** | Passing backend boundary tests do not prove the full user-facing product/runtime. Runtime Adoption and production runtime authorization remain not established/unauthorized; full current official test-register binding and coverage remain unresolved. | Map each valid and non-VALID state to exact source + test evidence; verify user-facing state mapping, entitlement, and no failure-to-Quiet-Sky relabelling on the exact release candidate. Do not invent test IDs while official register binding is conflicted. |
| **G3 — First-contact attraction, comprehension and claims** | Historical frontend prototypes were found but identified as demo/raw-inventory material, not an approved current V1 Note corpus or UI path. The A9 implementation tree inspected in the Zero-Point review contained no consumer-facing UI/editorial-library implementation path. | **NOT EVIDENCED / BLOCKED for public launch** | Current live screens, approved copy, truth-labelled sample outputs, and comprehension evidence have not been established in the reviewed scope. The first impression therefore cannot yet be certified against the new standard. | Use one focused first-contact release-QA check on the actual intended screens/copy, not an open-ended research programme. Test what users infer about the source of a result, whether they understand signal vs interpretation, and whether possibility language sounds guaranteed. Fix material misunderstandings; label simulations clearly. |
| **G4 — Paid value and transparent Credits offer** | Credits remain the intended primary monetization model; commercial design sources and owner-approved product decisions exist. | **NOT EVIDENCED / BLOCKED for paid launch** | Exact SKU/package prices, USD price presentation, cost in Credits per reading, customer-facing purchase disclosure, and live UX are not yet settled/verified in the reviewed candidate chain. | First choose a truthful offer the system can actually fulfil. Then show USD package price, Credits supplied, and reading cost before commitment; verify UI/copy against approved Commercial rules. Do not invent prices as placeholders in a live store. |
| **G5 — Purchase, entitlement, fulfilment and remedy** | PR #33 isolated commerce reference model at exact head a0dcd466e28ca822a43ef86c172f7e1c91ea46a4; candidate workflow #38036272045 passed. It models D1-A, D2-B exactly-once reading-Credit restoration, UTC Gregorian service date, health interlock, idempotency and failure states. The source expressly says model/schema are prototype only. | **PARTIAL / BLOCKED for launch** | Passing reference-model tests do not prove real provider callbacks/signatures, durable ledger, production persistence/transactions, deployed fulfilment service, provider refunds, monitoring, or end-to-end production behavior. Five-minute health lease in the prototype is not an approved production SLO. | Treat PR #33 as a source of candidate test ideas, not production code. Map the owner-approved commerce semantics to the intended implementation, add integration/end-to-end tests for duplicate/late/unknown outcomes and non-delivery restoration, then validate the exact deployed release identity. |
| **G6 — Security and privacy** | Minimal-data and account/security architectures plus A9 sources/tests provide an established design baseline; the A9 branch contains relevant code, schemas, test and provenance material. | **PARTIAL / BLOCKED for launch** | The inspected record does not establish end-to-end production evidence for trusted-device/account recovery, access boundaries, retention/deletion, event telemetry, incident operations, or the actual launched application. Privacy architecture is not proof of implementation. | Create a small, source-linked verification matrix for the exact V1 data flow: collected field/event, purpose, access, retention/deletion, authorization boundary and test. Reuse existing tests where identity and scope match. Exclude birth-data and reading-content dimensions from ordinary conversion analytics unless an approved specific need exists. |
| **G7 — Legal, seller and processor fit** | US customers first and USD customer-facing pricing/presentment are recorded as owner intent. PR #37 is a provider-policy research candidate; public-policy crosswalk flags conflicts for the current astrology + prepaid Credits offer. | **BLOCKED for paid launch** | Seller entity/jurisdiction, paid customer-state allowlist and written exact-product processor/acquirer approval remain unresolved. No provider has been contacted/selected in the current handoff. A provider's marketing page is not approval of CE's exact offer. | Prepare a no-cost, truthful written prescreen packet with product description, future-oriented reading language, Credits/top-up and remedy semantics, seller facts and target market. Compare providers against written responses. No onboarding spend or processor integration until eligible route is confirmed. |
| **G8 — Release identity, authority, official tests and rollback** | PR #27 exact head 4309a5e40dc7d3ee4e27233441104f346f65b481; run #38760707852 passed validator unit tests and R0–R3 Area Register structure checks. A9 authority/build evidence is exact-candidate scoped. | **BLOCKED** | PR #27 strict Pre-A10 gate remains blocked, recorded at 20/23 with A3/B1/D4 incomplete. The full active official Test Register binding remains NOT ESTABLISHED / DIRECTLY CONFLICTED. Runtime Adoption, full runtime coverage and production authorization are not established. PR #40 is a proposal, not an active gate. | Resolve the official Register/source binding through the valid controlled route. Preserve prior candidate identities. At final candidate head, rerun exact required controls, prove Runtime Adoption and production authorization as separate steps, and verify monitoring/rollback before launch. |
| **G9 — Customer value and voluntary repeat purchase** | The product strategy and measures are now specified as a candidate framework; there is no verified CE-specific conversion/retention/willingness-to-pay result in the reviewed evidence. | **NOT EVIDENCED; not itself a pre-launch demand-proof requirement** | CE must not claim the market has validated CE or forecast success before evidence exists. Actual repeat purchase can only be observed once users use a working product. Pre-launch readiness still requires a comprehensible core experience and honest paid offer, not proof of long-term market success. | Define minimal aggregate funnel events and complaint/fulfilment measures under the privacy design. After a properly authorized release, measure view → intent → purchase → fulfilled reading → remedy/complaint → voluntary repeat purchase, with clear denominators and caveats. Do not present correlation as evidence of astrology accuracy. |

## 3. Cross-cutting interpretation

1. **Do not re-run what has already been proven for the same bytes and scope.** Reuse the A9 test evidence for the A9 candidate only. Use PR #32's passing matrix only for its 62 selected prototype tests. Use PR #33's pass only for that isolated reference model.
2. **Candidate evidence does not compose automatically.** A9 + PR #32 + PR #33 is not an assembled production system. Different branches have different identities; successful tests or permissions do not transfer between branches.
3. **No quiet gate override.** PR #27 passing structural/unit tests does not mean the strict Pre-A10 gate passed; the recorded result remains blocked. A documentation candidate cannot change gate status.
4. **Keep A3 narrow.** The existing valid-QUIET_SKY Note disposition is settled but bounded by approved eligible content and conditions. Signal-present Note scope remains a separate owner decision; this crosswalk does not decide it or activate any Note.
5. **Separate launch modes.** A free limited launch may not require a payment provider, but it still requires the applicable legal/claim, source, calculation, privacy, security, product-state, runtime, and production gates. A paid Credits launch additionally requires G4/G5/G7 and commercial/legal readiness to pass. No mode may bypass technical/source/runtime gates.
6. **Do not equate “perfect” with infinite scope.** Stop adding features; reduce scope instead. Require complete evidence for the features included in V1. Excluded features should remain off and must not be represented as available.

## 4. Critical next-action ordering

### Track A — Source / release integrity (blocks any public launch)
- B1 source-to-runtime geometry/applicability binding and approved Canon/semantic-verifier source route.
- Full official Test Register / source-lineage reconciliation.
- Exact release candidate boundary tests, full required suite, runtime adoption, deployment identity, monitoring and rollback.

### Track B — First contact / trust (blocks public launch)
- Identify the actual V1 screens and samples to be exposed.
- Ensure every sample is genuine authorized output or clearly labelled simulation.
- Complete a focused comprehension and claim review; resolve critical misunderstanding before publication.

### Track C — Paid Credits (blocks paid launch; may proceed in parallel)
- Internally screen exact-product seller/payment eligibility; do not contact or commit externally absent the proper authority.
- Define valid SKU / USD / Credits package / per-reading cost only after the seller/provider/market constraints are understood.
- Integrate the approved provider only after written acceptance; verify end-to-end ledger, entitlement, fulfilment, failure, remedy and refund behaviours.

### Track D — Privacy / telemetry (must be included before instrumentation)
- Keep telemetry minimal, purpose-bound, and deletable under the approved privacy architecture.
- Do not collect raw reading text, birth data, relationship data or inferred traits to optimize conversion.
- Make performance metrics jointly consider conversion, comprehension, fulfilment, complaints and remedies.

## 5. Current outcome

**No readiness gate is promoted by this crosswalk.** The useful conclusion is not “CE is close to launch” or “CE is far from launch”; it is that the remaining blockers have distinct owners/evidence and can be addressed in parallel without redoing prior verified work. G1/G2/G8 are the critical source/runtime path for any public launch; G3/G6 are the critical consumer-trust path; G4/G5/G7 additionally block a paid Credits launch. G9 is a measurement plan rather than a demand-proof gate.

Next action: continue candidate-only B1 source/semantic closure and D4 internal eligibility research in parallel, while preparing the precise first-contact/paid UX against approved source/commerce semantics. Keep release fail-closed until the exact launch-scope gates pass.

End of R0.
