# Native Runtime Package Checksum Reconciliation R1

Date: 2026-09-30

## Source artifact

Filename:
CE_Calculation_Core_V1_Implementation_Native_Runtime_v0.2.2_HARDENED_NCRIT06.zip

Source SHA-256:
a1f591d64dfd01a0bc86e2bfb2aab300b4b18b5edec2ca9e38a1cbd71c843e29

Source entry count:
44

## Finding

The retained package's internal SHA256SUMS.txt was not self-consistent with the
current package bytes. It also used path/hash ordering rather than the common
GNU checksum ordering.

Seven current-file discrepancies were found when comparing the manifest to the
package bytes. Six previously recorded stale entries were confirmed, and
docs/CHANGELOG_0.2.2.md was also present without a corresponding manifest entry.

The affected paths are:

- README.md
- docs/CHANGELOG_0.2.2.md
- pyproject.toml
- src/ce_calculation_core/attestation.py
- src/ce_calculation_core/manifest.py
- src/ce_calculation_core/native.py
- tests/test_native_fail_closed.py

## Controlled reconciliation

The source package was not modified.

A derived package was created by preserving the original ZIP entries and
replacing only the internal SHA256SUMS.txt with hashes calculated from the
current package bytes. The checksum file excludes itself, and all other files
are covered.

Derived artifact:
CE_Calculation_Core_V1_Implementation_Native_Runtime_v0.2.2_HARDENED_NCRIT06_RECONCILED_R1.zip

Derived SHA-256:
a0604b7143b3fb508596dda3e84d0fd9aa3fe32e52603791094f735a3561b2ae

Derived size:
41420 bytes

Derived entry count:
44

Post-reconciliation verification:
- Manifest entries excluding SHA256SUMS.txt: 43
- Actual files excluding SHA256SUMS.txt: 43
- Hash mismatches: 0
- Missing manifest entries: 0

## Interpretation

This reconciliation closes only the package-internal checksum consistency issue
for this derived artifact. It does not establish native runtime adoption,
native object reproducibility, TZif runtime identity, 1900–2100 coverage,
cross-platform parity, production Calculation Core authorization, SEAL, or
Production Runtime authorization.

The derived package therefore remains a non-authoritative candidate artifact.

## Governance

SOURCE_AUTHORITY = NOT_ESTABLISHED
TRUSTED_BUILD = NOT_ESTABLISHED
PRODUCTION_RUNTIME = NOT_AUTHORIZED
DUAL_APPROVAL = NOT_ESTABLISHED
SEAL = NO
AUTHORIZATION = NON_AUTHORIZED
FAIL_CLOSED = TRUE
