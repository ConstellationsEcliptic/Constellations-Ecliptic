from __future__ import annotations

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from ce.ephemeris.adapter import EphemerisRequest, UnavailableSwissEphemerisAdapter
from ce.foundation.status import CalculationStatus


class EphemerisContractTests(unittest.TestCase):
    def test_ephemeris_request_rejects_nonfinite_julian_day(self) -> None:
        with self.assertRaises(ValueError):
            EphemerisRequest("sun", float("nan"), True)

    def test_unavailable_adapter_returns_invalid_input_for_bad_request(self) -> None:
        result = UnavailableSwissEphemerisAdapter().calculate_object("", float("inf"), True)
        self.assertEqual(result.status, CalculationStatus.INVALID_INPUT)

    def test_valid_request_stays_non_authorized_until_binding_exists(self) -> None:
        result = UnavailableSwissEphemerisAdapter().calculate_object("sun", 2451545.0, True)
        self.assertEqual(result.status, CalculationStatus.NON_AUTHORIZED)
