from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, sqrt
from typing import Callable

SOLVER_RESIDUAL = 1.0e-6
EVENT_TIME_TOLERANCE_SECONDS = 1.0


class SolverFailure(ValueError):
    """Deterministic solver failure with no implicit fallback."""


@dataclass(frozen=True)
class RootSearch:
    roots: tuple[float, ...]
    samples: int
    residual: float
    time_tolerance_seconds: float


@dataclass(frozen=True)
class ThresholdSearch:
    segments: tuple[tuple[float, float], ...]
    tangential_contacts: tuple[float, ...]
    samples: int
    threshold: float
    residual: float
    time_tolerance_seconds: float


def _require_number(value: float, name: str) -> None:
    if not isfinite(value):
        raise SolverFailure(f"{name} must be finite")


def _deduplicate(values: list[float], separation: float) -> tuple[float, ...]:
    ordered = sorted(values)
    result: list[float] = []
    for value in ordered:
        if not result or value - result[-1] > separation:
            result.append(value)
    return tuple(result)


def _bisect(
    function: Callable[[float], float],
    left: float,
    right: float,
    *,
    residual: float,
    time_tolerance_seconds: float,
    max_iterations: int,
) -> float:
    if right <= left:
        raise SolverFailure("root_interval_order_invalid")
    f_left = function(left)
    f_right = function(right)
    _require_number(f_left, "f(left)")
    _require_number(f_right, "f(right)")
    if abs(f_left) <= residual:
        return left
    if abs(f_right) <= residual:
        return right
    if f_left * f_right > 0.0:
        raise SolverFailure("root_not_bracketed")

    tolerance_days = time_tolerance_seconds / 86400.0
    lo, hi = left, right
    flo, fhi = f_left, f_right
    for _ in range(max_iterations):
        mid = (lo + hi) / 2.0
        fmid = function(mid)
        _require_number(fmid, "f(mid)")
        if abs(fmid) <= residual or hi - lo <= tolerance_days:
            return mid
        if flo * fmid <= 0.0:
            hi, fhi = mid, fmid
        else:
            lo, flo = mid, fmid
    raise SolverFailure("root_max_iterations_exceeded")


def _minimize_abs(
    function: Callable[[float], float],
    left: float,
    right: float,
    *,
    iterations: int = 64,
) -> float:
    # Golden-section search on |f| makes tangential roots independent of sign changes.
    phi = (sqrt(5.0) - 1.0) / 2.0
    a, b = left, right
    x1 = b - phi * (b - a)
    x2 = a + phi * (b - a)
    f1, f2 = abs(function(x1)), abs(function(x2))
    _require_number(f1, "|f(x1)|")
    _require_number(f2, "|f(x2)|")
    for _ in range(iterations):
        if f1 <= f2:
            b, x2, f2 = x2, x1, f1
            x1 = b - phi * (b - a)
            f1 = abs(function(x1))
        else:
            a, x1, f1 = x1, x2, f2
            x2 = a + phi * (b - a)
            f2 = abs(function(x2))
    return x1 if f1 <= f2 else x2


def find_roots(
    function: Callable[[float], float],
    start: float,
    end: float,
    *,
    samples: int = 256,
    residual: float = SOLVER_RESIDUAL,
    time_tolerance_seconds: float = EVENT_TIME_TOLERANCE_SECONDS,
    max_iterations: int = 200,
) -> RootSearch:
    if end <= start:
        raise SolverFailure("search_interval_order_invalid")
    if samples < 2:
        raise SolverFailure("samples_too_small")
    if residual <= 0.0 or time_tolerance_seconds <= 0.0:
        raise SolverFailure("solver_tolerance_invalid")

    step = (end - start) / samples
    xs = [start + i * step for i in range(samples + 1)]
    ys = [function(x) for x in xs]
    for y in ys:
        _require_number(y, "sample")

    roots: list[float] = []
    separation = time_tolerance_seconds / 86400.0

    for i, y in enumerate(ys):
        if abs(y) <= residual:
            roots.append(xs[i])
        if i == 0:
            continue
        left_x, right_x = xs[i - 1], xs[i]
        left_y, right_y = ys[i - 1], y
        if left_y * right_y < 0.0:
            roots.append(
                _bisect(
                    function,
                    left_x,
                    right_x,
                    residual=residual,
                    time_tolerance_seconds=time_tolerance_seconds,
                    max_iterations=max_iterations,
                )
            )

    # Bounded tangency detection: only emit a tangential root when refinement
    # independently verifies contact within the declared residual.
    for i in range(1, samples):
        left_y, mid_y, right_y = ys[i - 1], ys[i], ys[i + 1]
        if abs(mid_y) <= residual:
            continue
        if abs(mid_y) <= abs(left_y) and abs(mid_y) <= abs(right_y):
            candidate = _minimize_abs(function, xs[i - 1], xs[i + 1])
            if abs(function(candidate)) <= residual:
                roots.append(candidate)

    return RootSearch(
        roots=_deduplicate(roots, separation),
        samples=samples,
        residual=residual,
        time_tolerance_seconds=time_tolerance_seconds,
    )


def solve_threshold(
    criterion: Callable[[float], float],
    start: float,
    end: float,
    *,
    threshold: float = 0.0,
    samples: int = 256,
    residual: float = SOLVER_RESIDUAL,
    time_tolerance_seconds: float = EVENT_TIME_TOLERANCE_SECONDS,
) -> ThresholdSearch:
    if end <= start:
        raise SolverFailure("search_interval_order_invalid")
    if samples < 2:
        raise SolverFailure("samples_too_small")
    if not isfinite(threshold):
        raise SolverFailure("threshold_not_finite")

    def signed(value: float) -> float:
        result = criterion(value) - threshold
        _require_number(result, "criterion")
        return result

    step = (end - start) / samples
    xs = [start + i * step for i in range(samples + 1)]
    ys = [signed(x) for x in xs]
    roots: list[float] = []
    tangencies: list[float] = []
    for i in range(samples):
        x0, x1 = xs[i], xs[i + 1]
        y0, y1 = ys[i], ys[i + 1]
        if abs(y0) <= residual:
            roots.append(x0)
        if y0 * y1 < 0.0:
            roots.append(
                _bisect(
                    signed,
                    x0,
                    x1,
                    residual=residual,
                    time_tolerance_seconds=time_tolerance_seconds,
                    max_iterations=200,
                )
            )
    if abs(ys[-1]) <= residual:
        roots.append(end)

    for i in range(1, samples):
        if ys[i] <= ys[i - 1] and ys[i] <= ys[i + 1]:
            if ys[i - 1] > residual and ys[i + 1] > residual:
                candidate = _minimize_abs(signed, xs[i - 1], xs[i + 1])
                if abs(signed(candidate)) <= residual:
                    tangencies.append(candidate)
                    roots.append(candidate)

    deduped = _deduplicate(roots, time_tolerance_seconds / 86400.0)
    boundaries = (start, *deduped, end)
    segments: list[tuple[float, float]] = []
    for left, right in zip(boundaries[:-1], boundaries[1:]):
        if right <= left:
            continue
        midpoint = (left + right) / 2.0
        if signed(midpoint) <= 0.0:
            segments.append((left, right))

    return ThresholdSearch(
        segments=tuple(segments),
        tangential_contacts=_deduplicate(tangencies, time_tolerance_seconds / 86400.0),
        samples=samples,
        threshold=threshold,
        residual=residual,
        time_tolerance_seconds=time_tolerance_seconds,
    )
