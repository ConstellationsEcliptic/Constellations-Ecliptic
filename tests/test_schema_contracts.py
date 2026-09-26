from __future__ import annotations

import json
import os
import re
import sys
import unittest
from pathlib import Path
from typing import Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from ce.foundation.status import CalculationStatus, ScenarioState


ROOT = Path(__file__).resolve().parents[1]


def _type_matches(instance: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(instance, dict)
    if expected == "array":
        return isinstance(instance, list)
    if expected == "string":
        return isinstance(instance, str)
    if expected == "number":
        return isinstance(instance, (int, float)) and not isinstance(instance, bool)
    if expected == "boolean":
        return isinstance(instance, bool)
    if expected == "null":
        return instance is None
    return False


def _validate_schema_instance(schema: dict[str, Any], instance: Any, path: str = "$") -> list[str]:
    errors: list[str] = []

    if "type" in schema:
        expected_types = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
        if not any(_type_matches(instance, expected) for expected in expected_types):
            errors.append(f"{path}:type")
            return errors

    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}:enum")

    if "const" in schema and instance != schema["const"]:
        errors.append(f"{path}:const")

    if "not" in schema and not _validate_schema_instance(schema["not"], instance, path):
        errors.append(f"{path}:not")

    if "required" in schema and isinstance(instance, dict):
        for name in schema["required"]:
            if name not in instance:
                errors.append(f"{path}.missing:{name}")

    if isinstance(instance, dict):
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            for name in instance:
                if name not in properties:
                    errors.append(f"{path}.unexpected:{name}")
        for name, child in properties.items():
            if name in instance:
                errors.extend(_validate_schema_instance(child, instance[name], f"{path}.{name}"))
    elif isinstance(instance, list):
        if "minItems" in schema and len(instance) < schema["minItems"]:
            errors.append(f"{path}:minItems")
        if "maxItems" in schema and len(instance) > schema["maxItems"]:
            errors.append(f"{path}:maxItems")
        if "items" in schema:
            child = schema["items"]
            errors.extend(
                _validate_schema_instance(child, item, f"{path}[{index}]")
                for index, item in enumerate(instance)
            )
            errors = [item for group in errors for item in (group if isinstance(group, list) else [group])]
        if "contains" in schema and not any(
            not _validate_schema_instance(schema["contains"], item, f"{path}[{index}]")
            for index, item in enumerate(instance)
        ):
            errors.append(f"{path}:contains")
    elif isinstance(instance, str):
        if "minLength" in schema and len(instance) < schema["minLength"]:
            errors.append(f"{path}:minLength")
        if "pattern" in schema and re.fullmatch(schema["pattern"], instance) is None:
            errors.append(f"{path}:pattern")
    elif isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if "minimum" in schema and instance < schema["minimum"]:
            errors.append(f"{path}:minimum")
        if "exclusiveMaximum" in schema and instance >= schema["exclusiveMaximum"]:
            errors.append(f"{path}:exclusiveMaximum")

    if "allOf" in schema:
        for branch in schema["allOf"]:
            errors.extend(_validate_schema_instance(branch, instance, path))

    if "if" in schema:
        if not _validate_schema_instance(schema["if"], instance, path) and "then" in schema:
            errors.extend(_validate_schema_instance(schema["then"], instance, path))

    return errors


class SchemaContractTests(unittest.TestCase):
    def _schema(self, name: str) -> dict[str, Any]:
        return json.loads((ROOT / "schemas" / name).read_text(encoding="utf-8"))

    def _provenance(self) -> dict[str, str]:
        return {
            "source_commit": "a" * 40,
            "source_tree_sha256_v2": "b" * 64,
            "dependency_lock_digest": "c" * 64,
            "timezone_bundle_digest": "d" * 64,
            "ephemeris_bundle_digest": "e" * 64,
            "runtime_image_digest": "sha256:" + "f" * 64,
            "calculation_version": "0.1.0",
        }

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
        self.assertEqual(
            schema["properties"]["provenance"]["properties"]["source_commit"]["pattern"],
            "^[0-9a-fA-F]{40}$",
        )
        self.assertTrue(any("if" in branch and "then" in branch for branch in schema["allOf"]))

    def test_signal_schema_excludes_semantic_payload_from_nonvalid_states(self) -> None:
        schema = self._schema("signal_result.schema.json")
        result = {
            "status": "NON_AUTHORIZED",
            "classification": "appears-authoritative",
            "phase": None,
            "uncertainty_state": None,
            "evidence_packet_ref": None,
            "canon_input_valid": False,
            "provenance": {},
        }
        self.assertTrue(_validate_schema_instance(schema, result))

    def test_calculation_schema_accepts_valid_instance_and_rejects_contradictions(self) -> None:
        schema = self._schema("calculation_result.schema.json")
        valid = {
            "request_id": "R1",
            "status": "VALID",
            "execution_profile_id": "CE-CALC-V1-EP-001",
            "scenario_state": "STABLE",
            "normalized_time": "2026-01-01T00:00:00Z",
            "object_states": [{
                "object_id": "sun",
                "longitude_deg": 12.5,
                "speed_deg_per_day": 0.9,
                "status": "VALID",
            }],
            "warnings": [],
            "errors": [],
            "provenance": self._provenance(),
        }
        self.assertEqual(_validate_schema_instance(schema, valid), [])

        malformed_provenance = {**valid, "provenance": {**self._provenance(), "source_commit": "bad"}}
        self.assertTrue(_validate_schema_instance(schema, malformed_provenance))

        contradictory_object = {
            **valid,
            "object_states": [{
                "object_id": "sun",
                "longitude_deg": None,
                "speed_deg_per_day": None,
                "status": "NON_AUTHORIZED",
            }],
        }
        self.assertTrue(_validate_schema_instance(schema, contradictory_object))

        nonvalid_with_valid_object = {
            **valid,
            "status": "CALCULATION_FAILURE",
            "object_states": [{
                "object_id": "sun",
                "longitude_deg": 12.5,
                "speed_deg_per_day": 0.9,
                "status": "VALID",
            }],
        }
        self.assertTrue(_validate_schema_instance(schema, nonvalid_with_valid_object))

    def test_schema_instance_verifier_rejects_bool_as_number(self) -> None:
        schema = self._schema("calculation_result.schema.json")
        invalid = {
            "request_id": "R1",
            "status": "VALID",
            "execution_profile_id": "CE-CALC-V1-EP-001",
            "scenario_state": "STABLE",
            "normalized_time": "2026-01-01T00:00:00Z",
            "object_states": [{
                "object_id": "sun",
                "longitude_deg": True,
                "speed_deg_per_day": 0.9,
                "status": "VALID",
            }],
            "warnings": [],
            "errors": [],
            "provenance": self._provenance(),
        }
        self.assertTrue(_validate_schema_instance(schema, invalid))
