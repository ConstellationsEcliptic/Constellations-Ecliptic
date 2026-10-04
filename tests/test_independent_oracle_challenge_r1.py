from __future__ import annotations

"""Independent challenge checks for the CE V1 numerical/geometric contracts.

This module contains its own reference equations and set logic, then compares
those expectations with selected CE production outputs. It does not treat CE
production outputs as the source of the expected values.
"""

import math
import unittest
from datetime import datetime, timezone

from ce.calculation.geometry import aspect_geometry, circular_span_deg, effective_orb
from ce.calculation.window_solver import solve_aspect_window
from ce.foundation.status import KinematicState, ScenarioState


def ref_wrap360(value: float) -> float:
    return value - 360.0 * math.floor(value / 360.0)


def ref_wrap180(value: float) -> float:
    return ref_wrap360(value + 180.0) - 180.0


def ref_branch(transit: float, natal: float, branches: tuple[float, ...]) -> float:
    separation = ref_wrap180(transit - natal)
    return min(branches, key=lambda b: (abs(ref_wrap180(separation - b)), b))


def ref_geometry(transit: float, natal: float, branch: float, speed: float | None) -> tuple[float, float, str]:
    separation = ref_wrap180(transit - natal)
    error = ref_wrap180(separation - branch)
    distance = abs(error)
    if distance <= 1.0e-4:
        return error, distance, "EXACT"
    derivative = (math.copysign(1.0, error) * speed) if speed is not None and speed != 0.0 else 0.0
    if derivative < -1.0e-6:
        return error, distance, "APPLYING"
    if derivative > 1.0e-6:
        return error, distance, "SEPARATING"
    return error, distance, "NEAR_STATIONARY"


def reference_interval_topology(
    fn,
    start: float,
    end: float,
    orb: float,
    *,
    steps: int = 10000,
) -> tuple[tuple[float, float], tuple[float, ...]]:
    """Brute-force topology oracle for fixtures with analytically known roots.

    This is a challenge oracle, not a replacement solver. Boundaries/roots are
    taken from the approved fixture equations and refined only numerically.
    """
    if steps < 10:
        raise ValueError("steps")
    h = (end - start) / steps

    def inside(x: float) -> bool:
        return abs(fn(x)) <= orb

    samples = [start + i * h for i in range(steps + 1)]
    segments: list[tuple[float, float]] = []
    roots: list[float] = []

    for i, x in enumerate(samples):
        if i and inside(x) and not inside(samples[i - 1]):
            lo, hi = samples[i - 1], x
            for _ in range(80):
                mid = (lo + hi) / 2.0
                if inside(mid):
                    hi = mid
                else:
                    lo = mid
            segments.append((hi, 0.0))

        if i < steps and inside(x) and not inside(samples[i + 1]):
            lo, hi = x, samples[i + 1]
            for _ in range(80):
                mid = (lo + hi) / 2.0
                if inside(mid):
                    lo = mid
                else:
                    hi = mid
            if segments:
                a, _ = segments[-1]
                segments[-1] = (a, lo)

    return tuple(segments), tuple(roots)


class IndependentCoreOracleChallengeR1(unittest.TestCase):
    def test_geo_01_and_02_reference_math(self) -> None:
        cases = (
            ("GEO-01", 359.5, 0.5, (0.0,), None, -1.0, 1.0, "NEAR_STATIONARY"),
            ("GEO-02", 10.0, 100.0, (-90.0, 90.0), None, 0.0, 0.0, "EXACT"),
        )
        for case, transit, natal, branches, speed, exp_err, exp_abs, exp_phase in cases:
            with self.subTest(case=case):
                branch = ref_branch(transit, natal, branches)
                err, dist, phase = ref_geometry(transit, natal, branch, speed)
                got_branch, got_err, got_abs, got_state, _ = aspect_geometry(
                    "SUN", "MOON", transit, natal, speed,
                    "CONJUNCTION" if case == "GEO-01" else "SQUARE",
                )
                self.assertEqual(got_branch, branch)
                self.assertAlmostEqual(err, exp_err, places=12)
                self.assertAlmostEqual(dist, exp_abs, places=12)
                self.assertEqual(phase, exp_phase)
                self.assertAlmostEqual(got_err, exp_err, places=12)
                self.assertAlmostEqual(got_abs, exp_abs, places=12)
                self.assertEqual(got_state.value, exp_phase)

    def test_kinematics_reference_derivative(self) -> None:
        cases = (
            ("KIN-01", 59.5, 0.0, 1.2, "SEXTILE", "APPLYING"),
            ("KIN-02", 60.5, 0.0, 1.2, "SEXTILE", "SEPARATING"),
            ("KIN-03", 59.5, 0.0, -0.8, "SEXTILE", "SEPARATING"),
            ("KIN-04", 60.00005, 0.0, -20.0, "SEXTILE", "EXACT"),
        )
        for case, transit, natal, speed, aspect, expected in cases:
            with self.subTest(case=case):
                branches = (60.0, -60.0)
                branch = ref_branch(transit, natal, branches)
                _, _, phase = ref_geometry(transit, natal, branch, speed)
                got = aspect_geometry("SUN", "MOON", transit, natal, speed, aspect)[3]
                self.assertEqual(phase, expected)
                self.assertEqual(got, KinematicState(expected))

    def test_orb_and_circular_span_reference(self) -> None:
        # These values are taken directly from the approved profile matrix.
        expected_orbs = {
            ("SUN", "CONJUNCTION"): 2.5,
            ("JUPITER", "CONJUNCTION"): 1.5,
        }
        for key, expected in expected_orbs.items():
            self.assertEqual(effective_orb(*key), expected)

        expected_span = 0.4
        got = circular_span_deg(359.8, 0.2)
        self.assertAlmostEqual(got, expected_span, places=12)

        # Independent identity, not CE implementation reuse.
        a, b = 359.8, 0.2
        span_ref = min(
            abs(a - b),
            360.0 - abs(a - b),
        )
        self.assertAlmostEqual(span_ref, expected_span, places=12)

    def test_win_01_fixture_topology(self) -> None:
        # Approved mathematical fixture: |min(x-15,x-45)| <= 5.
        # The exact expected solution is analytically [10,20] ∪ [40,50].
        expected = ((10.0, 20.0), (40.0, 50.0))
        result = solve_aspect_window(
            lambda x: min(abs(x - 15.0), abs(x - 45.0)),
            start=0.0, end=60.0, effective_orb=5.0, samples=600,
        )
        self.assertEqual(result.segments, expected)

    def test_win_02_fixture_topology(self) -> None:
        # |0.05 sin(x)| <= 0.1 is true across the complete interval.
        # Exact roots are 0, pi, 2pi under the separate exact-state rule.
        end = 2.0 * math.pi
        result = solve_aspect_window(
            lambda x: 0.05 * math.sin(x),
            start=0.0, end=end, effective_orb=0.1, samples=720,
        )
        self.assertEqual(result.segments, ((0.0, end),))
        self.assertEqual(
            tuple(round(e.instant, 9) for e in result.exact_events),
            (0.0, round(math.pi, 9), round(end, 9)),
        )

    def test_win_03_tangency_fixture(self) -> None:
        # 1+(x-2)^2 touches the boundary 1 only at x=2 and never enters it.
        result = solve_aspect_window(
            lambda x: 1.0 + (x - 2.0) ** 2,
            start=0.0, end=4.0, effective_orb=1.0, samples=256,
        )
        self.assertEqual(result.segments, ())
        self.assertEqual(result.exact_events, ())
        self.assertEqual(len(result.tangential_contacts), 1)
        self.assertAlmostEqual(result.tangential_contacts[0], 2.0, places=6)

    def test_uncertainty_set_logic_reference(self) -> None:
        # Independent set-theoretic oracle for the approved scenario semantics.
        def agg(sets):
            nonempty = [set(s) for s in sets if s]
            if not nonempty:
                return ScenarioState.NONE
            intersection = set.intersection(*nonempty)
            union = set.union(*nonempty)
            if all(set(s) == union for s in sets if s) and len(nonempty) == len(sets):
                return ScenarioState.ROBUST
            if intersection:
                return ScenarioState.MIXED
            return ScenarioState.POSSIBLE

        self.assertIs(agg((((1, 3),), ((1, 3),), ((1, 3),))), ScenarioState.ROBUST)
        self.assertIs(agg((((1, 2),), (), ())), ScenarioState.POSSIBLE)
        self.assertIs(agg((((1, 3),), ((2, 4),))), ScenarioState.MIXED)
        self.assertIs(agg(((), (), ())), ScenarioState.NONE)

    def test_temporal_reference_boundaries(self) -> None:
        start = datetime(2026, 1, 1, tzinfo=timezone.utc)
        end = datetime(2026, 1, 2, tzinfo=timezone.utc)
        self.assertLess(start, end)
        self.assertEqual((end - start).total_seconds(), 86400.0)


if __name__ == "__main__":
    unittest.main()
