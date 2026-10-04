from __future__ import annotations

from enum import Enum

from ce.calculation.contracts import ObjectState
from ce.foundation.status import CalculationStatus


class ObjectRangeStatus(str, Enum):
    IN_RANGE = "IN_RANGE"
    OUTSIDE_SUPPORTED_RANGE = "OUTSIDE_SUPPORTED_RANGE"


def map_native_range_result(
    object_id: str,
    *,
    range_status: ObjectRangeStatus,
    native_return_code: int,
) -> ObjectState | None:
    """Map a provider range result without manufacturing a coordinate.

    A non-fatal provider response outside the supported object range is a
    known-unavailable state, not a calculation failure and never VALID.
    """
    if range_status is ObjectRangeStatus.OUTSIDE_SUPPORTED_RANGE:
        if native_return_code >= 0:
            return ObjectState(
                object_id=object_id,
                longitude_deg=None,
                speed_deg_per_day=None,
                status=CalculationStatus.KNOWN_UNAVAILABLE,
            )
        return ObjectState(
            object_id=object_id,
            longitude_deg=None,
            speed_deg_per_day=None,
            status=CalculationStatus.CALCULATION_FAILURE,
        )
    return None
