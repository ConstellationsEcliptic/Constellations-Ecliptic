# CONSTELLATIONS ECLIPTIC
# PRE-A10 C3 — PURCHASE-CAP SEMANTIC RECONCILIATION R0

Date: 2026-10-10  
Classification: OWNER-DIRECTED RECONCILIATION / CANDIDATE EVIDENCE / NON-NORMATIVE  
Recorded owner disposition: **RECONCILE**  
Authority effect: NONE  
Normative amendment: NONE  
Official Test Register change: NONE  
Schema / code / runtime / production / SEAL effect: NONE  
Implementation authorization: NONE  
FAIL_CLOSED: TRUE

## 1. Purpose and disposition

This record implements the owner's explicit **RECONCILE** disposition in response to the proposed pair D1-A + D2-B. RECONCILE is not approval of that pair, does not select D1-B or D2-A, and does not authorize the assistant or implementation team to infer a substitute owner decision.

The task is to align the candidate options with recorded owner direction and source evidence, expose where existing sources stop, and keep genuinely unresolved product semantics open.

## 2. Source map actually considered

1. [Owner Disposition — Daily Deep Sky Service-Day Boundary R0, Box 2515555580794](https://app.box.com/file/2515555580794): approves only the fixed UTC Gregorian service-day boundary and server-derived date assignment at the atomic reservation point after explicit confirmation; expressly does not approve the complete consumption, failure, refund, or slot-release state machine.
2. [DR-01 Decision-Evidence Reconciliation, Box 2515706725948](https://app.box.com/file/2515706725948): distinguishes the evidenced one-new-purchase premise from the still-proposed complete cap/order/remedy contract; preserves the historical DR-01 R0 entry rather than overwriting or backdating it.
3. [Daily Cap Semantic Consistency Finding R0, Box 2515747060613](https://app.box.com/file/2515747060613): records that “purchase” and “newly fulfilled reading” are not semantically interchangeable, and that reservation, purchase/redemption, and fulfillment are distinct events.
4. [Daily Cap Semantic Options & Test Consequences R0, Box 2515757204983](https://app.box.com/file/2515757204983): recommends preserving purchase-cap wording while defining its effective event; identifies a fulfilled-reading cap as a materially different product option.
5. [Daily Cap Normative Source-Lineage Boundary R0, Box 2515745492938](https://app.box.com/file/2515745492938) and [Update R1, Box 2515750096004](https://app.box.com/file/2515750096004): keep the exact individual normative-source byte lineage open. These candidate findings are not a normative redline.
6. [Account, Privacy & Commercial Specification v1.7, Box 2485319995048](https://app.box.com/file/2485319995048), especially §§11–14: account-bound/non-expiring Credits, retained-reading reread, purchase preview, server-issued idempotency, payment-credential separation, transaction and fulfillment records. It does not decide the C3 daily-slot state machine.
7. [Business Model v1.5, Box 2485331476456](https://app.box.com/file/2485331476456) and [Implementation Plan v1.3.1, Box 2491699264134](https://app.box.com/file/2491699264134), especially §7.8 and the commercial fulfillment phase: Credits-funded Deep Sky, stable logical purchase identity, database-enforced uniqueness, provider-event deduplication and reconciliation of unknown transaction states. They establish implementation requirements, not a live commerce implementation or the exact cap trigger.
8. [Technical Contracts v1.1 hardened R2, Box 2491799121573](https://app.box.com/file/2491799121573), §21: transaction/fulfillment identity, persistence uniqueness, atomic fulfillment, and unknown-provider-state reconciliation. The active implementation pointer R7 (Box 2492023501528) and Current Decision Register R7 (Box 2492022563209) name R2; the non-authoritative Stack Index/Manifest records from 2026-10-04 name a different earlier v1.1 artifact. This bounded pointer inconsistency remains recorded and does not make R2 a new constitution.
9. Historical Test Register v1.5, Box 2485336117840: PAY-01–05 cover generic payment idempotency, duplicate callbacks, payment-success/generation-failure reconciliation, deletion during fulfillment, and chargeback after deletion. Its current official binding is not established; no test registration is performed by this note.

## 3. Reconciled facts versus open semantics

| Proposition | Reconciled status | Consequence |
|---|---|---|
| Limit of at most one new Deep Sky purchase per authenticated account per CE service day | Owner-originated premise evidenced | Do not describe the entire cap premise as undecided. |
| UTC Gregorian day, 00:00 UTC inclusive to next 00:00 UTC exclusive; same account shares the allowance across trusted devices | Owner-approved, limited scope | Do not ask the owner to repeat this decision. |
| Server UTC timestamp at atomic reservation boundary after explicit confirmation assigns the service date | Owner-approved, limited scope | The assigned date is immutable for that logical order; it does not by itself define when quota consumption becomes effective. |
| Reservation, purchase/redemption, and fulfillment are three different events | Source-reconciled semantic distinction | Do not use one event as a silent substitute for another. |
| Exact event at which the cap counts | OPEN | Must not be silently inferred from the UTC-boundary approval. |
| Same-date slot after proven terminal non-delivery, exact reading-debit restoration and downstream closure | OPEN | Credits restoration does not, by itself, imply slot release or slot retention. |
| Repeated terminal failures / service-level availability interlock | Separate proposed reliability gap | Not approved, implemented, thresholded, or part of this RECONCILE disposition. |

## 4. D1 reconciliation — retain purchase-cap meaning; do not silently select fulfillment-cap semantics

The owner-originated language is a **purchase** cap. The sources distinguish three events:

1. **Reservation:** after explicit confirmation, atomically bind one logical order to server-derived service date D to prevent concurrent competing orders.
2. **Effective purchase/redemption:** the contract still needs to specify the precise committed event and the conditions under which a terminal reversal affects its quota effect.
3. **Fulfillment:** a valid reading passes output validation and becomes accessible through its entitlement.

Reservation assigns D and protects concurrency; it is not itself proof of a committed purchase or delivered reading. A Credits debit is not proof of delivery. A timeout or unknown provider state is not proof of failure.

Candidate comparison remains:

- **Purchase/redemption-cap path (closest wording fit; not owner-approved as a complete state machine):** define the effective event around a confirmed new-reading order with stable identity, immutable D, and authoritative one-time reading-Credits debit commit. Reserve before this event for concurrency. A proven pre-debit terminal failure with no unresolved operation can release the reservation once. This event definition is still a candidate detail, not a consequence automatically established by the date-boundary disposition.
- **Fulfilled-reading-cap path (not interchangeable; not owner-approved):** count only after a valid reading is accessible. This changes the promise from one purchase per service date toward one successful delivery per service date and may permit more than one purchase/redemption attempt on that date.

**Reconciliation result for D1:** preserve purchase-cap as the meaning baseline; do not treat the “fulfilled reading” option from older candidate drafts as already approved. The exact effective purchase event and all reversal interactions remain open for controlled disposition. This record does not choose an approved final D1.

## 5. D2 reconciliation — slot effect after terminal non-delivery is a separate policy choice

D2 is reachable only with affirmative evidence that:
- no valid reading became accessible;
- no generation, validation, entitlement or other downstream operation can still deliver the original reading;
- the exact reading-Credits debit is restored exactly once;
- no entitlement remains granted for that undelivered order; and
- all relevant operations and remedy transitions are closed.

A timeout, restart, missing callback, pending provider state, or UTC midnight does not satisfy these conditions. The original order ID and service date remain immutable and auditable. Reading-Credits restoration is distinct from any separate processor/card refund or other mandatory consumer remedy.

The slot options are materially different:

- **D2-A — retain slot:** even after full terminal reversal, D's quota effect remains occupied. This aligns more directly with a strict “one effective purchase/redemption event per date” rule, but can leave the customer unable to start a new paid purchase that day after CE definitively failed to deliver. Applicable consumer rights remain unaffected; any linked no-charge replacement or other remedy needs its own explicit contract.
- **D2-B — release slot after full reversal:** after all guards above close, release the quota effect once, and only if D remains the current service date. The original transaction history remains immutable. To keep this consistent, the contract must expressly state that a fully reversed, never-delivered order no longer consumes the **net daily quota effect**. Otherwise the same specification would say both that the purchase always consumes the cap and that its reversal releases it. This path allows a distinct new same-day purchase and must not be falsely described as “only one committed purchase ever occurred that day.”
- **Linked no-charge remedy/replacement:** this is a separate consumer-remedy design that may be considered without silently creating a second paid purchase. It must retain linkage to the original order and define debit, entitlement, reading identity and remedy idempotency. It is not automatically selected by either D2-A or D2-B and must not be invented by implementation.

If terminal non-delivery and restoration are concluded only after D expires, close the old date's slot without transferring it to D+1. If the outcome is still unknown, keep the original order/date in reconciliation; midnight is not terminal-failure evidence.

**Reconciliation result for D2:** no source inspected resolves the owner choice between retaining the slot and releasing its net quota effect following full terminal reversal. D2 remains OPEN. D2-B is not approved by this record.

## 6. Cross-effects and test consequences

The final contract must keep separate:
- order/fulfillment state;
- immutable service-date identity and quota/slot effect;
- Credits ledger and exact restoration identity;
- external payment/monetary remedies;
- entitlement and accessible-reading state.

Retries resume the same logical order. Duplicate provider callbacks or remedial requests must not duplicate credits, entitlement, restoration or slot release. Different trusted devices do not create separate account allowances. Credits top-up is not a new-reading purchase, and rereading an already retained, accessible entitlement is not a new purchase.

Candidate oracle mapping:
- existing PAY-01/PAY-02 generic payment/replay coverage is preserved, not duplicated;
- PAY-03 unknown/reconciliation coverage is preserved and only extended for missing date/slot-specific assertions;
- the existing register's TIME/SEC/SCALE cases do not by themselves prove the purchase UTC boundary or same-account/date atomic uniqueness;
- D1/D2 candidate oracles stay conditional on explicit semantic disposition and exact current Test Register binding.
- Do not allocate official test IDs or claim execution/pass: official full Test Register identity/current binding remains NOT ESTABLISHED.

## 7. Outcome of the owner's RECONCILE direction

- Owner disposition recorded: **RECONCILE**.
- D1-A + D2-B: **NOT APPROVED**.
- D1 effective purchase/redemption trigger: **OPEN**; preserve purchase-cap wording and show fulfillment-cap as a materially different option.
- D2 slot after proven terminal non-delivery and full exact restoration: **OPEN**; neither retain nor release is selected here.
- Service-level fulfillment interlock: separate proposal, no approved threshold or implementation.
- Commerce implementation within the owner-defined five-source universe: **NOT IMPLEMENTED / PLAN FROM ZERO**, as already recorded in the candidate area register. No continued search for an assumed historical implementation is implied.
- Official Test Register current identity/binding: **NOT ESTABLISHED**.
- Exact current normative source-byte lineage for a redline: **NOT ESTABLISHED**.
- Normative sources, official Test Register, schema, application code and runtime: **UNCHANGED**.
- Source Authority / Trusted Build / Production Runtime / SEAL: **NOT ESTABLISHED / NOT AUTHORIZED / NO**.
- FAIL_CLOSED=TRUE.

## 8. Next controlled action

Keep C3 at owner-discussion/reconciliation status. Only the genuinely unresolved product semantics (effective purchase event, then the slot effect/approved remedy for proven terminal non-delivery) require owner decision after this source-reconciled comparison. Do not turn this note into a normative redline, official test registration, schema, code, provider choice, persistence choice, A10 or production authorization.

End of R0.
