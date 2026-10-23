"""Unit tests for the pre-A10 register validator; standard library only."""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("pre_a10_area_gate.py")
spec = importlib.util.spec_from_file_location("pre_a10_area_gate", SCRIPT)
assert spec and spec.loader
gate = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = gate
spec.loader.exec_module(gate)


def sample_register():
    return {
        "schema_version": "1.0",
        "project": "CONSTELLATIONS ECLIPTIC",
        "document_id": gate.EXPECTED_DOCUMENT_ID,
        "classification": "WORKING_CONTROL_PLANE_CANDIDATE_NON_AUTHORITATIVE",
        "authority_effect": "NONE",
        "normative_effect": "NONE",
        "runtime_authorization_effect": "NONE",
        "a10_authorized": False,
        "current_gate": gate.EXPECTED_CURRENT_GATE,
        "allowed_statuses": sorted(gate.ALLOWED_STATUSES),
        "required_completion_statuses": sorted(gate.COMPLETE_STATUSES),
        "areas": [
            {
                "id": area_id,
                "title": f"Review area {area_id}",
                "status": "NOT_STARTED",
                "owner_decision_required": area_id in gate.EXPECTED_OWNER_DECISION_REQUIRED_IDS,
                "source_refs": [f"Box:source-{area_id}"],
                "review_summary": "",
                "evidence_refs": [],
                "disposition_ref": "",
                "owner_disposition": "",
            }
            for area_id in gate.EXPECTED_AREA_IDS
        ],
    }


class GateValidatorTests(unittest.TestCase):
    def test_incomplete_register_remains_blocked_and_never_authorizes_a10(self):
        report = gate.validate_register(sample_register())
        self.assertEqual(report["area_count"], 23)
        self.assertEqual(report["pre_a10_area_review"], "INCOMPLETE")
        self.assertEqual(report["incomplete_area_ids"], list(gate.EXPECTED_AREA_IDS))
        self.assertEqual(report["a10_runtime_adoption"], "NOT_AUTHORIZED_BY_THIS_TOOL")
        self.assertEqual(report["production_authorization"], "NOT_AUTHORIZED_BY_THIS_TOOL")
        self.assertEqual(report["seal"], "NOT_AUTHORIZED_BY_THIS_TOOL")
        self.assertEqual(report["authority_effect"], "NONE")

    def test_complete_register_can_only_complete_area_review_not_a10(self):
        data = sample_register()
        for area in data["areas"]:
            area["review_summary"] = f"Reviewed evidence for {area['id']}."
            area["evidence_refs"] = [f"GitHub:fixture-{area['id']}"]
            if area["owner_decision_required"]:
                area["status"] = "OWNER_DECISION_RECORDED"
                area["disposition_ref"] = f"Decision-fixture:{area['id']}"
                area["owner_disposition"] = "TEST_FIXTURE_ONLY"
            else:
                area["status"] = "CLOSED_PRESERVE"

        report = gate.validate_register(data)
        self.assertEqual(report["pre_a10_area_review"], "COMPLETE")
        self.assertEqual(report["complete_count"], 23)
        self.assertEqual(report["incomplete_count"], 0)
        self.assertEqual(report["a10_runtime_adoption"], "NOT_AUTHORIZED_BY_THIS_TOOL")
        self.assertEqual(report["production_authorization"], "NOT_AUTHORIZED_BY_THIS_TOOL")
        self.assertEqual(report["seal"], "NOT_AUTHORIZED_BY_THIS_TOOL")
        self.assertEqual(report["authority_effect"], "NONE")

    def test_missing_required_area_is_invalid(self):
        data = sample_register()
        data["areas"] = [a for a in data["areas"] if a["id"] != "F3"]
        with self.assertRaisesRegex(gate.RegisterError, "required area ids are missing"):
            gate.validate_register(data)

    def test_unexpected_area_is_invalid(self):
        data = sample_register()
        extra = dict(data["areas"][0])
        extra["id"] = "G1"
        data["areas"].append(extra)
        with self.assertRaisesRegex(gate.RegisterError, "unexpected area id"):
            gate.validate_register(data)

    def test_duplicate_area_id_is_invalid(self):
        data = sample_register()
        data["areas"][1]["id"] = data["areas"][0]["id"]
        with self.assertRaisesRegex(gate.RegisterError, "duplicate area id"):
            gate.validate_register(data)

    def test_malformed_unhashable_status_is_invalid_not_uncaught_exception(self):
        data = sample_register()
        data["areas"][0]["status"] = []
        with self.assertRaisesRegex(gate.RegisterError, "status is not an allowed status"):
            gate.validate_register(data)

    def test_current_gate_drift_is_invalid(self):
        data = sample_register()
        data["current_gate"] = "OPEN"
        with self.assertRaisesRegex(gate.RegisterError, "current_gate"):
            gate.validate_register(data)

    def test_allowed_status_metadata_must_match_validator_policy(self):
        data = sample_register()
        data["allowed_statuses"].remove("NOT_STARTED")
        with self.assertRaisesRegex(gate.RegisterError, "allowed_statuses"):
            gate.validate_register(data)

    def test_required_completion_metadata_must_match_validator_policy(self):
        data = sample_register()
        data["required_completion_statuses"].remove("CLOSED_PRESERVE")
        with self.assertRaisesRegex(gate.RegisterError, "required_completion_statuses"):
            gate.validate_register(data)

    def test_owner_decision_required_policy_cannot_be_weakened_in_register(self):
        data = sample_register()
        next(a for a in data["areas"] if a["id"] == "C3")["owner_decision_required"] = False
        with self.assertRaisesRegex(gate.RegisterError, "C3.owner_decision_required"):
            gate.validate_register(data)

    def test_owner_decision_area_cannot_close_without_disposition(self):
        data = sample_register()
        area = next(a for a in data["areas"] if a["id"] == "C3")
        area.update({
            "status": "OWNER_DECISION_RECORDED",
            "review_summary": "Decision recorded.",
            "evidence_refs": ["Box:source"],
            "disposition_ref": "",
            "owner_disposition": "",
        })
        with self.assertRaisesRegex(gate.RegisterError, "requires disposition_ref"):
            gate.validate_register(data)

    def test_missing_source_reference_is_invalid(self):
        data = sample_register()
        data["areas"][0]["source_refs"] = []
        with self.assertRaisesRegex(gate.RegisterError, "source_refs"):
            gate.validate_register(data)

    def test_attempt_to_mark_a10_authorized_is_invalid(self):
        data = sample_register()
        data["a10_authorized"] = True
        with self.assertRaisesRegex(gate.RegisterError, "a10_authorized"):
            gate.validate_register(data)

    def test_cli_strict_mode_returns_blocked_exit_code(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "register.json"
            path.write_text(json.dumps(sample_register()), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(path), "--require-complete"],
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertEqual(result.returncode, 2)
        self.assertIn('"pre_a10_area_review": "INCOMPLETE"', result.stdout)


if __name__ == "__main__":
    unittest.main()
