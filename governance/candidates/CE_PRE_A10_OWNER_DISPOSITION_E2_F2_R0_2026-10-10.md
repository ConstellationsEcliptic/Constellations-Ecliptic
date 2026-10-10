# CE PRE-A10 — BOUNDED OWNER DISPOSITION FOR E2 AND F2

**Date:** 2026-10-10  
**Classification:** WORKING CANDIDATE / NON-AUTHORITATIVE  
**Decision origin:** Explicit owner approval in the CE working conversation, recorded in [Owner Decision R0](CE_OWNER_DECISION_AUTONOMOUS_EVOLUTION_AND_CHANGE_CONTROL_R0_2026-10-10.md)  
**Authority / normative / runtime / production effect:** NONE

## Purpose

This record applies the owner's approved direction to the two review areas for which the approval is sufficiently specific. It closes the review disposition only; it does not represent that implementation work, technical qualification, or runtime authorization is complete.

## E2 — Autonomous operating mandate and delegated authority

**Disposition:** OWNER_DECISION_RECORDED — APPROVE THE DIRECTION, NOT FORMAL ADOPTION.

The owner approved a source-first completeness review, broader autonomous work for research, diagnostics, isolated candidate engineering, test development/execution, evidence generation and routine follow-through, evaluation of a persistent least-privilege execution capability, and adaptive revision when new evidence or cases emerge. If a novel case would materially change a principle or protected boundary, it must be discussed with the owner before being treated as approved.

Scope exclusions remain explicit:
- This is not formal adoption or normative promotion of the candidate operating mandate.
- A continuously running agent, persistent runner, least-privilege credential model, complete CI enforcement, independent verifier, automatic promotion, and rollback capability must each be implemented and evidenced before being claimed as available.
- No authority to change core product principles, Canon, data purposes, owner-held trust roots, Runtime Adoption, production authorization, required dual approval, merge/release restrictions or SEAL is implied.
- No A10 implementation is authorized by this disposition.

The review area is therefore marked OWNER_DECISION_RECORDED for this bounded decision. Actual implementation and qualification continue as separate work items.

## F2 — Birth-time input, Gregorian policy and pinned timezone-data release

**Disposition:** OWNER_DECISION_RECORDED — APPROVE PRE-LAUNCH EVALUATION OF IANA 2026e; DO NOT TREAT AS ADOPTION.

The owner approved the recommendation that relevant upstream updates be evaluated before CE launch rather than deferred merely because the current baseline is already established. IANA 2026e is a target for immediate candidate qualification.

Preserve all current 2026d profiles, bundles and historical capture identities until the update is qualified. Candidate qualification still requires the authentic official release/archive to be obtained and verified; a reproducible 2026d-versus-2026e build with the same toolchain; complete comparison of all 597 bundled zone entries, aliases, file hashes and relevant transition behavior; precise fixtures for the Manitoba and Ireland changes; downstream CE regression testing; and independent review of the results. A new versioned candidate profile and a separate Runtime Adoption disposition remain required.

This decision does not approve in-place replacement of 2026d or use of 2026e in a runtime or production environment. At this record's creation, the release archives had not been acquired and the complete compiled-bundle comparison and downstream qualification had not been performed; 2026e remains NOT_ADOPTED.

The area is marked OWNER_DECISION_RECORDED because the policy and next action are decided—not because technical qualification is complete. The remaining qualification tasks must be tracked and reported honestly.

## Evidence and authority boundary

- [Owner Decision R0](CE_OWNER_DECISION_AUTONOMOUS_EVOLUTION_AND_CHANGE_CONTROL_R0_2026-10-10.md)
- [Current 23-area register](CE_PRE_A10_AREA_REGISTER_R0_2026-10-09.json)
- [TZDB 2026d→2026e impact qualification R0](CE_PRE_A10_TZDB_2026D_TO_2026E_IMPACT_QUALIFICATION_R0_2026-10-10.md)
- [TZDB upstream source-tag delta reconciliation R1](CE_PRE_A10_TZDB_SOURCE_TAG_DELTA_RECONCILIATION_R1_2026-10-10.md)
- [Packet R8](CE_ZERO_POINT_OWNER_DECISION_PACKET_R8_2026-10-10.md)

All linked artifacts are working candidate records and do not amend normative authority. The pre-A10 gate remains separate from runtime adoption, production, deployment and SEAL. No source-normative artifact or implementation code is changed by this disposition.

---
End of bounded owner disposition.
