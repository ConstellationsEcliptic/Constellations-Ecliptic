# CE PRE-A10 — A9 28-ID TEST-SURFACE CROSSWALK R0

**Date:** 2026-10-10  
**Classification:** SOURCE-BOUND TEST TRACEABILITY / WORKING CANDIDATE / NON-AUTHORITATIVE  
**Authority effect:** NONE  
**Test Register promotion effect:** NONE  
**A9 source/code mutation:** NONE  
**Runtime Adoption / production / SEAL effect:** NONE

## 1. Purpose

The A9 manifest `manifests/convergent_test_register_r3.json` labels itself `CURRENT_IMPLEMENTATION_CANDIDATE`, declares 28 `current_named_rebindings`, and expressly keeps authoritative coverage, Source Authority, Trusted Build, Runtime Adoption and full runtime coverage unestablished in that manifest. This note traces each named ID to the exact A9 candidate test source and method inspected at commit `c8dab3542d3d4725cf591630c07f76366f7949d0`.

This establishes a repeatable **test-surface name binding** for those 28 IDs. It does not promote them into the excluded legacy v1.5 Test Register, prove complete coverage of that register, establish normative expected values for every domain, or qualify the test suite as a wholly independent oracle.

## 2. Candidate identity and source files

Repository: `ConstellationsEcliptic/Constellations-Ecliptic`  
Branch: `remediation/ce-r0-a9-trusted-build-r1/2026-10-08`  
Exact A9 HEAD: `c8dab3542d3d4725cf591630c07f76366f7949d0`

| File | Git blob SHA-1 | Rebinding use |
|---|---|---|
| `tests/test_planned_core_controls_r1.py` | `3924453239e09e85c7250e6311eb40e6177c40bc` | EPH-01, ERR-01/02/05/06, INT-01, TIME-01/02/03, UNC-01/02/03/04, WIN-01/02/03 |
| `tests/test_retry_and_range_r1.py` | `1febd3a934ad4e49b1774ec3ca90933e123f5983` | ERR-03/04, EPH-02 |
| `tests/test_core_golden_r1.py` | `201640bd652af6a67e8b4d102ba61348cff3f4cc` | GEO-01/02, KIN-01/02/03/04, ORB-01/02, STA-01 |
| `tests/test_independent_oracle_current_r1.py` | `5919cfc606c8378cb140c555d30909cba68e706a` | Supplemental expected-value checks for geometry/kinematics, orb/span, window topology, ephemeris flag interpretation, controlled TZIF examples and signal/daily boundaries. It does not add a new explicit legacy ID label to the 28-ID list. |

## 3. Named ID → method crosswalk

| ID | Exact test file and line | Test method | Main assertion scope |
|---|---|---|---|
| EPH-01 | `tests/test_planned_core_controls_r1.py:107` | `test_eph_01_requested_actual_resolution_mismatch_is_failure` | Requested/actual ephemeris flag mismatch maps to calculation failure. |
| EPH-02 | `tests/test_retry_and_range_r1.py:45` | `test_eph_02_chiron_out_of_range_is_known_unavailable` | Out-of-range Chiron behavior is classified as known-unavailable rather than silently fabricated. |
| ERR-01 | `tests/test_planned_core_controls_r1.py:124` | `test_err_01_corrupt_evidence_packet` | Malformed/non-finite evidence input is rejected. |
| ERR-02 | `tests/test_planned_core_controls_r1.py:151` | `test_err_02_malformed_calculation_input` | Malformed calculation input is rejected. |
| ERR-03 | `tests/test_retry_and_range_r1.py:17` | `test_err_03_retryable_worker_failure` | Retryable worker failure path. |
| ERR-04 | `tests/test_retry_and_range_r1.py:33` | `test_err_04_non_retryable_failure` | Non-retryable failure path. |
| ERR-05 | `tests/test_planned_core_controls_r1.py:161` | `test_err_05_failure_not_quiet_sky` | Invalid calculation/provider state cannot be treated as a valid aspect-window result. |
| ERR-06 | `tests/test_planned_core_controls_r1.py:180` | `test_err_06_non_valid_boundary_preserved` | Known-unavailable/non-valid provider state remains a failure at the solver boundary. |
| GEO-01 | `tests/test_core_golden_r1.py:18` | `test_geo_01_circular_boundary` | Circular wrap/conjunction boundary and expected signed/absolute deviation. |
| GEO-02 | `tests/test_core_golden_r1.py:29` | `test_geo_02_exact_square` | Directed square branch, exact deviation and exact-state classification. |
| INT-01 | `tests/test_planned_core_controls_r1.py:199` | `test_int_01_quiet_sky` | Valid provider with no matching events/windows yields empty result; by itself this is not the whole daily-product Quiet Sky contract. |
| KIN-01 | `tests/test_core_golden_r1.py:40` | `test_kin_01_applying` | Applying phase example. |
| KIN-02 | `tests/test_core_golden_r1.py:45` | `test_kin_02_separating` | Separating phase example. |
| KIN-03 | `tests/test_core_golden_r1.py:50` | `test_kin_03_retrograde_separating` | Retrograde/separating example. |
| KIN-04 | `tests/test_core_golden_r1.py:55` | `test_kin_04_exact_precedence` | Exact-state precedence near the tolerance boundary. |
| ORB-01 | `tests/test_core_golden_r1.py:60` | `test_orb_01_profile_a` | Profile A effective orb expected value. |
| ORB-02 | `tests/test_core_golden_r1.py:64` | `test_orb_02_profile_b` | Profile B effective orb expected value. |
| STA-01 | `tests/test_core_golden_r1.py:68` | `test_sta_01_circular_span` | Circular span across the 360° boundary. |
| TIME-01 | `tests/test_planned_core_controls_r1.py:221` | `test_time_01_historical_timezone_normative_fixture` | Controlled TZIF fixture with a fixed hash and expected UTC normalization. |
| TIME-02 | `tests/test_planned_core_controls_r1.py:233` | `test_time_02_ambiguous_rejected_normative_fixture` | Ambiguous local wall-time rejection. |
| TIME-03 | `tests/test_planned_core_controls_r1.py:245` | `test_time_03_nonexistent_rejected_normative_fixture` | Nonexistent local wall-time rejection. |
| UNC-01 | `tests/test_planned_core_controls_r1.py:75` | `test_unc_01_stable_robust` | Stable/robust scenario classification. |
| UNC-02 | `tests/test_planned_core_controls_r1.py:83` | `test_unc_02_variable_possible` | Variable scenario possibility/robust classification. |
| UNC-03 | `tests/test_planned_core_controls_r1.py:92` | `test_unc_03_variable_mixed_phase` | Mixed kinematic-phase scenario treatment. |
| UNC-04 | `tests/test_planned_core_controls_r1.py:100` | `test_unc_04_variable_no_qualification` | Variable scenario that does not qualify. |
| WIN-01 | `tests/test_planned_core_controls_r1.py:23` | `test_win_01_disjoint_possible_windows` | Two disjoint windows and fixed event times. |
| WIN-02 | `tests/test_planned_core_controls_r1.py:38` | `test_win_02_continuous_multi_peak` | One continuous window with three exact events. |
| WIN-03 | `tests/test_planned_core_controls_r1.py:57` | `test_win_03_tangential_contact` | Tangential contact does not create a window segment. |

## 4. Traceability caveats found by direct source inspection

### 4.1 TIME identifiers

The comment immediately preceding the time tests is `# TIME-01` at line 220. The next two methods are explicitly named `test_time_02_...` and `test_time_03_...`, but separate `# TIME-02` and `# TIME-03` comment markers are not present immediately before those methods in the inspected file. The mapping is recoverable from exact method names, but the line-comment mechanism is not a consistent explicit ID binding for TIME-02/TIME-03. A future successor register/generator should require one explicit ID marker per named case, without altering the frozen A9 source.

### 4.2 EPH-01 supplemental unlabelled test

The `# EPH-01` marker immediately precedes the named `test_eph_01_requested_actual_resolution_mismatch_is_failure` method. An additional method `test_ephemeris_data_integrity_mismatch_remains_separate` follows it before the next ID marker, without a separate stable ID. Treat that as supplemental coverage, not as a second EPH-01 fixture.

### 4.3 What these tests prove

The 28 cases are concrete executable tests on the exact A9 candidate. The passing recorded CI (Full Boundary #141 and Remediation #145) is genuine evidence those candidate suites ran and passed on Ubuntu, Windows and macOS (261 tests per platform in each run). The method map does not by itself prove:
- normative oracle lineage for each literal expected value;
- independent algorithmic oracle coverage for all solver/runtime layers;
- full equivalence to the excluded historical 100-ID register;
- complete product, Canon, voice/LLM, privacy, account recovery, commercial transaction and consumer-law coverage;
- full supported-domain runtime coverage, Runtime Adoption, or production qualification.

### 4.4 Independent expected-value examples are not a complete independent engine

`tests/test_independent_oracle_current_r1.py` contains separately stated expected values for geometry/kinematics, orb/circular span, three toy window topologies, ephemeris flag classification, controlled TZIF examples and minimal signal/daily boundaries. Important limits remain:
- its window topology tests call the candidate's `solve_aspect_window`; the expected toy topology is independent, but this is not a separately implemented full solver oracle;
- its controlled TZIF checks call the candidate's `TzifRuntime` on hash-pinned bytes; these are fixed-vector checks, not an independent TZif parser;
- its signal/daily boundary case calls candidate `SignalEngine` and daily aggregation against a constructed packet; it does not independently reconstruct the full Canon-to-user output contract;
- the geometry/kinematics test includes an independent wrap/error expression, but complete test and independent calculation of all returned semantic fields is not established by that fact alone.

Separate source-bound calculations, fixtures and independent validators are still required before any claim of complete authoritative oracle coverage.

## 5. Recommended next technical step

Preserve the frozen A9 candidate and its historic reports. In an isolated future test-contract candidate (not A9 itself):
1. create a single source-bound crosswalk from each required normative invariant to the current official test ID, exact fixture bytes, expected-value derivation, independent oracle implementation, tested profile/runtime identity, CI evidence and change-control lineage;
2. make the successor test ID binding mechanically one-to-one, including TIME-02/TIME-03; ensure extra supplemental tests have stable IDs or are explicitly labeled supplemental;
3. identify uncovered requirements from the active V1 Calculation, Signal, Canon, Evidence/AI, Privacy/Account and Commercial sources instead of inflating the existing 28-ID calculation-core scope;
4. bind the full successor register and crosswalk to the characterized Stack Index/Manifest only through its approved change-control process. Do not reuse/promote excluded v1.5 by filename or infer authority from passing candidate CI.

## 6. Non-actions / final boundary

- No A9 source file was changed.
- No official Test Register or Stack Index/Manifest was promoted or amended.
- No source/normative authority, test-register authority, Runtime Adoption, production authorization, merge permission or SEAL was established.
- A9 Source Authority / Trusted Build remain scoped only to the exact candidate identified above.
- PR #27 remains a draft, non-authoritative candidate; A10 remains unauthorized.

**End of R0.**
