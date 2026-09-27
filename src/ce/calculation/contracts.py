from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field, fields
from datetime import date, datetime, time, timezone
import math
import re
from typing import Any

from ce.calculation.evidence import EvidencePacket, EvidencePacketRef
from ce.foundation.hashing import sha256_bytes
from ce.foundation.identity import CANONICAL_EXECUTION_PROFILE_ID, RuntimeIdentity
from ce.foundation.serialization import canonical_json
from ce.foundation.status import BirthTimeState, CalculationStatus, ScenarioState


_TZ_VERSION_RE = re.compile(r"^\d{4}[a-z]$")
_COMMIT_RE = re.compile(r"^[0-9a-fA-F]{40}$")
_SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")
_RUNTIME_IMAGE_RE = re.compile(r"^sha256:[0-9a-fA-F]{64}$")
_UTC_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?Z$")


def _nonempty_string(value: Any, field_name: str) -> str | None:
    if not isinstance(value, str) or not value.strip():
        return f"invalid:{field_name}"
    return None


def _utc_instant(value: Any, field_name: str) -> tuple[datetime | None, str | None]:
    if not isinstance(value, str) or not _UTC_RE.fullmatch(value):
        return None, f"invalid:{field_name}:utc_canonical_z_required"
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError:
        return None, f"invalid:{field_name}:utc_iso8601_invalid"
    if parsed.tzinfo is None or parsed.utcoffset() != timezone.utc.utcoffset(parsed):
        return None, f"invalid:{field_name}:utc_timezone_invalid"
    return parsed, None


def _is_finite_number(value: Any) -> bool:
    if type(value) is int:
        return True
    return type(value) is float and math.isfinite(value)


def _freeze(value: Any) -> Any:
    from types import MappingProxyType

    if isinstance(value, dict):
        frozen = {key: _freeze(item) for key, item in value.items()}
        return MappingProxyType(frozen)
    if isinstance(value, MappingProxyType):
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(_freeze(item) for item in value)
    if isinstance(value, tuple):
        return tuple(_freeze(item) for item in value)
    return value


@dataclass(frozen=True)
class BirthInput:
    birth_date: date
    birth_time: time | None
    birth_time_state: BirthTimeState
    birth_city: str
    timezone_id: str
    timezone_version: str | None

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []

        if type(self.birth_date) is not date:
            errors.append("invalid:birth_date")
        if not isinstance(self.birth_time_state, BirthTimeState):
            errors.append("invalid:birth_time_state")
        elif self.birth_time_state is BirthTimeState.EXACT and self.birth_time is None:
            errors.append("inconsistent:birth_time_exact_requires_value")
        elif self.birth_time_state is BirthTimeState.ZERO_BIRTH_TIME and self.birth_time is not None:
            errors.append("inconsistent:zero_birth_time_requires_none")

        for value, name in (
            (self.birth_city, "birth_city"),
            (self.timezone_id, "timezone_id"),
        ):
            error = _nonempty_string(value, name)
            if error:
                errors.append(error)

        if self.timezone_version is not None:
            if not isinstance(self.timezone_version, str) or not _TZ_VERSION_RE.fullmatch(
                self.timezone_version
            ):
                errors.append("invalid:timezone_version")

        if self.birth_time is not None and type(self.birth_time) is not time:
            errors.append("invalid:birth_time")

        return tuple(errors)

    def __post_init__(self) -> None:
        errors = self.validate()
        if errors:
            raise ValueError(";".join(errors))


@dataclass(frozen=True)
class CalculationRequest:
    request_id: str
    birth: BirthInput
    target_interval_start_utc: str
    target_interval_end_utc: str
    execution_profile_id: str

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []

        error = _nonempty_string(self.request_id, "request_id")
        if error:
            errors.append(error)

        if not isinstance(self.birth, BirthInput):
            errors.append("invalid:birth")
        else:
            errors.extend(self.birth.validate())

        start, start_error = _utc_instant(
            self.target_interval_start_utc, "target_interval_start_utc"
        )
        end, end_error = _utc_instant(
            self.target_interval_end_utc, "target_interval_end_utc"
        )
        if start_error:
            errors.append(start_error)
        if end_error:
            errors.append(end_error)
        if start is not None and end is not None and end <= start:
            errors.append("invalid:target_interval_order")

        error = _nonempty_string(self.execution_profile_id, "execution_profile_id")
        if error:
            errors.append(error)

        return tuple(errors)

    def __post_init__(self) -> None:
        errors = self.validate()
        if errors:
            raise ValueError(";".join(errors))


@dataclass(frozen=True)
class ObjectState:
    object_id: str
    longitude_deg: float | None
    speed_deg_per_day: float | None
    status: CalculationStatus

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []
        error = _nonempty_string(self.object_id, "object_id")
        if error:
            errors.append(error)
        if not isinstance(self.status, CalculationStatus):
            errors.append("invalid:object_state_status")
            return tuple(errors)

        if self.status is CalculationStatus.VALID:
            if self.longitude_deg is None or not _is_finite_number(self.longitude_deg):
                errors.append("valid_object_requires_finite_longitude")
            elif not 0.0 <= float(self.longitude_deg) < 360.0:
                errors.append("valid_object_requires_normalized_longitude")

            if self.speed_deg_per_day is not None and not _is_finite_number(self.speed_deg_per_day):
                errors.append("valid_object_speed_must_be_finite")
        else:
            if self.longitude_deg is not None and not _is_finite_number(self.longitude_deg):
                errors.append("nonvalid_object_longitude_must_be_finite_or_none")
            if self.speed_deg_per_day is not None and not _is_finite_number(self.speed_deg_per_day):
                errors.append("nonvalid_object_speed_must_be_finite_or_none")

        return tuple(errors)

    def __post_init__(self) -> None:
        errors = self.validate()
        if errors:
            raise ValueError(";".join(errors))


_PROVENANCE_IDENTITY_FIELDS = (
    "source_commit",
    "source_tree_sha256_v2",
    "dependency_lock_digest",
    "timezone_bundle_digest",
    "ephemeris_bundle_digest",
    "runtime_image_digest",
)

_REQUIRED_RESULT_PROVENANCE = _PROVENANCE_IDENTITY_FIELDS + ("calculation_version",)


def _is_provenance_scalar(value: Any) -> bool:
    if value is None or isinstance(value, (str, bool)):
        return True
    if type(value) is int:
        return True
    return type(value) is float and math.isfinite(value)


def _validate_provenance_scalar_domain(provenance: Mapping[str, Any]) -> tuple[str, ...]:
    return tuple(
        f"provenance:extra:{name}:scalar_required"
        for name, value in provenance.items()
        if name not in _REQUIRED_RESULT_PROVENANCE and not _is_provenance_scalar(value)
    )


def _validate_result_provenance(
    provenance: Any, runtime_identity: RuntimeIdentity | None
) -> tuple[str, ...]:
    if not isinstance(provenance, Mapping):
        return ("provenance:invalid",)

    errors: list[str] = list(_validate_provenance_scalar_domain(provenance))

    shaped_fields = {
        "source_commit": (provenance.get("source_commit"), _COMMIT_RE, "40-hex"),
        "source_tree_sha256_v2": (
            provenance.get("source_tree_sha256_v2"),
            _SHA256_RE,
            "64-hex",
        ),
        "dependency_lock_digest": (
            provenance.get("dependency_lock_digest"),
            _SHA256_RE,
            "64-hex",
        ),
        "timezone_bundle_digest": (
            provenance.get("timezone_bundle_digest"),
            _SHA256_RE,
            "64-hex",
        ),
        "ephemeris_bundle_digest": (
            provenance.get("ephemeris_bundle_digest"),
            _SHA256_RE,
            "64-hex",
        ),
    }
    for name, (value, pattern, description) in shaped_fields.items():
        if not isinstance(value, str) or not pattern.fullmatch(value):
            errors.append(f"provenance:malformed:{name}:{description}")

    runtime_image_digest = provenance.get("runtime_image_digest")
    if not isinstance(runtime_image_digest, str) or not _RUNTIME_IMAGE_RE.fullmatch(
        runtime_image_digest
    ):
        errors.append("provenance:malformed:runtime_image_digest:sha256-prefixed")

    calculation_version = provenance.get("calculation_version")
    if not isinstance(calculation_version, str) or not calculation_version.strip():
        errors.append("provenance:invalid:calculation_version")

    if runtime_identity is None:
        errors.append("provenance:binding_required")
        return tuple(errors)

    for identity_error in runtime_identity.validate_shape():
        errors.append(f"provenance:runtime_identity:{identity_error}")

    for name in _PROVENANCE_IDENTITY_FIELDS:
        identity_value = getattr(runtime_identity, name)
        if identity_value is None:
            errors.append(f"provenance:missing_runtime_identity:{name}")
        elif provenance.get(name) != identity_value:
            errors.append(f"provenance:mismatch:{name}")

    if provenance.get("execution_profile_id") is not None:
        errors.append("provenance:execution_profile_id_must_not_be_nested")

    return tuple(errors)


def _validate_nonvalid_result_provenance(provenance: Any) -> tuple[str, ...]:
    if not isinstance(provenance, Mapping):
        return ("provenance:invalid",)

    errors: list[str] = list(_validate_provenance_scalar_domain(provenance))
    for name in _REQUIRED_RESULT_PROVENANCE:
        if name in provenance:
            errors.append(f"provenance:nonvalid_forbidden:{name}")

    runtime_authority = provenance.get("runtime_authority")
    if runtime_authority is not None and runtime_authority != "NON_AUTHORIZED":
        errors.append("provenance:nonvalid_runtime_authority_must_be_non_authorized")

    return tuple(errors)


@dataclass(frozen=True)
class CalculationResult:
    request_id: str
    status: CalculationStatus
    execution_profile_id: str
    scenario_state: ScenarioState
    normalized_time: str | None
    object_states: tuple[ObjectState, ...] = field(default_factory=tuple)
    warnings: tuple[str, ...] = field(default_factory=tuple)
    errors: tuple[str, ...] = field(default_factory=tuple)
    provenance: dict[str, Any] = field(default_factory=dict)
    evidence_packet_ref: EvidencePacketRef | None = field(
        default=None, init=False, repr=False, compare=False
    )
    _runtime_identity: RuntimeIdentity | None = field(
        default=None, repr=False, compare=False, kw_only=True
    )
    _evidence_packet: EvidencePacket | None = field(
        default=None, repr=False, compare=False, kw_only=True
    )
    _canonical_bytes: bytes = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        if not isinstance(self.status, CalculationStatus):
            raise ValueError("invalid:calculation_result_status")
        if not isinstance(self.scenario_state, ScenarioState):
            raise ValueError("invalid:scenario_state")

        if self._evidence_packet is not None and not isinstance(self._evidence_packet, EvidencePacket):
            raise ValueError("invalid:evidence_packet")

        evidence_packet_ref = (
            EvidencePacketRef.from_packet(self._evidence_packet)
            if self._evidence_packet is not None
            else None
        )
        object.__setattr__(self, "evidence_packet_ref", evidence_packet_ref)

        for item in fields(self):
            if item.name in {"_runtime_identity", "_evidence_packet", "_canonical_bytes", "evidence_packet_ref"}:
                continue
            object.__setattr__(self, item.name, _freeze(getattr(self, item.name)))

        errors = self.validate()
        if errors:
            raise ValueError(";".join(errors))

        payload = {
            item.name: getattr(self, item.name)
            for item in fields(self)
            if item.name not in {"_runtime_identity", "_evidence_packet", "_canonical_bytes", "evidence_packet_ref"}
        }
        payload["object_states"] = [
            {
                "object_id": state.object_id,
                "longitude_deg": state.longitude_deg,
                "speed_deg_per_day": state.speed_deg_per_day,
                "status": state.status.value,
            }
            for state in self.object_states
        ]
        payload["evidence_packet_ref"] = (
            self.evidence_packet_ref.as_dict()
            if self.evidence_packet_ref is not None
            else None
        )
        object.__setattr__(self, "_canonical_bytes", canonical_json(payload))

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []

        error = _nonempty_string(self.request_id, "request_id")
        if error:
            errors.append(error)

        if self.execution_profile_id != CANONICAL_EXECUTION_PROFILE_ID:
            errors.append("invalid:execution_profile_id:canonical_required")

        if self.normalized_time is not None:
            _, normalized_error = _utc_instant(self.normalized_time, "normalized_time")
            if normalized_error:
                errors.append(normalized_error)

        for index, state in enumerate(self.object_states):
            if not isinstance(state, ObjectState):
                errors.append(f"invalid:object_states[{index}]")
                continue
            errors.extend(f"object_states[{index}]:{e}" for e in state.validate())

        if self._evidence_packet is not None:
            packet_errors = self._evidence_packet.validate()
            errors.extend(f"evidence_packet:{e}" for e in packet_errors)
            if self.evidence_packet_ref is None:
                errors.append("evidence_packet:reference_missing")
            elif not self.evidence_packet_ref.matches(self._evidence_packet):
                errors.append("evidence_packet:reference_mismatch")

        if self.status is CalculationStatus.VALID:
            if not self.object_states:
                errors.append("valid_result_requires_object_states")
            if any(state.status is not CalculationStatus.VALID for state in self.object_states):
                errors.append("valid_result_requires_all_objects_valid")
            if self.normalized_time is None:
                errors.append("valid_result_requires_normalized_time")
            if self.errors:
                errors.append("valid_result_cannot_have_errors")
            if self.scenario_state is ScenarioState.NONE:
                errors.append("valid_result_requires_scenario_state")
            if self._runtime_identity is None:
                errors.append("provenance:binding_required")
            elif self.execution_profile_id != self._runtime_identity.execution_profile_id:
                errors.append("provenance:execution_profile_mismatch")
            if self._evidence_packet is None:
                errors.append("evidence_packet:binding_required")
            elif self.evidence_packet_ref is None:
                errors.append("evidence_packet:reference_required")
            provenance_errors = _validate_result_provenance(
                self.provenance, self._runtime_identity
            )
            errors.extend(provenance_errors)
        else:
            if self._evidence_packet is not None or self.evidence_packet_ref is not None:
                errors.append("nonvalid_result_evidence_packet_requires_null")
            errors.extend(_validate_nonvalid_result_provenance(self.provenance))
            if any(
                isinstance(state, ObjectState) and state.status is CalculationStatus.VALID
                for state in self.object_states
            ):
                errors.append("nonvalid_result_cannot_contain_valid_object_state")

        return tuple(errors)

    def canonical_bytes(self) -> bytes:
        return self._canonical_bytes

    def content_sha256(self) -> str:
        return sha256_bytes(self._canonical_bytes)
