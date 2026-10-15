# CONSTELLATIONS ECLIPTIC
# TEST REGISTER, GOLDEN ORACLE & CURRENT-BINDING AUDIT R1

**Date:** 2026-10-10  
**Classification:** READ-ONLY FORENSIC / CANDIDATE EVIDENCE / NON-AUTHORITATIVE  
**Authority effect:** NONE  
**Normative amendment:** NONE  
**Runtime Adoption / production / SEAL:** NOT AUTHORIZED

## 1. Corrected question

The current state must distinguish:
1. whether a test/oracle package exists;
2. whether its exact bytes and internal integrity verify;
3. whether the code has been tested and passed;
4. whether its expected values are independent for a particular domain;
5. whether its fixtures are identical to the currently governed CE contract;
6. whether the suite is bound as the current official register/oracle;
7. whether runtime and production are authorized.

This R1 supplements and narrows R0. It corrects any reading of R0 that could imply “no historical independent oracle package exists.” A historical B7 package exists, is embedded exactly inside B8, and has just been reverified. It is still not an automatically valid current Rev.4 oracle.

## 2. Fresh exact-byte verification of B8 and embedded B7

The exact B8 archive was materialized from the ChatGPT Library:
- Artifact: `CE_V1_STAGE_B8_HUMAN_REVIEW_DUAL_CONTROL_CUMULATIVE_GATE_A-2026-09-23.zip`
- Size: 15,563,329 bytes
- SHA-1: `4b1b45134d22936eb2b2cf45c115b9f7a1492b1e`
- SHA-256: `5c245f91d7efed1b32aba6f89508252959f58b5df5052ef892fb51510d05a61b`
- ZIP test: PASS; 668 entries.

I extracted B8 afresh and executed its exact internal verifier with bytecode writing disabled from process start:
`PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONHASHSEED=0 python tools/verify_stage_b8.py`

Observed result:
- B8 internal SHA256SUMS: 666 entries verified; no mismatch.
- B8 package manifest: 667 listed file entries verified.
- Embedded B7 parent was re-extracted and its exact SHA-256 matched `9f8ec942b093d8b67b37529170f110d4217d48404255a70416f17f08049ceb67`.
- B7 internal SHA256SUMS: 655 entries verified; no mismatch.
- B7 package manifest: 656 entries verified.
- B7 exact-parent verifier succeeded, including its own exact B6 parent check and fail-closed runtime markers.
- B7 test suite: **31 passed**.
- B8 test suite: **43 passed**.
- B8 status markers: human review NOT PERFORMED; dual approval NOT ESTABLISHED; production authorization non-authorized; SEAL NO; fail-closed TRUE.

This is a fresh successful re-execution against the exact materialized B8 bytes, not a claim of current CE production qualification.

## 3. What is useful about B7's golden oracle

The B7 package contains:
- independent reference functions in `tools/golden_oracle.py` for Gregorian Julian Day calculation, wrapped angular geometry/branch selection, and midpoint-lattice generation;
- fixed vectors in `golden_vectors/B7_GOLDEN_VECTORS.json`;
- tests in `tests/test_b7_golden.py` that compare the CE implementation with reference expectations for time, geometry, simple solver roots/threshold boundaries, zero-birth midpoint instants, DST classification, and fail-closed astronomy status;
- explicit oracle constitution separating independent deterministic math, astronomical-runtime evidence and platform evidence.

This is material reusable historical evidence. In particular, the B7 golden vectors are fixed test evidence, not user feedback and not evidence that astrology is true.

Its limits are equally material:
- the B7 current candidate was a different implementation interface/architecture from current A9 Rev.4;
- B7 DST tests use the host's `zoneinfo.ZoneInfo`, not the current CE policy-owned, digest-bound TZif runtime;
- its simple solver fixtures do not prove general continuous-window/threshold completeness;
- the astronomical runtime portion is explicitly not production-accepted because B6 detected SWIEPH fallback and missing canonical `.se1` inputs;
- B7's platform matrix makes a current-host-only claim rather than claiming all platforms ran.

The previously recorded 2026-10-04 Deep Oracle/R4 audit therefore remains relevant: the B7 oracle is partially independent and potentially reusable after controlled re-binding, but it is not a fully qualified current Rev.4 oracle package. That audit specifically found current interfaces/semantics diverged in solver/scenario-window/timezone layers, leaving substantial fixture rebinding required. Do not bulk-copy old golden results and label them equivalent to current Rev.4 without demonstrating each mapping.

## 4. Current A9 evidence: 261-test suite really ran

Exact A9 candidate:
- HEAD: `c8dab3542d3d4725cf591630c07f76366f7949d0`
- Source-tree SHA-256: `1a4004ac644331964ab9d540abf6b1631aed1cbbe0cbdd55316fe5356a0c7a8b`
- Control-plane SHA-256: `0bc4f88dc43549a1033434a2a3653c02b46002024630b4294c22ddb8a5f7c357`
- Dependency-lock SHA-256: `ef8ace995340aa53026991644521ed85bbc5282781af9e8d88f030e83b776be5`

Actual candidate CI evidence:
- Full Boundary CI run #141: https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/actions/runs/37765045306 — Ubuntu, Windows, macOS each report 261 tests OK.
- Remediation CI run #145: https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/actions/runs/37765045314 — Ubuntu, Windows, macOS each report 261 tests OK.
- Trusted Build A9 run #25: https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/actions/runs/37765045328 — exact identity and reproducibility steps successful.
- The separate owner/governance record (Box `2514341553097`) establishes Source Authority and formal Trusted Build for this exact A9 candidate only.

Directly inspected A9 test code now asserts WIN-02 as one continuous segment containing three exact events and WIN-03 as no qualifying segment for tangential contact. The historical 2026-10-04 28-test mismatch audit targeted older candidate HEAD `77cc615be55e0eaec446ad53913865d34c1cc9f6`; it must not be treated as proof that those assertions are still contradictory in A9 HEAD `c8dab354...`.

The A9 manifest `manifests/convergent_test_register_r3.json` labels itself `CURRENT_IMPLEMENTATION_CANDIDATE` and maps 28 Calculation-Core IDs. It also explicitly declares `authoritative_coverage=NOT_ESTABLISHED`, `runtime_adoption=NOT_ESTABLISHED`, `full_runtime_coverage=NOT_ESTABLISHED`, and `fail_closed=true`. The full 261-test CI pass is real, bounded evidence; it does not nullify those own-scope limitations.

## 5. Current register lineage remains unresolved

The governing Clean Current Set R3 archive:
- SHA-256: `d9c2f4abbe0a482e982488d5d2e332202c0c0dc8fceca3b5faaceb3d2c4a8abc`
- ZIP test PASS, 72/72 internal payload SHA-256 entries matched.

It explicitly excludes the legacy Execution Profile/Test Register v1.5, although its internal nominal document index still references that register. Finding: `R3-PKG-INDEX-001`.

The current characterized Stack Index/Manifest R1 do not bind an active replacement CE behavior-test register. Therefore:
- the exact current official CE behavior-test register identity remains NOT_ESTABLISHED in the characterized current stack;
- full normative fixture-identical coverage and the complete source-bound crosswalk from all required named IDs to approved independent expected values remain NOT_ESTABLISHED;
- this is not the same as saying no historical independent oracle exists;
- it is not correct to treat B7's historical register/oracle or A9's current implementation candidate register as automatically authoritative merely because each is internally complete or has passing tests.

## 6. Owner-disposition provenance caveat

The A9 clean-reimplementation note calls WIN-02, WIN-03 and architecture direction owner-approved, but a primary hash-bound disposition record for those specific decisions was not located in the inspected source set. The older 2026-10-04 continuation state had recorded these as reserved human decision topics before the later candidate note appeared.

Keep that source lineage issue bounded:
- do not reopen product semantics unnecessarily;
- do not represent the candidate note as the primary owner record;
- bind the primary record or record its exact controlled reference before using it as the sole approval citation in a future normative amendment.

No semantic change is proposed here.

## 7. Repository branch-protection evidence

A9 source artifact `provenance/github_platform_governance_observation_r2.json` (Box/GitHub candidate blob `a7ea88234ce9958bb19efa7f7a772db24fd3ffce`) records a live observation on 2026-10-08 that `main` was protected with six required CI checks: three CE R0 Remediation and three CE R0 Full Boundary platform checks. The connected integration could not read detailed settings (403), and current live settings were not freshly re-queried on 2026-10-10.

The new pre-A10 register validator is not listed among those six recorded checks. Its passing validator job / blocked strict-completion job is not itself proof it is a required main-branch check. Keep that distinction in governance adoption.

Further bounded details:
https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/blob/governance/candidates/ce-autonomous-evolution-charter-r0-2026-10-09/governance/candidates/CE_PRE_A10_REPOSITORY_GOVERNANCE_OBSERVATION_RECONCILIATION_R0_2026-10-10.md

## 8. Current disposition

- B8/B7 exact bytes, internal hashes and verifiers: freshly verified for the materialized archive stated above.
- Historical B7 oracle: exists, internally integrity-checked and tests pass; partial applicability and limited scope.
- A9 CE candidate suite: 261 tests passed on Ubuntu, Windows and macOS across runs #141/#145 at exact A9 head.
- Current authoritative CE behavior-test register / full Rev.4 fixture-oracle matrix: NOT_ESTABLISHED in the characterized stack.
- Runtime Adoption, full runtime coverage, TZIF runtime identity, production/deployment, and SEAL: not established/not authorized.
- No normative CE source, current official Test Register, A9/A10 code, trust root or production state changed.

The next admissible engineering step is a source-bound, per-ID crosswalk comparing Clean Set/current characterization, recovered B7 oracle fixtures, A9 candidate test implementations and approved semantics—without copying historical or candidate data into normative authority. Preserve fail-closed until that crosswalk and required governance disposition are established.

End of audit R1.
