# CE V1 — B4 Item 5 Remediation R1

Date: 2026-09-27

## Scope

This remediation addresses only the verified B4 Item 5 gap:

- \`CalculationResult.normalized_time\` Python validation accepted timestamp shapes that were more permissive than the established canonical UTC contract.
- Direct regression coverage for \`CalculationResult.normalized_time\` was incomplete.

## Lineage

Parent/current verified HEAD:

\`888d01fc7f02124a0db1b7b162a1ca84c2b5eb8f\`

Remediation branch:

\`development/b4-item5-remediation/2026-09-27-r1\`

This work creates a new development identity and does not modify the parent commit in place.

## Remediation

1. Added the established canonical UTC regex to the calculation-contract boundary.
2. Changed \`CalculationResult.normalized_time\` validation to require:
   - uppercase \`T\`;
   - seconds;
   - optional 1–6 fractional digits;
   - terminal \`Z\`;
   - no offset notation.
3. Preserved Python semantic calendar validation through \`datetime.fromisoformat\`.
4. Added direct \`CalculationResult\` regression coverage for:
   - canonical UTC acceptance;
   - six fractional digits acceptance;
   - space separator rejection;
   - lowercase \`t\` rejection;
   - missing seconds rejection;
   - more than six fractional digits rejection;
   - offset-based timestamp rejection;
   - invalid calendar date rejection.
5. No change was made to execution profile, provenance, EvidencePacket, timezone authority, ephemeris authority, C3 state, \`main\`, or approved candidate \`804036f...\`.

## Identity Transition

The final source-tree identity must be recomputed after this complete remediation set. The resulting commit is a B4 development identity and does not inherit the C3-1 disposition attached to \`804036f...\`.

## Verification Requirements

Acceptance requires:

- source-tree identity declared == actual;
- full deterministic test suite PASS;
- build-input hygiene PASS;
- foundation verifier PASS;
- fresh CI success;
- development-only/fail-closed governance invariants unchanged.

CI evidence remains development evidence only and must not be interpreted as Source Authority, Trusted Build, Production Runtime, SEAL, or Authorization.

## Disposition

Before final verification:

\`B4 ITEM 5 = REMEDIATION IN PROGRESS\`

After fresh successful verification, the intended disposition is:

\`B4 ITEM 5 = REMEDIATED / VERIFIED / DEVELOPMENT-ONLY / FAIL-CLOSED\`
