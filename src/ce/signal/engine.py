from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import Any

from ce.calculation.evidence import EvidencePacket, EvidencePacketRef
from ce.foundation.hashing import sha256_bytes
from ce.foundation.serialization import canonical_json
from ce.foundation.status import CalculationStatus


def _freeze(value: Any) -> Any:
    from types import MappingProxyType

    if isinstance(value, dict):
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(_freeze(item) for item in value)
    if isinstance(value, tuple):
        return tuple(_freeze(item) for item in value)
    return value


@dataclass(frozen=True)
class SignalResult:
    status: CalculationStatus
    classification: str | None
    phase: str | None
    uncertainty_state: str | None
    evidence_packet: EvidencePacket | None
    canon_input_valid: bool
    provenance: dict[str, Any] = field(default_factory=dict)
    evidence_packet_ref: EvidencePacketRef | None = field(
        default=None, init=False, repr=False, compare=False
    )
    _canonical_bytes: bytes = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        if not isinstance(self.status, CalculationStatus):
            raise ValueError("invalid:signal_status")
        if not isinstance(self.canon_input_valid, bool):
            raise ValueError("invalid:canon_input_valid")
        if self.evidence_packet is not None and not isinstance(self.evidence_packet, EvidencePacket):
            raise ValueError("invalid:evidence_packet")

        evidence_packet_ref = (
            EvidencePacketRef.from_packet(self.evidence_packet)
            if self.evidence_packet is not None
            else None
        )
        object.__setattr__(self, "evidence_packet_ref", evidence_packet_ref)

        object.__setattr__(self, "provenance", _freeze(self.provenance))
        errors = self.validate()
        if errors:
            raise ValueError(";".join(errors))

        payload = {
            item.name: getattr(self, item.name)
            for item in fields(self)
            if item.name not in {"evidence_packet", "evidence_packet_ref", "_canonical_bytes"}
        }
        payload["evidence_packet_ref"] = (
            self.evidence_packet_ref.as_dict()
            if self.evidence_packet_ref is not None
            else None
        )
        object.__setattr__(self, "_canonical_bytes", canonical_json(payload))

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []

        if self.evidence_packet is not None:
            packet_errors = self.evidence_packet.validate()
            errors.extend(f"evidence_packet:{e}" for e in packet_errors)
            if self.evidence_packet_ref is None:
                errors.append("evidence_packet:reference_missing")
            elif not self.evidence_packet_ref.matches(self.evidence_packet):
                errors.append("evidence_packet:reference_mismatch")

        if self.status is CalculationStatus.VALID:
            for value, name in (
                (self.classification, "classification"),
                (self.phase, "phase"),
                (self.uncertainty_state, "uncertainty_state"),
                (self.evidence_packet_ref, "evidence_packet_ref"),
            ):
                if not isinstance(value, str) or not value:
                    errors.append(f"valid_signal_requires:{name}")
            if not self.canon_input_valid:
                errors.append("valid_signal_requires_canon_input_valid")
            if self.evidence_packet is None:
                errors.append("valid_signal_requires_evidence_packet")
            elif self.evidence_packet_ref is None:
                errors.append("valid_signal_requires_evidence_packet_ref")
        else:
            for value, name in (
                (self.classification, "classification"),
                (self.phase, "phase"),
                (self.uncertainty_state, "uncertainty_state"),
                (self.evidence_packet_ref, "evidence_packet_ref"),
            ):
                if value is not None:
                    errors.append(f"nonvalid_signal_requires_null:{name}")
            if self.canon_input_valid:
                errors.append("nonvalid_signal_requires_canon_input_false")
            if self.evidence_packet is not None or self.evidence_packet_ref is not None:
                errors.append("nonvalid_signal_requires_null_evidence_packet")
        return tuple(errors)

    def canonical_bytes(self) -> bytes:
        return self._canonical_bytes

    def content_sha256(self) -> str:
        return sha256_bytes(self._canonical_bytes)


class SignalEngine:
    """Fail-closed foundation boundary; qualification rules are not yet materialized."""

    def evaluate(self, calculation_result: object) -> SignalResult:
        return SignalResult(
            status=CalculationStatus.NOT_IMPLEMENTED,
            classification=None,
            phase=None,
            uncertainty_state=None,
            evidence_packet=None,
            canon_input_valid=False,
        )
