from __future__ import annotations

from dataclasses import dataclass
from datetime import date, time, timedelta

from ce.foundation.status import CalculationStatus, NatalBirthState, ObservationTimeState


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


def resolve_zero_birth_interval(
    birth_date: date,
    timezone_id: str,
    timezone_version: str | None,
    *,
    authoritative_timezone_version: str | None,
) -> ZeroBirthIntervalResolution:
    """Represent the natal state as the full local civil day.

    This function deliberately does not choose noon, midnight, a midpoint,
    or any other representative natal instant. UTC conversion remains blocked
    until the authoritative TZif dataset is established.
    """
    next_day = birth_date + timedelta(days=1)
    start = f"{birth_date.isoformat()}T00:00:00"
    end = f"{next_day.isoformat()}T00:00:00"

    if authoritative_timezone_version is None or timezone_version != authoritative_timezone_version:
        return ZeroBirthIntervalResolution(
            status=CalculationStatus.NON_AUTHORIZED,
            natal_birth_state=NatalBirthState.ZERO_BIRTH_TIME,
            local_interval_start=start,
            local_interval_end=end,
            timezone_id=timezone_id,
            timezone_version=timezone_version,
            resolved_utc_interval_start=None,
            resolved_utc_interval_end=None,
            error="authoritative_timezone_identity_not_established",
        )

    return ZeroBirthIntervalResolution(
        status=CalculationStatus.NON_AUTHORIZED,
        natal_birth_state=NatalBirthState.ZERO_BIRTH_TIME,
        local_interval_start=start,
        local_interval_end=end,
        timezone_id=timezone_id,
        timezone_version=timezone_version,
        resolved_utc_interval_start=None,
        resolved_utc_interval_end=None,
        error="authoritative_tzif_bundle_not_established",
    )


def resolve_observation_civil_time(
    observation_date: date,
    observation_time: time | None,
    timezone_id: str,
    timezone_version: str | None,
    *,
    authoritative_timezone_version: str | None,
) -> ObservationTimeResolution:
    """Resolve an explicit observation/evaluation time.

    Observation time is intentionally separate from natal birth time.
    """
    if observation_time is None:
        return ObservationTimeResolution(
            status=CalculationStatus.INVALID_INPUT,
            observation_time_state=ObservationTimeState.INVALID,
            resolved_instant_utc=None,
            timezone_id=timezone_id,
            timezone_version=timezone_version,
            error="explicit_observation_time_required",
        )

    if authoritative_timezone_version is None or timezone_version != authoritative_timezone_version:
        return ObservationTimeResolution(
            status=CalculationStatus.NON_AUTHORIZED,
            observation_time_state=ObservationTimeState.EXACT,
            resolved_instant_utc=None,
            timezone_id=timezone_id,
            timezone_version=timezone_version,
            error="authoritative_timezone_identity_not_established",
        )

    return ObservationTimeResolution(
        status=CalculationStatus.NON_AUTHORIZED,
        observation_time_state=ObservationTimeState.EXACT,
        resolved_instant_utc=None,
        timezone_id=timezone_id,
        timezone_version=timezone_version,
        error="authoritative_tzif_bundle_not_established",
    )
