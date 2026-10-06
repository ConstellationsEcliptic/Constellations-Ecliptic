# CE-R0 REMEDIATION ARCHITECTURE R1
Date: 2026-10-06
Scope: CE-R0 provenance, issuance, runtime, schema and CI boundaries
Status: DESIGN / NON-AUTHORITATIVE

## Objective
Move CE from "internally consistent data structures" to "verified derivation chain".

Hard invariant:
A downstream object must not be treated as authoritative merely because it is well-shaped or internally consistent.

## R1 — Canonical provenance root

Define a single immutable ProvenanceRoot containing:
- calculation_request_id
- profile identity and revision
- source commit
- source-tree implementation identity
- control-plane identity
- dependency lock identity
- runtime/environment identity
- timezone bundle identity
- ephemeris bundle identity
- calculation version

All release-affecting records must bind to this exact root.

No function may accept free-form replacement provenance fields once the root exists.

## R2 — Evidence issuance

EvidencePacket must have one canonical issuance path.
Direct construction should either be private/internal or perform the same content-addressed identity proof as the issuance path.

The canonical evidence_packet_id must be derived from canonical packet content and verified at construction/verification time.

EvidencePacket references must identify both the ID and the content hash.

## R3 — CalculationResult binding

CalculationResult finalization must require:
- verified RuntimeIdentity
- verified EvidencePacket
- equality of the provenance root represented by both
- calculation_id equality
- execution profile equality

A valid result with an unrelated packet provenance context must be impossible.

## R4 — Signal issuance

SignalResult should become an internal/issued artifact, not a general-purpose authority-bearing constructor.

Preferred boundary:
SignalEngine.evaluate(packet) returns a sealed/issued result carrying:
- exact packet reference
- signal-engine contract/version
- canonical provenance root
- qualification outcome

QualifiedSignalRecord issuance should consume the issued result or deterministically re-derive the qualification from the packet. It should not accept caller-created qualification state.

## R5 — Qualified Signal identity

signal_id = canonical hash over:
- verified EvidencePacket content identity
- Signal Engine contract/version
- explicit signal identity dimensions

Do not derive identity from a subset of evidence.

environment_pin must be the canonical verified runtime/environment identity digest, not a local subset.

## R6 — Downstream aggregation

Daily aggregation must accept only verified issued QualifiedSignalRecords.
A raw dataclass instance is not enough.

## R7 — Authority separation

Split authority code into two concepts:
1. consistency evaluation — useful for diagnostics; never grants authority
2. authority verification — consumes a verified receipt/capability backed by controlled governance artifacts

Future AUTHORIZED state must never be reachable from caller-constructed SourceAuthorityEvidence/TrustedBuildEvidence/SignedProvenanceEvidence alone.

## R8 — Native runtime capability

Replace NativeSwissEphemerisAdapter(runtime_authorized: bool) with a verified runtime capability/receipt bound to:
- exact source identity
- exact build identity
- exact runtime identity
- exact ephemeris identity

The adapter must not self-authorize or trust a boolean supplied by application code.

## R9 — Native diagnostics

Native warnings/errors must have an explicit contract:
- warning preserved in canonical record when non-terminal
- error preserved in canonical error state when terminal
- no diagnostic may silently disappear between native call and EvidencePacket

The canonical severity mapping must be deterministic and tested.

## R10 — Schema closure

Python and JSON Schema must describe one contract.

EvidencePacket critical mappings should not remain arbitrary bags where semantic identity matters.
SignalResult schema must describe issuance/reference invariants or be explicitly declared non-authoritative.
Claim output schema must be identical in structure and required fields to the runtime validator.

## R11 — Claim output verifier

The release path must not depend on caller-selected SemanticConformanceCheck callbacks.

Use a CE-owned verifier with deterministic parsing/rule evaluation.
If semantic verification is unavailable, release remains forbidden.

Structured fields:
subject, scope, modality, tense, epistemic layer, certainty, evidence refs and numeric refs
must be present and checked against the Allowed Claim Manifest.

## R12 — Source/control-plane identity

Define two explicit identities if needed:
A. implementation source identity
B. trusted control-plane identity

The source identity scope must cover every file whose mutation can change:
- calculation behavior
- signal qualification
- release semantics
- build procedure
- workflow enforcement
- trust boundary

At minimum, .github workflow/control files cannot remain silently outside the trusted identity chain.

## R13 — CI hard gates

Candidate CI must:
1. compute exact source identity
2. verify it against manifest
3. verify control-plane identity
4. compile
5. run unit/regression suite
6. run adversarial issuance/provenance suite
7. fail on any identity mismatch

A compute-only success is not an identity pass.

## R14 — GitHub governance

Before authority establishment:
- main branch protection must be enabled
- required status checks must be enforced
- repository rulesets should protect release/source branches as appropriate
- workflow token permissions should be minimal
- supply-chain-sensitive actions should be pinned to immutable commit SHAs

These are repository governance controls, separate from CE application semantics.

## R15 — Temporal contract

Choose and document one exact temporal identity contract before normalization:
- arithmetic precision
- midpoint lattice construction
- canonical timestamp precision
- event-time precision
- serialization precision

A microsecond-bearing input must not collapse to second precision unless the normative contract explicitly says so.

## R16 — Requalification order

After source remediation:
1. exact source identity
2. schema/runtime contract alignment
3. provenance/issuance adversarial suite
4. full existing regression suite
5. native runtime controlled verification
6. TZIF controlled verification
7. cross-platform parity
8. build reproducibility
9. fresh candidate identity/scope package
10. fresh C3-1 human disposition

## Prohibited shortcuts
- no hand-editing a digest to match CI
- no trusting a green test suite as provenance proof
- no authority through object construction
- no caller-supplied semantic verifier as release authority
- no fallback to host timezone or alternate ephemeris
- no narrative rescue of numerical mismatches
- no inheritance of earlier C3-1 approval by lineage alone
