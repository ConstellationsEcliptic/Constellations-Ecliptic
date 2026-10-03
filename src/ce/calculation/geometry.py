from __future__ import annotations

import math
from typing import Final

from ce.foundation.status import KinematicState


ASPECT_BRANCHES: Final[dict[str, tuple[float, ...]]] = {
    "CONJUNCTION": (0.0,),
    "SEXTILE": (60.0, -60.0),
    "SQUARE": (90.0, -90.0),
    "TRINE": (120.0, -120.0),
    "OPPOSITION": (180.0,),
}

ORB_PROFILE_A: Final[dict[str, float]] = {
    "CONJUNCTION": 2.5,
    "SEXTILE": 1.5,
    "SQUARE": 2.0,
    "TRINE": 2.0,
    "OPPOSITION": 2.5,
}

ORB_PROFILE_B: Final[dict[str, float]] = {
    "CONJUNCTION": 1.5,
    "SEXTILE": 1.0,
    "SQUARE": 1.5,
    "TRINE": 1.5,
    "OPPOSITION": 1.5,
}

PROFILE_A_OBJECTS: Final[frozenset[str]] = frozenset(
    {"SUN", "MOON", "MERCURY", "VENUS", "MARS"}
)


def normalize_longitude_deg(value: float) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(float(value)):
        raise ValueError("longitude must be finite")
    return float(value) % 360.0


def circular_span_deg(start: float, end: float) -> float:
    """Shortest positive circular span from start to end in degrees."""
    return (normalize_longitude_deg(end) - normalize_longitude_deg(start)) % 360.0


def circular_separation_deg(a: float, b: float) -> float:
    a_n = normalize_longitude_deg(a)
    b_n = normalize_longitude_deg(b)
    difference = abs(a_n - b_n)
    return min(difference, 360.0 - difference)


def wrap180(value: float) -> float:
    normalized = value % 360.0
    return normalized - 360.0 if normalized >= 180.0 else normalized


def directed_phase(transit_longitude: float, natal_longitude: float) -> float:
    return wrap180(normalize_longitude_deg(transit_longitude) - normalize_longitude_deg(natal_longitude))


def signed_angular_deviation_deg(a: float, b: float, aspect_deg: float) -> float:
    if not math.isfinite(aspect_deg):
        raise ValueError("aspect must be finite")
    return wrap180(normalize_longitude_deg(a) - normalize_longitude_deg(b) - aspect_deg)


def resolve_branch(aspect: str, delta_lambda: float) -> float:
    branches = ASPECT_BRANCHES.get(aspect)
    if branches is None:
        raise ValueError(f"unsupported CE aspect: {aspect}")
    return min(
        branches,
        key=lambda branch: (abs(wrap180(delta_lambda - branch)), branch),
    )


def effective_orb(transit_object: str, aspect: str) -> float:
    if aspect not in ASPECT_BRANCHES:
        raise ValueError(f"unsupported CE aspect: {aspect}")
    table = ORB_PROFILE_A if transit_object in PROFILE_A_OBJECTS else ORB_PROFILE_B
    return table[aspect]


def aspect_geometry(
    transit_object: str,
    natal_object_or_scenario: str,
    transit_longitude: float,
    natal_longitude: float,
    transit_speed: float | None,
    aspect: str,
    *,
    exact_tolerance_deg: float = 1.0e-4,
    motion_tolerance_deg_per_day: float = 1.0e-6,
) -> tuple[float, float, float, KinematicState, bool]:
    delta_lambda = directed_phase(transit_longitude, natal_longitude)
    branch = resolve_branch(aspect, delta_lambda)
    signed_error = wrap180(delta_lambda - branch)
    absolute_error = abs(signed_error)
    orb = effective_orb(transit_object, aspect)

    if absolute_error <= exact_tolerance_deg:
        state = KinematicState.EXACT
    elif transit_speed is None or not math.isfinite(transit_speed):
        state = KinematicState.NEAR_STATIONARY
    else:
        derivative = (1.0 if signed_error > 0.0 else -1.0) * transit_speed
        if derivative < -motion_tolerance_deg_per_day:
            state = KinematicState.APPLYING
        elif derivative > motion_tolerance_deg_per_day:
            state = KinematicState.SEPARATING
        else:
            state = KinematicState.NEAR_STATIONARY

    return branch, signed_error, absolute_error, state, absolute_error <= orb
