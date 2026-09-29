# CE V1 Trusted Build Hardening — Candidate R1

## Purpose

This candidate turns the successful reproducibility audit into a durable, explicit build-input contract without changing PR #5.

## Exact build inputs

- CPython 3.13.15 x86_64
- GitHub-hosted ubuntu-24.04 runner; observed image version 20260920.314.1
- actions/setup-python v7 pinned to commit 5fda3b95a4ea91299a34e894583c3862153e4b97
- pip 26.2.1, locked by SHA-256
- setuptools 82.0.1, locked by SHA-256
- runtime dependencies: none
- build network: disabled after dependency acquisition
- SOURCE_DATE_EPOCH=0

## Important boundary

This package is a candidate hardening state. It does not establish Trusted Build, Production Runtime authorization, or SEAL.

The GitHub-hosted runner image is versioned in this candidate but is not content-addressed. Formal Trusted Build establishment therefore remains blocked on a governance decision about the accepted immutable environment identity.

## Required provenance

A future accepted build must bind, in one machine-readable record:

source commit
→ source-tree SHA-256
→ exact Python/toolchain identity
→ exact dependency artifact hashes
→ build configuration
→ output artifact hashes

Any mismatch must fail closed.

## Change-control rule

These files are intentionally placed on a separate candidate branch. They must not be merged into PR #5 without a new source-authority attestation for the new candidate commit.
