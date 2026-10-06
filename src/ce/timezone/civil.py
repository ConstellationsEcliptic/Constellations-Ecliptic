from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone

from ce.foundation.status import CALENDAR_POLICY_GREGORIAN_ONLY, CalculationStatus, NatalBirthState, ObservationTimeState
from ce.timezone.runtime import TzifRuntime, TzifRuntimeError


@dataclass(frozen=True)
class CivilResolution:
    status: CalculationStatus
    natal_birth_state: NatalBirthState
    local_interval_start: str
    local_interval_end: str
    resolved_utc_interval_start: str | None
    resolved_utc_interval_end: str | None
    timezone_id: str
    timezone_version: str
    error: str | None


def resolve_zero_birth_interval(
    *,
    birth_date: date,
    timezone_id: str,
    timezone_version: str,
    calendar_policy_id: str,
    tzif_runtime: TzifRuntime,
) -> CivilResolution:
    """Resolve the full local civil day through the policy-owned TZif runtime."""

    next_day = birth_date + timedelta(days=1)
    local_start = datetime.combine(birth_date, datetime.min.time())
    local_end = datetime.combine(next_day, datetime.min.time())

    if calendar_policy_id != CALENDAR_POLICY_GREGORIAN_ONLY:
        return CivilResolution(
            status=CalculationStatus.INPUT_UNSUPPORTED,
            natal_birth_state=NatalBirthState.ZERO_BIRTH_TIME,
            local_interval_start=f"{birth_date.isoformat()}T00:00:00",
            local_interval_end=f"{next_day.isoformat()}T00:00:00",
            resolved_utc_interval_start=None,
            resolved_utc_interval_end=None,
            timezone_id=timezone_id,
            timezone_version=timezone_version,
            error="unsupported_calendar_policy",
        )

    if timezone_version != tzif_runtime.version:
        return CivilResolution(
            status=CalculationStatus.NON_AUTHORIZED,
            natal_birth_state=NatalBirthState.ZERO_BIRTH_TIME,
            local_interval_start=f"{birth_date.isoformat()}T00:00:00",
            local_interval_end=f"{next_day.isoformat()}T00:00:00",
            resolved_utc_interval_start=None,
            resolved_utc_interval_end=None,
            timezone_id=timezone_id,
            timezone_version=timezone_version,
            error="timezone_version_mismatch",
        )

    try:
        resolved_start = tzif_runtime.resolve_local_instant(local_start, timezone_id)
        resolved_end = tzif_runtime.resolve_local_instant(local_end, timezone_id)
    except TzifRuntimeError as exc:
        return CivilResolution(
            status=CalculationStatus.NON_AUTHORIZED,
            natal_birth_state=NatalBirthState.ZERO_BIRTH_TIME,
            local_interval_start=f"{birth_date.isoformat()}T00:00:00",
            local_interval_end=f"{next_day.isoformat()}T00:00:00",
            resolved_utc_interval_start=None,
            resolved_utc_interval_end=None,
            timezone_id=timezone_id,
            timezone_version=timezone_version,
            error=str(exc),
        )

    if resolved_end <= resolved_start:
        return CivilResolution(
            status=CalculationStatus.CALCULATION_FAILURE,
            natal_birth_state=NatalBirthState.ZERO_BIRTH_TIME,
            local_interval_start=f"{birth_date.isoformat()}T00:00:00",
            local_interval_end=f"{next_day.isoformat()}T00:00:00",
            resolved_utc_interval_start=None,
            resolved_utc_interval_end=None,
            timezone_id=timezone_id,
            timezone_version=timezone_version,
            error="resolved_zero_birth_interval_order_invalid",
        )

    def utc_string(value: datetime) -> str:
        normalized = value.astimezone(timezone.utc)
        timespec = "microseconds" if normalized.microsecond else "seconds"
        return normalized.isoformat(timespec=timespec).replace("+00:00", "Z")

    return CivilResolution(
        status=CalculationStatus.NATAL_EVIDENCE_VARIABLE,
        natal_birth_state=NatalBirthState.ZERO_BIRTH_TIME,
        local_interval_start=f"{birth_date.isoformat()}T00:00:00",
        local_interval_end=f"{next_day.isoformat()}T00:00:00",
        resolved_utc_interval_start=utc_string(resolved_start),
        resolved_utc_interval_end=utc_string(resolved_end),
        timezone_id=timezone_id,
        timezone_version=timezone_version,
        error=None,
    )


@dataclass(frozen=True)
class ObservationResolution:
    status: CalculationStatus
    observation_time_state: ObservationTimeState
    resolved_instant_utc: str | None
    timezone_id: str
    timezone_version: str
    error: str | None


def resolve_observation_civil_time(
    *,
    observation_date: date,
    observation_time: time | None,
    timezone_id: str,
    timezone_version: str,
    calendar_policy_id: str,
    tzif_runtime: TzifRuntime,
) -> ObservationResolution:
    """Resolve one explicit observation instant through the policy-owned TZif runtime."""

    if calendar_policy_id != CALENDAR_POLICY_GREGORIAN_ONLY:
        return ObservationResolution(
            status=CalculationStatus.INPUT_UNSUPPORTED,
            observation_time_state=ObservationTimeState.INVALID,
            resolved_instant_utc=None,
            timezone_id=timezone_id,
            timezone_version=timezone_version,
            error="unsupported_calendar_policy",
        )

    if observation_time is None:
        return ObservationResolution(
            status=CalculationStatus.INVALID_INPUT,
            observation_time_state=ObservationTimeState.INVALID,
            resolved_instant_utc=None,
            timezone_id=timezone_id,
            timezone_version=timezone_version,
            error="explicit_observation_time_required",
        )

    if timezone_version != tzif_runtime.version:
        return ObservationResolution(
            status=CalculationStatus.NON_AUTHORIZED,
            observation_time_state=ObservationTimeState.EXACT,
            resolved_instant_utc=None,
            timezone_id=timezone_id,
            timezone_version=timezone_version,
            error="timezone_version_mismatch",
        )

    try:
        local = datetime.combine(observation_date, observation_time)
        resolved = tzif_runtime.resolve_local_instant(local, timezone_id)
    except TzifRuntimeError as exc:
        error = str(exc)
        if error.startswith("ambiguous_local_time") or error.startswith("nonexistent_local_time"):
            return ObservationResolution(
                status=CalculationStatus.INPUT_UNSUPPORTED,
                observation_time_state=ObservationTimeState.INVALID,
                resolved_instant_utc=None,
                timezone_id=timezone_id,
                timezone_version=timezone_version,
                error=error,
            )
        return ObservationResolution(
            status=CalculationStatus.NON_AUTHORIZED,
            observation_time_state=ObservationTimeState.EXACT,
            resolved_instant_utc=None,
            timezone_id=timezone_id,
            timezone_version=timezone_version,
            error=error,
        )

    return ObservationResolution(
        status=CalculationStatus.VALID,
        observation_time_state=ObservationTimeState.EXACT,
        resolved_instant_utc=resolved.isoformat(timespec="seconds").replace("+00:00", "Z"),
        timezone_id=timezone_id,
        timezone_version=timezone_version,
        error=None,
    )
