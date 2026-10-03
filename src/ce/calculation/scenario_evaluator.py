from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Callable, Sequence

from ce.calculation.scenario_windows import (
    DEFAULT_SCENARIO_COUNT,
    build_scenario_instants,
    canonical_utc,
    classify_sampled_windows,
    scenario_id,
)
from ce.foundation.status import CalculationStatus, ScenarioState


@dataclass(frozen=True)
class ScenarioEvaluation:
    scenario_id: str
    birth_instant_utc: str
    status: CalculationStatus
    segments: tuple[tuple[float, float], ...]
    error: str | None = None


@dataclass(frozen=True)
class ScenarioAggregate:
    status: CalculationStatus
    scenario_state: ScenarioState
    possible_segments: tuple[tuple[float, float], ...]
    robust_segments: tuple[tuple[float, float], ...]
    evaluations: tuple[ScenarioEvaluation, ...]


def evaluate_zero_birth_scenarios(
    birth_interval_start_utc: datetime,
    birth_interval_end_utc: datetime,
    *,
    target_scope: dict[str, object],
    evaluate_birth: Callable[[datetime], tuple[CalculationStatus, tuple[tuple[float, float], ...]]],
    scenario_count: int = DEFAULT_SCENARIO_COUNT,
) -> ScenarioAggregate:
    """Evaluate only an explicitly bounded midpoint lattice.

    UTC birth interval must already have been resolved by the authoritative
    timezone boundary. This function has no timezone database access.
    """
    instants = build_scenario_instants(
        birth_interval_start_utc,
        birth_interval_end_utc,
        scenario_count,
    )
    evaluations: list[ScenarioEvaluation] = []
    segment_sets: list[tuple[tuple[float, float], ...]] = []

    for instant in instants:
        birth_utc = canonical_utc(instant)
        sid = scenario_id(
            birth_instant_utc=birth_utc,
            target_scope=target_scope,
        )
        try:
            status, segments = evaluate_birth(instant)
        except Exception as exc:
            return ScenarioAggregate(
                status=CalculationStatus.CALCULATION_FAILURE,
                scenario_state=ScenarioState.NONE,
                possible_segments=(),
                robust_segments=(),
                evaluations=tuple(evaluations)
                + (ScenarioEvaluation(
                    sid, birth_utc, CalculationStatus.CALCULATION_FAILURE, (), str(exc)
                ),),
            )
        if status is not CalculationStatus.VALID:
            evaluation = ScenarioEvaluation(sid, birth_utc, status, (), "required_scenario_not_valid")
            return ScenarioAggregate(
                status=CalculationStatus.CALCULATION_FAILURE,
                scenario_state=ScenarioState.NONE,
                possible_segments=(),
                robust_segments=(),
                evaluations=tuple(evaluations) + (evaluation,),
            )
        evaluation = ScenarioEvaluation(sid, birth_utc, status, tuple(segments))
        evaluations.append(evaluation)
        segment_sets.append(tuple(segments))

    state, possible, robust = classify_sampled_windows(segment_sets)
    return ScenarioAggregate(
        status=CalculationStatus.NATAL_EVIDENCE_VARIABLE,
        scenario_state=state if state is not ScenarioState.NONE else ScenarioState.VARIABLE,
        possible_segments=possible,
        robust_segments=robust,
        evaluations=tuple(evaluations),
    )
