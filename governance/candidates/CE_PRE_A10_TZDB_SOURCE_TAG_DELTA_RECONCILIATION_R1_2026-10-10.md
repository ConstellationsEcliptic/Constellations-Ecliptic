# CE PRE-A10 TZDB SOURCE-TAG DELTA RECONCILIATION R1

**Date:** 2026-10-10  
**Classification:** SOURCE-LEVEL RECONCILIATION / WORKING CANDIDATE / NON-AUTHORITATIVE  
**Authority effect:** NONE  
**Execution Profile / TZIF bundle change:** NONE  
**Runtime Adoption / production / SEAL effect:** NONE  
**Current profile:** CE-CALC-V1-EP-001 revision 4, IANA 2026d — PRESERVE  
**IANA 2026e:** NOT ADOPTED

## 1. Purpose and boundary

This addendum advances the existing TZDB impact note by binding the two announced release changes to the exact upstream source files at the `2026d` and `2026e` tags. This is stronger than release-note-only identification, but it is **not** a compiled TZIF bundle diff, an independent compilation, or a downstream CE regression.

The container has no working DNS/network route to fetch IANA release archives (`curl https://data.iana.org/time-zones/releases/tzdata2026e.tar.gz` failed with name resolution). The local system reports `zic (Debian GLIBC 2.41-12+deb13u3) 2.41`, but no archive was compiled with it. Do not claim byte-level output from that compiler.

## 2. Upstream release identity

IANA’s official release page marks **2026e** released on **2026-09-29** and latest; its release history lists 2026d immediately before it. The official announcement identifies tzdb source commit `039ef27cc5f062a2055cb67435d6d71adbefd27d`, tagged `2026e`, and publishes SHA-512 for `tzdata2026e.tar.gz`:

`5be2f875f73b75e5783c474bf7a6c768e433cc90283f8fc6a75e3d05bd92aec97936e8a55ccca5e880b5dacc18ba65932bab0e783e1ed5d2af4a3a4df95512be`

That archive digest is **upstream-published, not locally downloaded or independently verified in this work**.

Sources:
- IANA 2026e: https://www.iana.org/time-zones/releases/2026e
- IANA release history: https://www.iana.org/time-zones/releases
- Upstream release announcement and signatures/checksums: https://lists.iana.org/hyperkitty/list/tz%40iana.org/thread/VXIA4AU73OQL3OZ3ZBZHWIASIIVBGUJV/
- Upstream source repository: https://github.com/eggert/tz

## 3. Exact tagged source file identities

The GitHub content API returned these Git blob identifiers for files at the stated upstream tags:

| Source file | 2026d Git blob SHA-1 | 2026e Git blob SHA-1 | Result |
|---|---|---|---|
| `northamerica` | `e5f858272c8b9a9faa0953b7fe01252c140f54fb` | `e3a4bd6d5332b901961381432a6f53cc95ce530f` | Changed |
| `europe` | `0dc31d9d85e62bd252aabf8a1ff4b7a67de39dca` | `c29d1f53db337aa9b5fffe3911bf93136b7cec61` | Changed |
| `backward` | `2971d038b9e615111c5ce077acd005315c222d07` | `2971d038b9e615111c5ce077acd005315c222d07` | Identical |

These are **Git object/blob identifiers**, not SHA-256 or SHA-512 digests of the release archives or compiled TZIF files. The table binds the source comparison to repeatable upstream tags and file objects.

## 4. Delta A — Manitoba / America-Winnipeg

### 4.1 Source difference

At tag `2026d`, `northamerica` defines `America/Winnipeg` with its Canada rules continuing after the 2006 history line:

```text
Zone America/Winnipeg  -6:28:36 -      LMT   1887 Jul 16
                          -6:00      Winn  C%sT  2006
                          -6:00      Canada C%sT
```

At tag `2026e`, the source adds a bounded Canada-rule interval, a temporary compatibility interval ending at the modeled 2026-11-01 02:00 boundary, and permanent UTC−05 / EST thereafter:

```text
Zone America/Winnipeg  -6:28:36 -      LMT   1887 Jul 16
                          -6:00      Winn  C%sT  2006
                          -6:00      Canada C%sT  2026 Oct 31
                          -6:00      Canada CDT  2026 Nov 1  2:00
                          -5:00      -      EST
```

The official release note explains that Manitoba's legal permanent UTC−05 change takes effect 2026-10-31, while tzdb temporarily models the clock change at **2026-11-01 02:00** to work around downstream CLDR limitations.

### 4.2 Backward-compatible alias

The `backward` file is byte-identical at the retrieved Git blob level for both tags and contains:

```text
Link America/Winnipeg Canada/Central
```

Therefore the source does not add a distinct rule body for `Canada/Central`; it resolves through the changed `America/Winnipeg` target in the normal tzdb link model. The actual CE compiled alias file still needs to be checked against the 597-entry package manifest before declaring the package-level identity impact complete.

### 4.3 Required CE fixtures

For the unchanged 2026d profile versus a separate 2026e candidate, build exact fixtures for `America/Winnipeg` and `Canada/Central` immediately before, at, and after the modeled transition; include the civil day boundary for 2026-11-01 and later supported dates. Record local input, UTC result, offset, abbreviation, resolution status, full half-open zero-birth interval endpoints, and runtime/profile identity. Derive expected values from each exact compiled TZIF output, not from a guessed one-hour offset.

## 5. Delta B — Ireland / Europe-Dublin

### 5.1 Source difference

At tag `2026d`, after Irish independence the `Europe/Dublin` source continues the `GB-Eire` rule set through the 1940 line:

```text
0:00  GB-Eire  %s       1921 Dec  6
0:00  GB-Eire  GMT/IST  1940 Feb 25  2:00s
```

At tag `2026e`, the zone instead explicitly ends the `GB-Eire` segment at the September 1925 transition, then remains GMT until 1926 before following later historical rules:

```text
0:00  GB-Eire  %s       1921 Dec  6
0:00  GB-Eire  GMT/IST  1925 Sep Sun>=16  2:00s
0:00  -        GMT      1926
0:00  GB-Eire  GMT/IST  1940 Feb 25  2:00s
```

The 2026e source comment explains that Ireland's 1925 Summer Time Act ended summer time on 1925-09-20; the October date applied in Great Britain from 1925 but in the Irish Free State only from 1926. Thus this is a real historical-zone source change within CE's stated 1900–2100 domain, not merely a comment correction.

### 5.2 Backward-compatible alias

The `backward` file is identical in both tagged blobs and includes:

```text
Link Europe/Dublin Eire
```

The alias definition itself is unchanged, while its target zone's historical rules change. Confirm inclusion and bytes of the compiled `Eire` link in the CE runtime package rather than assuming that presence from upstream alone.

### 5.3 Required CE fixtures

For `Europe/Dublin` and, if present in the exact manifest, `Eire`, compare the 1925-09-20 transition under both compiled releases; include local instants just before, at, and after the transition, plus full-day half-open intervals spanning 1925-09-20 and the old October date. Record exact UTC outputs, offsets, abbreviation, interval endpoints and profile identity. Do not treat a current host `zoneinfo` database as the expected-value authority.

## 6. What is established / still open

| Item | State |
|---|---|
| IANA 2026e is newer than 2026d; official release date and named changes | VERIFIED from official IANA sources |
| `northamerica` changes `America/Winnipeg` rule structure between exact upstream tags | VERIFIED from tagged source file identities and contents |
| `europe` changes the `Europe/Dublin` historical 1925 rule structure between exact upstream tags | VERIFIED from tagged source file identities and contents |
| `backward` alias definitions for `Canada/Central` and `Eire` | SOURCE FILE IDENTICAL at both tags |
| CE's existing profile pins 2026d, 597 entries, bundle SHA-256 `f3edd74a1bb77d092d6c2ed3eead8ebea9657954f5bb30b0ac031a08a5eed942`, manifest SHA-256 `a12881024bee3b801d63b0d9cb74118b6329512f63020f36c42412de1e0a6205` | VERIFIED from exact A9 candidate source |
| 2026d and 2026e official data archives fetched and signature/checksum verified locally | NOT PERFORMED |
| Both releases compiled with the same pinned tzcode/zic version and identical options | NOT PERFORMED |
| Full path-set and SHA-256 comparison for all 597 CE package entries | NOT PERFORMED |
| Parsed transition-table diff for all changed compiled zones | NOT PERFORMED |
| Independently derived exact UTC regression vectors and CE downstream run | NOT PERFORMED |
| 2026e adoption, new execution profile, TZIF runtime identity, Runtime Adoption, production, or SEAL | NOT AUTHORIZED / NOT ESTABLISHED |

## 7. Next admissible technical sequence

1. Obtain exact `tzdata2026d`, `tzdata2026e`, and the pinned/approved tzcode toolchain through an environment that can access IANA release archives; retain upstream signatures and independently verify their digests.
2. Compile both releases with the same controlled compiler and exact options; emit full path, size and SHA-256 manifests for the exact policy-owned CE zone set.
3. Diff all package paths and hashes, then parse transition changes for every changed supported zone—not only the two named cases.
4. Generate source-bound local-to-UTC and half-open-interval vectors for affected zones, and run downstream evidence/signal regressions under a new isolated candidate identity.
5. Obtain independent expected-value review before any future owner decision about a new profile or adoption.

Until then, preserve the exact 2026d profile and all 2026d capture identities. No in-place upgrade or release-label change is permitted by this note.

## 8. Non-actions

- No source normative file or A9 candidate was modified.
- No TZIF bundle, manifest, Execution Profile or historic capture was changed.
- No official test register was promoted.
- No Source Authority, Trusted Build scope, Runtime Adoption, production authorization, merge permission or SEAL state changed.

**End of R1.**
