from __future__ import annotations

import json
import os
import re
import sys
import unittest
from pathlib import Path
from typing import Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from ce.calculation.evidence import EvidencePacket
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
        additional_properties = schema.get("additionalProperties")
        if additional_properties is False:
            for name in instance:
                if name not in properties:
                    errors.append(f"{path}.unexpected:{name}")
        elif isinstance(additional_properties, dict):
            for name, value in instance.items():
                if name not in properties:
                    errors.extend(
                        _validate_schema_instance(
                            additional_properties, value, f"{path}.{name}"
                        )
                    )
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
        calculation_status_values = {item.value for item in CalculationStatus}
        self.assertEqual(
            set(schema["properties"]["status"]["enum"]),
            calculation_status_values,
        )
        self.assertEqual(
            set(schema["properties"]["object_states"]["items"]["properties"]["status"]["enum"]),
            calculation_status_values,
        )
        self.assertEqual(
            set(schema["properties"]["scenario_state"]["enum"]),
            {item.value for item in ScenarioState},
        )
        signal_schema = self._schema("signal_result.schema.json")
        self.assertEqual(
            set(signal_schema["properties"]["status"]["enum"]),
            calculation_status_values,
        )
        signal_nonvalid = {
            value
            for branch in signal_schema["allOf"]
            for value in branch.get("if", {}).get("properties", {}).get("status", {}).get("enum", [])
        }
        self.assertTrue(signal_nonvalid.issubset(calculation_status_values))
        self.assertIn("evidence_packet_ref", schema["required"])
        self.assertEqual(
            schema["properties"]["provenance"]["properties"]["source_commit"]["pattern"],
            "^[0-9a-fA-F]{40}$",
        )
        self.assertTrue(any("if" in branch and "then" in branch for branch in schema["allOf"]))

    def test_nonvalid_calculation_schema_rejects_authority_looking_provenance(self) -> None:
        schema = self._schema("calculation_result.schema.json")
        base = {
            "request_id": "R1",
            "status": "NON_AUTHORIZED",
            "execution_profile_id": "CE-CALC-V1-EP-001",
            "scenario_state": "NONE",
            "normalized_time": None,
            "object_states": [],
            "evidence_packet_ref": None,
            "warnings": [],
            "errors": ["not-authorized"],
            "provenance": {},
        }
        self.assertEqual(_validate_schema_instance(schema, base), [])

        for field_name in (
            "source_commit",
            "source_tree_sha256_v2",
            "dependency_lock_digest",
            "timezone_bundle_digest",
            "ephemeris_bundle_digest",
            "runtime_image_digest",
            "calculation_version",
        ):
            invalid = {**base, "provenance": {field_name: "a" * 64}}
            self.assertTrue(_validate_schema_instance(schema, invalid), field_name)

        authorized_metadata = {
            **base,
            "provenance": {"runtime_authority": "AUTHORIZED"},
        }
        self.assertTrue(_validate_schema_instance(schema, authorized_metadata))

        non_authorized_metadata = {
            **base,
            "provenance": {"runtime_authority": "NON_AUTHORIZED"},
        }
        self.assertEqual(_validate_schema_instance(schema, non_authorized_metadata), [])

    def test_provenance_extra_values_match_scalar_schema_domain(self) -> None:
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
            "evidence_packet_ref": {
                "evidence_packet_id": "E-REG-001",
                "content_sha256": "a" * 64,
            },
            "provenance": {
                **self._provenance(),
                "trace": "runtime-check",
            },
        }
        self.assertEqual(_validate_schema_instance(schema, valid), [])

        nested_extra = {
            **valid,
            "provenance": {
                **self._provenance(),
                "trace": {"nested": "value"},
            },
        }
        self.assertTrue(_validate_schema_instance(schema, nested_extra))

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
            "evidence_packet_ref": {
                "evidence_packet_id": "E-REG-001",
                "content_sha256": "a" * 64,
            },
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

    def test_evidence_reference_schema_requires_compound_identity(self) -> None:
        calculation = self._schema("calculation_result.schema.json")
        signal = self._schema("signal_result.schema.json")
        compound_ref = {
            "evidence_packet_id": "E-SCHEMA-001",
            "content_sha256": "a" * 64,
        }
        valid_calculation = {
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
            "evidence_packet_ref": compound_ref,
            "provenance": self._provenance(),
        }
        self.assertEqual(_validate_schema_instance(calculation, valid_calculation), [])

        valid_signal = {
            "status": "VALID",
            "classification": "classification",
            "phase": "phase",
            "uncertainty_state": "uncertain",
            "evidence_packet_ref": compound_ref,
            "canon_input_valid": True,
            "provenance": self._provenance(),
        }
        self.assertEqual(_validate_schema_instance(signal, valid_signal), [])

        malformed_ref = dict(compound_ref)
        malformed_ref["content_sha256"] = "not-a-sha256"
        self.assertTrue(
            _validate_schema_instance(
                signal,
                {**valid_signal, "evidence_packet_ref": malformed_ref},
            )
        )

        partial_ref = {"evidence_packet_id": "E-SCHEMA-001"}
        self.assertTrue(
            _validate_schema_instance(
                calculation,
                {**valid_calculation, "evidence_packet_ref": partial_ref},
            )
        )

        nonvalid_signal = {
            **valid_signal,
            "status": "NON_AUTHORIZED",
            "classification": None,
            "phase": None,
            "uncertainty_state": None,
            "evidence_packet_ref": None,
            "canon_input_valid": False,
            "provenance": {},
        }
        self.assertEqual(_validate_schema_instance(signal, nonvalid_signal), [])

    def test_signal_schema_valid_requires_complete_provenance(self) -> None:
        schema = self._schema("signal_result.schema.json")
        valid = {
            "status": "VALID",
            "classification": "classification",
            "phase": "phase",
            "uncertainty_state": "uncertain",
            "evidence_packet_ref": {
                "evidence_packet_id": "E-SCHEMA-001",
                "content_sha256": "a" * 64,
            },
            "canon_input_valid": True,
            "provenance": self._provenance(),
        }
        self.assertEqual(_validate_schema_instance(schema, valid), [])

        missing = {**valid, "provenance": {}}
        self.assertTrue(_validate_schema_instance(schema, missing))

        authorized_nonvalid = {
            **valid,
            "status": "NON_AUTHORIZED",
            "classification": None,
            "phase": None,
            "uncertainty_state": None,
            "evidence_packet_ref": None,
            "canon_input_valid": False,
            "provenance": {"runtime_authority": "AUTHORIZED"},
        }
        self.assertTrue(_validate_schema_instance(schema, authorized_nonvalid))

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
            "evidence_packet_ref": {
                "evidence_packet_id": "E-REG-001",
                "content_sha256": "a" * 64,
            },
            "provenance": self._provenance(),
        }
        self.assertTrue(_validate_schema_instance(schema, invalid))

    def test_evidence_packet_python_and_schema_contracts_align_for_established_semantics(self) -> None:
        schema = self._schema("evidence_packet.schema.json")
        packet_kwargs = {
            "evidence_packet_id": "E-REG-001",
            "input_identity": {"value": "x"},
            "profile_version": {"id": "CE-CALC-V1-EP-001", "revision": 2},
            "observation_instant_or_interval": {"start": "2000-01-01T00:00:00Z"},
            "timezone_context": {"id": "UTC", "version": "NOT_ESTABLISHED"},
            "execution_profile_id": "CE-CALC-V1-EP-001",
            "calculation_version": "0.1.0",
            "object_records": ({"object_id": "sun"},),
            "geometry_records": ({"kind": "angular_separation"},),
            "kinematics": ({"object_id": "sun"},),
            "warnings": ("warning",),
            "errors": (),
            "numerical_tolerances": {"exact_tolerance_deg": 1e-4},
            "solver_metadata": {},
            "actual_ephemeris_resolution": {"status": "NOT_ESTABLISHED"},
            "calculation_flags": {},
        }
        valid_packet = EvidencePacket(**packet_kwargs)
        valid_instance = json.loads(valid_packet.canonical_bytes().decode("utf-8"))
        self.assertEqual(_validate_schema_instance(schema, valid_instance), [])

        invalid_cases = (
            ("evidence_packet_id", 123),
            ("execution_profile_id", "CE-CALC-V1-EP-ALT"),
            ("calculation_version", 123),
            ("input_identity", []),
            ("object_records", [1]),
            ("geometry_records", ["not-an-object"]),
            ("kinematics", [None]),
            ("warnings", [123]),
            ("errors", [False]),
        )
        for field_name, invalid_value in invalid_cases:
            instance = dict(valid_instance)
            instance[field_name] = invalid_value
            self.assertTrue(_validate_schema_instance(schema, instance), field_name)

            python_kwargs = dict(packet_kwargs)
            python_kwargs[field_name] = invalid_value
            with self.assertRaises(ValueError, msg=field_name):
                EvidencePacket(**python_kwargs)

