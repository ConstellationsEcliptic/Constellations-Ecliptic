from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Protocol

from ce.calculation.contracts import ObjectRecord
from ce.calculation.geometry import aspect_geometry, effective_orb
from ce.calculation.registry import EXPECTED_OBJECTS, RegistryValidationError
from ce.calculation.window_solver import WindowSolution, solve_aspect_window
from ce.foundation.status import CalculationStatus, ScenarioState


class KernelFailure(ValueError):
    """Calculation cannot produce a valid downstream numerical state."""


class NumericalProvider(Protocol):
    def object_state_at(self, object_id: str, instant_utc: datetime) -> ObjectRecord:
        """Return one object state from the authoritative numerical provider."""


@dataclass(frozen=True)
class KernelEvent:
    instant_utc: str
    residual_deg: float


@dataclass(frozen=True)
class KernelWindow:
    entry_utc: str
    exit_utc: str


@dataclass(frozen=True)
class KernelCalculation:
    status: CalculationStatus
    natal_object: ObjectRecord
    events: tuple[KernelEvent, ...]
    windows: tuple[KernelWindow, ...]
    tangential_contacts: tuple[str, ...]
    samples: int
    solver_residual_deg: float
    event_time_tolerance_seconds: float


@dataclass(frozen=True)
class ZeroBirthKernelCalculation:
    """Scenario-bounded zero-birth calculation with sampled uncertainty semantics."""

    status: CalculationStatus
    scenario_state: ScenarioState
    window_classification: ScenarioState
    possible_segments_seconds: tuple[tuple[float, float], ...]
    robust_segments_seconds: tuple[tuple[float, float], ...]
    scenario_count: int
    scenario_ids: tuple[str, ...]


def _canonical_utc(value: datetime) -> str:
    if value.tzinfo is None or value.utcoffset() is None:
        raise KernelFailure("datetime_must_be_timezone_aware")
    return value.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _parse_target(value: str) -> datetime:
    if not value.endswith("Z"):
        raise KernelFailure("target_datetime_must_be_utc_z")
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise KernelFailure("target_datetime_invalid") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise KernelFailure("target_datetime_timezone_missing")
    return parsed.astimezone(timezone.utc)


def calculate_aspect_window(
    provider: NumericalProvider,
    *,
    birth_instant_utc: datetime,
    target_start_utc: datetime,
    target_end_utc: datetime,
    transit_object: str,
    natal_object: str,
    aspect: str,
    samples: int = 256,
) -> KernelCalculation:
    if transit_object not in EXPECTED_OBJECTS or natal_object not in EXPECTED_OBJECTS:
        raise RegistryValidationError("object_not_in_current_registry")
    if target_end_utc <= target_start_utc:
        raise KernelFailure("target_interval_order_invalid")
    if target_start_utc.tzinfo is None or target_end_utc.tzinfo is None or birth_instant_utc.tzinfo is None:
        raise KernelFailure("all_instants_must_be_timezone_aware")

    natal = provider.object_state_at(natal_object, birth_instant_utc)
    if natal.object_status is not CalculationStatus.VALID:
        raise KernelFailure(f"natal_object_not_valid:{natal_object}:{natal.object_status.value}")

    total_seconds = (target_end_utc - target_start_utc).total_seconds()
    if total_seconds <= 0.0:
        raise KernelFailure("target_interval_empty")

    def signed_residual(offset_seconds: float) -> float:
        instant = target_start_utc + timedelta(seconds=offset_seconds)
        transit = provider.object_state_at(transit_object, instant)
        if transit.object_status is not CalculationStatus.VALID:
            raise KernelFailure(f"transit_object_not_valid:{transit_object}:{transit.object_status.value}")
        _, signed, _, _, _ = aspect_geometry(
            transit_object,
            natal_object,
            float(transit.longitude),
            float(natal.longitude),
            transit.speed,
            aspect,
        )
        return signed

    effective = effective_orb(transit_object, aspect)
    solution: WindowSolution = solve_aspect_window(
        signed_residual,
        start=0.0,
        end=total_seconds,
        effective_orb=effective,
        samples=samples,
    )

    events = tuple(
        KernelEvent(
            instant_utc=_canonical_utc(target_start_utc + timedelta(seconds=event.instant)),
            residual_deg=event.residual,
        )
        for event in solution.exact_events
    )
    windows = tuple(
        KernelWindow(
            entry_utc=_canonical_utc(target_start_utc + timedelta(seconds=start)),
            exit_utc=_canonical_utc(target_start_utc + timedelta(seconds=end)),
        )
        for start, end in solution.segments
    )
    tangencies = tuple(
        _canonical_utc(target_start_utc + timedelta(seconds=offset))
        for offset in solution.tangential_contacts
    )
    return KernelCalculation(
        status=CalculationStatus.VALID,
        natal_object=natal,
        events=events,
        windows=windows,
        tangential_contacts=tangencies,
        samples=samples,
        solver_residual_deg=solution.root_search.residual,
        event_time_tolerance_seconds=solution.root_search.time_tolerance_seconds,
    )


def calculate_zero_birth_aspect_window(
    provider: NumericalProvider,
    *,
    birth_interval_start_utc: datetime,
    birth_interval_end_utc: datetime,
    target_start_utc: datetime,
    target_end_utc: datetime,
    transit_object: str,
    natal_object: str,
    aspect: str,
    scenario_count: int = 9,
    samples: int = 256,
) -> ZeroBirthKernelCalculation:
    """Compose the provider-backed kernel with the bounded zero-birth evaluator."""

    from ce.calculation.scenario_evaluator import evaluate_zero_birth_scenarios
    from ce.calculation.scenario_windows import build_scenario_instants, canonical_utc, scenario_id

    if birth_interval_end_utc <= birth_interval_start_utc:
        raise KernelFailure("birth_interval_order_invalid")
    if target_end_utc <= target_start_utc:
        raise KernelFailure("target_interval_order_invalid")
    for value in (
        birth_interval_start_utc,
        birth_interval_end_utc,
        target_start_utc,
        target_end_utc,
    ):
        if value.tzinfo is None or value.utcoffset() is None:
            raise KernelFailure("all_instants_must_be_timezone_aware")
    if scenario_count < 2:
        raise KernelFailure("scenario_count_too_small")

    target_scope = {
        "transit_object": transit_object,
        "natal_object": natal_object,
        "aspect": aspect,
        "target_start_utc": _canonical_utc(target_start_utc),
        "target_end_utc": _canonical_utc(target_end_utc),
    }
    total_seconds = (target_end_utc - target_start_utc).total_seconds()
    target_start_timestamp = target_start_utc.timestamp()

    def evaluate_birth(
        birth_instant: datetime,
    ) -> tuple[CalculationStatus, tuple[tuple[float, float], ...]]:
        result = calculate_aspect_window(
            provider,
            birth_instant_utc=birth_instant,
            target_start_utc=target_start_utc,
            target_end_utc=target_end_utc,
            transit_object=transit_object,
            natal_object=natal_object,
            aspect=aspect,
            samples=samples,
        )
        segments: list[tuple[float, float]] = []
        for window in result.windows:
            start = _parse_target(window.entry_utc).timestamp() - target_start_timestamp
            end = _parse_target(window.exit_utc).timestamp() - target_start_timestamp
            if start < 0.0 or end > total_seconds or end <= start:
                raise KernelFailure("kernel_window_outside_target_interval")
            segments.append((start, end))
        return result.status, tuple(segments)

    aggregate = evaluate_zero_birth_scenarios(
        birth_interval_start_utc,
        birth_interval_end_utc,
        target_scope=target_scope,
        evaluate_birth=evaluate_birth,
        scenario_count=scenario_count,
    )
    instants = build_scenario_instants(
        birth_interval_start_utc,
        birth_interval_end_utc,
        scenario_count,
    )
    expected_ids = tuple(
        scenario_id(
            birth_instant_utc=canonical_utc(instant),
            target_scope=target_scope,
        )
        for instant in instants
    )
    actual_ids = tuple(item.scenario_id for item in aggregate.evaluations)
    if actual_ids != expected_ids[: len(actual_ids)]:
        raise KernelFailure("scenario_identity_order_mismatch")

    return ZeroBirthKernelCalculation(
        status=aggregate.status,
        scenario_state=aggregate.scenario_state,
        window_classification=aggregate.window_classification,
        possible_segments_seconds=aggregate.possible_segments,
        robust_segments_seconds=aggregate.robust_segments,
        scenario_count=len(aggregate.evaluations),
        scenario_ids=actual_ids,
    )


def validate_kernel_window_result(result: KernelCalculation) -> None:
    if result.status is not CalculationStatus.VALID:
        raise KernelFailure("kernel_result_not_valid")
    if result.natal_object.object_status is not CalculationStatus.VALID:
        raise KernelFailure("kernel_result_contains_invalid_natal")
    for event in result.events:
        _parse_target(event.instant_utc)
    for window in result.windows:
        start = _parse_target(window.entry_utc)
        end = _parse_target(window.exit_utc)
        if end <= start:
            raise KernelFailure("kernel_window_order_invalid")
