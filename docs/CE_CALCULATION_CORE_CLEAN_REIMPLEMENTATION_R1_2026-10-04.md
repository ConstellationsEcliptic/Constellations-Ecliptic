# CE V1 — Calculation Core Clean Reimplementation R1

Status: controlled engineering candidate.

Owner-approved decisions:
- WIN-02: continuous multi-peak is one continuous qualifying segment containing its exact events.
- WIN-03: tangential contact does not create a Personal Window.
- Architecture: clean reimplementation against the current Source Foundation.

Current implemented hardening in this candidate:
- WIN-02/WIN-03 tests encode the approved contracts.
- EPH-01 distinguishes requested-vs-actual ephemeris flags from independent SE1 byte-integrity verification.
- Native Swiss adapter uses the centralized requested-vs-actual flag contract while retaining SWIEPH/speed-specific checks.
- Signal Engine has a fail-closed integrity gate and does not infer qualification from incomplete evidence.
- Signal result schema now reflects the implemented result object structure.

This document is intentionally outside the source-tree identity include roots and therefore is not identity-bearing under CE source_tree_sha256 policy.

No source authority, trusted build, runtime adoption, production authorization, signing, or SEAL is established by this checkpoint.
