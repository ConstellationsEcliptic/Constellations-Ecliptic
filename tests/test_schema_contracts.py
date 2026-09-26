from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from ce.foundation.status import CalculationStatus, ScenarioState


ROOT = Path(__file__).resolve().parents[1]


class SchemaContractTests(unittest.TestCase):
    def _schema(self, name: str) -> dict:
        return json.loads((ROOT / "schemas" / name).read_text(encoding="utf-8"))

    def test_calculation_schema_is_strict_and_semantic(self) -> None:
        schema = self._schema("calculation_result.schema.json")
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(
            set(schema["properties"]["status"]["enum"]),
            {item.value for item in CalculationStatus},
        )
        self.assertEqual(
            set(schema["properties"]["scenario_state"]["enum"]),
            {item.value for item in ScenarioState},
        )
        self.assertIn("provenance", schema["required"])
        self.assertTrue(any("if" in branch and "then" in branch for branch in schema["allOf"]))

    def test_evidence_schema_covers_all_current_fields(self) -> None:
        schema = self._schema("evidence_packet.schema.json")
        self.assertFalse(schema["additionalProperties"])
        expected = {
            "evidence_packet_id", "input_identity", "profile_version",
            "observation_instant_or_interval", "timezone_context",
            "execution_profile_id", "calculation_version", "object_records",
            "geometry_records", "kinematics", "warnings", "errors",
            "numerical_tolerances", "solver_metadata",
            "actual_ephemeris_resolution", "calculation_flags",
        }
        self.assertTrue(expected.issubset(schema["required"]))
        self.assertIn("execution_profile_id", schema["properties"])

    def test_signal_schema_enforces_valid_branch(self) -> None:
        schema = self._schema("signal_result.schema.json")
        self.assertFalse(schema["additionalProperties"])
        valid_branch = schema["allOf"][0]["then"]
        self.assertEqual(valid_branch["properties"]["canon_input_valid"]["const"], True)
        self.assertIn("classification", valid_branch["required"])
