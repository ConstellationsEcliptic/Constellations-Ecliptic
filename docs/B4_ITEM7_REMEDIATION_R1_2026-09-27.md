# CONSTELLATIONS ECLIPTIC
# B4 ITEM 7 — PROVENANCE REMEDIATION R1
Date: 2026-09-27

## Parent and identity boundary

Parent:
`5559b0f553c3816beba18f6dee36b3ca1b356b02`

Development branch:
`development/b4-item7/2026-09-27-r1`

Parent source-tree identity:
`f8ff84b2d2fd6707170c0b513bfbece79cd93e71f90fdd1cd78eb91ed895a076`

This remediation is development-only and creates a new development identity. The parent remains immutable.

## Remediation scope

### P7-1 — VALID provenance binding

VALID `CalculationResult` instances now require an explicit internal `RuntimeIdentity` binding. The six runtime identity fields must match the bound identity exactly:

- source_commit
- source_tree_sha256_v2
- dependency_lock_digest
- timezone_bundle_digest
- ephemeris_bundle_digest
- runtime_image_digest

The execution profile must also match the bound runtime identity.

The runtime identity is an internal binding input and is excluded from canonical serialized result bytes.

### P7-2 — Python/schema provenance conformance

The existing JSON Schema domain for additional provenance properties remains open by name but limited to scalar JSON values. Python validation now rejects nested mappings/sequences in extra provenance values, preventing Python acceptance of objects the schema would reject.

No closed provenance allowlist was introduced.

### P7-3 — NON-VALID provenance semantics

NON-VALID results may retain operational diagnostic provenance such as `runtime_authority=NON_AUTHORIZED`.

Identity-bearing provenance fields and `calculation_version` are forbidden on NON-VALID results. `runtime_authority=AUTHORIZED` is rejected.

This is a semantic guard, not an authority mechanism.

### P7-4 — Result → EvidencePacket edge

No new result-to-evidence field is introduced in this remediation. A formal identity edge remains a separately controlled design decision. No implicit provenance relationship is created.

## Explicit non-scope

No changes were made to:

- status.py enum values
- JSON Schema enum values
- calculation semantics
- signal semantics
- execution profile definition
- normalized-time contract
- timezone boundary
- ephemeris authority
- EvidencePacket schema/identity
- C3
- Source Authority
- Trusted Build
- Production Runtime
- SEAL
- authorization mechanism

## Verification requirement

Before closure:

- source-tree identity must be recomputed from the exact post-remediation bytes;
- manifest must be rebound only to the identity measured by verification CI;
- fresh cumulative verification must pass;
- parent identity must remain preserved;
- no authority transition may occur.

## Governance state

SOURCE_AUTHORITY = NOT_ESTABLISHED
TRUSTED_BUILD = NOT_ESTABLISHED
PRODUCTION_RUNTIME = NOT_AUTHORIZED
SEAL = NO
AUTHORIZATION = NON_AUTHORIZED
FAIL_CLOSED = TRUE

B4 Item 7 remains open until fresh verification and identity rebinding are complete.
