# CE V1 — B4 Item 6 Remediation R1

Date: 2026-09-27

## Scope

Remediation is limited to the verified regression-control gap identified by the B4 Item 6 read-only assessment.

Parent:
`34560a6c945a5d4c873758a871d3f8ec2564eaba`

Development branch:
`development/b4-item6/2026-09-27-r1`

## Finding

Current serialized enum values already correspond:

- `CalculationResult.status` ↔ `CalculationStatus`
- `CalculationResult.object_states[].status` ↔ `CalculationStatus`
- `CalculationResult.scenario_state` ↔ `ScenarioState`
- `SignalResult.status` ↔ `CalculationStatus`

The missing control was explicit regression coverage for the nested calculation object status and signal status, plus protection against a future schema list drifting from the Python enum.

## Remediation

Added regression assertions in `tests/test_schema_contracts.py` to require:

1. calculation root status enum equals `CalculationStatus`;
2. calculation object status enum equals `CalculationStatus`;
3. signal status enum equals `CalculationStatus`;
4. ScenarioState correspondence remains asserted;
5. signal non-VALID conditional enum values remain a subset of `CalculationStatus`.

No enum definition, schema value, calculation semantics, execution profile, provenance contract, timezone authority, ephemeris authority, C3 state, or production authority mechanism was changed.

## Governance boundary

This remediation is development-only.

`804036f...` remains immutable and untouched.

`main` remains untouched.

No signing, promotion, authority transition, trusted-build transition, production authorization, SEAL, or C3-3 opening is performed.

Required authority state remains:

```
SOURCE_AUTHORITY      = NOT_ESTABLISHED
TRUSTED_BUILD         = NOT_ESTABLISHED
PRODUCTION_RUNTIME    = NOT_AUTHORIZED
SEAL                  = NO
AUTHORIZATION         = NON_AUTHORIZED
FAIL_CLOSED           = TRUE
```

## Verification requirement

The branch must pass fresh CI with:

- exact checkout identity binding;
- source-tree identity verification;
- full deterministic test suite;
- build-input hygiene before and after tests.

The source-tree manifest is rebound only after the complete remediation/documentation set is fixed.
