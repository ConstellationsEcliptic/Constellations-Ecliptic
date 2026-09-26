# CONSTELLATIONS ECLIPTIC
# B4 ITEM 8 — CONTRACT CONSTRUCTOR / STATE-INTEGRITY REMEDIATION R1
Date: 2026-09-27

## Parent and development boundary

Parent:
`8d4f0915a7c3279cbaee495bd6b0b9aa67de675e`

Development branch:
`development/b4-item8/2026-09-27-r1`

The parent remains immutable. This remediation is development-only.

## Scoped remediation

### F8-1 — CalculationResult constructor closure

`CalculationResult.__post_init__()` now rejects every validation error returned by `validate()`.

Invalid-result construction is therefore closed at the contract boundary. The engine's invalid-input result path emits a contract-closed result representation using the canonical execution profile and a deterministic fallback request identifier when the incoming request identifier is unusable.

### F8-2 — ObjectState constructor closure

`ObjectState.__post_init__()` now rejects every validation error, including on NON-VALID states.

### F8-3 — TimeResolution constructor closure

`TimeResolution.__post_init__()` now rejects every validation error, including contradictory NON-VALID combinations.

### F8-4 — BirthInput / CalculationRequest closure

Both constructors now enforce `validate() == empty tuple` before an instance can exist.

CalculationRequest explicitly validates that `birth` is a BirthInput before delegating to its validation.

### F8-5 — Python/schema parity

The existing CalculationResult schema semantics remain unchanged. Regression tests now cover constructor closure for the same state-invalid combinations represented by the current schema semantics.

No enum or new semantic state domain was introduced.

### F8-6 — Packaging/source-tree boundary review

Reviewed `build/build_source_tree_hash.py` and `tools/package_source.py`.

Current finding:
- source-tree hashing excludes `evidence/` and `provenance/`;
- packaging utility does not exclude those directories;
- neither directory exists in the current Git tree;
- no current identity collision is therefore established.

No hash-scope change is made. The asymmetry remains a documented secondary hardening observation for a separately controlled identity-policy decision.

## Adversarial regression coverage

Added coverage for:
- NON-VALID CalculationResult invalid request_id
- NON-VALID CalculationResult non-canonical execution_profile_id
- NON-VALID CalculationResult malformed normalized_time
- NON-VALID CalculationResult containing VALID ObjectState
- NON-VALID ObjectState invalid object_id
- NON-VALID ObjectState non-finite numeric field
- invalid BirthInput construction
- invalid CalculationRequest construction
- NON-VALID TimeResolution contradictory state
- NON-VALID TimeResolution missing error
- existing Python/schema parity and fail-closed engine tests

## Non-scope

No changes to:
- CalculationStatus or ScenarioState values
- execution profile definition
- normalized-time contract
- timezone authority
- ephemeris implementation/authority
- provenance authority mechanism
- EvidencePacket
- C3
- Source Authority
- Trusted Build
- Production Runtime
- SEAL
- main
- approved candidate snapshot

## Acceptance targets

CONTRACT_CONSTRUCTOR_CLOSURE = PASS
NONVALID_STATE_INTEGRITY = PASS
PYTHON_SCHEMA_STATE_PARITY = PASS
ADVERSARIAL_CONTRACT_TESTS = PASS
PACKAGING_IDENTITY_BOUNDARY = REVIEWED
PARENT_IDENTITY = PRESERVED
NO_AUTHORITY_TRANSITION = CONFIRMED

Final source-tree identity must be measured by CI after all remediation bytes are fixed, and the manifest must be rebound only to that measured identity.

Current governance:
SOURCE_AUTHORITY=NOT_ESTABLISHED
TRUSTED_BUILD=NOT_ESTABLISHED
PRODUCTION_RUNTIME=NOT_AUTHORIZED
SEAL=NO
AUTHORIZATION=NON_AUTHORIZED
FAIL_CLOSED=TRUE
C3-2=PERFORMED / BLOCKED
C3-3=CLOSED
