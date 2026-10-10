# CONSTELLATIONS ECLIPTIC
# B1 RESEARCH-CANDIDATE IDENTITY GATE AND WORKFLOW TRIGGER RECONCILIATION
Date: 2026-10-11
Record: R0
Classification: CANDIDATE TECHNICAL / CONTROL-PLANE AUDIT / NON-NORMATIVE
Authority effect: NONE
Normative / official Test Register / production code / A9 identity mutation: NONE
A10 / Source Authority / Trusted Build / Runtime Adoption / merge / release / production / SEAL effect: NONE

## 1. Executive findings

This review separates two findings that had previously appeared together as broader CI failures on PR #32:

1. **The A9 identity mismatch is expected for a research candidate that is not the exact A9 source/control-plane tree.** The candidate continues to carry the preserved A9 identity manifests. The computed hashes include source/tests/schema/tool inputs and control-plane workflow bytes; the PR #32 candidate changes identity-bearing inputs. Broader CI and Trusted Build A9 correctly fail closed before downstream stages. Do not change the manifest to the candidate's observed hash and do not attribute the identity failure to the targeted test result.
2. **The dedicated B1 prototype workflow had a genuine trigger-coverage defect.** Its push branch filter named the earlier `research/b1-geometry-rule-binding-r0-2026-10-10` branch, not the current `research/b1-geometry-binding-single-identity-r0-2026-10-10` branch. Its path filters did not include `src/ce/signal/record.py` or `tests/test_qualified_signal_record_r1.py`, although those files contain the shared geometry-identity implementation and QSR regression coverage. A future push changing only those files could fail to trigger the dedicated workflow.

A candidate-only workflow correction has been committed to this research branch. It retains the old branch name for historical use, adds the current branch, and broadens path coverage to `src/ce/**`, `schemas/**`, `tests/**`, `tools/compute_source_identity_v2.py`, and the workflow itself. It does not alter A9 identity manifests or production controls.

## 2. Source-bound identity evidence

Repository: https://github.com/ConstellationsEcliptic/Constellations-Ecliptic
PR #32: https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/pull/32
Reviewed research HEAD before workflow correction:
`60659dc898db49f742bf1d4c75ec11eab77dcf70`

The exact source-tree and control-plane manifest paths and blob identities at the reviewed research HEAD were:
- `manifests/SOURCE_TREE_SHA256_V2.txt` — blob SHA-1 `3b0408cbfca6d626ac673391afafd53f90b9745c`; recorded SHA-256 `1a4004ac644331964ab9d540abf6b1631aed1cbbe0cbdd55316fe5356a0c7a8b`.
- `provenance/CONTROL_PLANE_SHA256_R1.txt` — blob SHA-1 `4a7b8d96d1a7db2c96f7a41c885439fe50530fed`; recorded SHA-256 `0bc4f88dc43549a1033434a2a3653c02b46002024630b4294c22ddb8a5f7c357`.

Those two manifest blobs are unchanged between research HEAD `60659dc...`, its stated parent `802408757e33d3d8a255d29b0d912f28b5770224`, and the exact A9 HEAD `c8dab3542d3d4725cf591630c07f76366f7949d0`. They are retained A9 identities, not per-research-branch expected values.

The identity function source is unchanged at these refs:
- `src/ce/foundation/source_tree_identity.py`, blob SHA-1 `e9fdad00d6bd8e3fb1ef83ff156a2f3691f2b3b9`.
- `src/ce/foundation/control_plane_identity.py`, blob SHA-1 `dd2d67ebe6fe806cf122b8e223bf2126379fa89b`.

Source-tree identity hashes canonical relative paths, byte lengths and file-content SHA-256s for files under `configs`, `src`, `tests`, `schemas`, `profiles`, `manifests`, `build`, `tools`, plus `pyproject.toml`, excluding the source manifest itself and standard generated/cache directories. Control-plane identity separately hashes relevant bytes beneath `.github` and `CHANGE_CONTROL.md`.

Observed candidate values in runs on research HEAD `60659dc...`:
- actual source tree: `fbc77e725871147d59bf8c58a1409e34fc64c2d9c660efd63e3f99609bb2d9de`
- retained manifest source tree: `1a4004ac644331964ab9d540abf6b1631aed1cbbe0cbdd55316fe5356a0c7a8b`
- actual control plane: `d200d76340e2ae75ba1cc2aad97da35030a3905b1ddb616a73daff339b6f7e70`
- retained manifest control plane: `0bc4f88dc43549a1033434a2a3653c02b46002024630b4294c22ddb8a5f7c357`

Because the research candidate differs from A9 in source/test content and workflow-control content, the mismatch is expected for this identity scope. This establishes why the equality checks fail; it does not prove a new Trusted Build, prove the research candidate safe for production, or authorize a candidate-specific identity-root update.

## 3. Exact workflow trigger defect

At research HEAD `60659dc...`, `.github/workflows/ce-b1-geometry-prototype.yml` had blob SHA-1 `90b99e2f423a7445f9596bf6ef18fbf8c9bcb2c3`.

The old push filter contained only:
`research/b1-geometry-rule-binding-r0-2026-10-10`

The active PR #32 branch is:
`research/b1-geometry-binding-single-identity-r0-2026-10-10`

The old `paths` filters enumerated `src/ce/claim/authorization.py`, `schemas/canon_rule.schema.json`, `tests/test_ce_r0_full_boundary_r1.py`, `tests/test_schema_structure_r1.py`, and the workflow, but omitted the modified geometry helper `src/ce/signal/record.py` and its direct new test file `tests/test_qualified_signal_record_r1.py`.

## 4. Candidate-only workflow change

At commit `5b0c430b9a74d6d3f7ea1de7d6806c8b4016dc89`, the workflow file was updated:
- old blob SHA-1: `90b99e2f423a7445f9596bf6ef18fbf8c9bcb2c3`;
- new blob SHA-1: `f6889dbd47b8c4c158652e2110dcc89a7c79846a`;
- file: https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/blob/5b0c430b9a74d6d3f7ea1de7d6806c8b4016dc89/.github/workflows/ce-b1-geometry-prototype.yml

The updated workflow:
- preserves the earlier push branch filter;
- includes current PR #32's push branch filter;
- runs the dedicated prototype when any file under `src/ce/**`, `schemas/**` or `tests/**` changes, when the source identity tool changes, or when this workflow changes;
- retains `pull_request` targeting `main` and least-privilege `contents: read`.

The workflow correction itself changes `.github` identity-bearing bytes. It is intentionally a research-candidate control-plane change, not an update to the A9 control-plane manifest. Accordingly, A9 Trusted Build and broad identity-pinned workflows may still fail at identity equality and must remain fail-closed.

## 5. Exact-head validation facts

Before the trigger correction, B1 dedicated run #38073186071 at `60659dc...` succeeded on Ubuntu, Windows and macOS, with 62 tests each and bytecode/cache-clean confirmation. This test result applies to that exact source/test head and is preserved as historical evidence.

The broader jobs at the same head behaved as follows:
- Full Boundary run #38073185970: all OS jobs fail at `Source identity`.
- Remediation run #38073186045: all OS jobs fail at `Source identity`.
- Trusted Build A9 run #38073186026: fails at source-tree/control-plane identity verification.
These are not failures of the dedicated 62-test suite.

Post-correction exact-head validation must be checked at the new commit and its associated run. Do not describe the pre-correction run as having tested the workflow change itself, and do not state the new head passed until its exact run completes.

## 6. Invariants and non-actions

- No source-tree or control-plane manifest was changed to force digest agreement.
- No A9 source bytes, approved A9 trust evidence, Canon rule corpus or production controls were promoted or mutated by this audit.
- No real/approved Canon rule was added; synthetic test rules remain TEST_ONLY.
- No official Test Register/Index/Constitution, application schema or runtime state was modified.
- No PR was merged; A10, Runtime Adoption, production/deployment and SEAL remain unauthorized.
- PR #32 remains research-only, OPEN / DRAFT / NOT MERGED.

**Current conclusion:** IDENTITY-GATE MISMATCH = EXPECTED FOR NON-A9 RESEARCH TREE UNDER RETAINED A9 MANIFESTS; DEDICATED B1 WORKFLOW HAD BRANCH/PATH TRIGGER DEFECT, CORRECTED CANDIDATE-ONLY AT `5b0c430...`; VALIDATE EXACT NEW HEAD; PRESERVE A9 MANIFESTS; FAIL-CLOSED.

END OF AUDIT R0
