"""Unit tests for pre_a10_area_gate.py; no third-party packages required."""
from __future__ import annotations

import copy
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
        "document_id": "test",
        "classification": "WORKING_CONTROL_PLANE_CANDIDATE_NON_AUTHORITATIVE",
        "authority_effect": "NONE",
        "normative_effect": "NONE",
        "runtime_authorization_effect": "NONE",
        "a10_authorized": False,
        "areas": [{
            "id": "A1",
            "title": "Example review topic",
            "status": "NOT_STARTED",
            "owner_decision_required": False,
            "source_refs": ["Box:example"],
            "review_summary": "",
            "evidence_refs": [],
            "disposition_ref": "",
            "owner_disposition": "",
        }]
    }


class GateValidatorTests(unittest.TestCase):
    def test_incomplete_register_remains_blocked_and_does_not_authorize_a10(self):
        report = gate.validate_register(sample_register())
        self.assertEqual(report["pre_a10_area_review"], "INCOMPLETE")
        self.assertEqual(report["incomplete_area_ids"], ["A1"])
        self.assertEqual(report["a10_runtime_adoption"], "NOT_AUTHORIZED_BY_THIS_TOOL")
        self.assertEqual(report["authority_effect"], "NONE")

    def test_complete_non_owner_area_requires_evidence_and_summary(self):
        data = sample_register()
        area = data["areas"][0]
        area.update({
            "status": "CLOSED_PRESERVE",
            "review_summary": "Source review completed; invariant preserved.",
            "evidence_refs": ["Box:source", "GitHub:commit"]
        })
        report = gate.validate_register(data)
        self.assertEqual(report["pre_a10_area_review"], "COMPLETE")
        self.assertEqual(report["complete_count"], 1)

    def test_owner_decision_area_cannot_close_without_disposition(self):
        data = sample_register()
        area = data["areas"][0]
        area.update({
            "owner_decision_required": True,
            "status": "OWNER_DECISION_RECORDED",
            "review_summary": "Decision recorded.",
            "evidence_refs": ["Box:source"],
            "disposition_ref": "",
            "owner_disposition": ""
        })
        with self.assertRaises(gate.RegisterError):
            gate.validate_register(data)

    def test_missing_source_reference_is_invalid(self):
        data = sample_register()
        data["areas"][0]["source_refs"] = []
        with self.assertRaises(gate.RegisterError):
            gate.validate_register(data)

    def test_attempt_to_mark_a10_authorized_is_invalid(self):
        data = sample_register()
        data["a10_authorized"] = True
        with self.assertRaises(gate.RegisterError):
            gate.validate_register(data)

    def test_cli_strict_mode_returns_blocked_exit_code(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "register.json"
            path.write_text(json.dumps(sample_register()), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(path), "--require-complete"],
                capture_output=True, text=True, check=False
            )
        self.assertEqual(result.returncode, 2)
        self.assertIn('"pre_a10_area_review": "INCOMPLETE"', result.stdout)


if __name__ == "__main__":
    unittest.main()
