# CE R0 Remediation Adversarial Audit R2 — 2026-10-06

Scope: independent review of remediation head b7e5c4df7750ed8d51d8607adfe4ff815453ac22 (PR #15). This branch is audit-only and non-authoritative.

## Findings

### A1 — Public EvidencePacket.issue() remains an issuance bypass candidate
The controlled builder issue_evidence_packet() now derives input identity, profile, timezone context and runtime digest from CalculationRequest + RuntimeIdentity. However EvidencePacket.issue() remains a public classmethod that accepts a caller-supplied runtime_identity_sha256 and provenance_root_sha256. validate(require_issued=True) proves only internal consistency and content addressing; it does not prove that the runtime digest was derived from an actual RuntimeIdentity or that the packet was issued through issue_evidence_packet().

Adversarial test: tests/test_ce_r0_remediation_adversarial_r2.py::test_public_issue_path_cannot_materialize_publishable_signal_without_authoritative_request_runtime
Expected disposition against PR #15: FAIL until issuance authority is non-forgeable.

### A2 — Source identity still excludes trust-bearing control-plane paths
source_tree_sha256() hashes configs/src/tests/schemas/profiles/manifests/build/tools and pyproject.toml. It excludes .github and other arbitrary root control-plane files. A workflow-only change therefore leaves the implementation source-tree identity unchanged.

Adversarial proof: tests/test_ce_r0_control_plane_identity_scope_r2.py mutates only .github/workflows/critical.yml and requires a changed identity.
Expected disposition against PR #15: FAIL until an explicit control-plane identity is included in the authority chain (or all trust-bearing controls are included in the canonical source identity).

### A3 — CE R0 CI identity reporting is not a hard gate
.github/workflows/ce-r0-remediation-ci-r1.yml uses set +e and records SOURCE_TREE_IDENTITY_MATCH=FALSE without exiting non-zero. The workflow can therefore remain green while source-tree manifest and computed identity disagree.

This is separate from A2: even if identity scope is eventually correct, the current remediation CI does not enforce equality.

### A4 — Output validator coerces schema-invalid values
validate_claim_output() stringifies claim subject/scope/modality/tense values before membership checks. A schema-invalid integer can therefore satisfy a string allow-list. The runtime validator should reject malformed types rather than rely on a later schema layer, especially at a trust boundary.

Adversarial test: tests/test_ce_r0_output_type_strictness_r2.py.
Expected disposition against PR #15: FAIL until type strictness is enforced.

## Governance
PR #15 remains RECONCILE / DO NOT MERGE. No C3-1 disposition is requested by this audit. Current production authority state remains unchanged and fail-closed.
