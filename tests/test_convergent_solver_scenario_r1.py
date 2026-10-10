from __future__ import annotations

import inspect
import unittest
from datetime import datetime, timezone

from ce.calculation.scenario_windows import (
    DEFAULT_SCENARIO_COUNT,
    MAX_SCENARIO_COUNT,
    MIN_SCENARIO_COUNT,
    build_scenario_instants,
    classify_sampled_windows,
)
from ce.calculation.solver import find_roots, solve_threshold
from ce.foundation.status import ScenarioState


class ConvergentSolverScenarioTests(unittest.TestCase):
    def test_root_with_sign_change(self) -> None:
        result = find_roots(lambda x: x - 2.0, 0.0, 4.0, samples=32)
        self.assertEqual(len(result.roots), 1)
        self.assertAlmostEqual(result.roots[0], 2.0, places=6)

    def test_tangential_root_without_sign_change(self) -> None:
        result = find_roots(lambda x: (x - 1.25) ** 2, 0.0, 2.0, samples=64)
        self.assertEqual(len(result.roots), 1)
        self.assertAlmostEqual(result.roots[0], 1.25, places=4)

    def test_threshold_returns_disjoint_segments(self) -> None:
        result = solve_threshold(
            lambda x: min(abs(x - 1.0), abs(x - 4.0)),
            0.0,
            5.0,
            threshold=0.2,
            samples=200,
        )
        self.assertEqual(len(result.segments), 2)
        self.assertLess(result.segments[0][1], result.segments[1][0])

    def test_midpoint_lattice_is_bounded_and_excludes_endpoint(self) -> None:
        start = datetime(2026, 1, 1, tzinfo=timezone.utc)
        end = datetime(2026, 1, 2, tzinfo=timezone.utc)
        samples = build_scenario_instants(start, end, DEFAULT_SCENARIO_COUNT)
        self.assertEqual(len(samples), DEFAULT_SCENARIO_COUNT)
        self.assertLess(samples[0], samples[-1])
        self.assertLess(samples[-1], end)
        self.assertGreater(samples[0], start)
        self.assertTrue(MIN_SCENARIO_COUNT <= DEFAULT_SCENARIO_COUNT <= MAX_SCENARIO_COUNT)

    def test_midpoint_lattice_uses_exact_integer_microseconds(self) -> None:
        start = datetime(1900, 1, 1, tzinfo=timezone.utc)
        end = datetime(2200, 1, 1, tzinfo=timezone.utc)
        count = 24
        samples = build_scenario_instants(start, end, count)
        total_microseconds = int((end - start).total_seconds()) * 1_000_000
        expected_offsets = [
            ((2 * index + 1) * total_microseconds) // (2 * count)
            for index in range(count)
        ]
        actual_offsets = [
            int((sample - start).total_seconds() * 1_000_000)
            for sample in samples
        ]
        self.assertEqual(actual_offsets, expected_offsets)

    def test_kernel_zero_birth_uses_canonical_scenario_count(self) -> None:
        from ce.calculation.kernel import calculate_zero_birth_aspect_window

        parameter = inspect.signature(calculate_zero_birth_aspect_window).parameters["scenario_count"]
        self.assertEqual(parameter.default, DEFAULT_SCENARIO_COUNT)

    def test_kernel_canonical_utc_preserves_microseconds(self) -> None:
        from ce.calculation.kernel import _canonical_utc

        precise = datetime(2026, 1, 2, 3, 4, 5, 123456, tzinfo=timezone.utc)
        exact_second = datetime(2026, 1, 2, 3, 4, 5, tzinfo=timezone.utc)
        self.assertEqual(_canonical_utc(precise), "2026-01-02T03:04:05.123456Z")
        self.assertEqual(_canonical_utc(exact_second), "2026-01-02T03:04:05Z")

    def test_canonical_utc_preserves_microseconds_without_padding_zeroes(self) -> None:
        from ce.calculation.scenario_windows import canonical_utc

        precise = datetime(2026, 1, 2, 3, 4, 5, 123456, tzinfo=timezone.utc)
        exact_second = datetime(2026, 1, 2, 3, 4, 5, tzinfo=timezone.utc)
        self.assertEqual(canonical_utc(precise), "2026-01-02T03:04:05.123456Z")
        self.assertEqual(canonical_utc(exact_second), "2026-01-02T03:04:05Z")

    def test_possible_and_robust_classification(self) -> None:
        state, possible, robust = classify_sampled_windows(
            (
                ((10.0, 20.0),),
                ((10.0, 20.0),),
                ((10.0, 20.0),),
            )
        )
        self.assertIs(state, ScenarioState.ROBUST)
        self.assertEqual(possible, robust)

        state, possible, robust = classify_sampled_windows(
            (
                ((10.0, 20.0),),
                ((15.0, 25.0),),
                ((10.0, 20.0),),
            )
        )
        self.assertIs(state, ScenarioState.MIXED)
        self.assertTrue(possible)
        self.assertEqual(robust, ((15.0, 20.0),))

    def test_none_and_possible_classification(self) -> None:
        state, possible, robust = classify_sampled_windows(((), (), ()))
        self.assertIs(state, ScenarioState.NONE)
        self.assertEqual(possible, ())
        self.assertEqual(robust, ())

        state, possible, robust = classify_sampled_windows(
            (
                ((1.0, 2.0),),
                (),
            )
        )
        self.assertIs(state, ScenarioState.POSSIBLE)
        self.assertEqual(possible, ((1.0, 2.0),))
        self.assertEqual(robust, ())


if __name__ == "__main__":
    unittest.main()
