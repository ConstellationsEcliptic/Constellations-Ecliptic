from __future__ import annotations

import math


def normalize_longitude_deg(value: float) -> float:
    if not math.isfinite(value):
        raise ValueError("longitude must be finite")
    result = value % 360.0
    if result < 0.0:
        result += 360.0
    return result


def circular_separation_deg(a: float, b: float) -> float:
    a_n = normalize_longitude_deg(a)
    b_n = normalize_longitude_deg(b)
    d = abs(a_n - b_n)
    return min(d, 360.0 - d)


def signed_angular_deviation_deg(a: float, b: float, aspect_deg: float) -> float:
    if not math.isfinite(aspect_deg):
        raise ValueError("aspect must be finite")
    raw = normalize_longitude_deg(a - b - aspect_deg)
    if raw > 180.0:
        raw -= 360.0
    return raw
