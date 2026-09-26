from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Protocol

from ce.calculation.contracts import ObjectState
from ce.foundation.status import CalculationStatus


def _finite_number(value: object) -> bool:
    if type(value) is int:
        return True
    return type(value) is float and math.isfinite(value)


@dataclass(frozen=True)
class EphemerisRequest:
    object_id: str
    julian_day_ut: float
    with_speed: bool

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []
        if not isinstance(self.object_id, str) or not self.object_id.strip():
            errors.append("invalid:ephemeris.object_id")
        if not _finite_number(self.julian_day_ut):
            errors.append("invalid:ephemeris.julian_day_ut")
        if not isinstance(self.with_speed, bool):
            errors.append("invalid:ephemeris.with_speed")
        return tuple(errors)

    def __post_init__(self) -> None:
        errors = self.validate()
        if errors:
            raise ValueError(";".join(errors))


class EphemerisAdapter(Protocol):
    def calculate_object(self, object_id: str, julian_day_ut: float, with_speed: bool) -> ObjectState: ...


@dataclass(frozen=True)
class UnavailableSwissEphemerisAdapter:
    """Fail-closed placeholder until the authoritative native binding exists."""

    library_version: str = "NOT_ESTABLISHED"
    data_bundle_sha256: str | None = None

    def calculate_object(self, object_id: str, julian_day_ut: float, with_speed: bool) -> ObjectState:
        try:
            EphemerisRequest(object_id, julian_day_ut, with_speed)
        except ValueError:
            return ObjectState(
                object_id=(
                    object_id
                    if isinstance(object_id, str) and object_id.strip()
                    else "INVALID_INPUT"
                ),
                longitude_deg=None,
                speed_deg_per_day=None,
                status=CalculationStatus.INVALID_INPUT,
            )
        return ObjectState(
            object_id=object_id,
            longitude_deg=None,
            speed_deg_per_day=None,
            status=CalculationStatus.NON_AUTHORIZED,
        )
