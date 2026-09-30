# CONSTELLATIONS ECLIPTIC V1 — R44 CONTROLLED RECONCILIATION CHECKPOINT

Date: 2026-09-30
Disposition: C3-1 = RECONCILE

## 1. Entry identity

Current candidate branch:
`candidate/trusted-build-hardening/2026-09-29-r3`

Current candidate HEAD:
`033e90cfd29e047578e70bbd20183e48682d7614`

Candidate source-tree SHA-256:
`da6a1d622940a4674a54d98656a940aee90aa32ec149ec9b0e8800e467a90ad9`

Canonical Data Lock:
`CE-V1-CANONICAL-DATA-2026D-SE-V2.10.3BFINAL`

Canonical lock revision:
`4`

Canonical lock SHA-256:
`0309a9d9385925f2c5eda478e2a7704e8600cf10abf258a8bcc9c4bdcb7689a2`

## 2. Controlled native-package reconciliation

Original retained package:
`CE_Calculation_Core_V1_Implementation_Native_Runtime_v0.2.2_HARDENED_NCRIT06.zip`

Original package SHA-256:
`a1f591d64dfd01a0bc86e2bfb2aab300b4b18b5edec2ca9e38a1cbd71c843e29`

Derived reconciliation package:
`CE_Calculation_Core_V1_Implementation_Native_Runtime_v0.2.2_HARDENED_NCRIT06_RECONCILED_R1.zip`

Derived package SHA-256:
`a0604b7143b3fb508596dda3e84d0fd9aa3fe32e52603791094f735a3561b2ae`

Direct ZIP verification:
- ZIP entries: 44
- Checksum manifest entries: 43
- Package files excluding checksum manifest: 43
- Missing checksum targets: 0
- Hash mismatches: 0
- Unlisted package files: 0
- ZIP integrity: PASS
- Package test suite: 22/22 PASS

Source package remains preserved and unmodified.

## 3. Critical reconciliation observation

The current Box `CE_V1_NATIVE_RUNTIME_HARDENED_NCRIT06_V0.2.2` folder is empty.
The active canonical-acquisition folder contains manifests, scripts, tests and documentation,
but the exact five canonical binary source bytes are not retained there as Box file objects.

Therefore the existing operator transcript proves that acquisition and local hashing occurred on
the Windows operator machine, but this execution environment cannot perform fresh byte-level
revalidation of those five binaries because the raw bytes are not available here.

The current operator transcript records:
- `tzdata2026d.tar.gz` size 479409 and the canonical SHA-256/SHA-512;
- `tzdata2026d.tar.gz.asc` size 833 and the canonical signature SHA-256;
- `sepl_18.se1` size 484061 and canonical SHA-256;
- `semo_18.se1` size 1304771 and canonical SHA-256;
- `seas_18.se1` size 223004 and canonical SHA-256;
- acquisition status `ACQUISITION_VERIFIED` with exit code 0;
- coverage `coverage_verified: false`.

Those operator measurements remain evidence, not a substitute for controlled byte retention.

## 4. Runtime execution gate

The reconciled native package contains the runtime code and test harnesses, but no native library,
no raw canonical `.se1` data, and no derived TZif runtime data inside the package.

The current controlled execution manifest remains NON_AUTHORIZED and contains null runtime identity
fields for native library, source build, and runtime TZif identity.

The runtime coverage validator is verification-only. It requires an already-completed report with:
- complete execution context identity;
- derived TZif SHA-256;
- three required range probes;
- all 13 required CE objects at each probe;
- all 28 required runtime test IDs PASS;
- deterministic oracle evidence;
- no prohibited fallback/network/host-TZDB behavior.

No such completed runtime coverage report exists in the current controlled evidence area.

## 5. Profile-version reconciliation

Current candidate development runtime profile:
`CE-CALC-V1-EP-001` revision `4`.

Retained Box runtime-coverage profile:
`CE-CALC-V1-EP-001` revision `2`.

This is a real version-skew finding. It is not silently resolved by editing either historical
artifact. A derived/current profile mapping must be created only after the applicable profile
revision and its source-document hashes are explicitly bound.

## 6. Native reproducibility boundary

The recorded final native DLL SHA-256 is:
`04AEDC75191CE7D257A20D6141AB889073A1CB6A501ECAD98FAA6305B24861F2`

R3 and R4 final DLLs were byte-identical.

Intermediate object reproducibility remains NOT_ESTABLISHED because R3/R4 object hashes differ.
This checkpoint does not promote that result.

## 7. Current open gates

- Canonical raw-byte controlled retention and revalidation
- IANA signer operational trust decision
- Profile revision reconciliation
- Native runtime adoption
- TZif runtime identity
- 1900–2100 runtime coverage
- Cross-platform parity
- Full Calculation Core production fixture/test gate
- Human/dual approval
- SEAL
- Production Runtime authorization

## 8. Explicit non-claims

This checkpoint does not claim:
- runtime coverage validated;
- native runtime adopted;
- Production Runtime authorized;
- SEAL;
- IANA operational trust;
- full-build object reproducibility;
- canonical byte retention in the active Box area.

## 9. Global state

SOURCE_AUTHORITY = NOT_ESTABLISHED
TRUSTED_BUILD = NOT_ESTABLISHED
PRODUCTION_RUNTIME = NOT_AUTHORIZED
DUAL_APPROVAL = NOT_ESTABLISHED
SEAL = NO
AUTHORIZATION = NON_AUTHORIZED
FAIL_CLOSED = TRUE
