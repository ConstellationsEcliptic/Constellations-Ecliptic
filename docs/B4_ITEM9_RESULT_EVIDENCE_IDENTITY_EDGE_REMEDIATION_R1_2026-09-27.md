# B4 Item 9 — Result→EvidencePacket Identity Edge Remediation R1

Date: 2026-09-27

## Scope

This remediation closes the B4 Item 9 Result→EvidencePacket identity edge gap identified by the read-only assessment.

Parent identity:

- `ea6cbef145743a0d1f71cb549a3afc30370447c0`

Development branch:

- `development/b4-item9/2026-09-27-r1`

Protected boundaries:

- Approved candidate: `804036f843a56d0029ceea08af35247d28cbde7e`
- Main: `ded37b47cadcc9420619776aacce52b98f9ad3dc`

## Normative identity form selected

The Result→EvidencePacket edge uses a compound identity:

1. `evidence_packet_id`
2. `content_sha256`

The packet identifier provides the logical issuance identity. The canonical content SHA-256 binds that logical identity to the immutable packet representation.

ID alone is therefore insufficient, and content hash alone is not used as the logical identifier.

## Implementation

### EvidencePacketRef

A frozen `EvidencePacketRef` value object is defined in `src/ce/calculation/evidence.py`.

Its invariants are:

- non-empty `evidence_packet_id`;
- exactly 64 hexadecimal characters for `content_sha256`;
- reference construction is derived from a concrete `EvidencePacket`;
- `matches(packet)` requires both packet ID equality and current packet content hash equality;
- canonical dictionary form is exactly:
  `{\"evidence_packet_id\": ..., \"content_sha256\": ...}`.

### CalculationResult

`CalculationResult` no longer accepts an arbitrary public reference value.

For VALID issuance:

- a concrete `EvidencePacket` must be supplied through the controlled private/keyword-only issuance input;
- `evidence_packet_ref` is derived from that packet;
- the derived reference must match the concrete packet;
- the reference is serialized into canonical result bytes;
- absence of the packet is rejected.

For NON-VALID states:

- no EvidencePacket may be attached;
- `evidence_packet_ref` is null.

The canonical result serializer also materializes `ObjectState` values into their established JSON representation so a VALID result can be canonically issued and hashed.

### SignalResult

`SignalResult` follows the same binding rule:

- VALID requires a concrete EvidencePacket;
- `evidence_packet_ref` is derived, never caller-supplied;
- NON-VALID states require a null reference;
- swapped/stale packet instances are detected by the compound identity comparison.

### JSON Schema

Both:

- `schemas/calculation_result.schema.json`
- `schemas/signal_result.schema.json`

now define `evidence_packet_ref` as an object-or-null with strict fields:

- `evidence_packet_id`: non-empty string;
- `content_sha256`: 64 hexadecimal characters.

VALID branches require the compound object. NON-VALID branches require null.

## Adversarial coverage

The remediation tests cover:

- derivation from a concrete packet;
- malformed reference rejection;
- same packet ID with different content;
- reference matching against the wrong packet;
- stale/swapped packet detection;
- refusal of caller-supplied string references;
- VALID result canonical issuance;
- NON-VALID result null reference;
- equivalent SignalResult binding;
- schema acceptance/rejection for compound identity shape;
- issuance identity stability after external source mutation.

## Authority and fail-closed boundary

No authority transition was introduced.

The remediation remains development-only and preserves:

- `SOURCE_AUTHORITY = NOT_ESTABLISHED`
- `TRUSTED_BUILD = NOT_ESTABLISHED`
- `PRODUCTION_RUNTIME = NOT_AUTHORIZED`
- `SEAL = NO`
- `AUTHORIZATION = NON_AUTHORIZED`
- `FAIL_CLOSED = TRUE`

C3-2 remains PERFORMED / BLOCKED and C3-3 remains CLOSED.

## Verification evidence

Development CI run:

- Run: `36290953592`
- Job: `108540688504`

Verified:

- checkout identity: PASS;
- source-tree identity declaration: PASS;
- deterministic foundation verification: PASS;
- explicit source identity verification: PASS;
- build-input hygiene: PASS;
- test suite: **111 / 111 PASS**;
- final result: `FOUNDATION_PASS`;
- final source-tree identity measured by CI: `e416cdc0cead2f62ff488fe67c27bee24de439c0ddd8770214ea48b34022632f`.

CI evidence is development evidence only and does not establish Source Authority, Trusted Build, production authorization, signing, SEAL, or production readiness.
