from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class SchemaStructureR1Tests(unittest.TestCase):
    def _load_without_duplicate_keys(self, path: Path) -> dict:
        def hook(pairs):
            seen = set()
            result = {}
            for key, value in pairs:
                if key in seen:
                    raise AssertionError(f"duplicate_json_key:{key}")
                seen.add(key)
                result[key] = value
            return result
        return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=hook)

    def test_current_schemas_have_no_duplicate_keys_and_parse(self) -> None:
        for name in (
            "calculation_result.schema.json",
            "evidence_packet.schema.json",
            "signal_result.schema.json",
            "qualified_signal_record.schema.json",
            "runtime_environment_identity_r1.schema.json",
            "runtime_capture_r2.schema.json",
        ):
            schema = self._load_without_duplicate_keys(ROOT / "schemas" / name)
            self.assertEqual(schema["type"], "object")
            self.assertFalse(schema["additionalProperties"])

    def test_canon_rule_condition_schema_is_closed_and_matches_supported_selectors(self) -> None:
        schema = self._load_without_duplicate_keys(ROOT / "schemas" / "canon_rule.schema.json")
        condition = schema["properties"]["condition"]
        self.assertFalse(condition["additionalProperties"])
        self.assertEqual(condition["minProperties"], 1)
        self.assertEqual(
            set(condition["properties"]),
            {
                "classification",
                "kinematic_phase",
                "phase_uniformity",
                "requires_uncertainty_disclaimer",
                "transit_object",
                "natal_object_or_scenario",
                "aspect",
                "directed_branch",
            },
        )
        self.assertEqual(
            condition["properties"]["kinematic_phase"]["enum"],
            ["EXACT", "APPLYING", "SEPARATING", "MIXED"],
        )
        self.assertEqual(condition["properties"]["directed_branch"]["type"], "number")

    def test_runtime_capture_r2_schema_pins_control_plane_and_abi(self) -> None:
        schema = self._load_without_duplicate_keys(ROOT / "schemas" / "runtime_capture_r2.schema.json")
        self.assertIn("control_plane_sha256", schema["required"])
        self.assertEqual(schema["properties"]["calling_convention"]["const"], "__cdecl")

    def test_runtime_capture_r2_schema_has_explicit_environment_one_of(self) -> None:
        schema = self._load_without_duplicate_keys(ROOT / "schemas" / "runtime_capture_r2.schema.json")
        self.assertEqual(len(schema["oneOf"]), 2)
        self.assertEqual(schema["oneOf"][0]["properties"]["runtime_environment_kind"]["const"], "OCI_IMAGE")
        self.assertEqual(schema["oneOf"][1]["properties"]["runtime_environment_kind"]["const"], "HOST_NATIVE")
        self.assertEqual(schema["oneOf"][0]["properties"]["runtime_image_digest"]["type"], "string")
        self.assertEqual(schema["oneOf"][1]["properties"]["runtime_image_digest"]["type"], "null")

    def test_runtime_environment_identity_schema_is_host_native_only(self) -> None:
        schema = self._load_without_duplicate_keys(ROOT / "schemas" / "runtime_environment_identity_r1.schema.json")
        self.assertEqual(schema["properties"]["kind"]["const"], "HOST_NATIVE")
        self.assertEqual(schema["properties"]["schema_version"]["const"], "CE-V1-HOST-NATIVE-ENV-R1")

    def test_calculation_result_schema_contains_status_closures(self) -> None:
        schema = self._load_without_duplicate_keys(ROOT / "schemas" / "calculation_result.schema.json")
        self.assertEqual(len(schema["allOf"]), 3)
        self.assertIn("NATAL_EVIDENCE_VARIABLE", schema["properties"]["status"]["enum"])

    def test_qualified_signal_record_schema_matches_normative_record_shape(self) -> None:
        schema = self._load_without_duplicate_keys(ROOT / "schemas" / "qualified_signal_record.schema.json")
        self.assertEqual(
            set(schema["required"]),
            {
                "schema_version",
                "signal_id",
                "evidence_packet_ref",
                "timestamp_observation_utc",
                "qualification_status",
                "classification",
                "kinematic_phase",
                "phase_uniformity",
                "canon_input_valid",
                "requires_uncertainty_disclaimer",
                "environment_pin",
            },
        )
        self.assertEqual(schema["properties"]["schema_version"]["const"], "CE-QUALIFIED-SIGNAL-RECORD-V1")
        self.assertEqual(schema["properties"]["canon_input_valid"]["const"], True)
        self.assertEqual(
            set(schema["properties"]["phase_uniformity"]["enum"]),
            {"UNIFORM", "MIXED"},
        )

    def test_signal_result_schema_matches_current_result_shape(self) -> None:
        schema = self._load_without_duplicate_keys(ROOT / "schemas" / "signal_result.schema.json")
        self.assertEqual(
            set(schema["required"]),
            {
                "status",
                "classification",
                "phase",
                "uncertainty_state",
                "evidence_packet_ref",
                "canon_input_valid",
            },
        )
        self.assertEqual(schema["properties"]["classification"]["type"], ["string", "null"])
        self.assertEqual(schema["properties"]["phase"]["type"], ["string", "null"])
        self.assertEqual(schema["properties"]["uncertainty_state"]["type"], ["string", "null"])
        self.assertEqual(schema["properties"]["evidence_packet_ref"]["type"], ["string", "null"])

    def test_evidence_packet_schema_uses_strict_record_shapes(self) -> None:
        schema = self._load_without_duplicate_keys(ROOT / "schemas" / "evidence_packet.schema.json")
        self.assertFalse(schema["properties"]["object_records"]["items"]["additionalProperties"])
        self.assertFalse(schema["properties"]["geometry_records"]["items"]["additionalProperties"])
        self.assertFalse(schema["properties"]["window_segments"]["items"]["additionalProperties"])

    def test_evidence_packet_schema_closes_canonical_identity_maps(self) -> None:
        schema = self._load_without_duplicate_keys(ROOT / "schemas" / "evidence_packet.schema.json")
        properties = schema["properties"]

        self.assertFalse(properties["input_identity"]["additionalProperties"])
        self.assertEqual(
            set(properties["input_identity"]["required"]),
            {
                "request_id",
                "birth_date",
                "birth_city",
                "timezone_id",
                "timezone_version",
                "natal_birth_state",
                "calendar_policy_id",
            },
        )

        self.assertFalse(properties["profile_version"]["additionalProperties"])
        self.assertEqual(
            set(properties["profile_version"]["required"]),
            {
                "id",
                "revision",
                "implementation_plan_version",
                "technical_contracts_version",
                "execution_profile_version",
            },
        )

        self.assertFalse(properties["observation_instant_or_interval"]["additionalProperties"])
        self.assertEqual(
            set(properties["observation_instant_or_interval"]["required"]),
            {"start", "end"},
        )

        self.assertFalse(properties["timezone_context"]["additionalProperties"])
        self.assertEqual(
            set(properties["timezone_context"]["required"]),
            {"database", "id", "version"},
        )


if __name__ == "__main__":
    unittest.main()
