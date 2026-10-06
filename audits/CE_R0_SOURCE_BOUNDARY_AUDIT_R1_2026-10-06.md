# CE-R0 SOURCE BOUNDARY AUDIT — R1
Date: 2026-10-06
Candidate commit: 29239adbe2b9fc94c78550802eb856277c502cae
Candidate branch: development/calculation-core-clean-reimpl-r1-privacy/2026-10-04
Governance disposition: NON-AUTHORITATIVE / NOT PRODUCTION / FAIL-CLOSED

## Source snapshot provenance
A user-created source archive for candidate 29239adbe2b9fc94c78550802eb856277c502cae was uploaded to Box:
- file: CE_SOURCE_CANDIDATE_29239_2026-10-06.zip
- Box file id: 2508476651294
- size: 168025 bytes
- Box SHA-1: 12fd64cf0a0e168f651701c9fd72abfb4f6fc16a
The archive is treated as a source snapshot reference only; Box download of raw ZIP was unavailable to the connected runtime, so code audit was performed against the exact same Git commit via GitHub.

## Positive controls verified
1. Runtime gate is fail-closed and always returns NON_AUTHORIZED. Identity presence does not constitute authority.
2. Native Swiss Ephemeris adapter pins library/data identities, rejects Moshier/alternate data paths, validates requested/actual flags, and rechecks canonical data before and after calculation.
3. Product boundary blocks Canon claims and AI release even for VALID calculations until downstream qualification exists.
4. Signal Engine consumes EvidencePacket as read-only numerical input and does not recompute astronomical coordinates.
5. EvidencePacket is deeply frozen, validates canonical JSON domain, and provides a content hash/reference.
6. Zero-birth scenario semantics are explicitly bounded to sampled uncertainty; the code does not claim unsampled continuous birth-time certainty.

## Root blockers

### B1 — Evidence issuance provenance is caller-supplied
File: src/ce/calculation/evidence_builder.py
issue_evidence_packet() accepts input_identity, profile_version, and timezone_context as caller-supplied mappings. These values are not derived or cross-checked against an authoritative CalculationRequest/runtime/profile binding.
Risk: a structurally valid packet can carry a false provenance context while remaining internally valid.
Required remediation: derive authoritative identity/context from the verified calculation/request/runtime chain; reject caller-provided substitutes except through a separately verified binding object.

### B2 — CalculationResult does not bind EvidencePacket provenance
File: src/ce/calculation/contracts.py
CalculationResult verifies runtime provenance against a supplied RuntimeIdentity and verifies EvidencePacket reference/content, but the implementation does not establish equality between the packet's provenance-bearing fields and the result/runtime provenance root.
Risk: individually valid records may have different provenance roots while remaining independently well-formed.
Required remediation: define one canonical provenance root and require result, packet, request, profile, and runtime identity to resolve to that exact root.

### B3 — SignalResult is forgeable as a direct dataclass
File: src/ce/signal/engine.py
SignalResult has a public constructor. issue_qualified_signal_record() accepts any SignalResult instance and checks status/ref/field presence, but does not prove that SignalEngine.evaluate() issued the supplied result.
Risk: a caller can construct a VALID SignalResult with canon_input_valid=True and an otherwise matching packet reference.
Required remediation: use an issuance receipt/token, sealed internal result type, or deterministic re-derivation from packet such that QSR issuance cannot accept caller-invented qualification state.

### B4 — QualifiedSignalRecord is directly constructible and insufficiently self-validating
File: src/ce/signal/record.py
QualifiedSignalRecord is a public frozen dataclass with no __post_init__ validation.
Risk: arbitrary records can be instantiated and passed to downstream aggregation as if normatively issued.
Required remediation: make canonical construction issuance-only; validate all invariants at the boundary; carry immutable issuance/provenance evidence.

### B5 — Qualified signal identity is incomplete
File: src/ce/signal/record.py
signal_id is derived from a selected geometry identity, observation start, and a subset of calculation-environment values. It is not bound directly to the complete immutable EvidencePacket content identity.
Risk: materially different evidence packets can potentially produce the same signal identifier.
Required remediation: bind signal identity to EvidencePacket content SHA plus Signal Engine contract/version and explicitly defined signal dimensions.

### B6 — environment_pin is not the full runtime identity
File: src/ce/signal/record.py
environment_pin is derived from a subset of packet calculation-environment fields and does not directly cover the complete RuntimeIdentity dimensions such as source commit/tree, dependency lock, native runtime identity, or full environment identity.
Required remediation: use the canonical runtime/environment identity digest rather than a locally reconstructed subset.

### B7 — Authority evaluation is a consistency checker, not an external proof
File: src/ce/runtime/authority.py
SourceAuthorityEvidence, TrustedBuildEvidence, and SignedProvenanceEvidence are direct dataclasses. evaluate_full_authority() can return authorized=True from internally consistent caller-supplied evidence.
Current safety: src/ce/runtime/gates.py still hard-fails to NON_AUTHORIZED, so no present production authorization is established.
Required remediation before any future AUTHORIZED path: separate descriptive evidence from verified authority receipts; require independently verified artifacts/attestations whose identities are bound to controlled records, not merely caller-constructed dataclasses.

### B8 — Source identity must be re-established on the exact candidate
Candidate manifest currently records source-tree identity:
845bd67d5e68c842b3107c4f95a4c803aa86489d767b462f27ac2c6ade63f2ab
This value is not accepted as proof by itself. Prior CI history contains source-identity divergences across different candidate/merge refs.
Required remediation: perform a controlled exact-commit source-tree identity computation and reconcile the manifest only after the calculation method, include set, and candidate ref are fixed.

### B9 — Scenario-time arithmetic remains a qualification item
File: src/ce/calculation/scenario_windows.py
Scenario midpoint construction uses integer microsecond arithmetic after floating-point width calculation. Historical CE analysis has identified sensitivity/divergence around microsecond truncation.
Required remediation: characterize the contract explicitly, add boundary tests, and do not normalize differing values merely to force parity.

## Governance
This audit does not establish:
- source authority
- trusted build
- runtime adoption
- cross-platform native parity
- full runtime coverage
- TZIF runtime authority
- production authorization
- dual approval
- SEAL

The current CE hard boundary remains FAIL-CLOSED.

## Next remediation order
1. Close provenance root and issuance boundaries (B1-B7).
2. Re-establish exact source identity (B8).
3. Resolve numerical/temporal contract characterization (B9).
4. Re-run complete test and controlled verification suite.
5. Produce a fresh candidate identity/scope package.
6. Only then request a fresh human C3-1 disposition for the resulting candidate.

No source remediation is included in this audit file.
