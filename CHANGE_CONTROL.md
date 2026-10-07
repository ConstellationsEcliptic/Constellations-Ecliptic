# CE V1 Source Foundation R1 — Change Control

Implementation status is `DEVELOPMENT_CANDIDATE`.

Any change that can affect numerical state, signal qualification, runtime identity, provenance, or failure behavior requires a new source-tree identity and controlled review.

No silent mutation of normative inputs is permitted.

## Platform governance control

Repository-controlled workflow bytes are not the complete GitHub control plane. GitHub server-side governance state (including branch protection, rulesets, required status checks, and equivalent merge controls) is a separate authority-chain input and must be freshly observed and qualified before any source-authority, trusted-build, production-authorization, or seal transition.

The current A7 observation recorded in `provenance/github_platform_governance_observation_r1.json` found:

- default branch: `main`;
- `main` is currently reported as unprotected;
- required status-check enforcement on `main` is currently off;
- repository rulesets query currently returns no rulesets;
- no `CODEOWNERS` file was found in the A7 tree;
- detailed branch-protection endpoint access is unavailable to the connected integration (HTTP 403).

Until protected-main governance (branch protection or equivalent ruleset) and the required human/release controls are freshly verified, the authority chain remains fail-closed and no authority transition is permitted.
