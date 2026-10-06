# CE-R0 ROOT RECONCILIATION MASTER R3
Date: 2026-10-06

## Candidate under reconciliation
Repository: ConstellationsEcliptic/Constellations-Ecliptic
Candidate branch: development/calculation-core-clean-reimpl-r1-privacy/2026-10-04
Candidate commit: 29239adbe2b9fc94c78550802eb856277c502cae

## Snapshot provenance
User-created source archive is retained in Box:
CE_SOURCE_CANDIDATE_29239_2026-10-06.zip
Box file id: 2508476651294
Size: 168025 bytes
Box SHA-1: 12fd64cf0a0e168f651701c9fd72abfb4f6fc16a
Raw ZIP download was unavailable to the connected Box runtime. Exact source code was therefore audited directly from the same Git commit through GitHub.

## Governance state
The normative implementation baseline is already established by controlled decision records:
Product Constitution v1.6.1 -> Implementation Plan v1.3.1 -> Technical Contracts v1.1 -> Canonical Execution Profile v1.3 / revision 4 -> Canonical Data Lock revision 4.

Candidate governance remains:
SOURCE_AUTHORITY=NOT_ESTABLISHED
TRUSTED_BUILD=NOT_ESTABLISHED
RUNTIME_ADOPTION=NOT_ESTABLISHED
FULL_RUNTIME_COVERAGE=NOT_ESTABLISHED
TZIF_RUNTIME_IDENTITY=NOT_ESTABLISHED
PRODUCTION_RUNTIME=NOT_AUTHORIZED
DUAL_APPROVAL=NOT_ESTABLISHED
SEAL=NO
AUTHORIZATION=NON_AUTHORIZED
FAIL_CLOSED=TRUE

The latest explicit C3-1 APPROVE applies to the materially earlier candidate 033e90cfd29e047578e70bbd20183e48682d7614. No fresh C3-1 disposition has been established for 29239....

## Controls positively observed
1. Runtime gate is hard fail-closed and currently always returns NON_AUTHORIZED.
2. Native Swiss data/library identities are pinned and checked before/after calculations.
3. Product boundary blocks Canon claims and AI release until downstream qualification.
4. Signal Engine reads EvidencePacket rather than recomputing astronomical state.
5. EvidencePacket deep-freezes content and computes a content hash.
6. Zero-birth scenario semantics are explicitly sampled and do not claim unsampled continuity.
7. Current candidate does not activate Canon semantic rules; canon registry remains non-materialized.
8. CalculationEngine does not currently produce production-valid astronomy; missing authority/adapter returns NON_AUTHORIZED or NOT_IMPLEMENTED.

## Root blockers

### B1 — Evidence issuance accepts caller-owned provenance
src/ce/calculation/evidence_builder.py accepts input_identity, profile_version and timezone_context as arbitrary caller mappings.
Impact: a packet can be internally well-formed while its claimed origin is wrong.
Required closure: derive these from a verified calculation/request/profile/runtime binding or require a verified issuance object.

### B2 — EvidencePacket identifier is forgeable by constructor
src/ce/calculation/evidence.py computes a content-addressed ID in issue(), but direct EvidencePacket(...) construction accepts any evidence_packet_id and does not verify that it equals the canonical content-derived ID.
Impact: packet identity is not intrinsically self-authenticating.
Required closure: canonical packet constructor only, or constructor-time proof that ID equals canonical content identity; downstream references must rely on that verified identity.

### B3 — CalculationResult and EvidencePacket lack one canonical provenance root
src/ce/calculation/contracts.py checks result provenance against a supplied RuntimeIdentity and checks packet reference/calculation id, but does not bind every provenance-bearing packet field to the same root.
Impact: individually valid artifacts can describe different execution origins.
Required closure: one canonical provenance root shared by request, result, evidence, execution profile and verified runtime identity.

### B4 — SignalResult is caller-forgeable
src/ce/signal/engine.py defines a public dataclass constructor.
impact: issue_qualified_signal_record() cannot distinguish an engine-issued qualification from a caller-constructed VALID/canon_input_valid=True result.
Required closure: sealed issuance receipt/internal type or deterministic re-derivation from packet.

### B5 — QualifiedSignalRecord is directly constructible
src/ce/signal/record.py exposes a public frozen dataclass without self-validation.
Impact: downstream code can receive an arbitrary record that only looks normative.
Required closure: issuance-only creation plus full invariant validation.

### B6 — Qualified signal identity is incomplete
signal_id is based on selected geometry identity, observation start, and a subset of calculation environment, not complete EvidencePacket content identity.
Impact: materially different evidence can collide at signal identity.
Required closure: bind signal identity to immutable EvidencePacket content hash + Signal Engine contract/version + explicit signal identity dimensions.

### B7 — environment_pin is a locally reconstructed subset
environment_pin is derived from selected packet environment fields, not the canonical RuntimeIdentity/environment identity.
Impact: runtime identity can diverge while environment_pin remains unchanged.
Required closure: pin the verified complete runtime/environment identity digest.

### B8 — Authority evaluator can authorize internally consistent synthetic evidence
src/ce/runtime/authority.py accepts caller-constructed SourceAuthorityEvidence/TrustedBuildEvidence/SignedProvenanceEvidence and returns authorized=True when fields line up.
Current safety: runtime gate still unconditionally returns NON_AUTHORIZED, so no current production authorization exists.
Required closure: separate descriptive evidence from verified authority receipts; no AUTHORIZED path may consume mere dataclass consistency.

### B9 — Native adapter trusts caller boolean authorization
src/ce/ephemeris/native_runtime.py accepts runtime_authorized: bool.
Impact: direct callers can activate the native adapter without passing a verified authority receipt.
Required closure: replace boolean with a verified authority capability/receipt that is unforgeable by ordinary application code and bound to the exact runtime identity.

### B10 — Native warning/error information is discarded
NativeSwissCalculation.to_object_record() maps warning_or_error to neither warnings nor errors.
Impact: native diagnostics can disappear before the calculation/evidence boundary.
Required closure: define exact treatment of native warning/error text and preserve it in the canonical record; a VALID state must never silently erase a calculation warning that affects interpretability.

### B11 — Daily aggregation trusts constructible QSR objects
aggregate_qualified_signal_records() checks type and canon_input_valid but not issuance provenance or packet binding.
Impact: a forged QualifiedSignalRecord can be aggregated as normative.
Required closure: aggregation must accept only verified issued records carrying a valid issuance receipt/reference.

### B12 — Source identity scope omits control-plane files
source_tree_identity.py covers configs/src/tests/schemas/profiles/manifests/build/tools and pyproject.toml, but not .github or arbitrary root control files.
Impact: a workflow/release-control mutation may leave the canonical source-tree identity unchanged.
Required closure: define and document the exact trusted control-plane identity; bind workflow/build policy files either into the canonical source identity or into a separately verified control-plane digest that is itself part of release provenance.

### B13 — Evidence JSON schema remains semantically open
schemas/evidence_packet.schema.json permits additionalProperties in input_identity, timezone_context, numerical_tolerances, solver_metadata, actual_ephemeris_resolution, calculation_flags and scenario_observations.
Impact: JSON schema shape does not close the same semantic boundary enforced by Python.
Required closure: schema-level semantic closure for identity/provenance fields and a canonical mapping between schema and Python contract.

### B14 — SignalResult schema cannot prove issuance/semantic coherence
schemas/signal_result.schema.json allows a broad combination of classification/phase/uncertainty/evidence reference/canon_input_valid.
Impact: schema validation alone can accept semantically incoherent or caller-generated signal results.
Required closure: issuance binding and cross-field conditions must be represented in the canonical contract or explicitly declared non-authoritative.

### B15 — Execution profile validation accepts untrusted sentinel strings
src/ce/runtime/profile.py checks non-empty source/build fields but accepts values such as NOT_ESTABLISHED as structurally valid strings.
Impact: structural profile validation can pass a profile that is formally unresolved.
Required closure: distinguish unresolved states from valid identity values with exact patterns/types and explicit status semantics.

### B16 — Scenario midpoint arithmetic remains a qualification boundary
src/ce/calculation/scenario_windows.py derives midpoint offsets using floating-point width followed by integer microsecond truncation.
Historical CE analysis identified microsecond boundary divergence.
Required closure: characterize the exact arithmetic contract, test pathological intervals/boundaries, and preserve divergences as evidence rather than normalizing them away.

## Non-blocking but future boundary items
- timezone_id and timezone_version need final binding to policy-owned TZIF runtime at the point of authoritative calculation;
- native cross-platform parity is not established;
- N-MID-03 native intermediate-object reproducibility remains open;
- full 1900–2100 native runtime coverage is not established;
- independent oracle requalification exists, but dedicated oracle audit upload was not established;
- final Source Authority / Trusted Build evidence is not established.

## Acceptance-test state
Added to this audit branch:
- tests/test_ce_r0_reconciliation_acceptance_r1.py
- tests/test_ce_r0_source_identity_acceptance_r1.py
- tests/test_ce_r0_additional_acceptance_r1.py
- tests/test_ce_r0_native_authorization_acceptance_r1.py

These tests are intended to fail against the current candidate where the invariant is not yet implemented. They are audit guardrails, not production authorization.

## Remediation order
1. Canonical provenance root and issuance receipts (B1-B8).
2. Native runtime activation capability boundary and diagnostic preservation (B9-B10).
3. Downstream issuance enforcement (B11).
4. Identity/control-plane closure (B12-B15).
5. Numerical/time-contract characterization (B16).
6. Full suite, cross-platform/native evidence, source identity, and build/reproducibility requalification.
7. Produce a fresh candidate identity/scope record.
8. Request fresh C3-1 candidate disposition for the final reconciled candidate.

## Explicit non-authority statement
This record does not authorize source authority, trusted build, runtime adoption, production runtime, dual approval, or SEAL.
