# CONSTELLATIONS ECLIPTIC
# B1 IDENTITY GATE AND WORKFLOW TRIGGER RECONCILIATION — VALIDATION ADDENDUM
Date: 2026-10-11
Record: R1
Predecessor: R0, preserved unchanged
Classification: CANDIDATE TECHNICAL / CONTROL-PLANE VALIDATION ADDENDUM / NON-NORMATIVE
Authority effect: NONE
Normative / official Test Register / A9 manifest / runtime mutation: NONE
A10 / Source Authority / Trusted Build / Runtime Adoption / merge / release / production / SEAL effect: NONE

## 1. Exact workflow-correction commit

R0 documented the workflow path/branch trigger defect and expected identity-gate mismatch:
- R0: https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/blob/89661c62a3a1c84596cfa997997994ce44a74e27/governance/candidates/CE_B1_IDENTITY_GATE_AND_WORKFLOW_TRIGGER_RECONCILIATION_R0_2026-10-11.md
- R0 blob SHA-1: `642d74df1681957edcd0a71e5b9fbe19dcfd75f8`.

The workflow correction was committed at:
`5b0c430b9a74d6d3f7ea1de7d6806c8b4016dc89`
Workflow file: https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/blob/5b0c430b9a74d6d3f7ea1de7d6806c8b4016dc89/.github/workflows/ce-b1-geometry-prototype.yml
- Prior blob SHA-1: `90b99e2f423a7445f9596bf6ef18fbf8c9bcb2c3`
- New blob SHA-1: `f6889dbd47b8c4c158652e2110dcc89a7c79846a`

The workflow change preserves the old research branch filter, adds the current PR #32 branch `research/b1-geometry-binding-single-identity-r0-2026-10-10`, and broadens path coverage to `src/ce/**`, `schemas/**`, `tests/**`, `tools/compute_source_identity_v2.py` and the workflow itself.

## 2. Exact-head dedicated CI result

After the workflow correction, GitHub Actions ran the dedicated research-only matrix on exact commit `5b0c430b9a74d6d3f7ea1de7d6806c8b4016dc89`:
- Run #38073712399: https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/actions/runs/38073712399
- A duplicate push-associated run #38073708478 also completed successfully: https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/actions/runs/38073708478

Run #38073712399 exact job results:
- Ubuntu job ID `114276194451`: 62 tests passed; `PYTHON_BYTECODE_CLEAN=TRUE`.
- Windows job ID `114276194552`: 62 tests passed; `PYTHON_BYTECODE_CLEAN=TRUE`.
- macOS job ID `114276194578`: 62 tests passed; `PYTHON_BYTECODE_CLEAN=TRUE`.
- All three platforms computed the same research-candidate source digest: `fbc77e725871147d59bf8c58a1409e34fc64c2d9c660efd63e3f99609bb2d9de`.

This validates the dedicated B1 test set and corrected workflow at the exact correction commit. It does not mean the later documentation-only audit commit ran those tests, and it is not a full CE suite, independent semantic review, Source Authority or Trusted Build.

## 3. Broader identity-pinned workflows remain correctly fail-closed

At the same correction commit, separate runs:
- Full Boundary #38073712499: https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/actions/runs/38073712499 — all OS jobs fail at `Source identity`.
- Remediation #38073712517: https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/actions/runs/38073712517 — all OS jobs fail at `Source identity`.
- Trusted Build A9 #38073712559: https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/actions/runs/38073712559 — fails at `Verify source-tree and control-plane identities`.

These runs use the retained A9 manifest values `1a4004ac644331964ab9d540abf6b1631aed1cbbe0cbdd55316fe5356a0c7a8b` and `0bc4f88dc43549a1033434a2a3653c02b46002024630b4294c22ddb8a5f7c357`, while the research candidate computes different identity-bearing source/control-plane digests. This is expected for this non-A9 branch. It must not be “fixed” by replacing A9 hashes with research-candidate hashes.

## 4. Current interpretation

- The source/control-plane identity mismatch is explained by the non-A9 candidate tree under retained A9 manifests; no evidence justifies changing those manifests.
- The dedicated prototype workflow had a trigger-coverage flaw; the branch/path filters have been corrected candidate-only and the corrected workflow's 62-test matrix passed at the exact workflow-correction commit.
- Continue treating the B1 implementation/tests as research-only. A populated approved V1 Canon corpus, independent semantic verifier, valid source/build authority and Runtime Adoption remain NOT ESTABLISHED.
- PR #32 remains OPEN / DRAFT / NOT MERGED. The new documentation does not change its authority.
- R0 and all earlier source/manifest/CI artifacts are preserved unchanged.

END OF ADDENDUM R1
