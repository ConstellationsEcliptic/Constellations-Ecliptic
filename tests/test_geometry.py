from __future__ import annotations

import math
import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from ce.calculation.geometry import circular_separation_deg, normalize_longitude_deg, signed_angular_deviation_deg


class GeometryTests(unittest.TestCase):
    def test_normalize(self) -> None:
        self.assertEqual(normalize_longitude_deg(-1.0), 359.0)
        self.assertEqual(normalize_longitude_deg(361.0), 1.0)

    def test_separation_wrap(self) -> None:
        self.assertEqual(circular_separation_deg(359.0, 1.0), 2.0)

    def test_signed_deviation(self) -> None:
        self.assertAlmostEqual(signed_angular_deviation_deg(10.0, 0.0, 0.0), 10.0)
        self.assertAlmostEqual(signed_angular_deviation_deg(350.0, 0.0, 0.0), -10.0)

    def test_nonfinite_rejected(self) -> None:
        with self.assertRaises(ValueError):
            normalize_longitude_deg(math.nan)

    def test_canonical_branch_and_orb(self) -> None:
        from ce.calculation.geometry import effective_orb, resolve_branch
        self.assertEqual(resolve_branch("SEXTILE", 60.2), 60.0)
        self.assertEqual(resolve_branch("SEXTILE", -59.8), -60.0)
        self.assertEqual(effective_orb("SUN", "CONJUNCTION"), 2.5)
        self.assertEqual(effective_orb("JUPITER", "CONJUNCTION"), 1.5)

    def test_kinematic_direction_is_signed(self) -> None:
        from ce.calculation.geometry import aspect_geometry
        from ce.foundation.status import KinematicState
        _, _, _, state, qualifies = aspect_geometry("SUN", "MOON", 59.0, 0.0, 1.0, "SEXTILE")
        self.assertIs(state, KinematicState.APPLYING)
        self.assertTrue(qualifies)

        _, _, _, state, _ = aspect_geometry("SUN", "MOON", 61.0, 0.0, 1.0, "SEXTILE")
        self.assertIs(state, KinematicState.SEPARATING)

    def test_exact_precedes_motion(self) -> None:
        from ce.calculation.geometry import aspect_geometry
        from ce.foundation.status import KinematicState
        _, _, _, state, _ = aspect_geometry("SUN", "MOON", 60.00005, 0.0, -20.0, "SEXTILE")
        self.assertIs(state, KinematicState.EXACT)
