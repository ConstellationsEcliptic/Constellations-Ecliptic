# CONSTELLATIONS ECLIPTIC
# C1-R3 SOURCE AUTHORITY HARDENING — REGRESSION COVERAGE GAP R0

**Date:** 2026-10-20  
**Classification:** SOURCE-BOUND AUDIT FOLLOW-UP / NON-NORMATIVE / NO AUTHORITY EFFECT  
**Historical artifact:** C1-R3 cumulative audit bundle, preserved unchanged  
**Disposition:** EXISTING MUTATION-TEST PASS RETAINED; ADDITIONAL SYMLINK / OPTIMIZED-MODE COVERAGE REQUIRED

## 1. Purpose

Record a narrow, reproducible test-coverage limitation discovered by reading the exact extracted C1-R3 audit package after R28. This is not a challenge to the recorded byte-mutation test result, not a claim of a new production vulnerability, and not permission to modify the historic package in place.

## 2. Exact artifacts and identities

- Historical C1-R3 bundle in Box: [CE_V1_C1_SOURCE_AUTHORITY_CUMULATIVE_REHARDENING_AUDIT_R3-2026-09-24.zip](https://account.box.com/file/2485694135130); size **124,019,414 bytes**, SHA-1 `a0e83db5d928ca07ac10748d2fd7fa81650214c7`.
- Extracted authoritative package tree name: `CE_V1_C1_SOURCE_AUTHORITY_CUMULATIVE_REHARDENING_AUDIT_R3-2026-09-24`.
- Embedded hardened validator: `tools/validate_source_authority_r1_hardened.py`; package manifest SHA-256 `ed1b1129f812235722b159e41f72a134aeac79f1d8c8d37cc590d456bb744e34`, size 5,226 bytes.
- Embedded adversarial test: `tests/adversarial_source_authority.py`; package manifest SHA-256 `343e914ca7f1356f6848dae9acac32ff51fb37b688fa78c74bb43599397a4786`, size 2,175 bytes.
- Embedded execution log: `evidence/VERIFICATION_EXECUTION_LOG.txt`; package manifest SHA-256 `d77ad0b63bf5297806a02701de9f1247ffda50f1dee390ddbe3ae62cc675cee5`.
- Exact historical Source Authority Resolution R1 parent: SHA-256 `f192d744eaabd59d37d1a5a5b78cf71d7c6cfbb22c7080f5abbe95c27fce347b`, 17,073,303 bytes.

The R3 manifest binds the extracted test and validator source. The original C1-R3 archive, parent ZIP, report, manifests, and pinned bytes must remain unchanged.

## 3. What the current evidence establishes

The archived `tests/adversarial_source_authority.py` reproduces the original security issue for a one-byte mutation of `seas_18.se1`:

- Legacy validator, normal execution: rejects (non-zero return).
- Legacy validator under `python -O`: incorrectly accepts (return code 0).
- Hardened validator after the mutation, normal execution: rejects (return code 20).
- Hardened validator after the mutation, `python -O`: rejects (return code 20).

The hardened validator contains explicit `req(condition, message)` checks rather than Python `assert` for the checked invariants. It also checks canonical ephemeris directory membership against the exact expected three-file set and checks for symlinks beneath the supplied root.

This supports the retained C1-R3 result for the tested byte-mutation path. The C1-R3 status still correctly says Source Authority is NOT ESTABLISHED and production AUTHORIZATION is NON_AUTHORIZED.

## 4. Newly observed coverage gap

The only file listed under the archived C1-R3 `tests/` folder is `adversarial_source_authority.py`. In that file, the section comment says “symlink/extra file mutation”, but the actual operation:

1. deletes the ephemeris directory;
2. recreates it;
3. writes `UNEXPECTED.se1`; and
4. invokes the hardened verifier **only in normal execution mode**.

The script does not create a symbolic link, does not exercise the hardened validator’s symlink-rejection branch, and does not run the extra-file mutation under `python -O`. The archived execution log likewise records normal/`-O` return codes for the byte mutation, but not separate symlink or optimized extra-file results.

This is a **test-coverage gap, not proof of a verifier defect**. Static inspection shows explicit symlink rejection in the hardened validator’s `safe_tree`; the missing point is an independently repeatable negative-path test that exercises the rejection behavior in both interpreter modes. The report’s wording that symlink checks were also a concern does not replace a test case that actually constructs the symlink.

## 5. Proposed successor test matrix (not yet run / not a result)

Run each destructive case against a fresh extraction of the exact Source Authority R1 parent and preserve logs. Do not reuse a mutated fixture.

| Case | Legacy verifier | Hardened verifier | Required modes |
|---|---|---|---|
| Pristine, exact R1 parent | Baseline expected result | Must pass structural validation | Normal and `python -O` |
| One-byte mutation to canonical `.se1` | Normal rejects; `-O` expected to expose legacy defect | Must reject | Normal and `python -O` |
| Extra file in canonical ephemeris directory | Record legacy result for both modes | Must reject | Normal and `python -O` |
| Expected `.se1` replaced by a symlink to a byte-identical external file | Normal rejects if the legacy path contains an explicit non-symlink check; `-O` negative path must be measured | Must reject | Normal and `python -O` |
| Symlink introduced at another path under the inspected root | Measure legacy behavior; do not assume | Must reject | Normal and `python -O` |

If the test platform cannot create symlinks (for example because OS permissions prohibit it), report the case as **NOT RUN / UNSUPPORTED**, never PASS. Run the symlink case on a supported POSIX runner or other environment with known symlink capability. Keep the legacy mutation reproduction distinct from a proof that the hardened verifier is currently adopted by the production authority chain.

## 6. Acceptance criteria for a successor test artifact

1. It is new, separately versioned, and cryptographically bound; it does not overwrite any file in the C1-R3 bundle.
2. Every negative-path test starts from a fresh copy whose parent ZIP hash is checked before extraction.
3. It checks explicit exit codes and outputs, not Python `assert` as the only test oracle for security-sensitive results.
4. The symlink and unexpected-file cases are each run both normally and with `python -O`.
5. The logs report platform, interpreter version, parent hash, candidate script hash, input mutation and exact result.
6. Any unsupported negative case is explicitly left uncovered.
7. It does not change current Authority, Trusted Build, Runtime Adoption, SEAL or Authorization status without the rest of the governing assurance chain.

## 7. Disposition

Preserve the existing C1-R3 adversarial byte-mutation result. Add the missing symlink and optimized-mode extra-file tests only in a separately identified successor test artifact, then review and bind that artifact into the legitimate current assurance chain. Do not edit or re-sign the historic R1 or C1-R3 archives in place.

Current state remains:

```text
C1_R3_BYTE_MUTATION_HARDENING = RECORDED_PASS
C1_R3_SYMLINK_NEGATIVE_PATH_TEST = NOT_PRESENT_IN_BUNDLED_TEST
C1_R3_EXTRA_FILE_OPTIMIZED_NEGATIVE_PATH_TEST = NOT_PRESENT_IN_BUNDLED_TEST
SOURCE_AUTHORITY = NOT_ESTABLISHED
TRUSTED_BUILD = NOT_ESTABLISHED
PRODUCTION_RUNTIME = NOT_AUTHORIZED
SEAL = NO
AUTHORIZATION = NON_AUTHORIZED
FAIL_CLOSED = TRUE
```

**End of report.**
