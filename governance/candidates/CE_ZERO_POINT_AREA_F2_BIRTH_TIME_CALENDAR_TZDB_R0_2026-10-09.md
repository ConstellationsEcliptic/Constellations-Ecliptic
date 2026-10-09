# CE ZERO-POINT AREA F2 — BIRTH-TIME INPUT, CALENDAR AND TIMEZONE RELEASE POLICY
Date: 2026-10-09
Classification: SOURCE RECONCILIATION / RECOMMENDATION / WORKING CANDIDATE / NON-AUTHORITATIVE
Status: RECOMMENDATION_READY
Authority effect: NONE
Normative amendment: NONE
Execution Profile / data-lock update: NONE
Runtime / production / SEAL effect: NONE

## 1. Owner policy already settled — do not reopen

The current product/input policy is that CE V1 does not use a user birth-time input. The supported calendar policy is Gregorian-only. Do not ask the owner to restate either decision.

Birth-Time Input Policy Correction R4 (Box 2491386800755) explicitly corrects earlier phrasing: birth time is NOT USED, not merely optional/not required. The user is not to be asked to provide, estimate, select or confirm a birth time for normal V1 Personal Sky. Historical Calendar Policy Decision R3 (Box 2491385407120) and Product Constitution v1.6.1 §15 set Gregorian-only; unsupported Julian/jurisdiction-specific historical calendar treatment must fail closed. These records do not authorize a silent change in either policy.

## 2. Separate product input from calculation representation

Product Constitution v1.6.1 §15 (Box 2491704535193) states:
- Birth Date = USED.
- Birth City / Canonical Birth Location = USED.
- Birth Time = NOT USED.
- Calendar = GREGORIAN ONLY.

The Calculation Constitution v1.9 §§13–14 and 26 (Box 2485336984594), together with Execution Profile v1.3/revision 4 §§2.2 and 6–7 (Box 2491702000320), retain an internal `ZERO_BIRTH_TIME_INTERVAL` representation: local midnight to the next local midnight, resolved through the approved IANA timezone rules. Internal derived scenario instants are calculation machinery; they are not user-supplied birth times and must not be exposed as such. Noon/midnight/arbitrary-hour substitution is forbidden.

This is not a contradiction when described precisely: CE does not collect or use a birth-time value from the user, while the numerical engine models uncertainty across the full birth-date interval. The UI must not suggest that the user's birth time was known or that a midpoint hour provides more precision.

## 3. Pinned timezone policy and current external fact

The characterized Calculation Constitution §4 and Execution Profile v1.3/revision 4 pin the TZDB baseline to IANA 2026d. The Execution Profile §6.3 says future TZDB changes must not replace the canonical data in place; a potentially result-affecting TZDB update requires a new Execution Profile revision and controlled qualification.

Fresh official IANA source check on 2026-10-09: **IANA 2026e was released 2026-09-29 and is the current latest release**, after CE's pinned 2026d. Its release notes include Manitoba moving to permanent UTC−05 effective 2026-10-31 (modeled as a transition on 2026-11-01 at 02:00 for compatibility reasons) and correction of Ireland's 1925 fall-back date from 10-04 to 09-20. Sources: IANA Release 2026e https://www.iana.org/time-zones/releases/2026e and official release list https://www.iana.org/time-zones/releases. citeturn474588search0turn474588search1

That release is a verified external update, not an authorization for CE to upgrade in place. CE must continue to identify exactly which TZIF bytes and historical runtime are actually bound to A9, whether affected fixtures/locations/dates are in the supported coverage contract, and how a new profile/digest would be qualified. The A9 full-range capture/parity is bound to A9's exact runtime identity; it must not be relabeled 2026e evidence unless its actual bundle identity says so.

## 4. Recommendation

**Preserve current V1 input semantics and pin integrity; begin a separate read-only qualification assessment of IANA 2026e, but do not change the production/canonical pin automatically.**

Required assessment work:
1. Verify exact current TZIF bundle and its SHA-256 in the active A9 candidate/runtime evidence; do not infer it from the label alone.
2. Compare the pinned 2026d bundle with an explicitly staged 2026e candidate bundle and identify byte-level/data differences and affected CE-supported locations and dates, including Manitoba and Ireland examples where relevant.
3. Review whether 2026e affects historical birth-location resolution, interval UTC endpoints, transit/observation instants, full-range output, or only cases outside V1's supported calendar/coverage scope.
4. Add deterministic regression fixtures for changed rules, adjacent dates, ambiguity/nonexistent-time handling, historical conversion, supported geographic aliases and cross-platform consistency.
5. Use a new candidate/profile revision and new immutable data/identity digests for any approved upgrade; do not mutate A9, its captures, or profile revision 4 in place.
6. Require independent full relevant-range/fixture verification and the governance/authority process applicable to the new identity before any promotion/runtime use.

Trade-off: staying pinned preserves reproducibility of existing evidence but can lag current civil-time rule changes; upgrading may correct supported local-time computations but requires a new identity and full regression/authority work. The safe recommendation is not to ignore 2026e, but to qualify it separately rather than silently upgrading.

## 5. Status and non-actions

- Birth time product input = NOT USED: OWNER-DECIDED / PRESERVE.
- Calendar = Gregorian-only: OWNER-DECIDED / PRESERVE.
- Internal zero-birth interval model: PRESERVE as engine representation; not exposed as a known user-supplied birth time.
- Current characterized TZDB pin = IANA 2026d.
- Latest external IANA release = 2026e (2026-09-29); verified by official IANA source.
- CE adoption of 2026e: NOT APPROVED / NOT PERFORMED.
- A9 runtime, profile, data bundle, captures, source and authority state changed: NO.
- No tests or comparison of actual pinned 2026d vs proposed 2026e bytes were performed in this review.
- Runtime Adoption/production/deployment/SEAL: unaffected.

## 6. Evidence

- Birth-Time Input Policy Correction R4: https://app.box.com/file/2491386800755
- Historical Calendar Policy Decision R3: https://app.box.com/file/2491385407120
- Product Constitution v1.6.1: https://app.box.com/file/2491704535193
- Calculation Constitution v1.9: https://app.box.com/file/2485336984594
- Canonical Execution Profile v1.3/rev4: https://app.box.com/file/2491702000320
- A9 runtime/build reconciliation R2: https://app.box.com/file/2514341553097
- IANA Release 2026e: https://www.iana.org/time-zones/releases/2026e

End of F2 review.