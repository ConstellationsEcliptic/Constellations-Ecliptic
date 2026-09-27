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

    def test_ephemeris_request_rejects_bool_as_julian_day(self) -> None:
        with self.assertRaises(ValueError):
            EphemerisRequest("sun", True, True)

    def test_unavailable_adapter_returns_invalid_input_for_bad_request(self) -> None:
        with self.assertRaises(ValueError):
            EphemerisRequest("sun", float("inf"), True)
        result = UnavailableSwissEphemerisAdapter().calculate_object(object())  # type: ignore[arg-type]
        self.assertEqual(result.status, CalculationStatus.INVALID_INPUT)

    def test_unavailable_adapter_rejects_raw_arguments_at_interface_boundary(self) -> None:
        with self.assertRaises(TypeError):
            UnavailableSwissEphemerisAdapter().calculate_object(
                "sun", 2451545.0, True
            )  # type: ignore[arg-type]

    def test_valid_request_stays_non_authorized_until_binding_exists(self) -> None:
        request = EphemerisRequest("sun", 2451545.0, True)
        result = UnavailableSwissEphemerisAdapter().calculate_object(request)
        self.assertEqual(result.status, CalculationStatus.NON_AUTHORIZED)
