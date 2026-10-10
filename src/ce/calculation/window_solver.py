from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from ce.calculation.solver import (
    EVENT_TIME_TOLERANCE_SECONDS,
    SOLVER_RESIDUAL,
    RootSearch,
    ThresholdSearch,
    find_roots,
    solve_threshold,
)


@dataclass(frozen=True)
class ExactEvent:
    instant: float
    residual: float


@dataclass(frozen=True)
class WindowSolution:
    exact_events: tuple[ExactEvent, ...]
    segments: tuple[tuple[float, float], ...]
    tangential_contacts: tuple[float, ...]
    root_search: RootSearch
    threshold_search: ThresholdSearch


def solve_aspect_window(
    signed_residual: Callable[[float], float],
    *,
    start: float,
    end: float,
    effective_orb: float,
    samples: int = 256,
) -> WindowSolution:
    """Solve one aspect window from an injected numerical residual function.

    The callable is the only source of numerical state. This layer never calls
    an ephemeris engine and therefore cannot invent astronomical positions.
    """
    if effective_orb <= 0.0:
        raise ValueError("effective_orb_must_be_positive")

    roots = find_roots(
        signed_residual,
        start,
        end,
        samples=samples,
        residual=SOLVER_RESIDUAL,
        time_tolerance_seconds=EVENT_TIME_TOLERANCE_SECONDS,
    )
    threshold = solve_threshold(
        lambda x: abs(signed_residual(x)),
        start,
        end,
        threshold=effective_orb,
        samples=samples,
        residual=SOLVER_RESIDUAL,
        time_tolerance_seconds=EVENT_TIME_TOLERANCE_SECONDS,
    )
    events = tuple(
        ExactEvent(instant=root, residual=signed_residual(root))
        for root in roots.roots
    )
    return WindowSolution(
        exact_events=events,
        segments=threshold.segments,
        tangential_contacts=threshold.tangential_contacts,
        root_search=roots,
        threshold_search=threshold,
    )
