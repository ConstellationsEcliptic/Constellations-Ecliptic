# CONSTELLATIONS ECLIPTIC
# AUTONOMOUS EXECUTION CAPABILITY SPECIFICATION R0

**Date:** 2026-10-10  
**Classification:** CAPABILITY DESIGN PROPOSAL / WORKING CANDIDATE / NON-AUTHORITATIVE  
**Owner direction:** AUTONOMOUS BY DEFAULT; OWNER CONSULTATION AT PROTECTED BOUNDARIES  
**Authority effect:** NONE  
**Credential / permission / workflow-setting change:** NONE  
**Runtime / production / SEAL effect:** NONE

## 1. Purpose

The standing operating mandate defines how CE work should be delegated. It does not itself provide an execution engine, durable cross-session state, repository credentials or background scheduling. This document specifies the smallest useful capability slice to evaluate next without granting unrestricted write authority.

The scope is a bounded research/engineering task runner that can discover pinned sources, inspect them, perform candidate-only work, run explicitly listed tests, and publish a tamper-evident result manifest. It is not a general-purpose autonomous production agent.

## 2. Verified platform boundary

The bounded read-only GitHub check documented in [Repository Governance Observation Reconciliation R1](https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/blob/governance/candidates/ce-autonomous-evolution-charter-r0-2026-10-09/governance/candidates/CE_PRE_A10_REPOSITORY_GOVERNANCE_OBSERVATION_RECONCILIATION_R1_2026-10-10.md) observed:

- the current PR27 candidate repository has a narrow register-validation workflow, not a general research/engineering runner;
- that workflow uses `contents: read`, tests a register validator and a strict completion gate, and does not orchestrate open-ended research, candidate code changes or cross-session task recovery;
- the live connection could not freshly inspect branch-protection detail because the endpoint returned HTTP 403; an empty repository-rulesets response is not proof that the main branch is unprotected;
- no external runner, LLM task credentials, dedicated GitHub App installation, durable execution database or background scheduler was established by the bounded repository inspection.

These observations are limited to the inspected repository and connected interface. They do not prove that no external or separate-repository capability exists.

## 3. Recommended capability slice

### Capability A — Source-bound research

Inputs: task manifest, exact source refs, allowed repositories/workspaces, search policy and an explicit question.

Allowed:
- read sources and their metadata;
- compare versions, lineages, hashes and contradictory requirements;
- produce a finding ledger that separates FACT, INFERENCE, HYPOTHESIS, RECOMMENDATION, OWNER DECISION and UNKNOWN;
- carry forward exact references and negative search scope;
- stop a conclusion when the source or source identity is unresolved.

Not allowed:
- infer that absence from one bounded search means universal absence;
- treat historical artifacts as current authority without lineage proof;
- modify normative source files as part of research;
- turn an assistant recommendation into an owner decision.

### Capability B — Isolated candidate work

A task may create or modify a candidate only if its manifest explicitly allows candidate output. Default write permission remains **NONE**. If candidate writes are later enabled, require all of the following:

1. An isolated branch/workspace created from the exact task parent SHA.
2. A task-specific allowlist for paths and artifact types; deny protected source/authority directories by default.
3. The task identity, parent SHA, allowlist, acceptance criteria and permitted toolchain recorded before the first write.
4. No write to `main`, A9 source-authority candidate, trusted-build manifests, trust roots, release gates, official normative files or the official Test Register unless a distinct controlled change is explicitly authorized.
5. No automatic merge, signing, promotion, authority-chain transition, Runtime Adoption, deployment, production authorization or SEAL.

Candidate writes must not include secrets, private account data, personal user content or payment data.

### Capability C — Bounded verification

A task manifest must list the exact commands/tests and permitted environment. The runner records pass/fail and raw output references. It must not relabel an identity-gate stop as a test pass, or call a targeted test slice the full suite.

Required properties:
- fixed timeout and maximum attempts per task;
- no unbounded recursive agent loops;
- only retry transient infrastructure faults, with retry count and changed inputs recorded;
- do not automatically retry a semantic/product finding by silently broadening scope;
- fail closed on source mismatch, missing pinned dependencies, unexplained dirty state, non-deterministic output where determinism is required, or protected-boundary crossing;
- verify that the test output corresponds to the exact tested head SHA;
- record environment/tool versions, run IDs, test counts, per-test outcomes where available, and cache/worktree residue.

A failed attempt is immutable evidence. A later passing attempt supersedes it for current status but does not erase the original finding.

## 4. Portable task manifest and result record

A task manifest should be self-contained and versioned. Candidate shape:

```json
{
  "schema": "CE-AUTONOMOUS-TASK-V1",
  "task_id": "stable-task-id",
  "task_type": "SOURCE_REVIEW",
  "parent_refs": [
    {"repository": "owner/repo", "ref": "commit-or-version", "sha256_or_git_sha": "exact-identity"}
  ],
  "objective": "bounded research or candidate change",
  "allowed_paths": [],
  "denied_paths": ["main", "trust-roots", "normative-source", "release-gates"],
  "permitted_tools": [],
  "acceptance_criteria": [],
  "max_attempts": 2,
  "timeout_minutes": 20,
  "protected_decision_tags": [],
  "status": "QUEUED"
}
```

The schema above is illustrative only; it is not an approved implementation schema.

For each attempt, append an immutable result record with:
- task and attempt IDs;
- exact source/parent/head identities;
- start/end timestamps and completion state;
- exact permitted commands and their exit codes;
- workflow/run/job references and test counts/results;
- hashes for candidate artifacts and output manifest;
- findings, unresolved questions, stop reason and any retry rationale;
- a clear status among `SUCCEEDED_WITHIN_SCOPE`, `FAILED`, `BLOCKED`, `OWNER_DECISION_REQUIRED`, or `REVIEW_REQUIRED`.

A status of `SUCCEEDED_WITHIN_SCOPE` means only that the defined task acceptance criteria passed. It must never imply Source Authority, Trusted Build, Runtime Adoption, production readiness or legal compliance.

## 5. Protected decision routing

Consult the owner only when the next action depends on a decision that cannot be derived from current authority and would materially affect one or more of:

- product/Canon meaning or epistemic promise;
- personal-data purpose, sensitive processing, retention, account lifecycle or AI-input boundary;
- consumer/commercial semantics, cap, price, refund or fulfillment promise;
- legal seller entity, market, jurisdiction or provider eligibility;
- trust root, source authority, trusted build, runtime adoption, production authorization or SEAL.

When one protected choice is unresolved, the runner marks that decision `OWNER_DECISION_REQUIRED`, preserves the evidence/options/consequences and continues unrelated reversible work. Silence is not approval. A prior owner decision may be revised only through an explicit, evidence-linked reconciliation.

Routine toolchain issues, test fixes, documentation and reversible candidate experiments should not be escalated unless they cross these boundaries.

## 6. Credential model

No new credentials are created by this specification.

Recommended sequence:
1. Start with read-only access and externally supplied candidate patches/results.
2. Verify the real account permissions and branch-protection controls before enabling any write workflow.
3. If candidate writes are required, use a repository-scoped GitHub App or equivalent short-lived credential with minimum repository permissions and candidate-branch restriction; never a personal access token with broad account scope if a narrower mechanism is available.
4. Keep candidate-writing credentials separate from release-signing/trust-root credentials; the autonomous runner must never have the latter.
5. Store secrets only in an approved secret store; never print them or embed them in a task manifest, logs or generated packet.
6. A model API provider, data-processing path or persistent runner service must have its own privacy/security/retention review before user or private data is transmitted. No such provider is selected by this document.

The exact credential mechanism depends on which controls can actually be verified on the repository/account; do not assume GitHub App, branch rules or a runner already exist.

## 7. Execution modes and triggers

V1 of the runner need not be always-on. Begin with:
- an explicit task manifest;
- manual/PR-triggered execution;
- bounded runtime;
- durable output committed as a candidate artifact;
- a recoverable queue/state record so the next session can resume from the last completed checkpoint.

A later scheduled monitor can be considered for a specific need (e.g. dependency updates or newly available source evidence). Scheduling and monitoring are separate capabilities with separate noise, permission and failure policies. Do not create an always-on process simply to satisfy a vague idea of autonomy.

## 8. Minimum acceptance tests

1. A task with no write grant can inspect sources but cannot mutate repository contents.
2. A task cannot write paths excluded by its allowlist even if its natural-language objective asks it to.
3. A stale parent SHA / changed source ref blocks execution before candidate mutation.
4. Tests report results against the exact candidate head; a later commit invalidates that exact-head claim until rerun.
5. A nonzero test exit, timeout or source-identity failure cannot be represented as success.
6. A bounded retry preserves the failed attempt and records why the retry is permitted.
7. An unresolved protected semantic yields `OWNER_DECISION_REQUIRED` and cannot be converted to approval by silence or model inference.
8. A routine blocked subtask does not prevent unrelated, authorized, reversible tasks from completing.
9. The runner cannot merge, sign, promote, modify trust roots, initiate A10/Runtime Adoption, deploy, enable production or SEAL.
10. Durable result records can be consumed by a fresh session without needing private conversational memory.
11. No secrets/personal/account/payment data appear in manifests, logs or output artifacts.
12. The report distinguishes targeted tests, full suite, authority checks, build reproducibility and production gates as separate evidence classes.

## 9. Implementation sequence

1. Confirm what runner/orchestration capabilities and repository controls already exist using read-only observations; document access denials honestly.
2. Prototype task/result schemas as test-only files in an isolated research branch.
3. Implement a read-only manifest parser and validator; use synthetic tasks and a no-write sandbox.
4. Demonstrate allowlist rejection, exact-head evidence, bounded retries and portable recovery.
5. Obtain independent security/control-plane review.
6. Only then ask for a narrow decision about candidate-write permissions if those writes are necessary.
7. Keep protected source/authority, signing and production credentials outside the autonomous runner permanently unless a separate owner-controlled trust architecture says otherwise.

## 10. State

- Standing owner mandate: **AUTONOMOUS BY DEFAULT; OWNER CONSULTATION AT PROTECTED BOUNDARIES**.
- General autonomous runner observed in the inspected CE repository: **NOT ESTABLISHED**.
- Existing read-only register workflow: **ESTABLISHED FOR ITS NARROW PURPOSE ONLY**.
- New executor, orchestration service, credentials or settings: **NOT IMPLEMENTED / NOT CONFIGURED BY THIS DOCUMENT**.
- Permission to merge, create a source-authority transition, Runtime Adoption, production deployment/authorization, or SEAL: **NONE**.

---

End of R0.
