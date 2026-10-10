# CONSTELLATIONS ECLIPTIC
# PRE-A10 C3 — TEST ORACLE MAP CANDIDATE R0

Date: 2026-10-10  
Classification: TEST DESIGN / NON-NORMATIVE / NOT REGISTERED / NOT EXECUTED  
Authority effect: NONE  
Official Test Register change: NONE  
Implementation authorization: NONE  
FAIL_CLOSED: TRUE

## 1. Purpose and binding limitation

This is a candidate map of deterministic tests for the proposed C3 purchase-cap contract. It is not the official Execution Profile & Test Register, does not allocate official test IDs, and reports no execution or pass.

Current Test Register identity/current binding remains NOT ESTABLISHED: Clean Current Set R3 omits document 07 although its archived Document Index lists Test Register v1.5; discoverable v1.5 copies reside in excluded raw-intake/staging locations. Preserve existing PAY/ERR/INT coverage and map only missing cap-specific assertions once the official register is reconciled.

The source map and limits are in [C3 Source-Lineage Reconciliation R0](https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/blob/governance/candidates/ce-autonomous-evolution-charter-r0-2026-10-09/governance/candidates/CE_PRE_A10_C3_SOURCE_LINEAGE_RECONCILIATION_R0_2026-10-10.md) and [C3 Crosswalk R1](https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/blob/governance/candidates/ce-autonomous-evolution-charter-r0-2026-10-09/governance/candidates/CE_PRE_A10_C3_SOURCE_BOUND_CONTRACT_CROSSWALK_R1_2026-10-10.md).

## 2. Deterministic vocabulary

- Account A / Account B: distinct authenticated accounts.
- Service date D: UTC Gregorian date assigned by server time at explicit-confirmation reservation point; D+1 is next UTC date.
- Order O: stable logical identity for one new-reading attempt.
- Debit: one reading-Credits ledger debit attributable to O, not the external payment used to top up Credits.
- Restoration R: one exact reversal of the reading-Credits debit for O; idempotent by a stable remedy identity.
- Accessible entitlement: valid reading has passed output validation and is available through its authorized entitlement.
- No mutation: no balance delta, new entitlement, slot release, reassigned service date, duplicate order side effect or other ledger mutation outside the explicit expected oracle.

Candidate IDs below are local labels only; they are not official Test Register IDs.

## 3. Candidate oracle matrix

| Candidate ID | Deterministic fixture/action | Required oracle | Status / mapping note |
|---|---|---|---|
| C3-T01 Top-up does not consume quota | A balance=0, quota AVAILABLE on D. Settle a +4 Credits top-up with one payment identity. | One top-up grant; balance=4; no new-reading order/debit/entitlement/quota reservation is created. | Candidate only; PAY-01/PAY-02 overlap generic payment idempotency/callbacks. |
| C3-T02 First D1-A purchase commit | A balance=4, quota AVAILABLE on D. Confirm O on D; authoritative one-time reading debit commits; generation remains pending. | O service date remains D; balance=0; one debit; quota effect COUNTED under D1-A; no accessible entitlement is claimed yet. | Candidate only; purchase-trigger oracle is conditional on D1-A owner disposition. |
| C3-T03 Second order after quota counted | A has O with committed debit on D, no full terminal reversal. A submits different order O2 from another device. | O2 cannot create second effective debit or entitlement; existing O and D remain unchanged. | Candidate only; daily quota check is new beyond general PAY tests. |
| C3-T04 Same account across devices | A reserves or counts D from device 1; device 2 submits a different new order for D. | Same account shares slot; no bypass by changing device. If it is a retry of O's same identity, it resolves O rather than creating O2. | Candidate only; account/date assertion is not inferred from device-auth tests. |
| C3-T05 Separate account isolation | A counts D. B with sufficient Credits submits an order on D, including from the same physical test device where test harness permits. | B's independent quota is evaluated separately; A's ledger/order/slot is unchanged. | Candidate only; complement to SCALE-06, not duplicate general cross-account test. |
| C3-T06 UTC assignment boundary | Use separate fresh accounts/orders at D 23:59:59.999 UTC and D+1 00:00:00.000 UTC. Manipulate client/display timezone and device clock. | Assigned service date follows server UTC at atomic reservation; first is D, second D+1; later retries do not re-date an existing order. | Candidate only; TIME-01–03 local civil-time tests do not automatically cover commerce UTC cap. |
| C3-T07 Concurrent new orders | A balance sufficient for two purchases; two different order identities confirm concurrently for D across two trusted devices. | At most one active account/date reservation and one effective purchase unless approved terminal-reversal sequence has released the slot; losing request has no debit/entitlement. | Candidate only; actual persistence-source required before this can be executable. |
| C3-T08 Proven pre-debit terminal failure | A balance=4. O is reserved on D. Inject and prove terminal failure before debit, with no live downstream operation; replay release twice. | Balance=4; no restoration/debit/entitlement fabricated; reservation released exactly once; quota returns AVAILABLE if D is current. | Candidate only; failure proof must be defined, not just timeout. |
| C3-T09 Unknown debit/result | O is reserved; debit callback or generation status becomes unknown. Advance time past timeout and UTC midnight. | Same O remains RECONCILIATION_REQUIRED with original D; no speculative terminal label, debit restoration, quota release, duplicate debit or entitlement. D+1 uses its own quota but O never changes date. | Candidate only; extends PAY-03 only with the new order/date/quota oracle. |
| C3-T10 Recoverable post-debit failure | O debit committed; an injected generation/validation transient fault is classified recoverable and linked recovery succeeds. | One debit and one accessible entitlement for O; service date D preserved; quota remains counted; no independent order/debit/entitlement created by recovery. | Candidate only; bounded retry fixture required. |
| C3-T11 Terminal non-delivery + D2-A | D is still current. O debit committed; authoritative evidence proves non-delivery/no possible delivery; restoration R succeeds and downstream operations close. | Exactly one debit restored; no entitlement; O marked terminal/remedied; D quota remains COUNTED. | Conditional on explicit D2-A fixture; not official. |
| C3-T12 Terminal non-delivery + D2-B | Same as T11 with D2-B selected; replay restoration and slot-release requests. | Exact reading debit restored once; no entitlement; slot released once only after all guards close; next independent order can enter normal confirmation/balance/cap checks. Historical O/date remain auditable. | Conditional on explicit D2-B disposition; not official. |
| C3-T13 Remedy replay idempotency | Submit same terminal restoration/remedy identity R four times. No monetary refund action is included in this fixture. | Exactly one +4 Credits restoration, three no-op replays; no duplicate slot release/refund/entitlement. | New remedy-specific oracle; PAY-02 provider callback idempotency is not a restoration test. |
| C3-T14 Terminal failure closes after D ends | O assigned D; at D+1 authoritative terminal non-delivery and restoration are confirmed. | Restore reading debit once; close old D slot; never transfer old slot to D+1; new D+1 quota is evaluated independently; no false entitlement. | Candidate only. |
| C3-T15 Reread | A has a retained accessible entitlement and balance=4; open that same reading repeatedly. | No new reading debit, order or date-D quota use; entitlement count unchanged. | Candidate only; preserve existing reread semantics. |
| C3-T16 Post-delivery complaint/remedy | O delivered on D; a fully specified policy fixture states remedy kind, balance delta, access state and any replacement entitlement/slot rule. Replay same remedy. | Apply that exact fixture once; preserve original fulfillment/date/history; repeated remedy is idempotent; quota cannot defeat mandatory rights. | Policy-dependent; no default remedy invented here. |
| C3-T17 Repeat terminal failures / service interlock | Fixture crosses a formally defined service-level health threshold before a new checkout request. | New confirmation is rejected as unavailable before debit/reservation; no charge, slot or entitlement for the rejected request; event is auditable; status copy is accurate. | Proposed gap, not current policy or implementation. Cannot execute until threshold/interlock is defined. |
| C3-T18 Commerce/Quiet Sky separation | Cause a terminal generation/validation failure while astronomical observation is non-VALID or no valid reading is available. | No false reading, signal, Canon claim or QUIET_SKY; no stale/synthetic replacement; order and observation states remain separate. | Preserve/extend ERR-05/ERR-06 and INT-02 only for new commerce-state assertion. |
| C3-T19 Preview disclosure | Configure daily cap and reset time; show pre-confirmation preview before any reservation/debit. | Disclosure states one new reading per account/UTC service date, actual next reset instant, top-up vs new-reading vs reread, and pending/remedy boundary alongside the existing scope/period/evidence/output/price/Credits fields. | Candidate only; exact copy and legal requirements remain reviewable. |

## 4. Preserve existing tests; do not double-register

Candidate mapping to inspect after official register binding:
- PAY-01: generic payment retry idempotency; add only order/date/slot assertions absent from its actual oracle.
- PAY-02: provider callback duplicate; do not treat it as proof of restore/slot-release idempotency.
- PAY-03: payment success + synthesis failure; add only the cap-specific debit/date/unknown/restore oracle.
- PAY-04/PAY-05 and privacy/deletion tests: preserve deletion/chargeback financial-record coverage; add no duplicate general transaction test.
- TIME-01–03: local-time semantics do not prove the UTC service-date purchase boundary.
- SEC-05: nonce/client-clock handling does not prove one account/date order.
- SCALE-04/SCALE-06: callback bursts/cross-account isolation do not prove same-account/date atomic uniqueness.
- INT-02 and ERR-05/ERR-06: preserve commercial independence and technical-failure/Quiet-Sky boundaries; add a slot assertion only if missing.
- Existing Test Register IDs and oracles must be inspected directly after its current identity/pointer has been reconciled. No candidate labels here become official IDs by convention.

## 5. Eligibility gates for official registration

Before registration, establish:
1. explicit owner disposition for D1 and D2, or a controlled RECONCILE outcome;
2. exact service-level interlock semantics or an explicit decision that it is out of C3 scope;
3. current official Test Register identity/pointer;
4. actual commerce/persistence source or an explicit finding that no implementation exists;
5. exact fixtures for balances, order/debit/remedy identities, service date, entitlement and slot result;
6. no duplicated oracle and independent review under controlled change management.

## 6. State

C3 purchase contract: NON-NORMATIVE / NOT APPROVED.  
Candidate oracles above: NOT OFFICIAL / NOT REGISTERED / NOT EXECUTED.  
Official Test Register: NOT ESTABLISHED.  
Commerce/persistence implementation: NOT ESTABLISHED IN INSPECTED SCOPE.  
Normative sources/test register/schema/code/runtime: UNCHANGED.  
Implementation/A10/Runtime Adoption/production/SEAL: NOT AUTHORIZED.  
FAIL_CLOSED: TRUE.

End of map.
