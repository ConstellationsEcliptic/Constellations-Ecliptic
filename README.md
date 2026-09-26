# Constellations Ecliptic V1 — Source Foundation R1

Status: `DEVELOPMENT_CANDIDATE`
Authority: `NON_AUTHORITATIVE`
Production Source Authority: `NOT_ESTABLISHED`
Runtime Authorization: `NON_AUTHORIZED`

This repository is the first real CE source-tree implementation foundation. It is not a production-authoritative release and must not be promoted to Trusted Build merely because its tests pass.

## Governing rules

- No fabricated astronomical state.
- No silent ephemeris fallback.
- No host timezone substitution on an authoritative path.
- No commercial input may alter calculation behavior.
- Unknown/missing/mismatched runtime identity fails closed.
- Evidence is deterministic and content-addressed.
- Calculation layer does not define interpretation.

## Current implementation scope

Implemented:

- strict typed contracts using Python standard library dataclasses;
- deterministic canonical JSON serialization;
- source/evidence hashing helpers;
- circular-angle geometry;
- explicit birth-time states including zero-birth-time;
- runtime authorization gate;
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
- production Source Authority.

A missing implementation produces `NOT_IMPLEMENTED` or `NON_AUTHORIZED`; it never produces synthetic astronomical values.

## Parent evidence

The exact H8 R2 full-chain hardened package is retained under `evidence/parents/` and is bound by SHA-256 in `provenance/parent_chain.json`.

## Test command

Use:

```text
python tools/run_tests.py
```

The runner disables bytecode generation and does not create a test cache.
