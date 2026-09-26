from __future__ import annotations

from dataclasses import dataclass
from datetime import date, time

from ce.foundation.status import BirthTimeState, CalculationStatus


@dataclass(frozen=True)
class TimeResolution:
    status: CalculationStatus
    birth_time_state: BirthTimeState
    resolved_instant_utc: str | None
    timezone_id: str
    timezone_version: str | None
    error: str | None


def resolve_exact_civil_time(
    birth_date: date,
    birth_time: time | None,
    timezone_id: str,
    timezone_version: str | None,
    *,
    authoritative_timezone_version: str | None,
) -> TimeResolution:
    if birth_time is None:
        return TimeResolution(
            status=CalculationStatus.INVALID_INPUT,
            birth_time_state=BirthTimeState.ZERO_BIRTH_TIME,
            resolved_instant_utc=None,
            timezone_id=timezone_id,
            timezone_version=timezone_version,
            error="exact_civil_time_required_for_exact_resolution",
        )
    if authoritative_timezone_version is None or timezone_version != authoritative_timezone_version:
        return TimeResolution(
            status=CalculationStatus.NON_AUTHORIZED,
            birth_time_state=BirthTimeState.EXACT,
            resolved_instant_utc=None,
            timezone_id=timezone_id,
            timezone_version=timezone_version,
            error="authoritative_timezone_identity_not_established",
        )
    # Host zoneinfo is deliberately not used as an authority in this foundation.
    return TimeResolution(
        status=CalculationStatus.NON_AUTHORIZED,
        birth_time_state=BirthTimeState.EXACT,
        resolved_instant_utc=None,
        timezone_id=timezone_id,
        timezone_version=timezone_version,
        error="authoritative_tzif_bundle_not_established",
    )
