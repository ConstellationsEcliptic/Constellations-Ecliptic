# CE R0 Remediation Adversarial Audit R3 Addendum — 2026-10-06

Additional residual blockers found by source review against PR #15 head b7e5c4df7750ed8d51d8607adfe4ff815453ac22.

### A7 — Execution profile sentinel values remain structurally accepted
configs/runtime_profile.dev.json contains source/build identity sentinels (NOT_ESTABLISHED / NOT_ESTABLISHED_AFTER_HARDENING), while validate_execution_profile() accepts any non-empty strings for those fields. Identity-bearing profile validation must reject unestablished sentinel values and require format/semantic conformity.

### A8 — canonical_utc() collapses distinct subsecond instants
scenario_windows.canonical_utc() uses timespec="seconds" despite the CE time contract permitting microseconds. Two distinct subsecond instants canonicalize to the same string, creating deterministic identity/ordering ambiguity.

### A9 — EvidencePacket schema leaves critical provenance/calculation maps open
evidence_packet.schema.json permits additionalProperties=true for input_identity, timezone_context, numerical_tolerances, solver_metadata, actual_ephemeris_resolution, calculation_flags and scenario_observations. The Python boundary is stricter in some places, but the canonical schema should not permit undefined trust-bearing fields.

### Audit status
These are separate from A1-A6 and should be fixed before any fresh C3-1 review.

Governance remains fail-closed and non-authoritative.
