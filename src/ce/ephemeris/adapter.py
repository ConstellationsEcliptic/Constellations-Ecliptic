from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from ce.calculation.contracts import ObjectState
from ce.foundation.status import CalculationStatus


class EphemerisAdapter(Protocol):
    def calculate_object(self, object_id: str, julian_day_ut: float, with_speed: bool) -> ObjectState: ...


@dataclass(frozen=True)
class UnavailableSwissEphemerisAdapter:
    """Fail-closed placeholder until the authoritative native binding exists."""

    library_version: str = "NOT_ESTABLISHED"
    data_bundle_sha256: str | None = None

    def calculate_object(self, object_id: str, julian_day_ut: float, with_speed: bool) -> ObjectState:
        return ObjectState(
            object_id=object_id,
            longitude_deg=None,
            speed_deg_per_day=None,
            status=CalculationStatus.NON_AUTHORIZED,
        )
