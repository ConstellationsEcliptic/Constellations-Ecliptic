from __future__ import annotations

import math


def _finite_numeric(value: object, field_name: str) -> float:
    if type(value) is int:
        return float(value)
    if type(value) is float and math.isfinite(value):
        return value
    raise ValueError(f"{field_name} must be a finite numeric value")


def normalize_longitude_deg(value: float) -> float:
    numeric = _finite_numeric(value, "longitude")
    result = numeric % 360.0
    if result < 0.0:
        result += 360.0
    return result


def circular_separation_deg(a: float, b: float) -> float:
    a_n = normalize_longitude_deg(a)
    b_n = normalize_longitude_deg(b)
    d = abs(a_n - b_n)
    return min(d, 360.0 - d)


def signed_angular_deviation_deg(a: float, b: float, aspect_deg: float) -> float:
    aspect = _finite_numeric(aspect_deg, "aspect")
    raw = normalize_longitude_deg(a - b - aspect)
    if raw > 180.0:
        raw -= 360.0
    return raw
