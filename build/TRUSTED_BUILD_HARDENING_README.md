# CE V1 Trusted Build Hardening — Candidate R2

## Purpose

This candidate upgrades the build-environment identity from a merely versioned hosted runner to a content-addressed container image while preserving fail-closed governance.

PR #5 is not modified by this candidate.

## Immutable build environment

Base image:
`python:3.13.15-slim-bookworm@sha256:3e2de9c40ca4e3d73240059f9d48baff27908f10293e985a2f382a0378e6df4a`

Platform:
linux/amd64

The digest is the environment identity. The mutable tag is informational only.

The GitHub-hosted runner and Docker engine remain external substrate and are not claimed to be immutable.

## Exact build inputs

- CPython 3.13.15 x86_64
- pip 26.2.1, content hash locked
- setuptools 82.0.1, content hash locked
- runtime dependencies: none
- dependency installation from pre-fetched artifacts only
- network disabled during the actual build
- SOURCE_DATE_EPOCH=0
- bytecode generation disabled by build/test tooling

## Evidence

The preceding R1 audit established reproducibility on the hosted runner. R2 must demonstrate that the same reproducibility holds inside the exact content-addressed image.

## Formal boundary

This is still a candidate.

`TRUSTED_BUILD = NOT_ESTABLISHED`
`PRODUCTION_RUNTIME = NOT_AUTHORIZED`
`SEAL = NO`
`AUTHORIZATION = NON_AUTHORIZED`
`FAIL_CLOSED = TRUE`

Formal Trusted Build establishment additionally requires:

1. accepted environment identity policy;
2. source-authority attestation for the exact final candidate source;
3. provenance reconciliation that binds source, environment, dependencies, build procedure and artifact hashes;
4. human authorization according to CE change control.

## Change-control rule

Do not merge this candidate into PR #5 without re-attesting the new source bytes. Existing PR5 R2 attestation does not cover this candidate.
