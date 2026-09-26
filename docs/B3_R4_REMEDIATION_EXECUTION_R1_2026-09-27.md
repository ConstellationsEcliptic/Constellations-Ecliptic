# CE B3 R4 REMEDIATION EXECUTION RECORD
## 2026-09-27

Status: DEVELOPMENT_CANDIDATE_ONLY

Parent checkpoint:
- B3 R3 branch: `development/b3-hardening/2026-09-27-r3`
- Parent commit: `1fb6c813ef121609e360103a211f0c98f0887b56`
- Parent source-tree identity: `d83a634d30266393078dab160532f524f99b6b6084fd6f535c6b8d1ac3aabd2e`

R4 scope:
1. total RuntimeIdentity type validation;
2. preserve CalculationRequest/BirthInput execution validation before authorization;
3. prove malformed nested requests cannot reach authorize_runtime;
4. exercise controlled authorized-path downstream boundary;
5. preserve regression suite and development-only governance.

Read-only reconciliation correction:
- R4 re-inspection found `CalculationEngine.calculate()` already calls `request.validate()` before profile mismatch and `authorize_runtime()`.
- Therefore the claimed R3-F2 "missing execution gate" is NOT reproducible at R3 HEAD and is reclassified as an existing invariant requiring stronger regression proof, not as a missing implementation.
- R4 adds an authorized-path negative test that fails the test if `authorize_runtime()` is reached for a malformed request.

Authority boundary:
- R4 is development-only.
- No signer, private key, authority transition, trusted-build transition, production runtime authorization, SEAL, or AUTHORIZATION is introduced.
- R2 and R3 remain immutable checkpoints.
- `804036f843a56d0029ceea08af35247d28cbde7e` and `main` remain untouched.

Governance remains:
- SOURCE_AUTHORITY = NOT_ESTABLISHED
- TRUSTED_BUILD = NOT_ESTABLISHED
- PRODUCTION_RUNTIME = NOT_AUTHORIZED
- SEAL = NO
- AUTHORIZATION = NON_AUTHORIZED
- FAIL_CLOSED = TRUE
