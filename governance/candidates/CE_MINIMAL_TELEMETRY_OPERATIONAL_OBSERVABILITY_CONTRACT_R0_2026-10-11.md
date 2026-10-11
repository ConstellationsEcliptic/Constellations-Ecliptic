# CONSTELLATIONS ECLIPTIC
# MINIMAL TELEMETRY / OPERATIONAL OBSERVABILITY CONTRACT R0

Date: 2026-10-11
Classification: NON-NORMATIVE CANDIDATE / PRIVACY CONTROL DESIGN
Status: DRAFT — NOT APPROVED / NOT IMPLEMENTED
Authority effect: NONE
Normative effect: NONE
Implementation / deployment / collection authorization: NONE
Official Test Register effect: NONE
A10 / Source Authority / Trusted Build / Runtime Adoption / SEAL effect: NONE

## 1. Purpose

This candidate narrows Finding 10 in the Zero-Point crosswalk. It is not permission to add telemetry, analytics SDKs, user event tracking or a new persistent store. It defines the minimum questions that must be answered before a field-level allowlist can be adopted.

A zero-event allowlist in the companion manifest means that no **additional product/user telemetry event** has been approved by this candidate. It does not cancel existing contract requirements for minimal security event logging or performance measurement, and it does not claim that existing telemetry/monitoring is absent.

## 2. Source baseline reviewed

- Account, Privacy & Commercial Specification v1.7 (Box 2485319995048): states that minimal security event logging is needed; sensitive recovery material must not be logged; purchase/entitlement idempotency and the commercial record are separate.
- Technical Contracts v1.1, metadata-reconciled R2 (Box 2491799121573): §23 names `MINIMAL SECURITY / OPERATIONAL LOGS` as a V1 data class and expressly excludes persistent free-text journals, persistent Personal Context, hidden personality profiles, social graphs, public identity profiles, third-party personal enrichment and behavioral profiles. §§24.1–24.2 define performance operation classes and require p50/p95/p99 latency, error rate, throughput, concurrency, CPU usage, memory usage and timeout rate.
- Historical Execution Profile & Test Register v1.5 (Box 2485336117840): SEC-08 expects abuse controls without persistent behavioral profiling; PRIV-13 limits retained financial records to documented retention purposes and rejects analytics-profile use; the register also requires deterministic state-oracle tests. It is historical content only here, not assumed to be the currently active official register while the Index/Test Register binding remains unresolved.
- Privacy Architecture Minimal Data (Box 2485335589220): V1 data-minimization and exclusion boundaries apply; a new data field is not allowed merely because it is convenient.

The source set establishes broad categories and some performance metrics. It does not, in the inspected text, bind an operational field-level telemetry allowlist with approved purposes, access roles, retention periods, deletion behavior, sampling/aggregation rules and anti-join controls.

## 3. Keep three data planes separate

### 3.1 Performance / infrastructure metrics

The Technical Contracts operation classes and metrics above are already specified. Any implementation should preserve their exact scope and purpose: benchmark, capacity, reliability and failure detection. This candidate does not authorize adding user identity, reading content or behavioral fields to these metrics.

Before the collection/storage path is treated as verified, evidence must bind:
- each metric to its operation class and operational purpose;
- aggregation granularity and whether a series can be linked to a person or account;
- the storage/processor location and authorized access;
- retention and deletion/aggregation treatment;
- alert/incident conditions and whether raw diagnostic values are transient or persisted.

The approved target values for latency/resource metrics remain governed by the existing execution-profile process; this candidate invents no numerical target or retention period.

### 3.2 Minimal security events

Security/recovery/rate-limit events may be necessary for abuse prevention and secure operation. Their payload must exclude passwords, recovery keys/phrases, session tokens, age-assurance raw materials and unnecessary sensitive data. Account/device/network identifiers may only be included when strictly necessary for an expressly documented security purpose and must not be reused for product analytics or cross-service identity graphs.

The exact security event types, required identifiers, reader roles, retention periods and deletion exceptions must come from the approved account/security contract and applicable legal obligations, not be guessed here.

### 3.3 Commercial and entitlement ledger

Payment transactions, Credits ledger entries, purchase idempotency, provider callbacks, fulfillment, entitlement and legally retained financial records remain in their separately governed commercial/security records. Do not copy them wholesale into general-purpose telemetry. Operational diagnostic events should reference a narrowly scoped opaque correlation ID only if required to reconcile a live transaction, with authorization and retention bound to the underlying approved purpose.

Financial records must not be repurposed for product personalization, behavioral analytics or restoration of deleted Personal Sky.

## 4. Prohibited telemetry joins and payload classes

No telemetry event, export, dashboard, processor or analytics join may be used to create or infer:
- a persistent personality, psychological or behavioral profile;
- hidden user traits, social graph or identity graph;
- a cross-account/device activity history beyond what an explicitly approved security function requires;
- product engagement, emotional vulnerability, forecast “accuracy” or resonance profile;
- ad targeting, sale of personal context or retention-based manipulation.

Unless a separately authorized security/financial record requires a specific field for a documented purpose, the candidate deny-list includes:
- birth date/time/city and raw coordinates;
- calculated placements, aspects, personal signal details or reading content;
- prompts, model inputs/outputs or raw free text;
- feedback answers and inferred personality/context;
- names, email/phone and public identity;
- passwords, recovery material, session/device secrets and age-assurance source documents;
- provider credentials, raw payment-card data or unneeded payment details;
- credit balance/reading purchase history in behavioral analytics;
- stable user-level identifiers used for general-purpose cross-service analytics.

This deny-list is a proposal boundary, not a claim that every field is already technically blocked in all implementations.

## 5. Field-level allowlist: required approval fields

For every event or metric admitted through controlled review, the allowlist must identify:
1. stable event/metric ID and version;
2. minimum fields, types, enum/range and whether nullable;
3. one specific operational/security/financial purpose;
4. data owner and source-of-record contract;
5. data plane: transient metric, security log, or commercial ledger;
6. accountable processor/storage and transfer region;
7. authorized readers/roles and access audit;
8. aggregation/sampling and anti-reidentification requirements;
9. collection trigger and frequency/rate limit;
10. retention period, expiry action and deletion/aggregation method;
11. account deletion / unlinking interaction and legally required exceptions;
12. prohibited joins/reuse and automated validation test IDs;
13. approval record, effective date, review/expiry date and rollback procedure.

If a required value is unknown, the event remains `NOT_ESTABLISHED` and must not be implemented as an additional persistent collection path. This rule does not disable monitoring already required by an adopted higher-authority contract.

## 6. Candidate test scenarios — not official IDs / not executed

No test IDs are allocated here. After the source authority and official Test Register binding are resolved, add only tests absent from existing controls:
- reject a proposed telemetry schema containing a prohibited payload field;
- prove operational metrics have no account/birth-data/reading-content identifiers unless a separately approved exception is bound;
- prove that SEC/recovery logs never contain recovery secrets, passwords or session tokens;
- prove commercial diagnostic correlation IDs cannot be queried as a behavioral-history/profile API;
- prove post-deletion financial records cannot be used for analytics profiling (preserve the existing PRIV-13 oracle where authoritative);
- prove expiry/deletion/aggregation behavior using exact approved retention fixtures;
- prove no analytics join combines Personal Sky, purchase/credit activity, feedback and output/content data;
- prove event/field changes fail closed if their approval/version reference is missing or expired.

The tests must have deterministic fixtures and expected database/log state; test names in this proposal are not active official IDs or evidence of execution.

## 7. Current proposal status

- Performance metric categories in Technical Contracts §24.2: **SOURCE-RECORDED**; exact measurement/storage binding is not proven by this candidate.
- Minimal security event logging: **SOURCE-RECORDED** at a broad category level; full field-level implementation proof is not established here.
- Separate product/user telemetry allowlist: **NOT ESTABLISHED**.
- Approved event additions in companion manifest: **0**.
- Retention periods, role map, aggregation, deletion contract and processor mapping for a new telemetry allowlist: **NOT ESTABLISHED**.
- Official Test Register binding / candidate-test execution: **NOT ESTABLISHED**.
- Normative source mutation, code, schema, logging config or runtime mutation: **NONE**.

This candidate preserves CE's rule that security, commerce, operational observability and product analytics are not interchangeable purposes. It does not approve a new telemetry event or authorize implementation.

End of candidate.
