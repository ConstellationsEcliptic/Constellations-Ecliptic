# CE V1 — B3 DEVELOPMENT HARDENING GAP ASSESSMENT R1

Date: 2026-09-27

Baseline under inspection:

- Approved candidate snapshot: `804036f843a56d0029ceea08af35247d28cbde7e`
- Candidate source identity: `19fa6954b8fcadcbaa0c69de7426c817d756c5aa4d5d1e383a0acf7fb45c15db`
- Candidate branch: `production-candidate/2026-09-26-r1`
- Governance state remains development-only and fail-closed.

## Verified baseline

The approved candidate is an immutable review snapshot. It is 8 commits ahead of main and remains unmerged. The commit is unsigned at GitHub's commit-verification layer. The repository exposes no readable branch-protection configuration through the current integration; that evidence remains NOT_ESTABLISHED.

The implementation intentionally contains no authoritative astronomical calculation path. Runtime authorization is fail-closed, the Swiss Ephemeris adapter is a non-authorizing placeholder, the timezone resolver does not use host zoneinfo as authority, and canon/signal boundaries do not fabricate values.

## Concrete B3 findings

### F1 — Evidence identity was only shallowly immutable

The dataclass was frozen, but nested dictionaries remained mutable. A caller could mutate an EvidencePacket's nested data after issuance and thereby change its canonical bytes and content hash.

Classification: IMPLEMENTATION DEFECT / HIGH INTEGRITY RISK.

### F2 — Runtime identity shape was not validated

Runtime identity fields were treated as present/absent only. Commit, SHA-256, image-digest, and canonical execution-profile shapes were not explicitly validated.

Classification: IMPLEMENTATION HARDENING GAP / HIGH LATENT AUTHORITY RISK.

### F3 — Verification tooling did not chain source identity verification

`verify_foundation.py` checked selected files and tests but did not require the declared source-tree identity to match the actual source tree, nor did it re-run build-input hygiene after the test runner.

Classification: VERIFICATION GAP / HIGH RELEASE-INTEGRITY RISK.

### F4 — Authorized-path profile mismatch boundary was implicit

CalculationEngine checked the runtime gate but did not explicitly reject a request using a different execution profile from the runtime identity. The current gate masks this path by always returning NON_AUTHORIZED, but a future authorized path would otherwise be exposed.

Classification: IMPLEMENTATION DEFECT / HIGH LATENT AUTHORITY RISK.

### F5 — Negative-path coverage was incomplete

Existing tests covered basic fail-closed behavior but did not cover malformed identity fields, unsupported canonical serialization types, non-string object keys, nested evidence mutation, or authorized-path profile mismatch.

Classification: TEST COVERAGE GAP.

## B3 R1 remediation set

Implemented on a NEW development branch:

1. Strict canonical-serialization input domain.
2. Explicit RuntimeIdentity shape validation and canonical profile constants.
3. Runtime gate integration of identity-shape checks while preserving unconditional authority blockers.
4. Authorized-path execution-profile consistency check.
5. Deep-frozen EvidencePacket payload plus cached issuance-time canonical bytes.
6. Stronger foundation verifier: source identity, build-input hygiene, required identity files, and exact governance invariants.
7. Expanded negative-path tests.
8. Development-only verification workflow; workflow evidence is not an authority root.

## Non-remediated boundaries

This B3 pass does not establish:

- Production Source Authority.
- Production signer/keyring/trust root.
- Signed Source Authority attestation.
- Independent authority verification.
- Trusted Build.
- Production Runtime.
- Complete astronomical Calculation Core.
- C3-3 eligibility.
- SEAL.
- AUTHORIZATION.

C3-2 remains PERFORMED / BLOCKED and C3-3 remains CLOSED.

## Identity boundary

`804036f...` remains unchanged.

All B3 changes are placed on a new development identity derived from the approved snapshot. The resulting commit must be treated as a new candidate identity and must not inherit C3-1 approval.

## Required verification

The new identity must pass:

- source-tree SHA-256 verification;
- build-input hygiene before and after test execution;
- full deterministic test suite;
- fresh checkout/workflow verification where available.

The source identity manifest is intentionally recomputed only after the complete B3 change set is fixed. No production authority claim may be inferred from a passing B3 verification.

