# CE ZERO-POINT AREA D1 — ACCOUNT IDENTITY, TRUSTED DEVICES AND RECOVERY
Date: 2026-10-09
Classification: SOURCE RECONCILIATION / WORKING CANDIDATE / NON-AUTHORITATIVE
Status: SOURCE_RECONCILED
Authority effect: NONE
Normative amendment: NONE
Implementation authorization: NONE
Tests executed: NONE

## 1. Conclusion

Preserve the account and recovery model already defined in the characterized V1 specification. One account owns one Personal Sky, profile versions, retained paid readings and Credits entitlement. A device is only a security layer—not account ownership. Account access is pseudonymous, without a normative requirement for real name, email, phone or social-login identity. Actual deployed auth/recovery/trusted-device service is NOT ESTABLISHED by the inspected sources.

## 2. Current norm and owner direction

Product Constitution v1.6.1, §§7–9 (Box 2491704535193) and Account, Privacy & Commercial Specification v1.7, §§1–6 (Box 2485319995048) establish:
- Minimum registration fields: username, password, birth date, birth city and user-controlled recovery mechanism. No requirement for real name, email, phone, social login or marketing profile.
- One account = one Personal Sky. The account owns profile versions, retained paid readings and Credits entitlement; devices do not own or transfer the account.
- Recovery uses a 12-word user-controlled recovery phrase. The server does not store plaintext phrase; it stores KDF version, salt and verifier material. Argon2id or another pinned memory-hard KDF is the normative example/baseline described in the spec.
- Recovery uses a server-issued challenge, single-use nonce, operation binding and short server-authoritative TTL; no client clock may determine expiry; recovery phrases are deterministically normalized but normalized plaintext is not retained.
- A maximum of five active trusted devices is specified. WebAuthn/passkey with user verification is preferred. A local PIN is acceptable only as part of a validated authenticator/credential mechanism—not a second server-side password.
- Personal CE session eligibility separates age eligibility, account authentication and current user verification. V1 default idle re-authentication boundary is 30 minutes, adjustable only through controlled security/jurisdiction review.
- On total loss of trusted devices, the user-controlled recovery mechanism is the standard path. Successful recovery revokes previous sessions and device credentials before creating a new authenticated session and enrolling the replacement device. If the recovery mechanism is unavailable, there is no alternate V1 identity-proofing path; CE must not transfer ownership or grant a support/manual bypass.
- Migration/integrity problems may freeze sensitive access but cannot silently destroy valid entitlement, create sessions, bypass recovery, manually grant Credits/entitlement outside controlled reconciliation, expose Personal Sky, change ownership or rewrite historical provenance.

Privacy Architecture Minimal V1 v1.5 (Box 2485335589220) keeps the stored account class minimal: opaque account ID, pseudonymous username, password hash, account status and recovery verifier material; it excludes real-name/email/phone/contact/marketing identity and plaintext recovery secrets. The architecture is a normative data boundary, not evidence a live database has been deployed.

## 3. Test contracts present

Execution Profile & Test Register v1.5 (Box 2485336117840) specifies relevant tests including:
- SEC-01/03: consumed nonce replay is rejected without a second action/state mutation;
- SEC-02: expired challenge rejected;
- SEC-04: challenge bound to another operation rejected;
- SEC-05: client-clock manipulation has no expiry influence;
- SEC-06: recovery revokes all prior sessions/devices;
- SEC-07: idle session boundary requires re-authentication;
- SEC-08: rate limiting causes no side effect and no persistent behavior profile;
- SEC-09/10/11: trusted-device total loss, replacement without recovery, and revoked-device reuse;
- SEC-12: prior device age verification is not proof for a current user, so missing current user verification blocks access;
- PRIV-03: deleted-account session reuse rejected;
- PRIV-08 / VERS-02: birth-data correction creates a new profile version and does not silently rewrite historical reading.

These are requirements/expected oracles in the controlled register. No tests were executed by this review and the existence of test descriptions is not a fresh test pass.

## 4. Recommendation

**CLOSED / PRESERVE the account/trusted-device/recovery contract at the semantic level.** Do not add email as a required identity, device IDs as ownership primitive, a support-based recovery override, or a fallback recovery path based on inferred personal identity. Preserve separate age assurance and current-user verification, account-owned entitlements, and historical profile version binding.

Before using any auth/commerce service as the current CE implementation, identify its authorized repository/worktree and verify its actual source identity, persistence and test evidence. The inspected connected main root and A9 calculation/runtime tree do not establish that a complete account/auth/trusted-device service exists; that is a bounded implementation-source gap, not proof that no separate private/local code exists.

## 5. Status

- Normative account/recovery/device contract: PRESERVE.
- Actual deployed auth/recovery/trusted-device implementation: NOT ESTABLISHED in inspected connected scope.
- Approved support override / alternate recovery path: NOT PRESENT in V1 contract; do not invent.
- Code/schema/normative document/Test Register changed: NO.
- Tests executed by this review: NONE.
- A10/Runtime Adoption/production/deployment/SEAL: unaffected.

## 6. Evidence

- Product Constitution v1.6.1: https://app.box.com/file/2491704535193
- Account, Privacy & Commercial Specification v1.7: https://app.box.com/file/2485319995048
- Privacy Architecture Minimal V1 v1.5: https://app.box.com/file/2485335589220
- Execution Profile & Test Register v1.5: https://app.box.com/file/2485336117840
- Implementation Plan v1.3.1: https://app.box.com/file/2491699264134
- Source-First Recommendation Protocol: https://app.box.com/file/2515488894918

End of D1 review.