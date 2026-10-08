# CE V1 Source Foundation R1

## Status

`DEVELOPMENT_CANDIDATE`

This source tree is the first concrete CE V1 implementation foundation. It is intentionally not production-authoritative.

## Normative basis

The foundation follows the current CE Calculation Constitution, Technical Contracts, Canonical Execution Profile, Signal Engine boundary, and evidence/AI validation constraints already established in the CE normative document stack.

## Implementation boundary

The calculation layer owns numerical/geometric state. Signal qualification remains a downstream boundary. Interpretation is not implemented here.

## Fail-closed rule

No authoritative astronomical result may be produced until all mandatory source/runtime identities are established. The current foundation therefore refuses authoritative calculation because the native Swiss Ephemeris binding, runtime TZif identity, source authority and trusted build are not established.

## First implemented contracts

1. Calculation request/input contract.
2. Calculation result/status contract.
3. Evidence Packet deterministic serialization/hash.
4. Runtime identity gate.
5. Canonical angle normalization/separation/deviation.
6. Explicit zero-birth-time state.
7. Single fail-closed ephemeris adapter boundary.
8. Deterministic standard-library test runner.

## Deliberately absent

The foundation does not invent:

- object registry values;
- aspect orb values;
- event times;
- planetary positions;
- timezone-derived runtime data;
- native library identity;
- production signer identity.
