from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any

from ce.foundation.status import CALENDAR_POLICY_GREGORIAN_ONLY, CalculationStatus, NatalBirthState, ScenarioState


@dataclass(frozen=True)
class BirthInput:
    """V1 Personal Sky natal input.

    Exact birth time is intentionally absent from this contract.
    """
    birth_date: date
    birth_city: str
    timezone_id: str
    timezone_version: str | None
    natal_birth_state: NatalBirthState = NatalBirthState.ZERO_BIRTH_TIME


@dataclass(frozen=True)
class CalculationRequest:
    request_id: str
    birth: BirthInput
    target_interval_start_utc: str
    target_interval_end_utc: str
    execution_profile_id: str
    calendar_policy_id: str = CALENDAR_POLICY_GREGORIAN_ONLY


@dataclass(frozen=True)
class ObjectState:
    object_id: str
    longitude_deg: float | None
    speed_deg_per_day: float | None
    status: CalculationStatus


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
