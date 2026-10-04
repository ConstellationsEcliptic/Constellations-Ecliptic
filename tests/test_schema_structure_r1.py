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
            "runtime_environment_identity_r1.schema.json",
            "runtime_capture_r2.schema.json",
        ):
            schema = self._load_without_duplicate_keys(ROOT / "schemas" / name)
            self.assertEqual(schema["type"], "object")
            self.assertFalse(schema["additionalProperties"])

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

    def test_evidence_packet_schema_uses_strict_record_shapes(self) -> None:
        schema = self._load_without_duplicate_keys(ROOT / "schemas" / "evidence_packet.schema.json")
        self.assertFalse(schema["properties"]["object_records"]["items"]["additionalProperties"])
        self.assertFalse(schema["properties"]["geometry_records"]["items"]["additionalProperties"])
        self.assertFalse(schema["properties"]["window_segments"]["items"]["additionalProperties"])


if __name__ == "__main__":
    unittest.main()
