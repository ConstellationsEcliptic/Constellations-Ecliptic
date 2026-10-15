# CONSTELLATIONS ECLIPTIC
# TEST REGISTER, GOLDEN ORACLE & CURRENT-BINDING AUDIT R2

**Date:** 2026-10-10  
**Classification:** READ-ONLY FORENSIC / CANDIDATE EVIDENCE / NON-AUTHORITATIVE  
**Authority effect:** NONE  
**Normative amendment:** NONE  
**Runtime Adoption / production / SEAL:** NOT AUTHORIZED

## 1. Purpose and correction

This R2 incorporates fresh direct execution of the exact historical B8/B7 packages and clarifies the scope of the current controlled test artifacts. It supersedes R0/R1 wording only where it was stale or too broad. It does not make B7 the current CE oracle, does not promote the raw-intake Test Register v1.5, and does not change any normative source.

Keep these distinctions separate:
1. package existence and byte/integrity verification;
2. successful package/test execution;
3. independence of the expected-value calculation for each domain;
4. fixture-identical binding to the current governing contract;
5. active official register/oracle identity;
6. runtime adoption / production authorization.

## 2. Exact B8 archive — independently checked from fresh extracted bytes

Artifact: `CE_V1_STAGE_B8_HUMAN_REVIEW_DUAL_CONTROL_CUMULATIVE_GATE_A-2026-09-23.zip`, materialized from the ChatGPT Library.

- Size: **15,563,329 bytes**
- SHA-1: `4b1b45134d22936eb2b2cf45c115b9f7a1492b1e`
- SHA-256: `5c245f91d7efed1b32aba6f89508252959f58b5df5052ef892fb51510d05a61b`
- ZIP CRC/integrity check: PASS
- ZIP entries: 668

Fresh extraction to a clean directory, followed by exact internal verification with bytecode writes disabled at process start:

```text
PYTHONDONTWRITEBYTECODE=1
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
PYTHONHASHSEED=0
python tools/verify_stage_b8.py
```

Observed:
- B8 checksum list: 666 entries; all verified.
- B8 package manifest: 667 file entries; all verified.
- Exact embedded B7 parent SHA-256 matched the pinned value.
- B7 checksum list: 655 entries; all verified.
- B7 package manifest: 656 file entries; all verified.
- B7 full verifier: PASS, including its exact B6 parent, golden-oracle/solver/TZIF checks, truthful platform claim, and production fail-closed markers.
- **B7 test suite: 31 passed.**
- **B8 test suite: 43 passed.**
- B8 result preserves `HUMAN_REVIEW=NOT_PERFORMED`, `DUAL_APPROVAL=NOT_ESTABLISHED`, `SEAL=NO`, `AUTHORIZATION=NON_AUTHORIZED`, and `FAIL_CLOSED=TRUE`.

B7 was also separately extracted from the exact embedded ZIP; direct `tests/test_b7_golden.py` execution returned **9 passed**.

These are fresh, reproducible development-verification observations on the exact historical packages. None is a production approval.

## 3. What B7 contributes as an oracle — and its limitations

B7 contains an independently implemented, standard-library-only `tools/golden_oracle.py` for:
- Gregorian Julian Day calculation;
- signed circular wrapping and aspect branch selection;
- geometric deviation and orb qualification;
- a bounded midpoint lattice.

Its fixed golden-vector package and tests cover examples including J2000/modern Julian Day values, circular geometry, simple solver roots/boundaries, a zero-birth midpoint example, DST classification, and fail-closed astronomical-runtime status. This is a real historical golden/oracle package; the task is **not** to search for whether any historical oracle exists.

It is only partially reusable against current CE Rev.4:
- B7's old implementation interfaces and solver/scenario-window/timezone semantics differ from the later Rev.4 candidate.
- Some packaged B7 reference modules are byte-identical to modules in its own wheel, which proves package consistency but is not independent derivation of those modules.
- B7 DST tests use host `zoneinfo.ZoneInfo`; they do not establish binding to CE's pinned, policy-owned TZif data bundle.
- B7 has limited solver examples; they do not by themselves prove completeness for general continuous windows, exact-event enumeration, boundary topology, or zero-birth uncertainty semantics.
- Its own runtime evidence records missing canonical `.se1` inputs, native SWIEPH fallback detection, and an unresolved TZif policy anchor; production remains `NOT_AUTHORIZED`.

Therefore, reusable pieces must be qualified per ID/domain, not copied wholesale into the current authoritative path.

## 4. A9 candidate tests did run and pass

Exact A9 candidate:
- PR #26 branch: `remediation/ce-r0-a9-trusted-build-r1/2026-10-08`
- HEAD: `c8dab3542d3d4725cf591630c07f76366f7949d0`
- source-tree SHA-256: `1a4004ac644331964ab9d540abf6b1631aed1cbbe0cbdd55316fe5356a0c7a8b`
- control-plane SHA-256: `0bc4f88dc43549a1033434a2a3653c02b46002024630b4294c22ddb8a5f7c357`
- dependency-lock SHA-256: `ef8ace995340aa53026991644521ed85bbc5282781af9e8d88f030e83b776be5`

Actual CI:
- [Full Boundary CI run #141](https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/actions/runs/37765045306): Ubuntu, Windows and macOS jobs each report **261 tests, OK**.
- [Remediation CI run #145](https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/actions/runs/37765045314): Ubuntu, Windows and macOS jobs each report **261 tests, OK**.
- [Trusted Build A9 run #25](https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/actions/runs/37765045328): identity, locked-input and reproducibility steps succeeded.
- Separate owner/governance records establish Source Authority and formal Trusted Build for this **exact A9 candidate only**.

Direct source inspection of A9's `tests/test_planned_core_controls_r1.py` confirms the newer A9 assertions for:
- WIN-02: one continuous segment with three exact events;
- WIN-03: tangential contact creates no window segment.

The October 4 mismatch audit that marked WIN-02/WIN-03 as contradictions was bound to the older candidate HEAD `77cc615be55e0eaec446ad53913865d34c1cc9f6`. That result must not be repeated as a proven current code mismatch on A9 HEAD `c8dab354...`.

However, a passing 261-test suite does not automatically prove the tests use every normative fixture verbatim, or that every expected value is independently qualified. A9's own `manifests/convergent_test_register_r3.json` labels itself `CURRENT_IMPLEMENTATION_CANDIDATE` and keeps `authoritative_coverage`, `runtime_adoption`, and `full_runtime_coverage` as `NOT_ESTABLISHED`, with `fail_closed=true`.

## 5. Which test-register artifacts exist — and why the current full-register identity remains open

Three artifact classes must not be conflated.

### 5.1 Historical full Execution Profile/Test Register v1.5

A Library variant exists:
- `07_EXECUTION_PROFILE_TEST_REGISTER(3).md`
- 27,592 bytes
- SHA-256 `97a977feb051999dcefec7ee9322c5980ba73ed961608bc021a4b889ed659de0`
- 1,537 lines
- labelled `EXECUTION PROFILE & TEST REGISTER v1.5`

A raw-intake Box copy exists as two duplicate-location objects:
- Box `2485323796025`, 27,957 bytes, SHA-1 `973749ba88112a7b4202c807bcc7635d286a5ea9`;
- Box `2485336117840`, same size and SHA-1.

The October 4 Rev.4 coverage audit establishes a **content relation**, not same-byte identity: the Box variant equals the 1,537-line Library variant plus four terminal completeness-principle lines. These copies reside under `99_LOCAL_INVENTORY_INTAKE_2026-09-24/00_RAW_UNSORTED` in a duplicate candidate hierarchy; they are not promoted into the current stack merely by being named “normative” or having a higher date.

The governing Clean Current Set R3 archive explicitly excludes the legacy Test Register v1.5 as superseded while the archive's older document index still points at Document 07. This is **R3-PKG-INDEX-001**, a bounded package-index/exclusion inconsistency. Do not edit the immutable R3 ZIP in place or elevate either raw-intake copy automatically.

### 5.2 Current controlled Gregorian-only matrix R4

Box `2491701673391`, `CE_V1_HISTORICAL_CALENDAR_TEST_MATRIX_2026-09-28_R4-ACTIVE.md`, is located in `02_IMPLEMENTATION_ACTIVE_V1`. It is expressly marked **ACTIVE V1 VERIFICATION SCOPE — GREGORIAN-ONLY** and covers the `CAL-G-001..005` positive and `CAL-N-001..005` negative calendar/time-input controls, including the zero-birth-time invariant.

This is a genuine active controlled verification artifact, but its scope is specifically Gregorian-only calendar/time input. It is not a replacement for the complete Calculation Core + Signal + Canon + AI/output + account/privacy/commercial test register.

The 2026-09-28 post-apply verification record also names this matrix and confirms its controlled active scope; its Phase 12 record simultaneously says numerical, signal, language, security/privacy/commercial, execution-profile/performance, and executable historical-calendar evidence are not all established.

### 5.3 Current A9 implementation candidate register

A9's `manifests/convergent_test_register_r3.json` maps all 28 Calculation-Core IDs to current implementation tests. It is important candidate coverage evidence, but the file itself says `CURRENT_IMPLEMENTATION_CANDIDATE`, not an approved normative register.

### Result of the lineage distinction

It is inaccurate to say “no CE tests or no historic golden oracle exist.” Actual counter-evidence is now verified: B7/B8 packages and tests exist, the active calendar matrix exists, and the A9 261-test suite passed.

It remains accurate to say:
- the current characterized Stack Index/Manifest (dated 2026-10-04) identifies the current product/calculation/contracts/plan/execution profile/data-lock artifacts but does **not** bind a full successor CE behavior-test register;
- current full-register authority and complete fixture-to-approved-oracle crosswalk are **NOT_ESTABLISHED in the characterized current stack**;
- fixture-identical coverage of all current required invariants, independent oracle provenance for every domain, and full 1900–2100 runtime coverage are **NOT_ESTABLISHED**.

## 6. Primary human-disposition provenance

The A9 clean-reimplementation note describes WIN-02, WIN-03 and implementation-direction decisions as owner-approved. A primary hash-bound owner disposition for those specific decisions was not located in the inspected current source set. Preserve this as a bounded lineage/approval citation finding; do not silently elevate a candidate implementation note to the primary disposition record. No change to those semantics is proposed in this audit.

## 7. Repository control observations

A9 candidate `provenance/github_platform_governance_observation_r2.json` records a live observation on 2026-10-08 that `main` was protected with six required CE R0 Remediation / Full Boundary platform checks. The GitHub API detail endpoint returned 403 to the connected integration; exact settings were not freshly queried on 2026-10-10.

A mis-targeted direct contents API write in this audit received HTTP 409 stating that changes must be made through a pull request and six of six required status checks were expected. The attempted write was rejected; no commit was made on `main`. The candidate document was then written only to the explicitly specified PR branch.

The new PR #27 pre-A10 validation workflow is not among the six required checks in the 2026-10-08 observation. Its tests and blocked gate do not by themselves make it a required check for the main branch.

## 8. Current register and release boundary

The autonomy register remains 23 areas:
- 13 `CLOSED_PRESERVE`;
- 1 `SOURCE_RECONCILED` (E4);
- 9 `RECOMMENDATION_READY`;
- 10 incomplete: A3, A4, B1, B3, C3, C4, D4, E2, E4, F2.

For E3, `CLOSED_PRESERVE` means the review disposition preserves test/oracle/reproducibility controls; it does not close the above technical findings. The pre-A10 structural validator job passes its 14 tests; the separate strict completion job exits 2 while the register is incomplete. This is the intended fail-closed result.

No normative source, active R4 calendar matrix, full Test Register, A9 source, A10 implementation, authority state, runtime, deployment or SEAL was changed by this audit.

**Current status remains:** `PRE_A10_REVIEW=INCOMPLETE`; `A10_AUTHORIZED=false`; `RUNTIME_ADOPTION=NOT_ESTABLISHED`; `PRODUCTION_RUNTIME=NOT_AUTHORIZED`; `SEAL=NO`; `FAIL_CLOSED=TRUE`.

End of audit R2.
