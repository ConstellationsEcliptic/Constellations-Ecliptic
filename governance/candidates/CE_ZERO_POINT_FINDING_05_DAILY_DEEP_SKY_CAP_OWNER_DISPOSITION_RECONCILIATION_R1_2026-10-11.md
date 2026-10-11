# CONSTELLATIONS ECLIPTIC
# FINDING 5 — DAILY DEEP SKY CAP OWNER DISPOSITION RECONCILIATION R1

Date: 2026-10-11
Classification: SOURCE-BOUND EVIDENCE ADDENDUM / NON-AUTHORITATIVE
Authority effect: NONE
Normative effect: NONE
Official Test Register effect: NONE
Implementation / deployment / runtime authorization: NONE

## 1. Why this R1 follows the prior addendum

Finding 5 Addendum R0 correctly preserved the owner-originated one-new-reading-per-account/service-day premise and UTC boundary, while describing the detailed cap contract as proposed. The later direct review of the live Pre-A10 R3 register and commerce reference-model PR #33 surfaced a further owner disposition that must be incorporated: **D1-A, D2-B and the fulfillment-health interlock principle have been selected at policy level.** R0 is not overwritten; this R1 records the newer evidence and narrows only the parts still open.

## 2. Exact decision record

Live [PR #33 — CE Commerce Reference Model R0](https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/pull/33) is OPEN / DRAFT / NOT MERGED at HEAD `a0dcd466e28ca822a43ef86c172f7e1c91ea46a4`. Its owner record is [owner-disposition-2026-10-10.md](https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/blob/a0dcd466e28ca822a43ef86c172f7e1c91ea46a4/prototypes/commerce-reference-model-r0-2026-10-10/owner-disposition-2026-10-10.md), blob SHA-1 `003157fbf53860880340549003e7037882e29714`. The explicit owner-disposition comment is dated 2026-10-10. Pre-A10 Area Register R3 marks C3 `OWNER_DECISION_RECORDED` and cites these decisions.

## 3. Recorded choices (do not re-ask)

### D1-A — effective new purchase
A new Deep Sky purchase becomes effective when the confirmed logical order is bound to an immutable server-derived UTC service date and its one-time reading-Credits debit is committed. Retry of that same logical purchase does not create another purchase, debit or slot. Credits top-up and rereading an already-entitled reading are not new Deep Sky purchases.

### D2-B — release after terminal non-delivery
Release is allowed only after positive terminal-non-delivery evidence establishes: no accessible valid reading, no live delivery-capable operation, no entitlement, all relevant operations closed, and exact once-only restoration of the reading debit. Reuse is allowed only while the original UTC service date remains current. After the date expires, close the old slot without transferring it into the next service date. Unknown/pending/timeout/restarted/callback-missing operations are not terminal evidence. Credits restoration is distinct from a card/cash refund.

### Fulfillment-health interlock — approved principle
A new purchase/admission and effective debit require explicit current READY health evidence. UNKNOWN/BLOCKED/expired readiness fails closed for new admission/debit. Health state alone must never cancel, terminalize or abandon an existing order that remains recoverable or needs fulfillment/reconciliation.

### Service-day boundary — separate limited approval
The CE service day is a fixed Gregorian UTC date, inclusive at 00:00:00 UTC and exclusive at next date 00:00:00 UTC, account-wide and not device-local. This limited decision does not approve every state transition or consumer remedy.

## 4. Exact candidate-test evidence

PR #33 HEAD `a0dcd466e28ca822a43ef86c172f7e1c91ea46a4` has successful Actions run [#38036272045](https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/actions/runs/38036272045). The PostgreSQL 18.6 candidate job reports `Ran 67 tests in 2.573s`. Named cases include concurrent account/date uniqueness, atomic D1-A debit/slot consumption, evidence-bound terminal failure, exact restoration, current-date release vs expired-date no-transfer, and READY/UNKNOWN health admission.

That is candidate integration evidence only. It is not an official CE Test Register execution, independent security review, production database proof, live payment-provider/webhook proof, distributed-runtime proof or authorization to merge/deploy.

## 5. What remains open

- **Pre-debit reservation failure/release is separate from D2-B.** PR #33 itself says its pre-debit rejection/release branch was derived from prior cap material and is not an owner-approved complete normative contract.
- Health-attestation producer/source, thresholds, expiry/renewal, monitoring/alerts, operator controls, recovery and audit remain to be designed and independently reviewed. The prototype's five-minute READY lease is not an approved production SLO.
- The source integration into Technical Contracts, Account/Commercial, Business Model, Implementation Plan, Index and the currently valid official Test Register remains incomplete. The historical Human Decision Register R0 (Box 2514894635417) still literally states DR-01 `NOT_RECORDED`; preserve it and reconcile later owner evidence through a successor register, not by rewriting history.
- Cap-specific candidate test cases are not official Test Register IDs. The active full-register/Index lineage conflict remains.
- PR #33's candidate SQL/reference model is not proof of the authorized production commerce/persistence implementation; the current source of record remains NOT ESTABLISHED within inspected connected scope.
- Cash/card refund, consumer remedies, provider, seller entity/jurisdiction, final market, price/currency/SKU and paid checkout remain separate unresolved/not-authorized matters.

## 6. Corrected disposition

Finding 5 remains **PARTIAL — key product-policy choices recorded**. The one-new-reading cap premise, UTC service day, D1-A effective-purchase point, D2-B same-date release after positively evidenced terminal non-delivery, and fulfillment-health interlock principle are already owner-disposed. The remaining work is controlled normative/Test Register integration, the distinct pre-debit failure policy, health-control design, authoritative persistence/application source, independent candidate review and paid-market remedies.

No historical register, normative source, official Test Register, product implementation, runtime, provider configuration, production system, A10 or SEAL state was changed.
