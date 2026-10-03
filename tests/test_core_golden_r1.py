from __future__ import annotations

import math
import unittest

from ce.calculation.geometry import (
    aspect_geometry,
    circular_span_deg,
    effective_orb,
    normalize_longitude_deg,
    resolve_branch,
)
from ce.foundation.status import KinematicState


class CoreGoldenR1Tests(unittest.TestCase):
    # GEO-01
    def test_geo_01_circular_boundary(self) -> None:
        self.assertAlmostEqual(normalize_longitude_deg(-0.2), 359.8)
        self.assertAlmostEqual(normalize_longitude_deg(360.2), 0.2)

    # GEO-02
    def test_geo_02_exact_square(self) -> None:
        branch, deviation, absolute, state, qualifies = aspect_geometry(
            "SUN", "MOON", 90.00001, 0.0, 0.1, "SQUARE"
        )
        self.assertEqual(branch, 90.0)
        self.assertLessEqual(absolute, 1.0e-4)
        self.assertEqual(state, KinematicState.EXACT)
        self.assertTrue(qualifies)
        self.assertAlmostEqual(deviation, 0.00001, places=5)

    # KIN-01
    def test_kin_01_applying(self) -> None:
        *_, state, _ = aspect_geometry("SUN", "MOON", 59.0, 0.0, 1.2, "SEXTILE")
        self.assertEqual(state, KinematicState.APPLYING)

    # KIN-02
    def test_kin_02_separating(self) -> None:
        *_, state, _ = aspect_geometry("SUN", "MOON", 61.0, 0.0, 1.2, "SEXTILE")
        self.assertEqual(state, KinematicState.SEPARATING)

    # KIN-03
    def test_kin_03_retrograde_separating(self) -> None:
        *_, state, _ = aspect_geometry("SUN", "MOON", 59.0, 0.0, -0.8, "SEXTILE")
        self.assertEqual(state, KinematicState.SEPARATING)

    # KIN-04
    def test_kin_04_exact_precedence(self) -> None:
        *_, state, _ = aspect_geometry("SUN", "MOON", 60.00005, 0.0, -20.0, "SEXTILE")
        self.assertEqual(state, KinematicState.EXACT)

    # ORB-01
    def test_orb_01_profile_a(self) -> None:
        self.assertEqual(effective_orb("SUN", "CONJUNCTION"), 2.5)

    # ORB-02
    def test_orb_02_profile_b(self) -> None:
        self.assertEqual(effective_orb("JUPITER", "CONJUNCTION"), 1.5)

    # STA-01
    def test_sta_01_circular_span(self) -> None:
        self.assertAlmostEqual(circular_span_deg(359.8, 0.2), 0.4, places=10)


if __name__ == "__main__":
    unittest.main()
