from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from ce.calculation.contracts import ObjectRecord
from ce.foundation.status import CalculationStatus


class EphemerisAdapter(Protocol):
    def calculate_object(self, object_id: str, julian_day_ut: float, with_speed: bool) -> ObjectRecord: ...


@dataclass(frozen=True)
class UnavailableSwissEphemerisAdapter:
    """Fail-closed placeholder until the authoritative native binding exists."""

    library_version: str = "NOT_ESTABLISHED"
    data_bundle_sha256: str | None = None

    def calculate_object(self, object_id: str, julian_day_ut: float, with_speed: bool) -> ObjectRecord:
        return ObjectRecord(
            object_id=object_id,
            object_status=CalculationStatus.NON_AUTHORIZED,
            requested_flags=2 | (256 if with_speed else 0),
            actual_flags=None,
            longitude=None,
            latitude=None,
            distance=None,
            speed=None,
            warnings=(),
            errors=("NON_AUTHORIZED_RUNTIME",),
        )
