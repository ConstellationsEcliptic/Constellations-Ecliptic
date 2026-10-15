# CONSTELLATIONS ECLIPTIC
# CLEAN CURRENT SET R3 — BYTE AND MEMBER-LINEAGE AUDIT R0

**Date:** 2026-10-10  
**Classification:** READ-ONLY FORENSIC EVIDENCE / WORKING CANDIDATE / NON-AUTHORITATIVE  
**Authority effect:** NONE  
**Normative amendment:** NONE  
**Runtime / production / SEAL effect:** NONE  
**Scope:** exact bytes of the retained Clean Current Set R3 archive, its internal manifest, and comparisons to the specifically characterized Box source copies.

## 1. Exact archive identity — now directly verified

Artifact: `CE_V1_CLEAN_CURRENT_SET_R3-2026-09-24.zip`  
Box ID: `2485715303669`  
Library materialized file: `CE_V1_CLEAN_CURRENT_SET_R3-2026-09-24.zip`  
Size: `2,654,872` bytes  
SHA-1: `58f8c3dcccc0ccb2e79a79ddd46ab0014c2783d6`  
SHA-256: `d9c2f4abbe0a482e982488d5d2e332202c0c0dc8fceca3b5faaceb3d2c4a8abc`

The archive was materialized from the ChatGPT Library source item and independently hashed locally. The exact outer size, SHA-1 and SHA-256 match the current-governing Box boundary record, Box object metadata, and available SHA-256 sidecar text. A second Library item with the underscore filename variant produced the same size, SHA-1 and SHA-256.

ZIP integrity check: `PASS` (`ZipFile.testzip() = None`).  
Entries: `74`.  
Payload count in `00_START_HERE/FILE_INDEX_R3.md`: `72`.  
Internal `00_START_HERE/CE_V1_CLEAN_CURRENT_SET_R3_SHA256SUMS.txt`: `72/72` listed payload SHA-256 values matched; no missing entries or mismatches.

This proves the exact archive bytes and integrity of the archive's 72 manifest-listed payload files. It does **not** prove production authority, and it does not silently elevate every file in the archive to current normative authority.

## 2. Byte comparisons to the characterized source copies

The following comparisons use SHA-1 and size from Box's exact file metadata against SHA-1 and size computed directly from the archive member bytes. The active successor identities are independently recorded by the 2026-09-28 Constitutional Harmonization Application Record (Box 2491700051951), Post-Apply Verification (Box 2491702950277), Active Implementation Pointer R3 (Box 2491701889475), and the 2026-10-04 Stack Index/Manifest. Those are scoped control/identity records; none grants production authority.

| Subject | Exact Clean Set R3 member identity | Characterized source identity | Result |
|---|---|---|---|
| Calculation Constitution v1.9 | SHA-1 `72abaeee50c3d49607cd99756df58f90ff96f8bf`; 19,235 bytes | Box 2485336984594; same SHA-1 and size | **EXACT MATCH** |
| Signal Engine Core v1.4 | SHA-1 `2408a9c84d4148c9f2cb37506b238b82a020a67b`; 9,438 bytes | Box 2485335414676; same SHA-1 and size | **EXACT MATCH** |
| Interpretive Canon v1.2 | SHA-1 `7ee32ee5f74477cf2674b50182be42aa8c5d439a`; 6,817 bytes | Box 2485337228722; same SHA-1 and size | **EXACT MATCH** |
| Evidence/AI Output Validation v1.4 | SHA-1 `bb95c2b6edcb1eb1e47477ebd776287aa21372bd`; 15,992 bytes | Box 2485336395859; same SHA-1 and size | **EXACT MATCH** |
| Account/Privacy/Commercial v1.7 | SHA-1 `39d3bcb982105f3442ba2b80a9803ce6ed869e39`; 16,741 bytes | Box 2485319995048; same SHA-1 and size | **EXACT MATCH** |
| Business Model Minimal V1 v1.5 | SHA-1 `653f7fd8803106b3a37427e87f1f182ea45ad1fd`; 10,690 bytes | Box 2485331476456; same SHA-1 and size | **EXACT MATCH** |
| Privacy Architecture Minimal V1 v1.5 | SHA-1 `21d08f82020aafe590397ec59d95404b3b210e0b`; 29,661 bytes | Box 2485335589220; same SHA-1 and size | **EXACT MATCH** |
| Product Constitution v1.6 in archive | SHA-1 `eec234e81b3948304ea3148938ed55691246fcb7`; 10,361 bytes | Characterized v1.6.1 successor: Box 2491704535193, SHA-1 `1fde1d44736e45614e8050769e60be6a875d964e`, 11,996 bytes | **DISTINCT VERSIONS; controlled successor record found** |
| Implementation Plan v1.3 in archive | SHA-1 `98cbb133323aac589039d6c81f4b204df1d2e204`; 41,779 bytes | Characterized v1.3.1 successor: Box 2491699264134, SHA-1 `684a1266287ca278ff0e68b0d4c991cca7e9098b`, 41,518 bytes | **DISTINCT VERSIONS; controlled successor record found** |
| Technical Contracts v1.0 in archive | SHA-1 `ad451dd496ef2990edb1234b779e82b49ab3cbc1`; 29,190 bytes | Characterized v1.1 successor: Box 2491699792103, SHA-1 `4ab2177f5a2cba26d8025399509378fb821e4349`, 30,349 bytes | **DISTINCT VERSIONS; controlled successor record found; NORM-META-001 remains open** |

The documented successor record says `DISPOSITION=APPLY`, `APPLICATION=COMPLETED`, `LINEAGE_MODE=SUCCESSOR MATERIALIZATION`, and `HISTORICAL_BYTES=PRESERVED` for Product v1.6.1, Implementation Plan v1.3.1, Technical Contracts v1.1 and Execution Profile v1.3/rev4. The Post-Apply Verification records PASS for those identities and retains the source/runtime/production hard blocks. Hence the table's three differences are identified version succession, not grounds to overwrite the older archive members.

## 3. Execution Profile and test-register boundary

The harmonized Canonical Execution Profile `CE-CALC-V1-EP-001`, version 1.3 / revision 4, is a separate successor artifact (Box 2491702000320; SHA-1 `9b2b4b7f833927867bc34cfbbc416a78d0d56849`; 24,190 bytes). It is **not** a member of this Clean Set R3 archive.

Likewise `07_EXECUTION_PROFILE_TEST_REGISTER.md`, Box 2485336117840 (SHA-1 `973749ba88112a7b4202c807bcc7635d286a5ea9`; 27,957 bytes), is **not** a member of this archive. This absence is consistent with `00_START_HERE/EXCLUDED_SUPERSEDED_FILES_R3.md`, which explicitly lists the “legacy Execution Profile/Test Register v1.5” among intentionally excluded artifacts. However, `01_NORMATIVE/00_DOCUMENT_INDEX.md` still lists `07_EXECUTION_PROFILE_TEST_REGISTER.md` in its nominal document stack.

**Finding R3-PKG-INDEX-001:** the packaged document index and package-exclusion record are internally inconsistent/stale with respect to document 07. The exclusion record clarifies that the v1.5 register is legacy and excluded from the clean set; the characterized 2026-10-04 Stack Index/Manifest does not bind a current successor Test Register. Therefore:

- do not treat the raw-intake Box copy of Test Register v1.5 as the currently established official CE behavior-test oracle merely because its old index entry exists;
- the current authorized CE behavior-test/oracle source remains **NOT_ESTABLISHED in the inspected characterized stack**;
- the pre-A10 validator's 14 unit tests are tests of the register-gating tool, not the missing CE product/calculation behavior suite;
- no test-register substitute or replacement oracle is created by this report.

## 4. Remaining internal package reconciliation

The archive's own `00_DOCUMENT_INDEX.md` has conflicting header/status language (“v1.9”, “v1.8”, “Release V1.6”) and references a nominal ten-document stack including item 07. The archive's exclusion record says the old item 07 is deliberately excluded. Keep both byte-preserved as evidence. Do not edit the archive, rebuild/relabel it, or amend the normative index through this finding.

The current governing archive itself remains the exact 2,654,872-byte R3 artifact identified above. The verified 490,850,627-byte six-part full-master backup is a separate artifact family and must not be confused with it.

## 5. Authority interpretation and non-actions

- Archive identity/integrity: **VERIFIED** for the exact R3 bytes stated above.
- Seventy-two manifest-listed payload files: **SHA-256 matched 72/72**.
- Seven compared characterized document copies listed as exact: **EXACT MATCH**.
- Product v1.6 / Plan v1.3 / Contracts v1.0 to their later harmonized successors: **DISTINCT BYTE IDENTITIES**, with a separate controlled successor application record found for each.
- Execution Profile v1.3/rev4: characterized successor artifact, not a member of the R3 ZIP.
- Test Register v1.5: explicitly excluded legacy artifact, not a member of the R3 ZIP; a current successor test-oracle source is not established in the inspected stack.
- NORM-META-001 / NORM-META-002 remain open.
- No normative document, official test register, A9/A10 source code, runtime, trust root, source authority, production state, or SEAL was modified or established by this work.

This is read-only forensic characterization and a candidate governance finding. It is not an amendment or authority transition.

End of report.
