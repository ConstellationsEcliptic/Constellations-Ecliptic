from __future__ import annotations

from datetime import datetime, timezone
import unittest

from ce.calculation.scenario_windows import canonical_utc


class CER0TemporalCanonicalizationTests(unittest.TestCase):
    def test_canonical_utc_preserves_microseconds(self):
        a = canonical_utc(datetime(2026, 1, 1, 0, 0, 0, 123456, tzinfo=timezone.utc))
        b = canonical_utc(datetime(2026, 1, 1, 0, 0, 0, 654321, tzinfo=timezone.utc))
        self.assertNotEqual(a, b, "SUBSECOND INSTANTS COLLAPSE IN CANONICAL UTC")
        self.assertEqual(a, "2026-01-01T00:00:00.123456Z")
