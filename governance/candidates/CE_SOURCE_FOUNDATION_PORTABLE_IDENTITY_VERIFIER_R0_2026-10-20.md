# Portable Source Identity Verification Candidate R0

**Date:** 2026-10-20  
**Status:** Draft technical candidate / non-normative / no authority effect  
**Purpose:** Address the observed audit limitation where Source Foundation identity verification could not run because the extracted evidence lacked a Git object database.

## Source-bound basis

The C1-R3 cumulative audit identified:
- Source Foundation R1 stage identity: 0e207377d398701b52c4517c1236e7c31e8e36db6e3f98b22fc97bbf6e06b5ad.
- Source Foundation's verify_foundation.py: PASS.
- verify_source_identity.py: HARNESS LIMIT because the Git object database was absent.
- The global audit remains Source Authority NOT_ESTABLISHED, Trusted Build NOT_ESTABLISHED, production runtime NOT_AUTHORIZED, authorization NON_AUTHORIZED, fail-closed TRUE.

The prior lineage also contains a source identity capture/verification design. Its CE_SOURCE_TREE_SHA256_V1 algorithm derives sorted records of blob mode, repository-relative path, and SHA-256 of content bytes. The verifier expects the exact Git commit, Git tree OID, computed source-tree digest, and tracked-file count.

## Candidate approach

The candidate verifier accepts three separate objects: an offline Git bundle, the identity statement, and a materialized source snapshot without a .git directory. It requires separately supplied expected SHA-256 pins for the exact bundle bytes and identity statement. It then:
1. checks those external content pins;
2. verifies and clones the Git bundle locally without network access;
3. re-derives commit, tree, blob object IDs and the source-tree digest from Git object bytes;
4. checks the source snapshot's exact file set, bytes, and executable modes against the committed Git tree; and
5. reports SOURCE_IDENTITY_CONSISTENCY_PASS_NOT_AUTHORITY.

The tool rejects missing/unpinned evidence, unsupported object modes, submodule entries, unsafe paths, symlinks in the source snapshot, mismatched file set/content/modes, and identity drift. It does not claim to create authority: independent signer verification, exact external pin provenance, owner review, Trusted Build, runtime promotion, and the rest of the governance chain remain separate gates.

## Test status

The companion candidate workflow constructs a synthetic local Git repository and offline Git bundle. It exercises the portable verifier against a source snapshot that contains no .git directory, then negative-path tests for extra files, modified content, executable-mode mismatch, and changed bundle bytes. These tests demonstrate the verifier mechanism only. They do not re-verify actual Source Foundation R1 bytes or close the historical audit's missing Git-object evidence.

## Required real-world closure

To use the candidate against Source Foundation R1, a separate approved evidence process must supply the exact source snapshot and an independently bound full Git bundle/object pack for the declared commit, with expected bundle and identity hashes backed by the proper signed or otherwise controlled provenance. Do not synthesize or guess the original commit/tree identity; do not replace the historic package or alter any pinned parent. When those exact inputs are available, run the byte-bound verification and the cumulative parent gates from the original audit order.

**Disposition:** useful proof-of-concept candidate only. No Source Authority, Trusted Build, Runtime Adoption, production, SEAL, payment, or release authorization follows.
