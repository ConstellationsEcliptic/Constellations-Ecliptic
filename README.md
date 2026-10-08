# Constellations Ecliptic V1 — Source Foundation R1

Status: `DEVELOPMENT_CANDIDATE`
Authority: `NON_AUTHORITATIVE`
Production Source Authority: `NOT_ESTABLISHED`
Runtime Authorization: `NON_AUTHORIZED`

This repository branch is a production-source candidate snapshot for human review. It is not a production-authoritative release and must not be promoted to Trusted Build merely because its tests pass.

## Governing rules

- No fabricated astronomical state.
- No silent ephemeris fallback.
- No host timezone substitution on an authoritative path.
- No commercial input may alter calculation behavior.
- Unknown/missing/mismatched runtime identity fails closed.
- Evidence is deterministic and content-addressed.
- Calculation layer does not define interpretation.
- Non-empty identity fields are never treated as proof of runtime authority.

## Current implementation scope

Implemented:

- strict typed contracts using Python standard library dataclasses;
- deterministic canonical JSON serialization;
- source/evidence hashing helpers;
- circular-angle geometry;
- explicit birth-time states including zero-birth-time;
- runtime fail-closed boundary;
- fail-closed Swiss Ephemeris adapter boundary;
- immutable-style Evidence Packet issuance contract;
- deterministic test runner.

Not yet implemented:

- authoritative Swiss Ephemeris native adapter;
- authoritative CE production timezone bundle/runtime TZif;
- complete object registry;
- complete aspect/orb registry;
- event solver;
- Personal Window solver;
- complete Signal Engine;
- trusted production toolchain/image;
- production Source Authority;
- independently verified runtime-identity authorization mechanism.

A missing implementation produces `NOT_IMPLEMENTED` or `NON_AUTHORIZED`; it never produces synthetic astronomical values.

## Evidence boundary

Historical hardening and provenance evidence remain retained in Box. This Git repository contains the source candidate and verification tooling, not the historical evidence bundles.

## Test command

Use:

```text
python tools/run_tests.py
```

The runner disables bytecode generation and does not create a test cache.
