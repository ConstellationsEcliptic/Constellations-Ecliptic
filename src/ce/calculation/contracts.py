from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field, fields
from datetime import date, datetime, time, timezone
import math
import re
from typing import Any

from ce.foundation.hashing import sha256_bytes
from ce.foundation.identity import CANONICAL_EXECUTION_PROFILE_ID
from ce.foundation.serialization import canonical_json
from ce.foundation.status import BirthTimeState, CalculationStatus, ScenarioState


_TZ_VERSION_RE = re.compile(r"^\d{4}[a-z]$")
_COMMIT_RE = re.compile(r"^[0-9a-fA-F]{40}$")
_SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")
_RUNTIME_IMAGE_RE = re.compile(r"^sha256:[0-9a-fA-F]{64}$")


def _nonempty_string(value: Any, field_name: str) -> str | None:
    if not isinstance(value, str) or not value.strip():
        return f"invalid:{field_name}"
    return None


def _utc_instant(value: Any, field_name: str) -> tuple[datetime | None, str | None]:
    if not isinstance(value, str) or not value.endswith("Z"):
        return None, f"invalid:{field_name}:utc_z_required"
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError:
        return None, f"invalid:{field_name}:iso8601"
    if parsed.tzinfo is None or parsed.utcoffset() != timezone.utc.utcoffset(parsed):
        return None, f"invalid:{field_name}:utc_required"
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
        if self.status is CalculationStatus.VALID and errors:
            raise ValueError(";".join(errors))


_REQUIRED_RESULT_PROVENANCE = (
    "source_commit",
    "source_tree_sha256_v2",
    "dependency_lock_digest",
    "timezone_bundle_digest",
    "ephemeris_bundle_digest",
    "runtime_image_digest",
    "calculation_version",
)


def _validate_result_provenance(provenance: Any) -> tuple[str, ...]:
    errors: list[str] = []
    if not isinstance(provenance, Mapping):
        return ("invalid:provenance",)

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
            errors.append(f"malformed:provenance:{name}:{description}")

    runtime_image_digest = provenance.get("runtime_image_digest")
    if not isinstance(runtime_image_digest, str) or not _RUNTIME_IMAGE_RE.fullmatch(
        runtime_image_digest
    ):
        errors.append("malformed:provenance:runtime_image_digest:sha256-prefixed")

    calculation_version = provenance.get("calculation_version")
    if not isinstance(calculation_version, str) or not calculation_version.strip():
        errors.append("invalid:provenance:calculation_version")

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
    _canonical_bytes: bytes = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        if not isinstance(self.status, CalculationStatus):
            raise ValueError("invalid:calculation_result_status")
        if not isinstance(self.scenario_state, ScenarioState):
            raise ValueError("invalid:scenario_state")

        for item in fields(self):
            if item.name == "_canonical_bytes":
                continue
            object.__setattr__(self, item.name, _freeze(getattr(self, item.name)))

        errors = self.validate()
        if self.status is CalculationStatus.VALID and errors:
            raise ValueError(";".join(errors))

        payload = {
            item.name: getattr(self, item.name)
            for item in fields(self)
            if item.name != "_canonical_bytes"
        }
        object.__setattr__(self, "_canonical_bytes", canonical_json(payload))

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []

        error = _nonempty_string(self.request_id, "request_id")
        if error:
            errors.append(error)

        error = _nonempty_string(self.execution_profile_id, "execution_profile_id")
        if error:
            errors.append(error)

        if self.normalized_time is not None:
            _, normalized_error = _utc_instant(self.normalized_time, "normalized_time")
            if normalized_error:
                errors.append(normalized_error)

        for index, state in enumerate(self.object_states):
            if not isinstance(state, ObjectState):
                errors.append(f"invalid:object_states[{index}]")
                continue
            errors.extend(f"object_states[{index}]:{e}" for e in state.validate())

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
            provenance_errors = _validate_result_provenance(self.provenance)
            errors.extend(provenance_errors)
        else:
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
