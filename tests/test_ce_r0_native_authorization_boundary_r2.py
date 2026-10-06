from __future__ import annotations

import inspect
import unittest

from ce.ephemeris.native_runtime import NativeSwissCalculation, NativeSwissEphemerisAdapter


class CER0NativeAuthorizationBoundaryTests(unittest.TestCase):
    def test_native_adapter_must_not_accept_caller_boolean_authorization(self):
        signature = inspect.signature(NativeSwissEphemerisAdapter.__init__)
        parameter = signature.parameters.get("runtime_authorized")
        self.assertIsNone(
            parameter,
            "CALLER-SUPPLIED runtime_authorized: bool REMAINS A FUTURE AUTHORITY BYPASS",
        )

    def test_native_diagnostics_are_preserved(self):
        detailed = NativeSwissCalculation(
            object_id="SUN",
            swiss_object_id=0,
            jd_ut=2451545.0,
            longitude_deg=1.0,
            latitude_deg=0.0,
            distance_au=1.0,
            speed_deg_per_day=1.0,
            requested_flags=258,
            actual_flags=258,
            ephemeris="SWIEPH",
            warning_or_error="NATIVE-WARNING",
        )
        record = detailed.to_object_record()
        self.assertEqual(record.warnings, ("NATIVE-WARNING",))
        self.assertEqual(record.errors, ())


if __name__ == "__main__":
    unittest.main()
