
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

The trusted-build logs nevertheless state FORMAL_TRUSTED_BUILD=NOT_ESTABLISHED, PRODUCTION_RUNTIME=NOT_AUTHORIZED, SEAL=NO, AUTHORIZATION=NON_AUTHORIZED and FAIL_CLOSED=TRUE. A successful candidate workflow does not grant source authority or production authorization.

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
- manifests/convergent_test_register_r3.json calls itself CURRENT_IMPLEMENTATION_CANDIDATE, but states authoritative coverage, Source Authority, Trusted Build, runtime adoption and full runtime coverage are NOT_ESTABLISHED.

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

Current 23-area snapshot: 13 CLOSED_PRESERVE; 6 OWNER_DECISION_RECORDED; 1 DEFERRED_BY_EXPLICIT_DISPOSITION; 1 OWNER_DISCUSSION_REQUIRED (A3); 2 RECOMMENDATION_READY (B1, D4). A3/B1/D4 remain open.

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
10. After official Test Register authority is established, build complete source-code-test crosswalk; only then proceed to separate Source Authority, Trusted Build, A10/runtime, release and SEAL gates.

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
4. The same claim-release function calls authorize_runtime(). At the exact A9 source reviewed, that function always appends source_authority_attestation_not_established and independent_runtime_identity_verification_not_established, returning NON_AUTHORIZED.
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
