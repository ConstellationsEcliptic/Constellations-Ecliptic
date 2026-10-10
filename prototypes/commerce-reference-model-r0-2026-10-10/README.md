# CE Commerce Reference Model R0

**Classification:** isolated engineering prototype / candidate-only / non-production.

This is an executable reference model based on the characterized CE Implementation Plan §7.8 / Phase 10, Technical Contracts §21, Account & Commercial v1.7, and the limited-scope UTC service-day decision.

It is not a payment integration, production persistence layer, schema decision, provider selection, or official CE Test Register. Purchase-cap trigger D1-A/D1-B and terminal non-delivery slot effect D2-A/D2-B must be supplied explicitly for simulations; this prototype does not approve either choice. Where a required policy is absent, the model avoids silently inferring an effect and blocks transitions that depend on it.

## Candidate contents

- `commerce_model.py` — in-memory order, UTC-date binding, daily-slot, ledger, fulfillment, and terminal non-delivery model.
- `topup_model.py` — Credits top-up model with server-owned SKU configuration, provider-observation matching, and explicit reconciliation for unknown/contradictory outcomes.
- `postgres_schema_candidate.sql` — candidate PostgreSQL schema with persistence constraints and trigger guards for SKU revision binding, provider-event identity, ledger append-only/exact restoration, account/date reservation, entitlement, terminal-failure evidence, and quota-release evidence.
- `test_*.py` — unit and PostgreSQL integration tests. The pull-request workflow runs them against a PostgreSQL 18.6 service with psycopg 3.3.6. PostgreSQL is a **test harness/candidate target only**, not an approved production database selection.

The in-memory dictionaries do **not** prove concurrent database uniqueness, distributed atomicity, durable webhook handling, signature verification, security, legal compliance, or production readiness. The SQL trigger guards depend on trusted application/provider-adapter validation and documented transaction ordering; this prototype is not a substitute for an independent security and database review.

Run the Python reference suite where dependencies and `CE_TEST_DATABASE_URL` are available:

```sh
python -m unittest -v
```

No normative document, official Test Register, application runtime, actual payment provider, production database, or production authorization is changed or selected by this prototype.
