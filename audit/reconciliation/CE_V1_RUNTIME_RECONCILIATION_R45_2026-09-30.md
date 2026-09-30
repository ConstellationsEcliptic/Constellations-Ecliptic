# CONSTELLATIONS ECLIPTIC V1 — R45 CONTROLLED RECONCILIATION / HUMAN BOUNDARY

Date: 2026-09-30
Human disposition: C3-1 = RECONCILE

## 1. Canonical raw-byte reconciliation

A fresh extraction from the retained current clean baseline yielded the preserved nested revalidated candidate and the separate Rev.4 lock candidate.

Fresh SHA-256 verification:
- tzdata2026d.tar.gz = 0CB2AA8E333C3DC049BADC42A0C61F21987B8CD44E107FA900BAD764AACC7767
- tzdata2026d.tar.gz.asc = 707EC6789D41FB268205DE0924680DF9A4C99B6DC9E0CF89B0D2FDAAE42D0824
- sepl_18.se1 = CA1393CEAB3A44FBC895887CF789C68819AE6A1CBC9B22225872DBE4CCD99A66
- semo_18.se1 = 1CA07BD67C24374D77226180C20A4F9996CBA013697894810518E7EB582CA4F7
- seas_18.se1 = A2CD8FC33807C78CA9A700C91C2E042258B12FC4796519E00781440B5AD8B2E2

Fresh Rev.4 lock verification:
- lock SHA-256 = 0309a9d9385925f2c5eda478e2a7704e8600cf10abf258a8bcc9c4bdcb7689a
- lock sidecar matches

Fresh Swiss aggregate recomputation:
- 0cfc76a9dc51296f2241492e3376f1e71d13dd4f36b476253d4b82df57dfc990

Derived canonical bundle:
- CE_V1_CANONICAL_DATA_CURRENT_REV4_RECONCILED_R1.zip
- SHA-256 = 330374719837f50db398756803d2ba8db25536577812aed1c7a46fc09c87c090
- ZIP integrity = PASS

The parent historical/current source artifacts were not modified.

## 2. IANA cryptographic verification

Fresh detached-signature verification against the preserved exact 2026d archive:
- GOODSIG = present
- VALIDSIG = present
- fingerprint = 7E3792A9D8ACF7D633BC1588ED97E90E62AA7E34
- TRUST_UNDEFINED = present

Conclusion: cryptographic signature validity is established. Operational trust remains a human governance decision and is not inferred.

## 3. TZif derivation and execution check

Derived from the exact 2026d source archive with zic (Debian GLIBC 2.41-12+deb13u3) 2.41.

Derived TZif dataset:
- 597 TZif files
- manifest SHA-256 = c0c7a9f32c37c2aae1299bcfcb774231d63f4bb1def9d91645996b1c661ff73b
- bundle SHA-256 = f3edd74a1bb77d092d6c2ed3eead8ebea9657954f5bb30b0ac031a08a5eed942
- ZIP integrity = PASS

Actual Python ZoneInfo execution used only the derived TZif root and exercised the 1900, 2000 and 2100 probe instants. Five representative zones loaded at each probe.

This proves the derived TZif bundle is executable and internally usable. It does not by itself establish CE runtime adoption.

## 4. Non-authoritative Swiss runtime diagnostic

An installed Linux Swiss Ephemeris 2.10.03 extension was executed with the exact canonical .se1 files.

Observed:
- 13 CE objects x 3 probes = 39 calculation calls
- all returned VALID results
- all actual flags = 258 = SWIEPH|SPEED
- module SHA-256 = 9663f57768a61c7c736290c732c0d856654972197edb3b2f84ca6d7e77c718f3

This is diagnostic only because the module binary is not byte-bound here to the exact CE-pinned Swiss source commit/tree. It is not trusted-build or runtime-coverage evidence.

## 5. Execution Profile reconciliation

Current controlled profile lineage establishes CE-CALC-V1-EP-001 revision 4, profile version 1.3, Implementation Plan v1.3.1, Technical Contracts v1.1, and Canonical Data Lock revision 4.

A machine-readable runtime-coverage R4 candidate was derived mechanically from the retained R2 coverage profile for revision alignment. It remains CANDIDATE_NON_AUTHORIZED.

## 6. Native package reconciliation

Derived native package:
CE_Calculation_Core_V1_Implementation_Native_Runtime_v0.2.2_HARDENED_NCRIT06_RECONCILED_R1.zip

SHA-256:
a0604b7143b3fb508596dda3e84d0fd9aa3fe32e52603791094f735a3561b2ae

Internal checksum reconciliation: 43/43 covered files PASS; 0 mismatch; 0 missing; 22/22 package tests PASS.

The exact current native DLL expected SHA-256 is 04AEDC75191CE7D257A20D6141AB889073A1CB6A501ECAD98FAA6305B24861F2.

However, the exact DLL is not currently present in this execution environment and the Windows MSVC host is not accessible here. Therefore DLL-to-current-runtime execution evidence is not yet established.

## 7. Human boundary reached

All machine-verifiable work available in the current environment has now been advanced to the point where the next mandatory evidence requires the controlled Windows host.

Operator action:
run scripts/run_ce_runtime_reconciliation.ps1 from the Human Handoff package.

The script verifies supplied hashes, stages canonical data and TZif, verifies the exact Swiss commit and tag, builds libswe.dll with the recorded MSVC recipe, requires the expected DLL hash, captures runtime identity evidence, and stops without SEAL or Production Runtime authorization.

## 8. Remaining human governance boundary

- IANA signer operational trust
- formal human/dual approval and SEAL after all technical gates are complete

## 9. Global state

SOURCE_AUTHORITY = NOT_ESTABLISHED
TRUSTED_BUILD = NOT_ESTABLISHED
PRODUCTION_RUNTIME = NOT_AUTHORIZED
DUAL_APPROVAL = NOT_ESTABLISHED
SEAL = NO
AUTHORIZATION = NON_AUTHORIZED
FAIL_CLOSED = TRUE