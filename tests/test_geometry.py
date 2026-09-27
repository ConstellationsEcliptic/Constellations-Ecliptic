from __future__ import annotations

import math
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from ce.calculation.geometry import (
    circular_separation_deg,
    normalize_longitude_deg,
    signed_angular_deviation_deg,
)


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

    def test_bool_is_rejected_as_numeric_geometry_input(self) -> None:
        with self.assertRaises(ValueError):
            normalize_longitude_deg(True)
        with self.assertRaises(ValueError):
            normalize_longitude_deg(False)
        with self.assertRaises(ValueError):
            circular_separation_deg(1.0, True)
        with self.assertRaises(ValueError):
            signed_angular_deviation_deg(1.0, 2.0, True)
