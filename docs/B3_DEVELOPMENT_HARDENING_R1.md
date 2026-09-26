# CE B3 Development Hardening R1

## Boundary

Status: `DEVELOPMENT_CANDIDATE`

Parent approved candidate snapshot:

`804036f843a56d0029ceea08af35247d28cbde7e`

Development branch:

`development/b3-hardening-2026-09-27-r1`

This branch is intentionally a new source identity. The parent approved candidate snapshot is not modified.

## Hardening implemented

The runtime authorization gate now explicitly validates the runtime-identity object before evaluating identity fields.

Malformed identity input is required to produce:

```text
authority = NON_AUTHORIZED
```

with deterministic reason codes, rather than raising an exception that a caller could mis-handle.

Covered cases:

- wrong runtime-identity object type;
- missing/blank execution-profile identity;
- invalid execution-profile revision type/value;
- missing or non-string identity fields.

## Non-escalation invariant

The hardening does not and must not establish any production-chain state.

```text
SOURCE_AUTHORITY     = NOT_ESTABLISHED
TRUSTED_BUILD        = NOT_ESTABLISHED
PRODUCTION_RUNTIME   = NOT_AUTHORIZED
SEAL                 = NO
AUTHORIZATION        = NON_AUTHORIZED
FAIL_CLOSED          = TRUE
```

## Candidate identity rule

Any subsequent source modification produces a new commit and therefore a new candidate identity. No development branch may be described as candidate `804036f...` itself.

## Next B3 work

Further B3 engineering should extend calculation-core hardening only from evidenced contracts and should not manufacture missing production authority, signer, trust-root, or trusted-build material.
