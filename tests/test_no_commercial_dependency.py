from __future__ import annotations

import inspect
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from ce.calculation.engine import CalculationEngine
from ce.calculation.geometry import circular_separation_deg, signed_angular_deviation_deg


class CommercialIndependenceTests(unittest.TestCase):
    def test_calculation_modules_have_no_commercial_imports(self) -> None:
        modules = [CalculationEngine, circular_separation_deg, signed_angular_deviation_deg]
        banned = ("credits", "payment", "commerce", "retention", "advertising")
        for obj in modules:
            source = inspect.getsource(obj)
            lowered = source.lower()
            self.assertFalse(any(term in lowered for term in banned), obj)
