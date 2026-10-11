
# CONSTELLATIONS ECLIPTIC
# ZERO-POINT — CURRENT EVIDENCE AND CODE REVIEW R1

Date: 2026-10-11
Classification: SOURCE-BOUND AUDIT CONTINUATION / NON-AUTHORITATIVE CANDIDATE
Authority effect: NONE
Normative / official Test Register / production code / schema / runtime mutation: NONE
A10 / Source Authority / Trusted Build / Runtime Adoption / production / SEAL effect: NONE

Related records:
- Full Revalidation Audit R0: https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/blob/cfcededa01d143e6cce0e58cbba8115ad9f71ba4/governance/candidates/CE_ZERO_POINT_FULL_REVALIDATION_AUDIT_R0_2026-10-11.md
- 11 Findings + 3 Notes Crosswalk R0, PR #38: https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/pull/38
- Clean Current Set R3 archive-member identity audit: https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/blob/governance/candidates/ce-autonomous-evolution-charter-r0-2026-10-09/governance/candidates/CE_PRE_A10_GOVERNING_ARCHIVE_MEMBER_IDENTITY_AUDIT_R0_2026-10-10.md
- Source-chain reconciliation R0: https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/blob/governance/candidates/ce-autonomous-evolution-charter-r0-2026-10-09/governance/candidates/CE_ZERO_POINT_SOURCE_CHAIN_RECONCILIATION_R0_2026-10-11.md

## 1. Current determination

The review is continuing from existing evidence. It is not restarted and is not complete.

New direct findings:
1. The substantive 11 findings + 3 notes are recovered through the owner's re-supply in this conversation. The original historical artifact itself (original chat/export/file bytes, hash and complete thread metadata) remains not independently recovered.
2. The three Calculation / Signal / Canon anchor hashes were already independently matched to exact member bytes inside retained Clean Current Set R3. Do not describe these as merely metadata matches or repeat raw-byte hash verification as if it had never happened. The downstream authority lineage remains open.
3. The governance candidate branch and the A9 implementation candidate are distinct scopes. The governance branch contains governance docs and an area-register validator, not the CE product/runtime source. A separate A9 candidate branch contains implementation source, profiles, schemas and tests.
4. One concrete test-discovery defect exists in the exact A9 candidate commit.
5. A profile/configuration-to-runtime traceability gap is visible in the B1 geometry candidate. It is a candidate control/test gap, not proof that current numerical outputs are wrong.
6. Later exact-candidate records establish Source Authority and formal Trusted Build for A9 HEAD `c8dab3542d3d4725cf591630c07f76366f7949d0`. Runtime Adoption, full runtime coverage, TZIF runtime identity and production authorization remain unestablished/not authorized.
7. The separate retained implementation pointer still names PR #5, so the pointer/supersession link from that retained chain to A9 PR #26 remains unreconciled. This does not reverse A9’s exact-candidate authority records.
8. The A3 search found historical hard-coded frontend prototypes in Box raw-inventory intake, but no approved current V1 Today’s Note editorial library. A3 remains open; the prototype text is demo content and must not be promoted into V1.
9. A successor R1 crosswalk now maps all 11 findings and 3 cross-cutting notes to the 23-area Pre-A10 register. This resolves navigation, not implementation, Test Register authority or gate completion.

## 2. The three source anchors are already verified in exact R3 archive bytes

The existing archive-member identity audit independently compared SHA-1 and size against the actual bytes of the members in the exact Clean Current Set R3 ZIP, and recorded all three as EXACT MATCH. That same audit records the outer archive identity and 72/72 payload hashes:
- ZIP size: 2,654,872 bytes.
- ZIP SHA-1: 58f8c3dcccc0ccb2e79a79ddd46ab0014c2783d6.
- ZIP SHA-256: d9c2f4abbe0a482e982488d5d2e332202c0c0dc8fceca3b5faaceb3d2c4a8abc.
- ZIP integrity: PASS; 74 entries; 72 manifest-listed payloads; 72/72 payload SHA-256 matches.

| Source | SHA-1 | Member size | Exact characterized Box copy |
|---|---|---:|---|
| 02_CALCULATION_CONSTITUTION.md v1.9 | 72abaeee50c3d49607cd99756df58f90ff96f8bf | 19,235 bytes | Box 2485336984594 |
| 03_SIGNAL_ENGINE_CORE_V1_SPECIFICATION.md v1.4 | 2408a9c84d4148c9f2cb37506b238b82a020a67b | 9,438 bytes | Box 2485335414676 |
| 04_INTERPRETIVE_CANON.md v1.2 | 7ee32ee5f74477cf2674b50182be42aa8c5d439a | 6,817 bytes | Box 2485337228722 |

Two Box copies per current source version also have matching metadata hash/size and identical returned text representations. Different older raw-inventory copies exist: Calculation v1.7, Signal v1.1, and Canon v1.0.

This proves exact identity for these three members. It does not prove that the documents are fully connected to the current Index, valid successor route, Source Authority, implementation, or official full Test Register.

## 3. Repository scope and exact-head CI

### PR #27 — governance control plane

Observed exact head: 549e53c0abccc3fb6d26f2cf0e32b7b3f7e00668.
PR #27: OPEN / DRAFT / NOT MERGED.

Its exact recursive tree has 113 entries: 107 files and 6 directories. The 107 files are 100 Markdown, 4 JSON, 2 Python and 1 YAML. Non-candidate top-level files are the README, Pre-A10 workflow and its two validator Python files. There are no src, runtime, application backend or frontend directories in this branch. It would be incorrect to describe the PR #27 tree as a full CE source-code audit.

Exact-head Actions run #38077875438:
https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/actions/runs/38077875438
- R0, R1, R2 and R3 Area Register structural checks: PASS.
- All 14 validator unit tests: PASS.
- Strict Pre-A10 completion gate: BLOCKED / exit 2 by design because A3, B1 and D4 remain incomplete.

This is not an overall all-green release gate.

### PR #26 — A9 implementation candidate, a separate scope

PR #26: OPEN / DRAFT / NOT MERGED.
Exact source HEAD: c8dab3542d3d4725cf591630c07f76366f7949d0.
https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/pull/26

The exact tree has 213 entries: 185 files and 28 directories, including 111 Python files. It contains source, tests, candidate profiles, schemas, manifests, provenance and build controls. I inspected a subset of core source and tests at this exact commit; this is not a line-by-line audit of all 111 Python files.

Historical exact-head Actions results:
- Full Boundary run #37765045306 — success; 261 tests per operating system.
- Remediation run #37765045314 — success; 261 tests per operating system.
- Trusted Build A9 run #37765045328 — workflow checks passed.

At the workflow-log cutoff, the technical output still carried FORMAL_TRUSTED_BUILD=NOT_ESTABLISHED along with fail-closed runtime/production fields. That documentary interpretation was later superseded for this exact candidate by R2 reconciliation and the formal human authorization record (see §25). The current record-backed state is SOURCE_AUTHORITY=ESTABLISHED UNDER SOLO OWNER MODEL and TRUSTED_BUILD_FORMAL=ESTABLISHED for A9 commit c8dab3542d3d4725cf591630c07f76366f7949d0; RUNTIME_ADOPTION remains NOT_ESTABLISHED, PRODUCTION_RUNTIME remains NOT_AUTHORIZED, SEAL=NO, AUTHORIZATION=NON_AUTHORIZED and FAIL_CLOSED=TRUE. Successful Trusted Build is not runtime or production authorization.

## 4. Concrete A9 finding: one test is not discovered

Exact file: tests/test_source_tree_identity_r1.py
Blob SHA-1: dc2fa10ce90487d8561f1cf1809bdebe7f80807d
Exact A9 HEAD: c8dab3542d3d4725cf591630c07f76366f7949d0.

The method test_source_digest_manifest_is_not_self_referential is indented inside the module-level if __name__ == "__main__" block but appears after unittest.main(). It is not inside the SourceTreeIdentityR1Tests class. Under normal discovery/import the block is skipped, so the method is never defined. If the file is executed directly, unittest.main() runs before the later definition is reached.

The exact-head Full Boundary and Remediation logs show only three collected SourceTreeIdentityR1Tests: same-content identity, filesystem mode independence, and path/content identity. They do not show the intended self-reference exclusion test.

This is a concrete test-discovery/coverage defect, not proof that the source-tree identity function itself is incorrect. The reported 261 tests passed, but that intended test was not part of the count.

A read-only finding was posted to PR #26 (comment ID 6101309193). The pinned A9 branch was not edited. Any correction must be a separate candidate revision with a new source-tree identity and exact-head verification; do not rewrite manifests merely to make pinned values match.

Disposition: AMEND in a separate candidate branch; preserve the original candidate and its historical test results.

## 5. B1 finding: candidate profile JSON is not explicitly bound to runtime constants

Exact candidate source objects at A9 / B1:
- src/ce/calculation/geometry.py — blob SHA-1 481691b05c35a567ca144fae9df2c09f010b4313.
- src/ce/calculation/registry.py — blob SHA-1 ffc977e434fa8da2b88b4c69821296a9689c7c30.
- profiles/aspect_registry_rev4_candidate.json — blob SHA-1 f10815ebbc697d6aec0f04291816fc0bca67ea51.
- profiles/orb_registry_rev4_candidate.json — blob SHA-1 f17b0e551b7729e58ff87eeb268b42117becaf17.
- profiles/object_registry_rev4_candidate.json — blob SHA-1 331186613024f55b77c519cb57c74dc32bee1366.
- tests/test_registry_r1.py — blob SHA-1 03efb7dd4609f070473a13fe8ac7c34ccdc38175.
- tests/test_core_golden_r1.py — blob SHA-1 201640bd652af6a67e8b4d102ba61348cff3f4cc.

Observed:
- geometry.py contains hard-coded aspect branches, orb profiles A/B, and object-profile assignments. Runtime functions resolve_branch, effective_orb and aspect_geometry use these constants.
- profile JSON files are explicitly labelled CONTROLLED_CURRENT_CANDIDATE and authority NOT_ESTABLISHED.
- registry.py validates profile payloads against its own hard-coded expected objects/aspects and profile revision 4. It does not construct or bind the values consumed by geometry.py.
- test_registry_r1.py checks JSON candidate data shape and registry invariants. test_core_golden_r1.py checks runtime numeric behavior using literal expected values. The inspected tests do not explicitly compare all geometry runtime constants/assignments against the candidate JSON values.
- The corrected B1 prototype workflow at PR #32 head 1c3459836996ce4cc1a6ffb5ff76cb77e6a488d8 runs six selected test modules. It does not directly invoke test_geometry.py, test_core_golden_r1.py or test_registry_r1.py by name. Its 62-test matrix is valid for the modules it ran, but should not be described as direct execution of those omitted modules without evidence of indirect imports.

This is a traceability/test-oracle gap, not a proven numeric defect. The inspected values appear consistent today, but a future candidate profile update could drift from runtime constants without a binding invariant. Do not promote candidate JSON into authoritative runtime data by assumption. Clarify which controlled source is meant to determine the values, then add an appropriate candidate-only consistency test or document the intended compile-time contract.

PR #32 remains OPEN / DRAFT / NOT MERGED:
https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/pull/32
Its B1 workflow correction and 62-test results are candidate evidence, not semantic Canon approval, A9 Source Authority or Trusted Build.

Disposition: HYPOTHESIS / OPEN TRACEABILITY FINDING. Candidate-only closure required; no numerical rule change.

## 6. Fail-closed runtime/Canon observations

At the A9 HEAD reviewed:
- src/ce/canon/registry.py rejects an empty/unmaterialized registry, and the public get_rule entry point raises CanonRegistryNotEstablished. No populated, approved current V1 Canon semantic rule registry was found in that inspected tree. Do not create Canon rules from historical content merely to unblock.
- src/ce/calculation/engine.py can return NON_AUTHORIZED when authoritative adapter evidence is not established.
- src/ce/runtime/gates.py refuses runtime authorization unless source-authority attestation and independent runtime identity verification are established.
- src/ce/timezone/runtime.py pins IANA/TZDB to 2026d and rejects missing/mismatched identity/bundles. Investigation of 2026e does not authorize a runtime change.
- manifests/convergent_test_register_r3.json calls itself CURRENT_IMPLEMENTATION_CANDIDATE and still records authoritative coverage, Source Authority, Trusted Build, runtime adoption and full runtime coverage as NOT_ESTABLISHED. For Source Authority and Trusted Build, those artifact-local state fields are stale against the later exact-candidate R2/formal authorization records; authoritative coverage, Runtime Adoption and full runtime coverage remain NOT_ESTABLISHED. This is an unresolved control-plane/source-state inconsistency, not grounds to discard or silently overwrite the manifest.

These are fail-closed controls to preserve, not release evidence.

## 7. Governance and full Test Register blockers

The retained Index object has established identity: 9,517 bytes; SHA-256 a6a2d482d27777bae21f78ae11593eef62a35f19ee899d0a69ab83e3ccb8025f; SHA-1 c1af95dd68f570586ece7d73e8893dc08ba45ed6. It has a v1.9 header / v1.8 closing-status conflict and still identifies Test Register v1.5 as current.

Historical full Test Register v1.5 text and lineage exist in raw-intake copies; the H8 SHA-256 lineage is 10566c5bba753f9be9a791406c110fbd54e43fce0bd976b6bec6d277bbe0f72a. But R3 explicitly excludes it and has no Document 07 payload. The active full V1 Test Register binding remains NOT ESTABLISHED / conflicted. The A9 28-ID calculation-core candidate is not a substitute for the full cross-domain official register.

The general Index/GDE-01 adoption route remains unresolved in inspected evidence. The owner’s master autonomy mandate is already approved (CE-OD-GDE-2026-10-10-001, Box 2517806798198); do not request it again.

## 8. The user's 11 initial areas and three notes

The complete owner-supplied content and item-level crosswalk is now preserved in PR #38. Current disposition summary:
1. Product — PRESERVE core integrity; source-to-implementation and test mapping remains.
2. Deep Sky — PRESERVE sole paid core V1; tie entitlement, reread and Credits to contract/tests.
3. 3-AI — current V1 direction is deterministic Core plus one constrained Deep Sky LLM and validator; historical 3-AI is not automatically adopted and measured benefit is not established.
4. Voice Boundary — preserve truth/evidence/claim boundaries; full rule-vs-style matrix and tests remain.
5. Credits / scope uniqueness — PARTIAL; daily service date/idempotency do not prove a separate one-scope-per-account-per-day rule.
6. English/en-US — not implied by US-first; separate product/locale decision if required.
7. USD — USD-focused customer sales intent is recorded; provider, final price and settlement currency remain open.
8. US-first — owner direction recorded; seller entity/jurisdiction and nationwide launch approval remain undecided.
9. Privacy — preserve minimization; end-to-end implementation proof remains bounded.
10. Minimal telemetry — define exact event/field, purpose, access, retention and deletion allowlist.
11. Autonomy — master mandate approved; operational source-amendment/promotion route remains open.

Three notes remain: old and later baseline discussions need version crosswalk; Share Card remains excluded from V1 but the normative retirement chain needs valid source propagation; the three Calculation/Signal/Canon anchor bytes are already verified while authority/implementation/test lineage remains open.

## 9. Pre-A10 status and dependency-aware next steps

Latest PR #27 exact head checked: 549e53c0abccc3fb6d26f2cf0e32b7b3f7e00668. Exact-head Actions run #38077875438 has 14 validator tests and structure checks R0-R3 PASS; strict gate remains blocked by A3/B1/D4. The gate is correctly fail-closed.

Exact JSON Area Register R2 at the same PR #27 HEAD reports: 13 CLOSED_PRESERVE; 6 OWNER_DECISION_RECORDED; 1 DEFERRED_BY_EXPLICIT_DISPOSITION; 3 RECOMMENDATION_READY (A3, B1, D4). The PR #27 description still contains an older label of A3=OWNER_DISCUSSION_REQUIRED; treat that prose summary as stale where it conflicts with the exact-head JSON blob. A3/B1/D4 remain open and the strict gate remains blocked.

Next work:
1. Reconcile retained R3 archive/member -> embedded Index -> controlled successor -> Source Authority -> implementation -> official Test Register/fixture. Do not edit retained Index/R3 in place.
2. Keep original 11+3 content as recovered-by-owner-resupply; original source artifact identity remains unresolved.
3. Map all 11 findings to 23 Pre-A10 areas, exact source sections, implementation and official tests.
4. Raise and fix the A9 missing-test method in a separate candidate revision, then run exact-head CI without rewriting pinned identities.
5. Close B1 profile/runtime traceability gap with a candidate-only test/contract; do not change numerical rule values.
6. Resolve official full Test Register authority and Index amendment route separately.
7. Keep Canon registry fail-closed; complete A3 editorial sources/UI/tests and the separate signal-present Note decision.
8. Reconcile C3 commerce PRs #33-#36, Technical Contracts and official test oracle; distinguish account-scope uniqueness from daily service-credit semantics.
9. D4 remains US-customer/USD-first: prescreen providers for exact astrology/Credits, true seller eligibility, US card acquiring, USD presentment/settlement, named acquirer and all fees/reserves before integration or paid onboarding.
10. Resolve official full Test Register authority, then establish the complete source-code-test crosswalk for the intended successor. Source Authority and formal Trusted Build are already recorded as established for exact A9 HEAD c8dab3542d3d4725cf591630c07f76366f7949d0; any successor must have its own applicable identity-bound authority/build reconciliation. The current PR #5 implementation pointer versus PR #26 A9 lineage, Runtime Adoption, full runtime coverage, TZIF identity, production and SEAL remain separate open controls.

## 10. Completed and outstanding

Completed in this continuation:
- Preserved the owner's 11 findings + 3 notes and their crosswalk.
- Correctly re-used prior raw-byte archive-member identity evidence for the three normative anchors.
- Verified the exact Pre-A10 gate result at PR #27 head.
- Inspected the exact A9 tree and a subset of core runtime, registry, profile and test sources.
- Identified a concrete test-discovery defect and recorded it on PR #26 without modifying the pinned branch.
- Identified a candidate profile/runtime binding coverage gap without asserting a numerical error.
- Kept all normative, source-authority, runtime and production boundaries unchanged.

Still open:
- Full line-by-line review of all 111 Python files and all local/historical source material.
- Original historical 11+3 file/export/hash/thread metadata.
- Index -> approved successor -> Source Authority -> implementation -> full official Test Register chain.
- Resolution of the active Test Register conflict and Index adoption route.
- Candidate fix and exact-head retest for the missing source-tree identity test.
- B1 profile/runtime binding decision and explicit regression coverage.
- Populated approved Canon Rule Registry; closure of A3/B1/D4.
- Complete C3 contract/application/official test integration.
- Full privacy/telemetry and consumer/commercial lifecycle implementation review.
- A10, runtime adoption, production, release, Trusted Build and SEAL. All remain separate gates.

## 11. Boundary

This is an audit evidence/status artifact only. It changes no retained Index, Constitution, official Test Register, Source Authority, production code, schema, runtime profile, A10, Trusted Build, deployment, release or SEAL state. Findings are bound to the exact sources and commits identified above.

End of R1.


## 12. Claim-release pipeline recheck — why a passing candidate suite is not a release

Additional exact-A9 source files reviewed:
- src/ce/output/semantic.py, blob SHA-1 b33e37111770e55521c50f01ee6c7b699b5d9c61.
- src/ce/claim/authorization.py, blob SHA-1 59a88041cbf39c86faeffdef65a50dcb866b93d5.
- src/ce/claim/manifest.py, blob SHA-1 20e64047510a98aa34c5a84abc50885b12ca76b3.
- src/ce/product/boundary.py, blob SHA-1 2759fea7f3f0ed4cc6554c8416e1f2d271983898.
- src/ce/runtime/gates.py, blob SHA-1 40a1874392af704cb1bd837a40275c27b5adbb87.
- tests/test_product_boundary_fail_closed_r1.py, blob SHA-1 7969fcf8ce38e5a1d4540269ebd3f9de95b017b7.
- tests/test_runtime_gate.py, blob SHA-1 7f397ebb1fe8d0ab634f1db1ffb33bbafc9e7eab.

Observed behavior:
1. get_verified_semantic_conformance() explicitly returns None and comments that a controlled, independently verified semantic verifier is not yet established.
2. validate_claim_output appends semantic_conformance_unavailable when no verifier is supplied; any conformance callback error becomes semantic_conformance_check_error, so this layer fails closed.
3. evaluate_claim_release() uses the Canon registry to fetch the approved rule and validate the manifest against a registry digest; missing/unpopulated rule authority produces manifest_registry_binding_failed.
4. The same claim-release function calls authorize_runtime(). At the exact A9 source reviewed, the gate unconditionally appends source_authority_attestation_not_established and independent_runtime_identity_verification_not_established, returning NON_AUTHORIZED. This is the runtime code’s receipt-verification state; it must not be misreported as absence of the later external A9 Source Authority record. The record exists, but the source gate does not yet consume a verified runtime-authority receipt and independent runtime-identity proof, so remaining fail-closed is correct.
5. product.boundary.preserve_calculation_truth explicitly allows downstream signal processing after VALID calculation but continues to deny direct Canon claim, AI release and Quiet Sky; it requires downstream qualification.
6. Existing tests verify non-VALID states cannot imply release and that runtime remains non-authorized without authority evidence.

Conclusion: the inspected candidate source is currently guarded such that there is no supported active claim-release path under its present unmaterialized Canon registry / missing verified semantic conformance / non-authorized runtime gates. This is consistent with the known non-authorized status and must not be “fixed” by removing guards, substituting a historical rule corpus, or injecting caller-supplied semantic verification. A future claim-release path requires approved Canon data, a controlled semantic verifier, valid source/build/runtime authority, and official tests/source authority established through the proper process.

This is a direct implementation-control finding, not evidence that a release should proceed or that the gates are incorrect.



## 13. Structural scan of all 111 Python files in the exact A9 tree

After the initial core-file review, a structural/pattern scan was run across all 111 Python-file blobs enumerated by the recursive tree at exact commit c8dab3542d3d4725cf591630c07f76366f7949d0. Each file's retrieved content was scanned for:
- a module-level __main__ block and a later unittest.main() call;
- test-method definitions placed after unittest.main();
- obvious lexical markers for eval, exec, pickle, shell=True, TODO/FIXME and NotImplemented;
- broad Exception/BaseException handlers for focused follow-up.

Result within that bounded scan:
- Exactly one misplaced test-method pattern was found: tests/test_source_tree_identity_r1.py, described in Section 4.
- The scan found no lexical matches in the inspected Python blobs for eval, exec, pickle, shell=True, TODO, FIXME or NotImplemented.
- Broad exception handlers were found in calculation/contracts.py, calculation/evidence.py, calculation/scenario_evaluator.py, output/validation.py, runtime/retry.py and timezone/runtime.py. Representative instances were opened and followed:
  - scenario_evaluator catches an evaluation exception and returns CALCULATION_FAILURE with no possible/robust windows;
  - runtime/retry catches an unclassified failure and returns CALCULATION_FAILURE with value=None and stale_result_substitution=False;
  - timezone/runtime wraps zone-file parse failures as TzifRuntimeError after its path, size and SHA-256 checks;
  - output/validation treats a missing semantic verifier as semantic_conformance_unavailable and verifier exceptions as semantic_conformance_check_error;
  - evidence/contracts convert provenance-validation errors into invalid result diagnostics.

No further confirmed defect was concluded from these broad-exception observations alone. They were screened as leads, not mechanically marked bugs.

This is a **whole-tree structural/pattern scan of the 111 Python file texts at one exact candidate commit**, not a semantic line-by-line review of all their behavior, dependencies, numerical algorithms or operating-system behavior. It reduces uncertainty about a narrow set of common test-discovery/unsafe-call patterns but does not prove the absence of other defects.

## 14. Newly completed scope versus remaining full-review limitation

Completed after the first drafting of R1:
- all 111 Python file blobs in the exact A9 tree were enumerated and subjected to the structural/pattern scan described in §13;
- the sole surfaced misplaced test-method pattern was inspected and is linked to exact-head Actions collection evidence;
- the broad exception handling locations surfaced by the scan were inspected at relevant return paths.

Still not completed:
- semantic review of every line in all 111 Python modules;
- independent rerun of the entire project test suite inside a locally materialized checkout;
- full numerical oracle/property-based review of every geometry/window/time case;
- full test-runner coverage of every test file (the A9 Actions run uses named workflow module lists and does not imply all repository tests were collected);
- native Windows/MSVC controlled runtime capture and other human-boundary evidence recorded as not established in A9 governance;
- production or authority transition of any kind.

The scope statement in §3 remains in force: this is more than a governance-only review but less than a complete production-code certification.


## 15. Additional provenance integrity finding — malformed H2 mapping digest strings

Exact A9 source objects were re-opened and the H2 mapping digest strings counted as hexadecimal characters:

| File | Blob SHA-1 | Field / observed value | Character count |
|---|---|---|---:|
| manifests/convergent_test_register_r1.json | 5364dc2e1eda7b5cd3ecb00203594c64f5f36625 | recovered_h2_mapping_sha256 = babcccf81636df1e65eb92fe9119d474787fc3801b547fa5703e9048993d441 | 63 |
| manifests/convergent_test_register_r2.json | 0a014f5f33498328c3f86e687469372df0e375b2 | same value | 63 |
| manifests/convergent_test_register_r3.json | 13eb21577d7deca5f47ab5fe78b4c0ec8cc37e71 | same value | 63 |
| provenance/b1_h2_registry_recovery.json | fa120bad1034228e1de93ef3a1a709a5edb6d5cf | mapping SHA-256 value matches the same 63-character string | 63 |
| provenance/rev4_registry_rebind_candidate_r1.json | 3e6268e0cfce96a4a9e6f9def11ff939ddd0f0ab | mapping_sha256 = babcccf81636df1e5eb92fe9119d474787fc3801b547fa5703e9048993d441 | 62 |

A SHA-256 hex digest must have 64 characters. These are malformed digest strings regardless of whether the underlying H2 source is genuine. This is a concrete candidate provenance-integrity defect: the pointer/manifests do not faithfully encode a valid complete SHA-256 value.

Related external source record:
- Box file 2506851548670, CE_V1_H2_PROVENANCE_RAW_INTAKE_VERIFICATION_R1, records the expected 64-character H2 mapping SHA-256 as:
  BABCCCF81636DF1E65EB92FE9119D474787FCF3801B547FA5703E9048993D441
- That same source record explicitly states direct SHA-256 re-hashing of the Box binary payload was NOT performed. It reports exact size, Box SHA-1 consistency across copies, and logical content equality with canonical Dropbox H2 copies, while treating SHA-256 as an expected identity from prior provenance.
- The canonical Dropbox mapping object is discoverable as Dropbox file id id:C0IKLeFCqbMAAAAAAAAAAQ, 9,553 bytes, with matching duplicate copies reported by Dropbox search. This review retrieved the extracted text and metadata; it did not download/materialize the original bytes and compute their SHA-256.

Therefore the corrected 64-character string is **an expected value present in prior provenance documentation**, not a new direct hash computation from the mapping bytes in this review. Do not fill the missing character(s) by assumption in the pinned A9 branch. The correct remediation sequence is to retrieve the original canonical mapping bytes, compute SHA-256 directly, reconcile that result to the archive and prior H2 record, and then update the digest through a controlled candidate successor with exact-head tests. Keep the malformed predecessor artifacts unchanged and preserve their history.

A read-only finding was posted to PR #26 (comment id 6101429127). No candidate source, manifest, authority or production state was modified by this finding.


## 16. Structural scan of all 41 JSON files in the exact A9 tree

A second bounded automated inspection parsed all 41 JSON blobs enumerated by the exact A9 recursive tree. This scan only treats a leaf value whose field name contains `sha256` as an expected digest; JSON Schema's legitimate `type` and `pattern` children were excluded from the digest-length check.

### 16.1 Concrete malformed H2 digest references (nine locations)

Nine candidate metadata fields carry the same H2 mapping value with invalid SHA-256 length:

| File | Exact A9 blob SHA-1 | Field | Length |
|---|---|---|---:|
| `manifests/convergent_a1_b1_manifest.json` | `83938d1c60e7383cfb5edd37837aa683735e2500` | `registry_candidate.mapping_sha256` | 62 |
| `manifests/convergent_test_register_r1.json` | `5364dc2e1eda7b5cd3ecb00203594c64f5f36625` | `recovered_h2_mapping_sha256` | 63 |
| `manifests/convergent_test_register_r2.json` | `0a014f5f33498328c3f86e687469372df0e375b2` | `recovered_h2_mapping_sha256` | 63 |
| `manifests/convergent_test_register_r3.json` | `13eb21577d7deca5f47ab5fe78b4c0ec8cc37e71` | `recovered_h2_mapping_sha256` | 63 |
| `provenance/b1_h2_registry_recovery.json` | `fa120bad1034228e1de93ef3a1a709a5edb6d5cf` | `recovered_candidates.test_mapping_100_h2_provenance_reconciled.sha256` | 63 |
| `provenance/CONVERGENT_A1_B1_STATE_R1.json` | `82aefc05b2a7a79213e39e3dd17e5cd6abf6253e` | `recovered_h2_registry.mapping_sha256` | 63 |
| `provenance/CONVERGENT_A1_B1_STATE_R2.json` | `93c1028b39c17fb3bba98f711de7d878b2f2a666` | `recovered_h2_registry.mapping_sha256` | 63 |
| `provenance/CONVERGENT_A1_B1_STATE_R4.json` | `763b1a70b237795c8b6c0d90ae871639a505ee86` | `current_candidate_basis.h2_mapping_sha256` | 63 |
| `provenance/rev4_registry_rebind_candidate_r1.json` | `3e6268e0cfce96a4a9e6f9def11ff939ddd0f0ab` | `source_h2_recovery.mapping_sha256` | 62 |

Two exact malformed literal patterns recur:
- 63 characters: `babcccf81636df1e65eb92fe9119d474787fc3801b547fa5703e9048993d441`
- 62 characters: `babcccf81636df1e5eb92fe9119d474787fc3801b547fa5703e9048993d441`

The prior Box H2 intake verification record (Box `2506851548670`) reports an expected 64-character digest:
`babcccf81636df1e65eb92fe9119d474787fcf3801b547fa5703e9048993d441`
but explicitly states that direct SHA-256 re-hashing of the original Box binary payload was NOT performed in that verification. The Dropbox source mapping artifact is identifiable and its metadata reports size 9,553 bytes, Dropbox content hash `7fcec8db732ddfbb82112c6690158180e8c9770d2270cc96339f3f8be64ccb68`, with duplicate content objects. However, the raw file bytes have not been downloaded and independently rehashed in this audit. Therefore the 64-character expected value remains a prior-provenance value, not an independently recomputed raw-byte result here.

Disposition: **confirmed malformed candidate digest pointers; raw underlying mapping hash remains to be independently confirmed.** Do not guess a missing character, rewrite a pinned manifest in place, or treat these candidate pointer files as the official full Test Register. Reacquire the exact mapping bytes, compute SHA-256 directly, compare with archive/previous provenance, then create a controlled successor with a new source identity and exact-head tests.

### 16.2 Invalid JSON syntax in a historical governance-observation R1 object

File: `provenance/github_platform_governance_observation_r1.json`
Exact blob SHA-1: `42e3bd4287321a34bf3a439cc864611efc3330ac`.

The file fails JSON parsing because its `a7_candidate_scope.branch` value is the unquoted token `branch`:
```json
"a7_candidate_scope": {
  "branch": branch,
  "head": "a2ba5067f36247086ed3049371fc471c5a320585"
}
```

The exact A9 tree also contains `provenance/github_platform_governance_observation_r2.json`, blob SHA-1 `a7ea88234ce9958bb19efa7f7a772db24fd3ffce`, which parses as valid JSON and explicitly records R1 as `HISTORICAL_STALE_SNAPSHOT`. Thus R1 is a malformed retained historical snapshot, and R2 is a syntactically valid successor. The defect has been identified; the pinned bytes remain unchanged. If the malformed historical file is intended to remain referenced in future control packages, its historical form must remain preserved and a corrected/superseding valid artifact should be produced under a new identity, with R2 and all other consumers reviewed rather than retroactively rewriting history.

### 16.3 Explicit placeholders are not treated as digest errors

Other hash-named fields include explicit non-hex placeholders such as `NOT_ESTABLISHED`, `NOT_ESTABLISHED_AFTER_HARDENING`, `RECORDED_IN_SOURCE_TREE_SHA256_V2_MANIFEST` and `RECORDED_IN_PROVENANCE_CONTROL_PLANE_SHA256_R1`. These are not SHA-256 digests; they appear to be deliberately unresolved/external-reference states. They should be evaluated against each artifact's declared schema/contract and status, not mislabeled as valid hashes. No candidate value has been silently replaced during this scan.

### 16.4 Scan scope and result

- Total JSON blobs enumerated and checked: 41.
- Malformed H2 mapping SHA-256 references: 9 fields in 9 JSON files.
- Syntactically invalid JSON artifact: 1 historical R1 file, with a valid R2 successor that marks R1 stale.
- No other non-placeholder malformed SHA-256 leaf values were returned by this bounded scan.
- This was a parse/shape/value-length scan at one exact commit, not a semantic review of all JSON meanings or runtime consumers.

The malformed mapping references and invalid historical JSON are recorded as candidate/lineage findings. The A9 source tree remains unchanged. Any candidate repair affecting its source-tree/control-plane identities needs a successor branch, accurate identity recomputation, and new exact-head checks.


## 17. H2 digest defect also appears in Markdown lineage records

The exact A9 non-JSON tree was scanned for the same mapping hash and long hexadecimal strings. Two additional artifacts reproduce the invalid 63-character mapping digest:
- `CE_CONVERGENT_A1_B1_CHECKPOINT_R1.md`, blob SHA-1 `7c8215bc6641282482d74afcccb346ca856fafdd`, line 32.
- `docs/CE_A1_B1_CONVERGENT_LINEAGE_STATUS_R1.md`, blob SHA-1 `56d16017294137bb1f79451985754c765ac3ca9d`, line 16.

Their registry digest is 64 characters, while the adjacent mapping digest is 63. Combined with Section 16's nine JSON fields, the same malformed mapping identity is reproduced in **11 artifacts in the pinned A9 tree** (9 JSON artifacts + 2 Markdown records). This shows copied candidate metadata drift, not independent evidence for the missing byte. The expected 64-character value recorded in H2 verification remains to be matched against raw bytes before any successor corrects those records.

Other 56–72-character hash-like tokens observed in the remaining non-code text files were checked at their local context; the additional ones were valid 64-character source/build identities or environment image/dependency digests. The A9 source-tree manifest currently records `1a4004ac644331964ab9d540abf6b1631aed1cbbe0cbdd55316fe5356a0c7a8b`, and control-plane manifest records `0bc4f88dc43549a1033434a2a3653c02b46002024630b4294c22ddb8a5f7c357`. These are identities bound to this candidate control package; do not transplant them to a successor branch.

## 18. Active implementation pointer vs later A9 candidate — source route is not self-evident

A fresh read of the current retained harmonization records found:
- Box `2492339224632`, `CE_ACTIVE_IMPLEMENTATION_POINTER_2026-09-28_R23-PROVENANCE-REMEDIATED.md`, points to PR #5 at exact HEAD `3db976fd7293f0d4c5d367a81fc87489a97ba900`, branch `development/constitutional-harmonization/2026-09-28-r1`, OPEN / DRAFT / NOT MERGED.
- Box `2492332324704`, `CE_V1_CURRENT_DECISION_REGISTER_2026-09-28_R23-PROVENANCE-REMEDIATED.md`, repeats the same PR #5 HEAD and says the current-head Source Authority attestation is pending reissue; Trusted Build NOT_ESTABLISHED; Production Runtime NOT_AUTHORIZED.
- PR #5 is still OPEN / DRAFT / NOT MERGED at that same exact HEAD, and its 11 changed files focus on the birth-time/calendar harmonization.
- PR #26 is a separate OPEN / DRAFT / NOT MERGED A9 technical candidate at HEAD `c8dab3542d3d4725cf591630c07f76366f7949d0`, with 185 files including runtime, test, profile, schema and build-control content.

This does **not** prove PR #26 is an authorized successor to the PR #5 implementation pointer, nor does it prove that PR #5 contains the full newer A9 engineering state. It proves the control documents still explicitly name PR #5 as the active candidate pointer, while later technical candidate work exists separately. Until a valid successor pointer/decision establishes supersession, treat the implementation lineage as **NOT RECONCILED**, and do not infer Source Authority from either candidate's existence or test success. Scope correction: this pointer-lineage finding must not be read as cancelling the separate R2/formal authorization records that explicitly establish Source Authority and formal Trusted Build for the exact A9 HEAD. It means the active implementation pointer and its supersession trail have not yet been reconciled to that A9 candidate.

The prior harmonization apply/post-apply records (Box `2491700051951`, `2491702950277`) correctly state that their work applied Product Constitution v1.6.1, Implementation Plan v1.3.1, Technical Contracts v1.1, and Execution Profile v1.3/revision 4 through successor materialization, while explicitly preserving SOURCE_AUTHORITY=NOT_ESTABLISHED, TRUSTED_BUILD=NOT_ESTABLISHED, PRODUCTION_RUNTIME=NOT_AUTHORIZED and SEAL=NO. This application is not an implementation-pointer update and does not solve the active full Test Register conflict.

Relevant source links:
- Implementation pointer: https://app.box.com/file/2492339224632
- Current Decision Register: https://app.box.com/file/2492332324704
- Harmonization application: https://app.box.com/file/2491700051951
- Post-apply verification: https://app.box.com/file/2491702950277
- PR #5: https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/pull/5
- PR #26: https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/pull/26

Disposition: keep PR #5 and PR #26 untouched as historical/candidate branches; prepare a source-bound implementation-pointer successor only through a proven authority route, showing which tree is the current candidate basis and which predecessor remains preserved. This is a governance/source lineage task, not a request to merge either PR.

## 19. Consolidated structural scan status (A9 exact HEAD)

The exact A9 tree at `c8dab3542d3d4725cf591630c07f76366f7949d0` has now been enumerated by type and scanned structurally:
- 111 Python files: all blobs fetched and scanned for selected test-discovery and unsafe-call patterns; one confirmed misplaced test method found.
- 41 JSON files: syntax/field scan; one invalid historical R1 JSON, nine invalid-length H2 mapping digest fields, plus explicit non-materialized hash placeholders that were kept distinct from malformed digest values.
- 31 text/config/workflow/build files excluding Python/JSON and binary TZIF fixtures: scanned for the H2 digest and long digest-like strings. Two Markdown H2 mapping references were also found malformed, making 11 artifact copies of the same bad mapping digest.
- Binary/timezone fixtures are not part of this text pattern scan and were not claimed inspected byte-by-byte here; separate TZif code/runtime controls exist but native runtime qualification is still unestablished.

This gives a stronger code/configuration structural view than the initial bounded governance-only review, but it still is not a semantic line-by-line audit of all source logic or every operating-system execution. The candidate must remain non-authoritative until the provenance, tests, source lineage and release gates are corrected/verified through their proper routes.


## 20. PR #5 versus PR #26 — direct file comparison

To distinguish an actual lineage relationship from assumptions based only on dates, the 11 paths changed by PR #5 were read at both exact heads:
- PR #5 HEAD `3db976fd7293f0d4c5d367a81fc87489a97ba900`
- PR #26 A9 HEAD `c8dab3542d3d4725cf591630c07f76366f7949d0`

Observed identity comparison:

| Path | PR #5 vs A9 result | Interpretation |
|---|---|---|
| `configs/runtime_profile.dev.json` | identical blob SHA `a4a087ac553ca59e9c6bf6d7feddbb25481ff90f` | shared file content |
| `docs/NORMATIVE_BASELINE_REFERENCES.md` | identical blob SHA `342383e1a9dfbca05019d33d906266759c1b2ee0` | both trees cite the same summary-level normative bases |
| `src/ce/calculation/engine.py` | identical blob SHA `19d23c545ed48d4bc2a4e9a68ea0d6f63a91a0b6` | this specific engine file is shared |
| `manifests/SOURCE_TREE_SHA256_V2.txt` | differs: PR #5 SHA `b85c24f388877247248ffa4d333728c9a5a60be7`; A9 SHA `3b0408cbfca6d626ac673391afafd53f90b9745c` | different whole-tree identities |
| `manifests/implementation_manifest.json` | differs; PR #5 1,026 chars, A9 1,113 chars | different candidate manifest state |
| `src/ce/calculation/contracts.py` | differs; PR #5 1,431 chars, A9 32,908 chars | the A9 source tree is substantially extended here |
| `src/ce/calculation/time.py` | differs; PR #5 5,213 chars, A9 3,917 chars | differing time-layer implementation |
| `src/ce/foundation/status.py` | differs; PR #5 1,132 chars, A9 1,098 chars | differing status definitions |
| `tests/test_evidence.py` | differs; PR #5 1,379 chars, A9 1,561 chars | differing test implementation |
| `tests/test_runtime_gate.py` | differs; PR #5 7,299 chars, A9 9,099 chars | differing runtime-gate coverage |
| `tests/test_time_signal_boundaries.py` | differs; PR #5 5,001 chars, A9 12,072 chars | differing time/signal boundary coverage |

This gives a concrete conclusion: the later A9 candidate is neither a byte-identical copy of the PR #5 source tree nor an unrelated tree with no shared lineage. It shares selected implementation/baseline files but also has material source, test and manifest divergence. The older implementation pointer's SHA `3ff8c6fdd8e78a8466c4b556912de0a70b62624222d1ab52a990d7e648600898` and the A9 tree's `1a4004ac644331964ab9d540abf6b1631aed1cbbe0cbdd55316fe5356a0c7a8b` therefore cannot be substituted for each other.

**Disposition:** source-lineage / active-pointer reconciliation remains open. Do not infer that A9 supersedes PR #5 solely because it is later, and do not infer PR #5 contains the A9 extension solely because some files match. A controlled successor must name the selected candidate basis, list the precise predecessor(s) and retained hashes, and update the active implementation pointer only through the valid source-authority route. PR #5 and PR #26 remain untouched and unmerged.


## 21. Original “11 findings + 3 important notes” — content recovery versus historical artifact provenance

A new cross-store reconciliation separates two states that were previously easy to conflate.

### 21.1 Dated recovery records — historically correct within their cutoff

The Box record **CE_ORIGINAL_11_FINDINGS_3_NOTES_SOURCE_RECOVERY_AUDIT_R0_2026-10-10.md** (Box file ID `2517866785521`, https://account.box.com/file/2517866785521) and **CE_11_FINDINGS_3_NOTES_SOURCE_RECOVERY_LOG_R0_2026-10-10.md** (Box file ID `2518016790491`, https://account.box.com/file/2518016790491) document the search completed on 2026-10-10. They explicitly distinguish the desired original list from later working registers and report that the exact original item-by-item source was not recovered in the searched stores. Those findings remain valid for that search window; they do not establish universal absence.

### 21.2 Updated status from owner-supplied content — 2026-10-11

The draft [PR #38 — 11 Findings + 3 Notes Crosswalk R0](https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/pull/38) preserves the substantive 11-area findings and three notes supplied by the owner in the current conversation. The crosswalk records the material as directly available/re-supplied and explicitly preserves the original historical artifact gap.

Therefore the current status must be expressed as three distinct claims:

| Recovery dimension | Current disposition | What the evidence supports |
|---|---|---|
| Substantive content of the 11 findings + 3 notes | **RECOVERED FROM OWNER RE-SUPPLY** | The supplied content has been preserved in the crosswalk; do not keep saying its substance is wholly unavailable. |
| Original historical chat message/export/file/attachment and its original byte identity/hash/signature | **NOT INDEPENDENTLY RECOVERED** | The owner identifies the re-supplied material as the earlier content, but the old source object and its historical metadata have not been independently established. |
| Historical status labels such as PROVEN / PARTIAL / HUMAN DECISION REQUIRED | **PRESERVED AS REPORTED, NOT AUTOMATICALLY RE-CERTIFIED** | Each current disposition still requires its own current source, authority and test evidence. |

The undifferentiated sentence in the current PR #27 description that the original “11 findings + 3 important notes” are still NOT RECOVERED is now stale **with respect to substantive content availability**. It remains accurate only when narrowed to the independent recovery of the original historical source artifact and provenance. The dated Box records should remain unchanged as evidence of the earlier search result; this addendum does not rewrite their historical cutoff.

### 21.3 The three notes and later source-specific correction

The current crosswalk records three distinct notes: (1) historical versus current baseline differences; (2) Share Card retirement status must not be collapsed into a normative amendment; and (3) Calculation / Signal / Canon source anchors and the birth-time/calendar boundary. The notes are preserved as crosswalk items, not as automatic approvals or a replacement Constitution.

For the three named normative anchors, the separate R3 archive-member identity audit linked in §2 already verified the archived bytes for Calculation Constitution v1.9, Signal Engine Core v1.4 and Interpretive Canon v1.2 as exact matches. That closes the **specific archived-byte identity check**; it does not close the distinct source-authority, retained Index pointer, active full Test Register or implementation/test-lineage questions. Any earlier crosswalk wording that the raw hash recomputation was pending should be read as a historical state superseded only for those specifically identified archived members.

### 21.4 Operational consequence

No additional request for the owner to restate the 11+3 is warranted merely because the historic source object remains missing. Use the preserved owner-supplied crosswalk for the substantive item map, retain the provenance limitation, and continue validating each present-day disposition against its own source and test evidence. Do not infer an unrecorded mapping from the initial labels alone. This reconciliation changes no normative source, official Test Register, production code, source authority, Trusted Build, runtime, A10 or SEAL state.


## 22. H2 mapping-file identity — Box copies found; raw SHA-256 still unverified

### 22.1 Matching objects found in Box and Dropbox

A fresh Box search for `test_mapping_100.h2_provenance_reconciled.yaml` returned three Box files of the same reported size and SHA-1:

| Box object | Name | Reported size | Box-reported SHA-1 |
|---|---|---:|---|
| [2506856840608](https://account.box.com/file/2506856840608) | `test_mapping_100.h2_provenance_reconciled.yaml` | 9,553 bytes | `c85d30641a57f19c3a921d62f4873abcecb24d5f` |
| [2506877416506](https://account.box.com/file/2506877416506) | `test_mapping_100.h2_provenance_reconciled (2).yaml` | 9,553 bytes | `c85d30641a57f19c3a921d62f4873abcecb24d5f` |
| [2506878150665](https://account.box.com/file/2506878150665) | `test_mapping_100.h2_provenance_reconciled (1).yaml` | 9,553 bytes | `c85d30641a57f19c3a921d62f4873abcecb24d5f` |

Dropbox search also returns three same-name copies of 9,553 bytes in the H8 recursive extraction lineage. One record exposed Dropbox content hash `7fcec8db732ddfbb82112c6690158180e8c9770d2270cc96339f3f8be64ccb68`. The Dropbox content hash is a provider-specific value; it is not treated here as a raw-file SHA-256.

The prior [H2 Raw Intake Verification R1](https://account.box.com/file/2506851548670) names the expected 64-hex SHA-256 as:

`BABCCCF81636DF1E65EB92FE9119D474787FCF3801B547FA5703E9048993D441`

That same verification record explicitly says that direct SHA-256 rehash of the original Box binary payload had not been performed. During this continuation, the catalogued Box raw-download helper returned “Tool get_download_url not found”; the raw binary bytes were therefore not recovered through that route. Extracted text and matching Box size/SHA-1 metadata are corroboration, not a substitute for a direct SHA-256 of the original bytes.

### 22.2 Current disposition

- **PROVEN:** three Box copies report the same 9,553-byte size and same Box SHA-1; multiple Dropbox copies of the same named payload also appear in the historical extraction tree.
- **NOT PROVEN:** the expected 64-hex SHA-256 has not been independently computed from raw payload bytes in this continuation. Provider metadata/content hashes do not establish the SHA-256 value.
- **CONFIRMED DEFECT IN A9 TEXT/JSON REFERENCES:** nine JSON fields and two Markdown references still carry 62- or 63-character strings where the field asserts a SHA-256 mapping digest. The malformed literals must not be silently replaced from visual guesswork, even though an expected 64-character value appears in prior provenance text.
- **NEXT ADMISSIBLE STEP:** obtain the raw mapping file through an operational raw-byte download path; compute SHA-256 over those exact bytes; compare it with the provenance-recorded expected value; preserve original candidates and perform any correction only on a controlled successor branch with newly computed source identity. Do not rewrite the pinned A9 candidate or reuse its trust/build attestations.

This is an evidence-retrieval boundary, not permission to waive digest validation. Source Authority, Trusted Build, runtime, production, A10 and SEAL remain unchanged.


## 23. Share Card — product scope closed; explicit retirement pointer awaits valid Index adoption

### 23.1 Source anchors inspected

| Source | Identity / location | Evidence and scope |
|---|---|---|
| Product Constitution v1.6.1 | Box [2491704535193](https://account.box.com/file/2491704535193), §13 (V1 Hard Exclusions) | Explicitly excludes public sharing and social-sharing workflow. |
| Business Model material labelled v1.5 | Box [2485331476456](https://account.box.com/file/2485331476456), §§11 and 15 | Excludes public sharing and referral/sharing rewards from the V1 business baseline. The current Index / full-register lineage conflict remains separate; this row is not an assertion that every Index pointer is reconciled. |
| Implementation Plan v1.3.1 | Box [2491699264134](https://account.box.com/file/2491699264134), §3.2 | Lists Share Card among features out of scope unless a later controlled change explicitly reopens it. |
| V1.6 release validation | Box [2485336557011](https://account.box.com/file/2485336557011) | Reports no active Share Card feature headings and no Share Card/social-sharing activation in the validated bundle. |
| Explicit owner product decision | Box [2510397781891](https://account.box.com/file/2510397781891), dated 2026-10-07 | Says Share Card is retired, not part of CE V1, and not to be implemented, activated, maintained or treated as an acquisition mechanism. The same record says its classification is **“NORMATIVE DECISION INPUT / NON-AUTHORITATIVE UNTIL DOCUMENT STACK IS VERSIONED.”** |
| Follow-up global reconciliation | Box [2510417318335](https://account.box.com/file/2510417318335), G-022 | Records Share Card as closed for V1 product scope; no exception to no-public-sharing, no sharing acquisition/reward/social-sharing flow or public Share Card URL; historical references remain history. |
| Proposed Index v2.0 candidate R3 | Box [2518414473182](https://account.box.com/file/2518414473182), §12.8 and §13 | Includes the explicit “Share Card is retired from V1” clause, but expressly remains a non-normative candidate; adoption route is not established. |

### 23.2 Reconciled disposition

**PRODUCT SCOPE: CLOSED — SHARE CARD RETIRED / EXCLUDED FROM V1.**

This is not an open product choice and does not warrant asking the owner again. The specific retirement instruction is consistent with the inspected baseline exclusions of public/social sharing and sharing rewards. The available evidence does not show a current V1 semantic requirement to implement Share Card or to retain a Share Card exception. Historical mentions are provenance, not permission to build or reactivate the feature.

A distinction remains at the governance-document layer: the 2026-10-07 decision record expressly says it is not authoritative until the document stack is versioned, while the proposed Index v2.0 R3 that carries the explicit retirement clause is still a candidate. The active retained Index has its own version/pointer and Test Register binding conflicts. Therefore the explicit decision-to-active-Index propagation is **NOT ESTABLISHED**. This is a controlled documentation/adoption gap; it does not reopen the already-closed product decision and must not be “fixed” by silently editing the current Index or by merging a candidate without the valid route.

### 23.3 Cleanup and verification boundaries

- Preserve the existing Share Card decision, historical references and prior reconciliation evidence.
- Do not implement, activate, maintain or promote Share Card, its public URL, social-sharing path, sharing rewards or acquisition mechanism into V1.
- Do not perform a blanket destructive deletion of every historical reference. Any additional cleanup must inspect the actual artifact, distinguish historical evidence from executable/current-scope material, and follow the applicable retention/change-control route.
- If the valid Index adoption route is independently established later, the successor should carry the explicit retirement clause and its decision provenance. Until then, keep the active Index unchanged and the pointer gap open.
- No Product Constitution, Business Model, Implementation Plan, official Test Register, Index, code, schema, runtime, Source Authority, Trusted Build, A10 or SEAL state was changed by this finding.


## 24. Delegated autonomy versus one-off Index adoption — distinct approval boundary confirmed

### 24.1 Approved mandate: routine work may proceed; Index adoption is not implied

The owner decision record [CE_OWNER_DECISION_RECORD_AUTONOMOUS_EXECUTION_GOVERNANCE_MANDATE, Box 2517806798198](https://app.box.com/file/2517806798198) records the master autonomous-execution mandate as approved. It authorizes source discovery, reconciliation, audit, candidate preparation, permitted corrections and verification without step-by-step approval; the same record explicitly says this is not automatic approval of every GDE-01 clause or other substantive change. It identifies governance integration as pending a source-verified target and route.

That boundary is explicit in §3 of the owner record:
- the mandate does not itself amend or supersede a controlling normative source;
- the assistant must verify the exact current governing instrument and valid change/adoption/promotion route;
- if no valid route exists, prepare the narrow governance instrument as a candidate but do not declare it active merely because it was created.

No repeat approval of the already-approved master mandate is warranted.

### 24.2 Concrete one-off Index packet exists, but it asks for a different owner disposition

The [GDE-01 one-off Document Index amendment decision packet, Box 2518435701566](https://app.box.com/file/2518435701566), is classified “OWNER DECISION PACKET / NON-NORMATIVE UNTIL EXPRESS DISPOSITION” and says in §§1–2 that no authority effect arises before an explicit disposition. Its single requested decision is whether to approve the exact Index v2.0 Candidate R3 identity and the proposed one-off successor route in §6.

The packet states that:
1. the retained Index §8 governs feature/schema/data change-control, but does not establish a general self-amendment route for its own delegation clauses;
2. C3-3 is limited to Source Authority identity/authorization;
3. an earlier harmonization route was specific to that transaction, not a proven universal Index amendment route;
4. the owner-approved master mandate alone is not this missing route;
5. no owner response had been recorded in that packet at its preparation cutoff (2026-10-10).

The same distinction is repeated in the [proposed Index v2.0 Candidate R3, Box 2518414473182](https://app.box.com/file/2518414473182): the text is a non-normative candidate until exact target, route, owner-disposition scope, lineage and gates are evidenced.

### 24.3 Current determination

| Item | Status | Allowed next treatment |
|---|---|---|
| Autonomous routine investigation, source reconciliation, candidate drafting and evidence verification | **OWNER MANDATE APPROVED** | Continue without repeated approval, within actual access and existing gates. |
| The exact Index v2.0 Candidate R3 text as active governing Index | **NOT APPROVED / NOT ADOPTED BY THE EVIDENCE INSPECTED** | Keep non-normative; preserve the retained Index and its history. |
| The specific one-off successor/adoption route in GDE-01 packet §6 | **SEPARATE OWNER DISPOSITION REQUIRED; NOT RECORDED IN THE PACKET INSPECTED** | Do not execute adoption/promotion without the exact disposition. |
| Source Authority, Trusted Build, A10 Runtime Adoption, production, release and SEAL | **SEPARATE PROTECTED GATES; NOT AUTHORIZED HERE** | Continue candidate-only investigation; do not infer these permissions from the master mandate or Index route. |

This does not ask the owner to approve the mandate again. It records that one specific unresolved decision—adopting a named proposed Index and its unique one-off route—is different in scope from the already-approved general operating mandate. The assistant must not manufacture that owner disposition, assume silence is consent, or treat the existence of a prepared packet as approval.

### 24.4 Immediate permissible work

Continue source searches, candidate evidence, source/test-lineage reconciliation and non-authoritative audit records. Preserve current retained Index, archived sets, Test Register and normative documents unchanged. If the owner later provides the exact disposition, verify it against the candidate digest and §6 preconditions before following that route. Until then: no Index replacement, no in-place edits to the retained archive, no normative promotion, and no A10 start.


## 25. A9 Source Authority / Trusted Build — later formal records supersede earlier status interpretation

### 25.1 Exact candidate and controlling evidence

The exact candidate remains:
- Repository: `ConstellationsEcliptic/Constellations-Ecliptic`
- Branch: `remediation/ce-r0-a9-trusted-build-r1/2026-10-08`
- HEAD: `c8dab3542d3d4725cf591630c07f76366f7949d0`
- Source-tree SHA-256: `1a4004ac644331964ab9d540abf6b1631aed1cbbe0cbdd55316fe5356a0c7a8b`
- Control-plane SHA-256: `0bc4f88dc43549a1033434a2a3653c02b46002024630b4294c22ddb8a5f7c357`
- Dependency-lock SHA-256: `ef8ace995340aa53026991644521ed85bbc5282781af9e8d88f030e83b776be5`

The later [A9 Runtime / Trusted-Build Evidence Reconciliation R2, Box 2514341553097](https://account.box.com/file/2514341553097) explicitly supersedes only the state interpretation of its R1 predecessor and reports:
- formal human Trusted Build authorization exists at [Box 2513654771321](https://account.box.com/file/2513654771321);
- the authorization binds the exact A9 HEAD and source-tree/control-plane/dependency-lock identities above;
- C3-1 = APPROVE, C3-2 = VERIFIED, C3-3 = SATISFIED-BY-SOLO-OWNER-MODEL;
- SOURCE_AUTHORITY_FOR_A9 = ESTABLISHED UNDER SOLO OWNER MODEL;
- TRUSTED_BUILD_TECHNICAL_GATE_A9 = PASS;
- TRUSTED_BUILD_FORMAL = ESTABLISHED.

The formal authorization record gives the recorded Trusted Build run as `37765039886`, wheel SHA-256 `293f235d7074a506afb4654aebe99b4cfb88ed393f3abdabcaa5f4c9dbf532b7`, source-package SHA-256 `77f2baddc508c26cb25dcbdbfd74f25fbc206e98d259712f9cbd3154b5c47191`, source package boundary PASS, Git-archive source materialization parity PASS and two independent build/test/package executions with 261 tests each. The separate exact-head Actions results in §3 remain additional technical evidence; they are not the only basis for the formal status.

### 25.2 Corrected current status — scope is exact and narrow

| Gate / state | Current disposition for exact A9 HEAD | Source basis |
|---|---|---|
| C3-1 human disposition | **APPROVE** | R2 reconciliation and formal authorization record |
| C3-2 cryptographic verification | **VERIFIED** | R2 reconciliation; C3-2 record Box 2513652710150 |
| C3-3 Source Authority | **ESTABLISHED UNDER SOLO OWNER MODEL** | R2 reconciliation; C3-3 record Box 2513650472663 |
| Trusted Build technical gate | **PASS** | Formal authorization record / recorded run evidence |
| Formal Trusted Build | **ESTABLISHED** | Human authorization record Box 2513654771321, bound to exact candidate identity |
| Runtime Adoption | **NOT ESTABLISHED** | A9 R2 and A10 design/boundary records |
| Full runtime coverage | **NOT ESTABLISHED** | Captured 201/201 annual shards are parity evidence, not proof of the complete production runtime domain |
| TZIF runtime identity | **NOT ESTABLISHED** | Runtime identity must be independently verified and bound to a separate runtime receipt |
| Production / deployment / merge authorization | **NOT AUTHORIZED / NOT ESTABLISHED as applicable** | Explicit non-establishments in the authorization record |
| SEAL | **NO** | Explicit non-establishment |
| Overall authorization | **NON_AUTHORIZED; FAIL_CLOSED=TRUE** | Exact A9 R2 state |

### 25.3 What this correction does — and does not — change

The earlier sentence in §3 that carried forward `FORMAL_TRUSTED_BUILD=NOT_ESTABLISHED` from technical workflow/log state was an outdated status interpretation. It is corrected here and in the present-tense wording above. The current conclusion follows the later, exact-candidate R2 reconciliation and formal authorization record, rather than preferring a log snapshot merely because it was seen first.

However, the audit's independently identified A9 issues remain material and open:
1. the intended fourth test in `tests/test_source_tree_identity_r1.py` is misplaced and absent under normal discovery;
2. the malformed 62-/63-character H2 mapping digest references remain in nine JSON files and two Markdown references, and raw H2 bytes were not available here for a direct SHA-256 recomputation;
3. the current-candidate manifest still carries state fields that conflict with the later Source Authority / Trusted Build records;
4. the candidate has not been promoted or merged, and the formal Trusted Build record does not establish Runtime Adoption or production use.

The existence of a formal Trusted Build authorization is a **status fact for the recorded exact candidate**; it is not a claim that the later audit findings have been fixed, that every intended test ran, that the entire candidate's semantic/source/test lineage is clean, or that production is authorized. Any remediation must use a controlled successor with fresh source-tree and control-plane identities, complete digest repairs from verified raw bytes, a re-run/review of the relevant tests and a fresh applicable authority/build disposition. The pinned A9 candidate and its historical evidence remain unchanged.

### 25.4 No authority promotion

This appendix corrects the audit's record interpretation only. It does not alter the source tree, its manifests, Box authorization records, workflow runs, PR #26, runtime, protected branches, Index, official Test Register, A10 state or SEAL. Keep PR #26 OPEN / DRAFT / NOT MERGED. The defensible current boundary is: **A9 Source Authority and formal Trusted Build are established for the exact candidate; Runtime Adoption is not established; production remains unauthorized; new audit findings still require controlled disposition before any successor or use.**


## 26. A3 — Today’s Note: historical editorial prototypes found, but no approved V1 source/library

### 26.1 New bounded discovery in Box raw-inventory intake

A wider second pass reached the historical visual-prototype folders under the Box intake area `99_LOCAL_INVENTORY_INTAKE_2026-09-24/00_RAW_UNSORTED`. These objects were not an approved current V1 UI/source chain; their parent path identifies them as raw intake.

| Artifact | Box identity | Metadata / observed content | Authority implication |
|---|---|---|---|
| CE 1.4 Editorial Minimal prototype | [Folder 420937715067](https://account.box.com/folder/420937715067) | Contains hard-coded `app.js` [2485682769599](https://account.box.com/file/2485682769599), SHA-1 `fc00b4025b9996afe63ce47206cf121f8943ea1b`, 6,020 bytes; `README.md` [2485684125139](https://account.box.com/file/2485684125139), 2,698 bytes. | Historical prototype, not an approved V1 editorial library. |
| CE 2.0 Editorial Recast prototype | [Folder 420933551087](https://account.box.com/folder/420933551087) | Contains hard-coded `app.js` [2485689820604](https://account.box.com/file/2485689820604), SHA-1 `15e428cec9dc6f9d34953d839ab64e95c42c270e`, 6,157 bytes; `README.md` [2485686200649](https://account.box.com/file/2485686200649), 3,328 bytes. | Later visual recast in the same raw-intake lineage, not approval or normative successor. |
| Prototype API placeholder | `daily-reading.js` Box [2485691382652](https://account.box.com/file/2485691382652), also duplicated in the v2 folder at [2485683267619](https://account.box.com/file/2485683267619) | Returns HTTP 501 and explicitly says the visual preview contains no live AI endpoint. | Confirms that this is a static/demo prototype, not the current production reading service. |
| Prototype context adapter | `frontend-context.js` Box [2485689760174](https://account.box.com/file/2485689760174), also present at [2485695577864](https://account.box.com/file/2485695577864) | States it performs no astronomical calculation and only forwards sign plus structured signal `ruleId/theme/provenance` values. | Not a calculation or approved editorial-source implementation. |
| Structured-signal schema | Box [2485696088753](https://account.box.com/file/2485696088753) and [2485690659682](https://account.box.com/file/2485690659682) | Simple schema requiring `ruleId`, `theme` and `provenance`; no editorial content catalogue/library was present in the inspected `data` folder. | A signal schema is not a Today’s Note library or source-approval record. |

### 26.2 What the prototype’s embedded content does

The two inspected `app.js` files contain a hard-coded `READINGS` map keyed directly by zodiac sun sign, along with generated display values derived from a hash of the sign and current date:
- “energy” metrics and score bars;
- “lucky word”, stone and color;
- reflection prose and a “tomorrow” message;
- locally stored journal text through `localStorage`;
- a signup/“quiet list” interaction.

The score values are derived in the prototype from `hash(sign + current date)`, not from the CE astronomical calculation/geometry/signal pipeline. The embedded horoscope-style prose is selected by sign, rather than being a separately approved, versioned, source-accountable general editorial item. Its presence is therefore evidence that historical demonstration copy exists, not proof that those claims/content are approved for present CE V1.

The README in both folders expressly calls the project a standalone visual prototype and says the daily content is deterministic demo content that **must not be represented as live astronomical calculation** until the CE Astrology Core and ephemeris are connected. The README also lists a private local Journal and an email-routine/signup placeholder. Those historical features must not be promoted into V1 by copying them across merely because the CSS/visual design is reusable.

### 26.3 Cross-check against current owner disposition and source contract

The [owner disposition for Today’s Note × valid Quiet Sky, Box 2515533522798](https://account.box.com/file/2515533522798), approves only this limited product-semantic direction:
- an optional, separate and non-personal Note may accompany a **valid** `QUIET_SKY` result;
- the Note is not a personal signal, Canon interpretation, prediction, or evidence that a signal exists;
- if no approved item exists, omit the Note;
- the Note must not mask a technical, calculation, integrity or semantic-validation failure.

The same decision explicitly does **not** approve an editorial database, exact UI copy, selection algorithm, schema/code change, free-form runtime AI generation or deployment. The [Today’s Note contract recommendation R0, Box 2515537459111](https://account.box.com/file/2515537459111) and [controlled change proposal R2, Box 2517767431094](https://account.box.com/file/2517767431094) remain non-normative proposals. The latter explicitly says an accountable/versioned source, approval state, locale where relevant, review/expiry rule, and deterministic selection rule are still needed.

The [Source/UI Authority Discovery R1, Box 2515543958136](https://account.box.com/file/2515543958136) remains valid within its original search boundary: it found no separate approved current UI specification or approved Today’s Note editorial library in the inspected current-governing/documentation and repository locations. This wider search refines that statement, rather than contradicting it: **historical demo prototypes exist in the raw-inventory intake, but no approved current V1 editorial source/library has been established by their existence.**

### 26.4 Current A3 disposition and admissible next step

| Question | Current status |
|---|---|
| Is the high-level product behavior already decided? | **YES, limited scope.** Optional non-personal Note beside valid `QUIET_SKY`, only when an approved item exists; otherwise omit; never mask failure. Do not ask for this choice again. |
| Does an approved content source/library exist in the accessible examined chain? | **NOT ESTABLISHED.** Historical demo prose is available, but the source is hard-coded into legacy prototype code and lacks the necessary editorial provenance/version/approval/expiry/locale contract. |
| Are exact copy, current item selection, locale fallback, UI/display contract and official tests approved? | **NOT ESTABLISHED.** They were expressly excluded from the owner’s limited disposition and remain open in the non-normative R2 proposal. |
| May prototype readings/metrics be reused as Today’s Note or current personal readings? | **NO, not on the evidence inspected.** They are demo content; their apparent scores are not calculated CE signals. Any selected words would require separate content review, provenance, approval and controlled integration. |
| Does A3 allow the A10 gate to pass? | **NO.** A3 remains open until the required current item source/library and controls are evidenced. |

The smallest defensible next artifact is a **candidate editorial-library manifest and lifecycle contract**, not a bulk import of the prototype’s `READINGS` object. It should define each item's stable ID, exact text, source/author or licensed origin, version, approval state, locale, reviewed-at/expiry, deterministic selection eligibility, and the rule that missing/expired/unapproved/wrong-locale content is omitted. The source must be reviewed independently for unsupported personal claims and must never imply an astronomical event or personal forecast. Create it only as a non-authoritative candidate; do not silently change Product Constitution, Implementation Plan, UI or code while the active Index/adoption route and official Test Register binding remain unresolved.

This appendix changes no raw-inventory prototype, approved owner decision, normative source, official Test Register, Index, implementation, code, schema, Source Authority, Trusted Build, Runtime Adoption, A10, production or SEAL state.


## 27. Runtime gate's hard-coded authority reason versus the later A9 authority record

### 27.1 Exact source behavior

At exact A9 HEAD `c8dab3542d3d4725cf591630c07f76366f7949d0`, `src/ce/runtime/gates.py` (blob SHA-1 `40a1874392af704cb1bd837a40275c27b5adbb87`) implements `authorize_runtime(identity)`. After identity-shape/profile/required-field checks, the function unconditionally appends both:
- `source_authority_attestation_not_established`;
- `independent_runtime_identity_verification_not_established`;

and returns `RuntimeAuthority.NON_AUTHORIZED`. The same file describes its invariant: identity presence never constitutes authority.

### 27.2 Reconciled interpretation

The later [A9 Runtime / Trusted-Build Evidence Reconciliation R2, Box 2514341553097](https://account.box.com/file/2514341553097) and [formal Trusted Build authorization, Box 2513654771321](https://account.box.com/file/2513654771321) establish external Source Authority and formal Trusted Build for the exact A9 candidate. Therefore the reason token `source_authority_attestation_not_established` no longer accurately describes the status of the **external A9 authority record**.

That does not make the runtime gate wrong to deny authorization. The source code is deliberately not wired to accept the presence of an external document, identity object or capture as runtime authority. It still lacks the separately verified receipt and independent runtime-identity check required for Runtime Adoption. So there are three different statements:
1. **External Source Authority record:** ESTABLISHED for exact A9.
2. **Runtime code receipt/identity verification:** NOT ESTABLISHED; the implementation does not yet consume a verified runtime-authority receipt.
3. **Runtime Adoption / production:** NON_AUTHORIZED; fail-closed remains correct.

This is a naming/state-reconciliation issue plus an expected missing runtime-authority mechanism; it is not permission to remove the guards.

### 27.3 Required handling

- Preserve A9 code and all formal authority records unchanged.
- Do not change the gate's unconditional reasons in the pinned A9 tree.
- In any controlled successor/A10 implementation, bind a separate verified receipt to exact candidate/source-tree/control-plane/dependency-lock, signed Source Authority, formal Trusted Build, runtime profile, native/Swiss/TZIF artifacts, environment and independent verification result.
- Replace a generic “source authority not established” reason only after the receipt verifier determines the exact status from verified inputs; preserve NON_AUTHORIZED when the receipt or any required identity proof is absent, stale, malformed or mismatched.
- Add acceptance tests for both states: external Source Authority/Trusted Build exists but Runtime Adoption receipt is absent ⇒ remain NON_AUTHORIZED; valid fully matched receipt plus independent identity verification ⇒ only then can the specific Runtime Adoption gate be evaluated.
- Reconcile the reason-token language, implementation pointer and official test-oracle evidence in the controlled successor's change record. Do not alter official Test Register status through this audit report.

This section corrects interpretation only. No code, manifest, Source Authority, Trusted Build, Runtime Adoption, Index, official Test Register, A10, production or SEAL state was changed.


## 28. Pre-A10 Area Register status-label drift in PR #27 description

### 28.1 Exact identity comparison

At exact PR #27 HEAD `549e53c0abccc3fb6d26f2cf0e32b7b3f7e00668`, the file `governance/candidates/CE_PRE_A10_AREA_REGISTER_R2_2026-10-10.json` has blob SHA-1 `3dad17c41515f7104808dc1d199568e309f09b45`. Direct JSON parsing returns:
- 13 `CLOSED_PRESERVE`;
- 6 `OWNER_DECISION_RECORDED`;
- 1 `DEFERRED_BY_EXPLICIT_DISPOSITION` (E4);
- 3 `RECOMMENDATION_READY` (A3, B1, D4).

It returns no `OWNER_DISCUSSION_REQUIRED` area. A3 is explicitly `RECOMMENDATION_READY` in that register version.

The PR #27 description's opening summary still reads A3 as `OWNER_DISCUSSION_REQUIRED`, and older historic descriptions contain other counts from earlier registers. This is a **status-summary drift between the PR narrative and its exact-head area-register JSON**, not a change to the product semantics and not a gate bypass.

### 28.2 Gate effect

The exact-head strict gate still identifies A3/B1/D4 as the three incomplete areas and remains blocked at 20/23 completion. The stale label does not change which three areas remain open, nor the strict gate result. The 14 validator tests and structure checks can pass while the separate strict completion gate fails as designed.

### 28.3 Required treatment

- Use the exact-head JSON as the current declared status source for this candidate register.
- Treat the PR description's older A3 status label as historical/stale where it conflicts with that JSON; record rather than silently erasing the discrepancy.
- Do not set A3 to a completion status to harmonize the description. A3 still lacks an approved current editorial item/library and approved downstream implementation/test contract.
- Preserve the PR history and register bytes. A later controlled status/handoff update may correct the prose summary; this report does not mutate the PR body or area register.

No official Test Register, normative source, application code, schema, A10, runtime, Source Authority, Trusted Build, production or SEAL state was changed by this finding.

## 29. Superseding correction to §28 — current Pre-A10 gate target and register lineage

### 29.1 Why the earlier §28 conclusion is narrowed

Section 28 compared the PR #27 narrative to `CE_PRE_A10_AREA_REGISTER_R2_2026-10-10.json` and concluded that the PR narrative's A3 label had drifted. That conclusion was too broad because it treated the R2-named file as the current gate target without verifying which register the exact-head workflow actually gates. The current PR #27 HEAD and its workflow explicitly target R3. **The claim that the current PR #27 description is wrong about A3 is withdrawn.** Its current A3 label matches the R3 register used by the gate.

### 29.2 Exact current-head evidence

- PR #27 exact HEAD at this check: `242bc16ac7ad29a471239b736d5b3915a92d07be`; PR remains OPEN / DRAFT / NOT MERGED.
- Exact-head Actions run: [#38076234592](https://github.com/ConstellationsEcliptic/Constellations-Ecliptic/actions/runs/38076234592).
- The run executes `scripts/governance/pre_a10_area_gate.py governance/candidates/CE_PRE_A10_AREA_REGISTER_R3_2026-10-10.json --require-complete`.
- R0, R1, R2 and R3 structure validators PASS; all 14 validator unit tests PASS.
- The strict R3 completion gate fails with exit code 2 by design. Its emitted result has `area_count=23`, `complete_count=20`, `incomplete_count=3`, IDs `A3`, `B1`, `D4`, `pre_a10_area_review=INCOMPLETE`, empty `errors`, and explicit non-authorization of A10/runtime adoption, production and SEAL. Combined-status lookup returned no separate status records; the workflow run is the exact CI evidence cited here.
- R3 blob SHA-1: `ab6e005bed107d8b909a16af9f24fc239b138ae8`; internal `revision=R3`; current counts: 13 `CLOSED_PRESERVE`, 6 `OWNER_DECISION_RECORDED`, 1 `DEFERRED_BY_EXPLICIT_DISPOSITION` (E4), 1 `OWNER_DISCUSSION_REQUIRED` (A3), and 2 `RECOMMENDATION_READY` (B1, D4).

### 29.3 The real register lineage/name mismatch

Comparing all four exact files on that same PR #27 HEAD gives:

| Path suffix | Blob SHA-1 | Internal revision | Status summary |
|---|---|---|---|
| `R0_2026-10-09.json` | `0062647a794f3c20e8b4ca96a66ada96fa5a2442` | absent | 13 closed; 5 owner decisions; 4 recommendation-ready; 1 deferred |
| `R1_2026-10-10.json` | `16b0666122b699e94a975650cd7cbbc9d8305413` | `R1` | 13 closed; 6 owner decisions; 3 recommendation-ready; 1 deferred |
| `R2_2026-10-10.json` | `3dad17c41515f7104808dc1d199568e309f09b45` | `R1` | Same blob as R1; same statuses and content identity |
| `R3_2026-10-10.json` | `ab6e005bed107d8b909a16af9f24fc239b138ae8` | `R3` | 13 closed; 6 owner decisions; 2 recommendation-ready; A3 owner-discussion; 1 deferred |

The concrete discrepancy is therefore the **R2 filename versus its internal R1 revision and identical R1 blob**, not the current PR description's A3 label. The current workflow gates against the R3 path and R3 revision. This audit does not infer that the R2-named copy was intended to be a new semantic revision; it records the naming/lineage anomaly for controlled maintenance.

### 29.4 Corrected disposition

- Keep A3, B1 and D4 incomplete; the latest exact R3 gate remains blocked.
- Treat §28's accusation of a current PR-description label drift as superseded by this correction; do not use it as an outstanding defect.
- Retain the R2 filename/internal-revision mismatch as a distinct provenance/naming finding. If corrected, do so only as a separate candidate change with an explicit predecessor/successor identity and exact-head tests; do not rewrite historical candidate evidence in place.
- No product semantics, owner disposition, normative Index, official Test Register, A9 authority, source code, runtime, A10, production, merge or SEAL state is altered by this correction.

