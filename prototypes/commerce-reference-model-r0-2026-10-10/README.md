# CE Commerce Reference Model R0

**Classification:** isolated engineering prototype / candidate-only / non-production.

This is an executable reference model based on the characterized CE Implementation Plan §7.8 / Phase 10, Technical Contracts §21, Account & Commercial v1.7, and the limited-scope UTC service-day decision.

It is not a payment integration, approved production persistence layer, provider selection, or official CE Test Register. On 2026-10-10, the owner selected D1-A, D2-B, and the fulfillment-health interlock principle for candidate implementation. The durable record is `owner-disposition-2026-10-10.md`. The in-memory model now defaults to D1-A/D2-B; explicit overrides remain useful for counterfactual tests only. This disposition is not a normative CE document or production authorization.

## Candidate contents

- `commerce_model.py` — in-memory order, UTC-date binding, daily-slot, ledger, fulfillment, terminal non-delivery model, selected D1-A/D2-B defaults, and a fail-closed new-purchase admission gate.
- `topup_model.py` — Credits top-up model with server-owned SKU configuration, provider-observation matching, and explicit reconciliation for unknown/contradictory outcomes.
- `postgres_schema_candidate.sql` — candidate PostgreSQL schema with persistence constraints and trigger guards for SKU revision binding, provider-event identity, ledger append-only/exact restoration, current-UTC-date and health admission, a matching reserved account/date slot at the reading-debit boundary, immutable account/date slot identity, exact +1 slot-state versioning, active-order rebinding only through evidence-backed same-day D2-B reuse, rejection of slot deletion, entitlement rejection after restoration, immutable terminal non-delivery, restoration eligibility, and a deferred constraint requiring reading-debit restoration and terminal non-delivery to commit atomically.
- `test_*.py` — unit and PostgreSQL integration tests. The pull-request workflow runs them against a PostgreSQL 18.6 service with psycopg 3.3.6. PostgreSQL is a **test harness/candidate target only**, not an approved production database selection.

The in-memory dictionaries do **not** prove concurrent database uniqueness, distributed atomicity, durable webhook handling, signature verification, security, legal compliance, or production readiness. The candidate health gate requires an explicit `READY` state backed by a non-empty health-attestation reference and a future expiry; stale or missing attestations fail closed. Each transition is versioned and append-only, with the event insert atomically updating the current state; direct state updates without a matching audit event are rejected. The gate must not cancel or terminalize existing operations. The candidate imposes a provisional maximum READY lease of five minutes, and the database owns transition timestamps; this ceiling is an engineering safety guard for this prototype, not an approved production SLO or normative policy. The health source, attestation producer, production expiry/renewal cadence, monitoring, recovery behavior, operator controls, and production database privileges remain to be designed and independently reviewed. Test lease durations are fixtures. The SQL trigger guards depend on trusted application/provider-adapter validation and documented transaction ordering; this prototype is not a substitute for an independent security and database review.

Run the Python reference suite where dependencies and `CE_TEST_DATABASE_URL` are available:

```sh
python -m unittest -v
```

No normative document, official Test Register, application runtime, actual payment provider, production database, or production authorization is changed or selected by this prototype. The owner disposition is policy-level only; the PR remains isolated, draft, candidate-only, and non-production.
