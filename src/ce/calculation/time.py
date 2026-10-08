from __future__ import annotations

"""Compatibility-only time API.

The authoritative civil-time implementation is now in :mod:`ce.timezone.civil`.
These wrappers exist only for older callers that do not yet provide a controlled
TZif runtime. They never resolve local time to UTC and never provide authority.
"""

from dataclasses import dataclass
from datetime import date, time, timedelta

from ce.foundation.status import (
    CALENDAR_POLICY_GREGORIAN_ONLY,
    CalculationStatus,
    NatalBirthState,
    ObservationTimeState,
)


@dataclass(frozen=True)
class ZeroBirthIntervalResolution:
    status: CalculationStatus
    natal_birth_state: NatalBirthState
    local_interval_start: str
    local_interval_end: str
    timezone_id: str
    timezone_version: str | None
    resolved_utc_interval_start: str | None
    resolved_utc_interval_end: str | None
    error: str | None


@dataclass(frozen=True)
class ObservationTimeResolution:
    status: CalculationStatus
    observation_time_state: ObservationTimeState
    resolved_instant_utc: str | None
    timezone_id: str
    timezone_version: str | None
    error: str | None


def _day_bounds(birth_date: date) -> tuple[str, str]:
    next_day = birth_date + timedelta(days=1)
    return (
        f"{birth_date.isoformat()}T00:00:00",
        f"{next_day.isoformat()}T00:00:00",
    )


def resolve_zero_birth_interval(
    birth_date: date,
    timezone_id: str,
    timezone_version: str | None,
    *,
    authoritative_timezone_version: str | None,
    calendar_policy_id: str = CALENDAR_POLICY_GREGORIAN_ONLY,
) -> ZeroBirthIntervalResolution:
    start, end = _day_bounds(birth_date)
    if calendar_policy_id != CALENDAR_POLICY_GREGORIAN_ONLY:
        return ZeroBirthIntervalResolution(
            CalculationStatus.INPUT_UNSUPPORTED, NatalBirthState.ZERO_BIRTH_TIME,
            start, end, timezone_id, timezone_version, None, None,
            "unsupported_calendar_policy",
        )
    if authoritative_timezone_version is None or timezone_version != authoritative_timezone_version:
        return ZeroBirthIntervalResolution(
            CalculationStatus.NON_AUTHORIZED, NatalBirthState.ZERO_BIRTH_TIME,
            start, end, timezone_id, timezone_version, None, None,
            "authoritative_timezone_identity_not_established",
        )
    return ZeroBirthIntervalResolution(
        CalculationStatus.NON_AUTHORIZED, NatalBirthState.ZERO_BIRTH_TIME,
        start, end, timezone_id, timezone_version, None, None,
        "authoritative_tzif_bundle_not_established",
    )


def resolve_observation_civil_time(
    observation_date: date,
    observation_time: time | None,
    timezone_id: str,
    timezone_version: str | None,
    *,
    authoritative_timezone_version: str | None,
    calendar_policy_id: str = CALENDAR_POLICY_GREGORIAN_ONLY,
) -> ObservationTimeResolution:
    if calendar_policy_id != CALENDAR_POLICY_GREGORIAN_ONLY:
        return ObservationTimeResolution(
            CalculationStatus.INPUT_UNSUPPORTED, ObservationTimeState.INVALID,
            None, timezone_id, timezone_version, "unsupported_calendar_policy",
        )
    if observation_time is None:
        return ObservationTimeResolution(
            CalculationStatus.INVALID_INPUT, ObservationTimeState.INVALID,
            None, timezone_id, timezone_version, "explicit_observation_time_required",
        )
    if authoritative_timezone_version is None or timezone_version != authoritative_timezone_version:
        return ObservationTimeResolution(
            CalculationStatus.NON_AUTHORIZED, ObservationTimeState.EXACT,
            None, timezone_id, timezone_version, "authoritative_timezone_identity_not_established",
        )
    return ObservationTimeResolution(
        CalculationStatus.NON_AUTHORIZED, ObservationTimeState.EXACT,
        None, timezone_id, timezone_version, "authoritative_tzif_bundle_not_established",
    )
