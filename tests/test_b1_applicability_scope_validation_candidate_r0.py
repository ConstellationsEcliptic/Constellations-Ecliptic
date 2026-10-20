from __future__ import annotations

import json
from pathlib import Path
import unittest

from ce.canon.registry import CanonRule, CanonRuleInvalid


ROOT = Path(__file__).resolve().parents[1]


def record(applicability_scope: list[str]) -> dict[str, object]:
    # Synthetic values exercise structure only; they are not CE Canon.
    return {
        "rule_id": "TEST-ONLY-SCOPE-VALIDATION",
        "canon_version": "TEST_ONLY",
        "tradition_track": "TEST_ONLY",
        "source_reference": "TEST_ONLY",
        "source_scope": "TEST_ONLY",
        "condition": {"classification": "TEST_ONLY"},
        "allowed_interpretation": {},
        "forbidden_extrapolation": ["TEST_ONLY"],
        "confidence_language_boundary": {},
        "applicability_scope": applicability_scope,
    }


class B1ApplicabilityScopeValidationCandidateTests(unittest.TestCase):
    """Structural candidate tests only; no Canon semantics or authority are implied."""

    def test_empty_applicability_scope_is_rejected(self) -> None:
        with self.assertRaisesRegex(
            CanonRuleInvalid,
            "canon_rule_invalid:applicability_scope",
        ):
            CanonRule.from_mapping(record([]))

    def test_nonempty_applicability_scope_is_preserved(self) -> None:
        rule = CanonRule.from_mapping(record(["self-reflection"]))
        self.assertEqual(rule.applicability_scope, ("self-reflection",))
        self.assertEqual(
            rule.canonical_payload()["applicability_scope"],
            ["self-reflection"],
        )

    def test_blank_applicability_scope_item_is_rejected(self) -> None:
        with self.assertRaisesRegex(
            CanonRuleInvalid,
            "canon_rule_invalid:applicability_scope",
        ):
            CanonRule.from_mapping(record(["   "]))

    def test_json_schema_requires_at_least_one_scope_item(self) -> None:
        schema_path = ROOT / "schemas" / "canon_rule.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        scope_schema = schema["properties"]["applicability_scope"]
        self.assertEqual(scope_schema.get("minItems"), 1)
        self.assertTrue(scope_schema.get("uniqueItems"))


if __name__ == "__main__":
    unittest.main()
