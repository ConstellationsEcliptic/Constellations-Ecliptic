from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timezone
import re

from ce.foundation.status import BirthTimeState, CalculationStatus


_TZ_VERSION_RE = re.compile(r"^\d{4}[a-z]$")
_UTC_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?Z$")


def _closed_timezone_id(value: object) -> str:
    return value if isinstance(value, str) and value.strip() else "INVALID_INPUT"


def _closed_timezone_version(value: object) -> str | None:
    return value if isinstance(value, str) and _TZ_VERSION_RE.fullmatch(value) else None


def _parse_utc_z(value: object) -> tuple[datetime | None, str | None]:
    if not isinstance(value, str) or not _UTC_RE.fullmatch(value):
        return None, "utc_canonical_z_required"
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError:
        return None, "utc_iso8601_invalid"
    if parsed.tzinfo is None or parsed.utcoffset() != timezone.utc.utcoffset(parsed):
        return None, "utc_timezone_invalid"
    return parsed, None


@dataclass(frozen=True)
class TimeResolution:
    status: CalculationStatus
    birth_time_state: BirthTimeState
    resolved_instant_utc: str | None
    timezone_id: str
    timezone_version: str | None
    error: str | None

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []
        if not isinstance(self.status, CalculationStatus):
            errors.append("invalid:time_resolution_status")
        if not isinstance(self.birth_time_state, BirthTimeState):
            errors.append("invalid:time_resolution_birth_time_state")
        if not isinstance(self.timezone_id, str) or not self.timezone_id.strip():
            errors.append("invalid:timezone_id")
        if self.timezone_version is not None and (
            not isinstance(self.timezone_version, str)
            or not _TZ_VERSION_RE.fullmatch(self.timezone_version)
        ):
            errors.append("invalid:timezone_version")

        if self.status is CalculationStatus.VALID:
            if self.resolved_instant_utc is None:
                errors.append("valid_time_requires_resolved_instant")
            else:
                _, utc_error = _parse_utc_z(self.resolved_instant_utc)
                if utc_error:
                    errors.append(f"invalid:resolved_instant_utc:{utc_error}")
            if self.error is not None:
                errors.append("valid_time_cannot_have_error")
        else:
            if self.resolved_instant_utc is not None:
                errors.append("nonvalid_time_requires_no_resolved_instant")
            if not isinstance(self.error, str) or not self.error:
                errors.append("nonvalid_time_requires_error")

        return tuple(errors)

    def __post_init__(self) -> None:
        errors = self.validate()
        if errors:
            raise ValueError(";".join(errors))


def resolve_exact_civil_time(
    birth_date: date,
    birth_time: time | None,
    timezone_id: str,
    timezone_version: str | None,
    *,
    authoritative_timezone_version: str | None,
) -> TimeResolution:
    if type(birth_date) is not date:
        return TimeResolution(
            status=CalculationStatus.INVALID_INPUT,
            birth_time_state=BirthTimeState.ZERO_BIRTH_TIME,
            resolved_instant_utc=None,
            timezone_id=_closed_timezone_id(timezone_id),
            timezone_version=_closed_timezone_version(timezone_version),
            error="invalid_birth_date",
        )
    if birth_time is None:
        return TimeResolution(
            status=CalculationStatus.INVALID_INPUT,
            birth_time_state=BirthTimeState.ZERO_BIRTH_TIME,
            resolved_instant_utc=None,
            timezone_id=timezone_id,
            timezone_version=timezone_version,
            error="exact_civil_time_required_for_exact_resolution",
        )
    if not isinstance(timezone_id, str) or not timezone_id.strip():
        return TimeResolution(
            status=CalculationStatus.INVALID_INPUT,
            birth_time_state=BirthTimeState.EXACT,
            resolved_instant_utc=None,
            timezone_id="INVALID_INPUT",
            timezone_version=_closed_timezone_version(timezone_version),
            error="invalid_timezone_id",
        )
    if timezone_version is not None and (
        not isinstance(timezone_version, str)
        or not _TZ_VERSION_RE.fullmatch(timezone_version)
    ):
        return TimeResolution(
            status=CalculationStatus.INVALID_INPUT,
            birth_time_state=BirthTimeState.EXACT,
            resolved_instant_utc=None,
            timezone_id=_closed_timezone_id(timezone_id),
            timezone_version=None,
            error="invalid_timezone_version",
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
    return TimeResolution(
        status=CalculationStatus.NON_AUTHORIZED,
        birth_time_state=BirthTimeState.EXACT,
        resolved_instant_utc=None,
        timezone_id=timezone_id,
        timezone_version=timezone_version,
        error="authoritative_tzif_bundle_not_established",
    )
