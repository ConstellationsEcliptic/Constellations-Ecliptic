from __future__ import annotations

from datetime import datetime, timedelta, timezone
import unittest

from ce.calculation.scenario_evaluator import evaluate_zero_birth_scenarios
from ce.calculation.window_solver import solve_aspect_window
from ce.foundation.status import CalculationStatus, ScenarioState


class WindowOrchestrationR1Tests(unittest.TestCase):
    def test_injected_residual_produces_exact_event_and_window(self) -> None:
        solution = solve_aspect_window(
            lambda x: x - 2.0,
            start=0.0,
            end=4.0,
            effective_orb=0.5,
            samples=128,
        )
        self.assertEqual(len(solution.exact_events), 1)
        self.assertAlmostEqual(solution.exact_events[0].instant, 2.0, places=6)
        self.assertEqual(len(solution.segments), 1)
        self.assertAlmostEqual(solution.segments[0][0], 1.5, places=3)
        self.assertAlmostEqual(solution.segments[0][1], 2.5, places=3)

    def test_tangential_window_contact_does_not_create_nonexistent_window(self) -> None:
        solution = solve_aspect_window(
            lambda x: (x - 2.0) ** 2,
            start=0.0,
            end=4.0,
            effective_orb=0.0 + 1e-6,
            samples=256,
        )
        self.assertTrue(solution.segments)
        self.assertTrue(solution.exact_events)

    def test_zero_birth_aggregate_is_fail_closed(self) -> None:
        start = datetime(2026, 1, 1, tzinfo=timezone.utc)
        end = start + timedelta(days=1)

        result = evaluate_zero_birth_scenarios(
            start,
            end,
            target_scope={"object": "SUN"},
            evaluate_birth=lambda _: (
                CalculationStatus.CALCULATION_FAILURE,
                (),
            ),
            scenario_count=4,
        )
        self.assertIs(result.status, CalculationStatus.CALCULATION_FAILURE)
        self.assertIs(result.scenario_state, ScenarioState.NONE)
        self.assertEqual(result.possible_segments, ())

    def test_zero_birth_possible_vs_robust_is_sampled_only(self) -> None:
        start = datetime(2026, 1, 1, tzinfo=timezone.utc)
        end = start + timedelta(days=1)

        def evaluate(birth: datetime):
            hour = birth.hour
            if hour < 6:
                return CalculationStatus.VALID, ((1.0, 2.0),)
            return CalculationStatus.VALID, ((1.5, 2.5),)

        result = evaluate_zero_birth_scenarios(
            start,
            end,
            target_scope={"object": "SUN"},
            evaluate_birth=evaluate,
            scenario_count=4,
        )
        self.assertIs(result.status, CalculationStatus.NATAL_EVIDENCE_VARIABLE)
        self.assertIs(result.scenario_state, ScenarioState.VARIABLE)
        self.assertIs(result.window_classification, ScenarioState.MIXED)
        self.assertEqual(result.robust_segments, ((1.5, 2.0),))


if __name__ == "__main__":
    unittest.main()
