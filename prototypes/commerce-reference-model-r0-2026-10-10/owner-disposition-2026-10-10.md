# Owner Product Policy Disposition — CE Commerce

**Disposition date:** 2026-10-10  
**Classification:** owner-confirmed product policy; candidate implementation input only  
**Record source:** explicit owner disposition in the CE working conversation

## Recorded decisions

| Item | Owner disposition | Binding meaning for this candidate |
|---|---|---|
| D1 — effective Deep Sky purchase | **D1-A** | A new purchase counts when the confirmed logical order is bound to its immutable server-derived UTC service date and the one-time Deep Sky reading-Credits debit is committed. The account/date cap is enforced against this effective purchase. |
| D2 — same-date slot following terminal non-delivery | **D2-B** | A slot may be released only after terminal non-delivery is positively evidenced: no valid reading is accessible, no operation can still deliver, no entitlement exists, all relevant operations are closed, and the exact reading debit has been restored once. The slot may be released for another purchase only while its original UTC service date is still current. After that date expires, the old slot closes without transfer to another date. |
| Fulfillment-health interlock | **APPROVED PRINCIPLE** | Do not admit a new Deep Sky purchase unless the service is explicitly in a state that permits new purchases. Unknown or blocked admission state fails closed. This interlock applies to new purchase admission; it must not cancel, reclassify, or abandon existing operations that still require reconciliation or fulfillment. |

## Related invariants

- The service date is server-derived in UTC and is immutable once bound to the logical purchase.
- Account/date uniqueness is shared across trusted devices.
- Retries of the same logical purchase do not create a new purchase, debit, or slot.
- An unknown, pending, timed-out, restarted, or callback-missing operation is not terminal non-delivery evidence.
- Credits top-up is not a Deep Sky purchase. Re-reading an existing entitlement is not a new purchase.
- Credits ledger restoration is distinct from any external-money/card refund.
- Product-delivery failure must not be represented as Quiet Sky and must not alter astronomical facts, CE Canon, signals, uncertainty, or reading content.

## Boundaries not approved by this disposition

This record does **not** authorize or establish:
- changes to a normative Constitution, Technical Contract, official Test Register, or other source-authority chain;
- production application changes, deployment, runtime adoption, trusted-build status, SEAL, or production authorization;
- a payment provider, seller/legal jurisdiction, live market, currency, price, refund policy, or commercial integration;
- a production database/schema choice or a claim that this reference model is production-ready.

The fulfillment-health state source, evaluation thresholds, operator controls, recovery behavior, and audit/monitoring contract remain engineering design items to validate in the candidate. The selected policy is recorded here so implementation and tests can be aligned; this file is not itself an authoritative CE normative document.

## CE authority status remains unchanged

`SOURCE_AUTHORITY=NOT_ESTABLISHED`  
`TRUSTED_BUILD=NOT_ESTABLISHED`  
`PRODUCTION_RUNTIME=NOT_AUTHORIZED`  
`SEAL=NO`  
`AUTHORIZATION=NON_AUTHORIZED`  
`FAIL_CLOSED=TRUE`
