from __future__ import annotations

from datetime import datetime, timedelta, timezone
from hashlib import sha256
from typing import Iterable, Sequence

from ce.calculation.solver import EVENT_TIME_TOLERANCE_SECONDS
from ce.foundation.serialization import canonical_json
from ce.foundation.status import CalculationStatus, ScenarioState


SCENARIO_SAMPLING_POLICY_ID = "CE-ZERO-BIRTH-SCENARIO-MIDPOINT-LATTICE-V1"
SCENARIO_SEGMENT_TIME_UNIT = "SECONDS"
MIN_SCENARIO_COUNT = 4
DEFAULT_SCENARIO_COUNT = 24
MAX_SCENARIO_COUNT = 96


def build_scenario_instants(start_utc: datetime, end_utc: datetime, count: int) -> tuple[datetime, ...]:
    if (
        start_utc.tzinfo is None
        or end_utc.tzinfo is None
        or start_utc.utcoffset() is None
        or end_utc.utcoffset() is None
    ):
        raise ValueError("scenario_bounds_must_be_timezone_aware")
    start_utc = start_utc.astimezone(timezone.utc)
    end_utc = end_utc.astimezone(timezone.utc)
    if end_utc <= start_utc:
        raise ValueError("scenario_interval_order_invalid")
    if not MIN_SCENARIO_COUNT <= count <= MAX_SCENARIO_COUNT:
        raise ValueError("scenario_count_out_of_policy_range")

    total_microseconds = int((end_utc - start_utc).total_seconds() * 1_000_000)
    width = total_microseconds / count
    result = []
    for index in range(count):
        offset_microseconds = int((index + 0.5) * width)
        value = start_utc + timedelta(microseconds=offset_microseconds)
        if value >= end_utc:
            raise ValueError("scenario_endpoint_included")
        result.append(value)
    return tuple(result)


def scenario_id(*, birth_instant_utc: str, target_scope: dict[str, object]) -> str:
    payload = {
        "policy": SCENARIO_SAMPLING_POLICY_ID,
        "birth_instant_utc": birth_instant_utc,
        "target_scope": target_scope,
    }
    return sha256(canonical_json(payload)).hexdigest()


def _microseconds(value: float) -> int:
    return int(round(value * 86_400_000_000.0))


def normalize_segments(segments: Iterable[tuple[float, float]]) -> tuple[tuple[float, float], ...]:
    ordered = sorted((float(a), float(b)) for a, b in segments if b > a)
    if not ordered:
        return ()
    result = [ordered[0]]
    for start, end in ordered[1:]:
        prev_start, prev_end = result[-1]
        if start <= prev_end + EVENT_TIME_TOLERANCE_SECONDS:
            result[-1] = (prev_start, max(prev_end, end))
        else:
            result.append((start, end))
    return tuple(result)


def _union(all_sets: Sequence[tuple[tuple[float, float], ...]]) -> tuple[tuple[float, float], ...]:
    merged = [segment for segments in all_sets for segment in segments]
    return normalize_segments(merged)


def _intersection_pair(
    left: tuple[tuple[float, float], ...],
    right: tuple[tuple[float, float], ...],
) -> tuple[tuple[float, float], ...]:
    result: list[tuple[float, float]] = []
    for left_start, left_end in left:
        for right_start, right_end in right:
            start = max(left_start, right_start)
            end = min(left_end, right_end)
            if end > start:
                result.append((start, end))
    return normalize_segments(result)


def _intersection(all_sets: Sequence[tuple[tuple[float, float], ...]]) -> tuple[tuple[float, float], ...]:
    if not all_sets:
        return ()
    current = normalize_segments(all_sets[0])
    for other in all_sets[1:]:
        current = _intersection_pair(current, normalize_segments(other))
        if not current:
            return ()
    return current


def classify_sampled_windows(
    per_scenario_segments: Sequence[tuple[tuple[float, float], ...]],
) -> tuple[ScenarioState, tuple[tuple[float, float], ...], tuple[tuple[float, float], ...]]:
    if not per_scenario_segments:
        return ScenarioState.NONE, (), ()
    possible = _union(per_scenario_segments)
    robust = _intersection(per_scenario_segments)
    if not possible:
        state = ScenarioState.NONE
    elif not robust:
        state = ScenarioState.POSSIBLE
    elif possible == robust:
        state = ScenarioState.ROBUST
    else:
        state = ScenarioState.MIXED
    return state, possible, robust


def canonical_utc(value: datetime) -> str:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("datetime_must_be_timezone_aware")
    normalized = value.astimezone(timezone.utc)
    return normalized.isoformat(timespec="seconds").replace("+00:00", "Z")


def validate_scenario_observation(
    status: CalculationStatus,
    *,
    window_segments: Sequence[tuple[float, float]],
) -> None:
    if status is not CalculationStatus.VALID:
        if window_segments:
            raise ValueError("nonvalid_scenario_cannot_publish_windows")
