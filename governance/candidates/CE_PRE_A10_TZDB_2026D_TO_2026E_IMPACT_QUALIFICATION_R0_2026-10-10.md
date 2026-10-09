# CONSTELLATIONS ECLIPTIC
# TZDB 2026d → 2026e IMPACT QUALIFICATION NOTE R0

**Date:** 2026-10-10  
**Classification:** SOURCE-BASED IMPACT ANALYSIS / WORKING CANDIDATE / NON-AUTHORITATIVE  
**Authority effect:** NONE  
**Data/runtime mutation:** NONE  
**Runtime Adoption / production / deployment / SEAL:** NOT AUTHORIZED  
**Current pinned profile:** `CE-CALC-V1-EP-001`, revision 4, IANA 2026d  
**Candidate upgrade:** 2026e — NOT ADOPTED

## 1. Executive determination

The upstream 2026e release creates at least two directly relevant CE fixture families because the policy-owned TZIF candidate bundle contains 597 entries and its declared supported domain is 1900–2100:

1. **Future transition:** Manitoba moves to permanent UTC−05. IANA says the change is modeled at 2026-11-01 02:00 and affects `America/Winnipeg` and its backward-compatible alias `Canada/Central`.
2. **Historical transition:** Ireland's 1925 autumn rollback is corrected from October 4 to September 20. This affects the historical `Europe/Dublin` rule family and must be qualified for any supported alias/compatibility path.

IANA release 2026e is dated 2026-09-29. The official release history lists 2026e as latest and 2026d as the immediately preceding release. The upstream announcement identifies source commit `039ef27cc5f062a2055cb67435d6d71adbefd27d`; its SHA-512 for `tzdata2026e.tar.gz` is recorded below as **upstream-published, not locally reverified here**. [IANA release notes](https://www.iana.org/time-zones/releases/2026e) · [IANA release history](https://www.iana.org/time-zones/releases) · [upstream announcement](https://lists.iana.org/hyperkitty/list/tz%40iana.org/thread/VXIA4AU73OQL3OZ3ZBZHWIASIIVBGUJV/)

**Disposition:** retain 2026d for current A9/profile evidence. Do not update the bundle or profile in place, relabel existing captures, or promote 2026e based only on the upstream release note. Proceed with a separate delta fixture candidate and independent qualification.

## 2. Exact current identity and open authority boundary

The A9 source candidate declares:
- Profile `CE-CALC-V1-EP-001`, revision 4.
- IANA release 2026d; release commit `d633fe7ed3de8e00ce7cac991376a064a1373bb1`.
- Source archive SHA-256 `0cb2aa8e333c3dc049badc42a0c61f21987b8cd44e107fa900bad764aacc7767`.
- Compiled TZIF bundle SHA-256 `f3edd74a1bb77d092d6c2ed3eead8ebea9657954f5bb30b0ac031a08a5eed942`.
- Runtime manifest SHA-256 `a12881024bee3b801d63b0d9cb74118b6329512f63020f36c42412de1e0a6205`.
- Entry count 597.
- TZIF runtime authority remains `NOT_ESTABLISHED`; runtime package binding remains `OPERATOR_EVIDENCE_BINDING_PENDING_CURRENT_RUNTIME_ADOPTION`.

The current dependency qualification artifact in A9 already records `current_policy_release=2026d`, `external_latest_release_observed=2026e`, `adoption_decision=NOT_ADOPTED`, `upgrade_mode=NO_SILENT_UPGRADE`, and calls for changed-zone/transition discovery and downstream impact analysis. This note makes the first source-bounded change classes explicit. It does not verify every byte of either compiled 597-entry bundle because no exact 2026e compiled bundle has been built and compared in this work.

## 3. Upstream release delta

### 3.1 Manitoba — `America/Winnipeg` / `Canada/Central`

IANA 2026e says Manitoba's 2026-03-08 spring-forward was its last foreseeable clock change as Manitoba moves to permanent UTC−05. For compatibility with downstream consumers, tzdb temporarily models the change at **2026-11-01 02:00**, rather than applying the legal date label directly. It also changes the abbreviation to traditional `EST` for affected timestamps and applies the behavior to `Canada/Central`.

Expected CE impact if those zone identifiers are in the supported bundle (the 597-entry full candidate strongly suggests they are, but the exact compiled file-set still must be verified against the manifest):
- local-to-UTC normalization around 2026-11-01 may change;
- the local civil day of 2026-11-01 can have different UTC endpoints under 2026d versus 2026e;
- future local times after the transition resolve with a different offset under the two releases;
- derived observation instant, transit positions, event topology, signal qualification and evidence identity can therefore differ where the affected local zone is used.

Do not hardcode only a 1-hour difference as the test oracle. Generate expected UTC transitions from each exact release and compare all supported time forms, including the full half-open zero-birth interval.

### 3.2 Ireland — historical 1925 rollback

IANA 2026e corrects Ireland's rollback date to **1925-09-20**, not **1925-10-04**. This is inside the CE-supported 1900–2100 calculation domain and is directly relevant to historical local-to-UTC conversion for `Europe/Dublin` and any included alias. The exact offsets/transition instants should be obtained from the two verified TZIF files, not inferred from the short release note.

Expected CE impact:
- historical local times between the old/new transition treatment may normalize differently;
- full-day birth intervals near the corrected transition may have different UTC boundaries;
- historical observation-time conversion may differ;
- downstream astronomy and all dependent signal/evidence artifacts must be version-bound to the profile that produced them.

### 3.3 Scope of this source comparison

The official 2026e release note names these two rules changes. This is **a source-release delta identification**, not a byte-for-byte compiled TZIF bundle diff. Other compiled outputs can vary because of aliases, release/compiler options or data generation; the actual CE supported 597-entry set must still be compared from exact release sources with the same controlled compilation procedure before claiming a complete delta report.

## 4. Required per-zone qualification matrix

Create a candidate-only matrix before any bundle/profile change:

| Fixture family | Required data | Expected comparison |
|---|---|---|
| Manitoba transition | `America/Winnipeg`, `Canada/Central`; local times immediately before/at/after modeled 2026-11-01 02:00 transition | exact local→UTC outputs, offset, abbreviation and transition instant under 2026d and 2026e |
| Manitoba full-day interval | birth/observation date 2026-11-01 and adjacent dates; half-open local midnight boundaries | exact start/end UTC under both releases; day duration; no guessed noon/midnight surrogate |
| Manitoba future | representative dates after 2026-11-01, within supported range | exact local time normalization under both releases |
| Ireland rollback | `Europe/Dublin` and included compatibility aliases; dates around 1925-09-20 and 1925-10-04 | exact historical transition and local→UTC resolution under both releases |
| Ireland full-day interval | civil days spanning each candidate transition boundary | exact half-open UTC endpoints and interval ordering |
| Existing regression zones | all existing 597 current zone paths plus every normative/test-bound path | classify unchanged/changed/missing/added by path; record both file hashes and parsed transition deltas |
| CE downstream oracle | affected time fixtures plus representative astronomical/evidence fixtures in dependent scenarios | compare complete evidence identities, status and qualifying signal outcomes; never narrative-rescue a mismatch |

Expected behavior for the existing profile is unchanged: current 2026d captures stay bound to 2026d even if re-evaluated under 2026e for comparison. A re-evaluation is a new comparison record, not mutation of historic output.

## 5. Controlled procedure required to finish qualification

1. Fetch the official IANA 2026d and 2026e data archives from their versioned release URLs. Verify signatures/checksums using independently captured official release evidence. For 2026e, upstream publishes SHA-512 `5be2f875f73b75e5783c474bf7a6c768e433cc90283f8fc6a75e3d05bd92aec97936e8a55ccca5e880b5dacc18ba65932bab0e783e1ed5d2af4a3a4df95512be` for `tzdata2026e.tar.gz`; this digest has not been independently downloaded/verified in the present note.
2. Use the same pinned tzcode/compiler version and identical compilation flags/options for both releases. Record compiler identity and exact commands. Do not compare unlike build processes and call it data-only impact.
3. Compile both data releases to candidate TZif trees. Compute per-file SHA-256, sizes, full manifests, entry counts and path set differences. Retain full inventory with added/removed/changed paths.
4. Compare exact transition tables for every changed supported zone, emphasizing Manitoba and Ireland, and emit machine-readable expected outputs.
5. Run the complete impacted time fixtures and downstream Calculation Core golden/regression tests in a separate candidate identity. Bind every result to both TZDB version and runtime/profile digest.
6. Have an independent reviewer inspect the fixture source and expected-output derivation. Do not use the existing runtime being evaluated as the sole oracle for its own outputs.
7. Record a future owner disposition on whether a new Execution Profile revision is to be adopted. Until that disposition and the runtime adoption gates pass, 2026e remains not adopted.

## 6. Evidence status

| Claim | State |
|---|---|
| IANA 2026e release and date | Verified from official IANA release page |
| Manitoba modeled change / zones named by IANA | Verified from official release notes |
| Ireland 1925 correction | Verified from official release notes |
| CE current candidate pins 2026d and has 597-entry / digest-bound bundle | Verified from exact A9 candidate source |
| Both named zones have byte-compared CE 2026d vs 2026e compiled TZif | **NOT YET PERFORMED** |
| Full 597-entry path/hash/transition delta | **NOT YET PERFORMED** |
| 2026e expected UTC fixture values independently generated | **NOT YET PERFORMED** |
| Downstream CE impact regression run on a new 2026e candidate | **NOT YET PERFORMED** |
| Adoption / new profile revision / Runtime Adoption / production / SEAL | **NOT AUTHORIZED** |

## 7. Non-actions and result

- Current 2026d profile, compiled TZIF bundle, historical captures, A9 source and trust identity remain unchanged.
- No file in A9/PR #26 was modified.
- No normatively binding timezone policy was changed.
- No claim is made that 2026e is compatible or incompatible in every supported zone; only the two explicit upstream rule changes are identified pending the full bundle delta.
- This candidate note creates no authority.

**Recommendation:** continue with a read-only compiled-bundle delta in a separate workspace, using identical compiler/build settings and a complete path/hash manifest. If that data cannot yet be built and independently reviewed, the correct result is to preserve 2026d and leave the 2026e adoption decision open.

End of report.
