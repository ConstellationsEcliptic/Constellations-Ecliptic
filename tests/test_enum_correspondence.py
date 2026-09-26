from __future__ import annotations

import json
import os
import sys
import unittest
from enum import Enum
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from ce.foundation.status import CalculationStatus, ScenarioState


ROOT = Path(__file__).resolve().parents[1]


def _schema(name: str) -> dict:
    return json.loads((ROOT / "schemas" / name).read_text(encoding="utf-8"))


def _enum_values(enum_type: type[Enum]) -> set[str]:
    return {member.value for member in enum_type}


def _assert_enum_correspondence(
    testcase: unittest.TestCase,
    label: str,
    python_values: set[str],
    schema_values: set[str],
) -> None:
    missing_from_schema = sorted(python_values - schema_values)
    missing_from_python = sorted(schema_values - python_values)
    testcase.assertEqual(
        missing_from_schema,
        [],
        msg=f"{label}: missing_from_schema={missing_from_schema}; "
        f"missing_from_python={missing_from_python}",
    )
    testcase.assertEqual(
        missing_from_python,
        [],
        msg=f"{label}: missing_from_schema={missing_from_schema}; "
        f"missing_from_python={missing_from_python}",
    )


class EnumCorrespondenceTests(unittest.TestCase):
    def test_calculation_result_status_correspondence(self) -> None:
        schema = _schema("calculation_result.schema.json")
        python_values = _enum_values(CalculationStatus)
        schema_values = set(schema["properties"]["status"]["enum"])
        _assert_enum_correspondence(
            self,
            "CalculationResult.status",
            python_values,
            schema_values,
        )

    def test_calculation_result_object_status_correspondence(self) -> None:
        schema = _schema("calculation_result.schema.json")
        python_values = _enum_values(CalculationStatus)
        schema_values = set(
            schema["properties"]["object_states"]["items"]["properties"]["status"]["enum"]
        )
        _assert_enum_correspondence(
            self,
            "CalculationResult.object_states[].status",
            python_values,
            schema_values,
        )

    def test_signal_result_status_correspondence(self) -> None:
        schema = _schema("signal_result.schema.json")
        python_values = _enum_values(CalculationStatus)
        schema_values = set(schema["properties"]["status"]["enum"])
        _assert_enum_correspondence(
            self,
            "SignalResult.status",
            python_values,
            schema_values,
        )

    def test_calculation_result_scenario_state_correspondence(self) -> None:
        schema = _schema("calculation_result.schema.json")
        python_values = _enum_values(ScenarioState)
        schema_values = set(schema["properties"]["scenario_state"]["enum"])
        _assert_enum_correspondence(
            self,
            "CalculationResult.scenario_state",
            python_values,
            schema_values,
        )


if __name__ == "__main__":
    unittest.main()
