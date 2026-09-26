# CE V1 — B3 R2 REMEDIATION EXECUTION RECORD

Date: 2026-09-27

Baseline:
- B3 R1 development identity: 0af6028b3b853b51980c3e7a7abf8103c8755f4b
- Approved candidate snapshot: 804036f843a56d0029ceea08af35247d28cbde7e
- R2 branch: development/b3-hardening/2026-09-27-r2

R2 remediation scope:
- Contract-state invariants for CalculationResult, ObjectState, SignalResult, BirthInput, CalculationRequest, and TimeResolution.
- Immutable CalculationResult and SignalResult issuance state.
- True immutable mapping representation for nested evidence/provenance.
- Total RuntimeIdentity input handling.
- Explicit ephemeris request validation.
- JSON-schema alignment and strict additional-properties policy.
- Source-tree identity independent of host filesystem mode bits.
- PR-head checkout identity binding.
- Development verification toolchain pinning.

Governance boundary:
- DEVELOPMENT_CANDIDATE only.
- Source Authority not established.
- Trusted Build not established.
- Production Runtime not authorized.
- SEAL=NO.
- AUTHORIZATION=NON_AUTHORIZED.
- FAIL_CLOSED=TRUE.

This record does not authorize promotion, signing, attestation, production runtime, or C3-3.
