from __future__ import annotations

from datetime import datetime, timezone
import unittest

from ce.calculation.scenario_windows import canonical_utc, scenario_id


class CER0TemporalCanonicalizationAcceptanceTests(unittest.TestCase):
    def test_subsecond_instants_must_not_collapse_during_canonicalization(self) -> None:
        a = datetime(2026, 1, 1, 0, 0, 0, 100000, tzinfo=timezone.utc)
        b = datetime(2026, 1, 1, 0, 0, 0, 900000, tzinfo=timezone.utc)
        self.assertNotEqual(
            canonical_utc(a),
            canonical_utc(b),
            "canonical time must preserve the precision permitted by the input contract",
        )

    def test_subsecond_scenario_id_must_remain_distinct(self) -> None:
        target_scope = {"object": "SUN"}
        a = datetime(2026, 1, 1, 0, 0, 0, 100000, tzinfo=timezone.utc)
        b = datetime(2026, 1, 1, 0, 0, 0, 900000, tzinfo=timezone.utc)
        self.assertNotEqual(
            scenario_id(
                birth_instant_utc=canonical_utc(a),
                target_scope=target_scope,
            ),
            scenario_id(
                birth_instant_utc=canonical_utc(b),
                target_scope=target_scope,
            ),
        )


if __name__ == "__main__":
    unittest.main()
