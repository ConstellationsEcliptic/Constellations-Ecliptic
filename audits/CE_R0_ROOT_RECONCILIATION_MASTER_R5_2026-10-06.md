# CE-R0 ROOT RECONCILIATION MASTER R5
Date: 2026-10-06

## Candidate and evidence
Candidate commit: 29239adbe2b9fc94c78550802eb856277c502cae
Candidate branch: development/calculation-core-clean-reimpl-r1-privacy/2026-10-04
Candidate CI run: 37308224511
Candidate computed SOURCE_TREE_SHA256_V2: 22616659b86823e96340ff032c17a64280fb97b3fdb3a801e0a0b2c7ed8c4498
Candidate manifest value: 845bd67d5e68c842b3107c4f95a4c803aa86489d767b462f27ac2c6ade63f2ab
Candidate source identity: NOT ESTABLISHED (hard mismatch)

User source ZIP in Box:
CE_SOURCE_CANDIDATE_29239_2026-10-06.zip
Box id 2508476651294
Size 168025 bytes
SHA-1 12fd64cf0a0e168f651701c9fd72abfb4f6fc16a

## Executable audit evidence
Audit branch: audit/ce-r0-reconciliation-r1/2026-10-06
Latest audit probe commit at this record: 8e09b07bbe29dc175880aa70f838e3520f8d827d
Probe workflow: run 37402636434
Probe result: SUCCESS
Probe-confirmed findings: B1, B2, B3, B4, B5, B6, B7, plus direct packet-ID weakness.
Regression suites in probe: 39 tests PASS.
Probe source identity on audit branch: actual 3fdd08d01a692f980052d124d1b7d09a33813f5f9cdfe3561f257ea004149f95 vs manifest 845bd67d5e68c842b3107c4f95a4c803aa86489d767b462f27ac2c6ade63f2ab.

Important: the 3fdd... audit-branch identity is not the candidate identity. The exact candidate 29239... independently computed 22616659... in run 37308224511.

## Governance evidence
GitHub API reports:
- main branch protected: false
- required status checks: none
- repository rulesets: []
The connected integration cannot read the detailed branch-protection endpoint (403), but the branch object itself explicitly reports protected=false and no rulesets exist.

Consequence: GitHub currently does not provide an enforceable repository-level boundary preventing direct mutation/merge of protected source lines. CE governance remains independently fail-closed, but repository governance is not yet an authority control.

## Root blockers
B1 caller-supplied Evidence issuance provenance — CONFIRMED
B2 EvidencePacket ID direct-constructor forgeability — CONFIRMED
B3 CalculationResult/EvidencePacket provenance-root mismatch — CONFIRMED
B4 SignalResult direct forgery — CONFIRMED
B5 QualifiedSignalRecord direct construction — CONFIRMED
B6 incomplete signal identity binding — CONFIRMED
B7 environment_pin incomplete runtime binding — CONFIRMED
B8 synthetic authority evidence can evaluate authorized — CONFIRMED
B9 native adapter accepts caller boolean authorization — CONFIRMED by API inspection
B10 native warning/error information dropped — CODE REVIEW FINDING
B11 daily QSR aggregation accepts constructible records — CONFIRMED
B12 source identity excludes control-plane files — CODE REVIEW FINDING
B13 EvidencePacket JSON schema semantically open — CODE REVIEW FINDING
B14 SignalResult schema lacks issuance/coherence proof — CODE REVIEW FINDING
B15 execution-profile validation accepts unresolved sentinel strings — CODE REVIEW FINDING
B16 scenario midpoint arithmetic needs contract characterization — HISTORICAL TECHNICAL FINDING
B17 candidate CI provenance verification incomplete — CONFIRMED
B18 GitHub repository protection/ruleset enforcement absent — CONFIRMED

## Candidate CI fact
Run 37308224511 on exact 29239... was green:
- source identity computation step: PASS
- full unittest suite: 223 PASS
- source identity verification step: ABSENT
Therefore green CI does not establish source-tree identity.

## PR14 downstream status
PR #14 remains OPEN / RECONCILE — DO NOT MERGE.
Its downstream audit also found schema/runtime contradiction and caller-supplied semantic conformance callback. No Canon rule registry is activated.

## Remediation order
R1 Canonical provenance root and issuance-only capabilities.
R2 Remove direct constructor authority paths and caller boolean/native activation.
R3 Preserve diagnostics and make downstream aggregation consume verified issued records only.
R4 Align Python contracts and JSON schemas.
R5 Establish complete source/control-plane identity and mandatory identity verification CI.
R6 Pin CI actions, minimize workflow permissions, and establish main branch protection/rulesets.
R7 Characterize numerical/time edge cases and rerun full tests.
R8 Requalify native runtime, TZIF, cross-platform parity and build reproducibility.
R9 Produce a fresh candidate identity/scope package.
R10 Request fresh C3-1 disposition only for the final reconciled candidate.

## Non-authority
No source authority, trusted build, runtime adoption, production authorization, dual approval, or SEAL is established.
