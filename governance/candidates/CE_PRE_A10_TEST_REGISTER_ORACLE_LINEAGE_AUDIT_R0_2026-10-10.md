# CONSTELLATIONS ECLIPTIC
# TEST REGISTER, FIXTURE BINDING & ORACLE LINEAGE AUDIT R0

**Date:** 2026-10-10  
**Classification:** READ-ONLY FORENSIC / WORKING CANDIDATE / NON-AUTHORITATIVE  
**Authority effect:** NONE  
**Normative amendment:** NONE  
**A10 / production / SEAL:** NOT AUTHORIZED

## 1. Question

This audit distinguishes five different statements that must not be collapsed into one:

1. a test suite actually ran and passed;
2. test methods are mapped to named implementation IDs;
3. exact expected-value fixtures are identical to the currently authorized source contract;
4. the expected-value oracle has independently established provenance and review;
5. the candidate is authorized for Runtime Adoption/production.

Evidence proves these separately. A pass in one category does not imply the next.

## 2. Governing archive result and the R3 package finding

The exact Clean Current Set R3 ZIP has been locally verified against the retained governing boundary:

- Box archive ID: `2485715303669`
- Size: 2,654,872 bytes
- SHA-1: `58f8c3dcccc0ccb2e79a79ddd46ab0014c2783d6`
- SHA-256: `d9c2f4abbe0a482e982488d5d2e332202c0c0dc8fceca3b5faaceb3d2c4a8abc`
- ZIP integrity PASS; 72/72 internal payload SHA256 entries matched.

In the archive, `01_NORMATIVE/00_DOCUMENT_INDEX.md` names `07_EXECUTION_PROFILE_TEST_REGISTER.md` as Document 07 and describes it as the production-gate test register. However `00_START_HERE/EXCLUDED_SUPERSEDED_FILES_R3.md` explicitly lists the legacy Execution Profile/Test Register v1.5 as intentionally excluded. The v1.5 file is absent from the R3 ZIP. The characterized Stack Index/Manifest R1 do not bind a current successor test register.

This is the bounded candidate finding **R3-PKG-INDEX-001**: a stale package index reference conflicts with the archive's explicit exclusion record. It is not permission to repair the archive in place or to promote another test registry by default.

Detailed archive member audit:
https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/blob/governance/candidates/ce-autonomous-evolution-charter-r0-2026-10-09/governance/candidates/CE_PRE_A10_GOVERNING_ARCHIVE_MEMBER_IDENTITY_AUDIT_R0_2026-10-10.md

## 3. Historic October 4 audit must be scoped to its exact candidate

The following Library audits inspect candidate HEAD `77cc615be55e0eaec446ad53913865d34c1cc9f6`, branch `development/convergent-a1-b1/2026-10-04-r1`:

- `CE_V1_CURRENT_28_TEST_SEMANTIC_REBINDING_AUDIT_R1_2026-10-04.md`
- `CE_V1_REV4_BOUND_COVERAGE_CANDIDATE_R3_2026-10-04.md/.json`
- `CE_V1_CONTINUATION_STATE_R3_2026-10-04.json`
- `CE_V1_ORACLE_QUALIFICATION_MATRIX_R1_2026-10-04.md/.json`

That historical snapshot reports 28 named test rebindings, but not fixture-identical/authoritative coverage or an established independent deterministic oracle. It marks multiple cases as fixture/provenance divergence and specifically marks WIN-02/WIN-03 as contract contradictions **for that 77cc615 candidate snapshot**.

Do not generalize those exact assertions to the later A9 candidate without inspecting the later source. The historical audit is useful lineage evidence, not the current test verdict for every descendant.

## 4. Direct inspection of the exact A9 candidate and its CI

Current inspected A9 candidate:
- PR #26: https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/pull/26
- Branch: `remediation/ce-r0-a9-trusted-build-r1/2026-10-08`
- HEAD: `c8dab3542d3d4725cf591630c07f76366f7949d0`
- Source-tree SHA-256: `1a4004ac644331964ab9d540abf6b1631aed1cbbe0cbdd55316fe5356a0c7a8b`
- Control-plane SHA-256: `0bc4f88dc43549a1033434a2a3653c02b46002024630b4294c22ddb8a5f7c357`
- Dependency lock SHA-256: `ef8ace995340aa53026991644521ed85bbc5282781af9e8d88f030e83b776be5`

### 4.1 Actual CI execution

The following workflows were retrieved for that exact HEAD:

- Full Boundary CI run #141: https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/actions/runs/37765045306
- Remediation CI run #145: https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/actions/runs/37765045314
- Trusted Build A9 run #25: https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/actions/runs/37765045328

Observed:
- Full Boundary CI: Ubuntu, Windows and macOS jobs completed successfully; logs report **261 tests, OK** per platform.
- Remediation CI: Ubuntu, Windows and macOS jobs completed successfully; logs report **261 tests, OK** per platform.
- Trusted Build A9: exact candidate identification, immutable build image, source/control-plane identity, locked input, repeated source materialization, repeated build/test/package, and determinism checks all completed successfully. Run output continued to state formal Trusted Build/production/SEAL are not authorized in the workflow itself; the separate owner/governance record (Box `2514341553097`) establishes Source Authority and formal Trusted Build for this exact A9 candidate only.

This corrects any broad statement that “no CE candidate test suite ran.” The 261-test A9 candidate suite did run. It does **not** establish that the official current normative test register was fully/fixture-identically reproduced, that every oracle is independently established, that the runtime covers all required dates/platforms, or that A9 is adopted into production.

### 4.2 Test ID bindings in the exact A9 tree

A9 `manifests/convergent_test_register_r3.json` (Blob SHA `13eb21577d7deca5f47ab5fe78b4c0ec8cc37e71`) labels itself `CURRENT_IMPLEMENTATION_CANDIDATE`; it maps 28 named Calculation-Core IDs to test methods and lists supplemental regressions. It explicitly says:

- `authoritative_coverage = NOT_ESTABLISHED`
- `source_authority = NOT_ESTABLISHED` within this candidate manifest's own field set
- `trusted_build = NOT_ESTABLISHED` within this manifest
- `runtime_adoption = NOT_ESTABLISHED`
- `full_runtime_coverage = NOT_ESTABLISHED`
- `fail_closed = true`

The manifest is a coverage characterization, not an authority grant. Its source/build-status fields must be read within their own declared artifact and date; they do not negate the later separately recorded owner/governance disposition establishing Source Authority and Trusted Build for exact A9.

Directly fetched tests at the same A9 HEAD include:
- `tests/test_core_golden_r1.py`
- `tests/test_planned_core_controls_r1.py`
- `tests/test_independent_oracle_current_r1.py`

The current A9 source directly asserts WIN-02 as one continuous segment with three exact events and WIN-03 as tangential contact with no window segments. Thus the October 4 mismatch finding for HEAD `77cc615` cannot be described as a demonstrated current mismatch on A9 HEAD `c8dab354`; the later source is different and encodes those expected shapes.

The “independent oracle” module contains candidate reference calculations and expected topology checks separated from production imports for portions of the domain. Its presence is useful supporting evidence, but it is not a source-bound, owner-approved, independently qualified oracle package for all normative CE fixtures. The current manifest itself keeps authoritative coverage NOT_ESTABLISHED. Full normative fixture/provenance mapping and oracle independence must be evidenced rather than inferred from the filename or the tests passing.

### 4.3 Human decision provenance caveat

A9 candidate document `docs/CE_CALCULATION_CORE_CLEAN_REIMPLEMENTATION_R1_2026-10-04.md` calls WIN-02, WIN-03 and the clean-reimplementation direction “Owner-approved decisions.” The historical continuation state at 2026-10-04 recorded these as reserved human decision topics before that later note appeared. Searches of the inspected Library sources did not independently locate a primary, hash-bound owner-disposition record for those three items.

Accordingly:
- preserve the A9 candidate's claim as a candidate-source statement, not as the primary approval record;
- do not reopen the already recorded product discussion without need;
- for formal normative lineage, locate/bind the primary disposition record or document its exact reference under controlled governance;
- do not reinterpret or alter the agreed WIN-02/WIN-03 semantics in this audit.

## 5. Correct consolidated conclusion

| Claim | Current finding |
|---|---|
| Governing Clean Set R3 outer identity and internal payload hashes | **VERIFIED** — archive SHA-256 matches; ZIP valid; 72/72 payload hashes pass |
| Historical Oct 4 28-test mismatch audit | **VERIFIED AS A SNAPSHOT OF HEAD 77cc615 ONLY** |
| A9 candidate suite ran | **VERIFIED** — 261 tests passed on each of Ubuntu, Windows, macOS in runs #141 and #145 |
| Current A9 WIN-02/WIN-03 test code reflects the stated window semantics | **VERIFIED BY DIRECT SOURCE INSPECTION** at exact A9 HEAD |
| Current A9 manifest maps named rebindings for 28 Calculation-Core IDs | **VERIFIED AS CANDIDATE MAPPING** |
| Official current CE behavior-test register bound by current characterized stack | **NOT_ESTABLISHED** |
| Full normative fixture-identical coverage of all required test IDs | **NOT_ESTABLISHED** |
| Independently qualified, source-bound oracle for every required fixture/domain | **NOT_ESTABLISHED** |
| Direct primary owner-disposition record for the later-reported WIN-02/WIN-03/architecture decisions | **NOT LOCATED in inspected source set** |
| Source Authority and formal Trusted Build for exact A9 | **ESTABLISHED by separate owner/governance records, within exact scope only** |
| Runtime Adoption / full runtime coverage / TZIF runtime identity / production / deployment / SEAL | **NOT ESTABLISHED / NOT AUTHORIZED** |

## 6. Consequence for pre-A10 E3

E3 may close the **review principle/disposition** to preserve test/oracle and release-control boundaries, but it must keep technical findings open. It must not state that the 261-test A9 suite was never executed, and must not inflate those passes into normative test-register authority or full oracle coverage. The 14 unit tests in the autonomy PR validate the pre-A10 register-gating tool only; they are a different test suite.

The remaining safe technical work is to establish the approved current test-register identity and source lineage, assemble a source-bound fixture/oracle crosswalk with independent derivation evidence, reconcile the owner-disposition record for any protected semantics where a primary record is required, and verify repository required-check enforcement through an authorized settings path.

## 7. Non-actions

No CE normative source, current Test Register, A9 source code, A10 implementation, runtime state, trust root, or production state was edited by this audit. No A10, merge, production, deployment, or SEAL authorization is granted. PR #26 stays OPEN / DRAFT / DO NOT MERGE; PR #27 stays OPEN / DRAFT / DO NOT MERGE until its own controlled decision path is satisfied.

End of report.
