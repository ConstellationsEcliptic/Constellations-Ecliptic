from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class CER0EvidenceSchemaStrictnessTests(unittest.TestCase):
    def test_evidence_packet_critical_maps_are_closed(self):
        schema = json.loads((ROOT / "schemas" / "evidence_packet.schema.json").read_text(encoding="utf-8"))
        for field in (
            "input_identity",
            "timezone_context",
            "numerical_tolerances",
            "solver_metadata",
            "actual_ephemeris_resolution",
            "calculation_flags",
            "scenario_observations",
        ):
            self.assertFalse(
                schema["properties"][field].get("additionalProperties", True),
                f"CRITICAL EVIDENCE FIELD {field} REMAINS OPEN-ENDED",
            )
