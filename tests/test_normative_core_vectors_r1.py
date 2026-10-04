from __future__ import annotations

import unittest

from ce.calculation.geometry import (
    aspect_geometry,
    circular_span_deg,
    effective_orb,
)
from ce.calculation.scenario_windows import classify_sampled_windows
from ce.foundation.status import KinematicState, ScenarioState


class NormativeCoreVectorsR1Tests(unittest.TestCase):
    """Bind registered fixture values directly to current behavior.

    This is a fixture-binding suite, not an independent astronomical oracle.
    """

    def test_geo_01_registered_fixture(self) -> None:
        branch, deviation, absolute, _, qualifies = aspect_geometry(
            "SUN", "MOON", 359.5, 0.5, 1.0, "CONJUNCTION"
        )
        self.assertEqual(branch, 0.0)
        self.assertEqual(deviation, -1.0)
        self.assertEqual(absolute, 1.0)
        self.assertTrue(qualifies)

    def test_geo_02_registered_fixture(self) -> None:
        branch, deviation, absolute, state, qualifies = aspect_geometry(
            "SUN", "MOON", 10.0, 100.0, 1.0, "SQUARE"
        )
        self.assertEqual(branch, -90.0)
        self.assertEqual(deviation, 0.0)
        self.assertEqual(absolute, 0.0)
        self.assertIs(state, KinematicState.EXACT)
        self.assertTrue(qualifies)

    def test_kin_01_registered_fixture(self) -> None:
        *_, state, _ = aspect_geometry("SUN", "MOON", 59.5, 0.0, 1.2, "SEXTILE")
        self.assertIs(state, KinematicState.APPLYING)

    def test_kin_02_registered_fixture(self) -> None:
        *_, state, _ = aspect_geometry("SUN", "MOON", 60.5, 0.0, 1.2, "SEXTILE")
        self.assertIs(state, KinematicState.SEPARATING)

    def test_kin_03_registered_fixture(self) -> None:
        *_, state, _ = aspect_geometry("SUN", "MOON", 59.5, 0.0, -0.8, "SEXTILE")
        self.assertIs(state, KinematicState.SEPARATING)

    def test_kin_04_registered_fixture(self) -> None:
        *_, state, _ = aspect_geometry("SUN", "MOON", 60.00005, 0.0, -20.0, "SEXTILE")
        self.assertIs(state, KinematicState.EXACT)

    def test_orb_01_registered_fixture(self) -> None:
        self.assertEqual(effective_orb("SUN", "CONJUNCTION"), 2.5)

    def test_orb_02_registered_fixture(self) -> None:
        self.assertEqual(effective_orb("JUPITER", "CONJUNCTION"), 1.5)

    def test_sta_01_registered_fixture(self) -> None:
        self.assertAlmostEqual(circular_span_deg(359.8, 0.2), 0.4, places=10)

    def test_unc_01_registered_semantics(self) -> None:
        state, possible, robust = classify_sampled_windows(
            (((1.0, 3.0),), ((1.0, 3.0),), ((1.0, 3.0),))
        )
        self.assertIs(state, ScenarioState.ROBUST)
        self.assertEqual(possible, ((1.0, 3.0),))
        self.assertEqual(robust, ((1.0, 3.0),))

    def test_unc_02_registered_semantics(self) -> None:
        state, possible, robust = classify_sampled_windows(
            (((1.0, 2.0),), (), ())
        )
        self.assertIs(state, ScenarioState.POSSIBLE)
        self.assertEqual(possible, ((1.0, 2.0),))
        self.assertEqual(robust, ())

    def test_unc_03_registered_semantics(self) -> None:
        state, possible, robust = classify_sampled_windows(
            (((1.0, 3.0),), ((2.0, 4.0),))
        )
        self.assertIs(state, ScenarioState.MIXED)
        self.assertEqual(possible, ((1.0, 4.0),))
        self.assertEqual(robust, ((2.0, 3.0),))

    def test_unc_04_registered_semantics(self) -> None:
        state, possible, robust = classify_sampled_windows(((), (), ()))
        self.assertIs(state, ScenarioState.NONE)
        self.assertEqual(possible, ())
        self.assertEqual(robust, ())


if __name__ == "__main__":
    unittest.main()
