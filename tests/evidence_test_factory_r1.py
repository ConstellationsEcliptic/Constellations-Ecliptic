from __future__ import annotations

from typing import Any

from ce.calculation.evidence import EvidencePacket
from ce.foundation.hashing import sha256_bytes


def build_test_bound_evidence_packet(**kwargs: Any) -> EvidencePacket:
    """Create deterministic bound synthetic evidence for tests only."""

    runtime_digest = kwargs.pop("runtime_identity_sha256", None)
    provenance_root = kwargs.pop("provenance_root_sha256", None)

    if runtime_digest is None:
        raise AssertionError("test fixture runtime identity missing")

    if provenance_root is None:
        raise AssertionError("test fixture provenance root missing")

    kwargs.setdefault("scenario_window_state", "NONE")
    kwargs.setdefault("possible_window_segments", ())
    kwargs.setdefault("robust_window_segments", ())
    kwargs.setdefault("scenario_observations", ())
    kwargs.setdefault("evidence_packet_id", "TEST-UNISSUED")

    packet = EvidencePacket(**kwargs)

    object.__setattr__(packet, "runtime_identity_sha256", runtime_digest)
    object.__setattr__(packet, "provenance_root_sha256", provenance_root)

    canonical_bytes = packet._expected_canonical_bytes()

    object.__setattr__(
        packet,
        "evidence_packet_id",
        sha256_bytes(canonical_bytes),
    )
    object.__setattr__(
        packet,
        "_canonical_bytes",
        canonical_bytes,
    )

    errors = packet.validate(require_issued=True)
    if errors:
        raise AssertionError(
            "test fixture produced invalid packet: " + ";".join(errors)
        )

    return packet
