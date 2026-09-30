# CE V1 — Controlled Runtime Reconciliation R1

Date: 2026-09-30
Base candidate:
- Branch: candidate/trusted-build-hardening/2026-09-29-r3
- HEAD: 033e90cfd29e047578e70bbd20183e48682d7614
- Source-tree SHA-256 at entry: da6a1d622940a4674a54d98656a940aee90aa32ec149ec9b0e8800e467a90ad9

## Human disposition

C3-1 = RECONCILE

This audit branch exists solely for controlled reconciliation and evidence production.
It does not promote source authority, trusted-build authority, production runtime,
dual approval, or SEAL.

## Canonical identity retained

- Lock: CE-V1-CANONICAL-DATA-2026D-SE-V2.10.3BFINAL
- Revision: 4
- Lock SHA-256: 0309a9d9385925f2c5eda478e2a7704e8600cf10abf258a8bcc9c4bdcb7689a2
- Swiss commit: f4dcd18e8005dde95fd8a8d2312ed12f9accd1b0
- Swiss tree: f06fbd2b4608e87f7874e67e732bbc444abccba1
- Swiss aggregate checksum: 0cfc76a9dc51296f2241492e3376f1e71d13dd4f36b476253d4b82df57dfc990

## Reconciliation findings entering R1

1. Native runtime execution evidence is not yet established on the operator machine.
2. The hardened native-runtime package exists as a retained derived artifact, but
   its internal SHA256SUMS manifest contains stale values for a subset of current
   package files and uses nonstandard path/hash ordering.
3. Runtime TZif derived identity is not yet established.
4. 1900–2100 execution coverage is not established.
5. Cross-platform parity is not established.
6. Full Calculation Core production fixture/test gate is not established.
7. IANA cryptographic signature verification is recorded as valid, while operational
   trust remains a separate human governance decision and is still pending.

## Required evidence before technical gates can close

- Exact native Swiss library bytes bound to the expected DLL hash.
- Controlled ephemeris data bytes bound to the canonical hashes.
- Derived TZif manifest produced from the verified IANA source, not host timezone data.
- Runtime identity manifest matching the canonical lock/profile.
- Actual execution evidence for the defined range probes and all required runtime tests.
- Deterministic oracle evidence with explicit expected/actual state.
- Parity evidence for the required execution environments.
- Fresh authority-graph verification after runtime adoption evidence exists.

## Hard controls

- No hand-created runtime coverage report.
- No synthetic PASS evidence.
- No host-timezone substitution.
- No Moshier/network fallback.
- No canonical hash modification.
- No mutation of frozen historical evidence.
- No SEAL.
- No Production Runtime authorization.
- Fail closed on missing or ambiguous evidence.

## Current governance

SOURCE_AUTHORITY = NOT_ESTABLISHED
TRUSTED_BUILD = NOT_ESTABLISHED
PRODUCTION_RUNTIME = NOT_AUTHORIZED
DUAL_APPROVAL = NOT_ESTABLISHED
SEAL = NO
AUTHORIZATION = NON_AUTHORIZED
FAIL_CLOSED = TRUE
