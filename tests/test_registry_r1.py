from __future__ import annotations

import json
from pathlib import Path
import unittest

from ce.calculation.registry import (
    validate_aspect_registry,
    validate_orb_registry,
    validate_registry_bundle,
    validate_object_registry,
)


ROOT = Path(__file__).resolve().parents[1]


class RegistryR1Tests(unittest.TestCase):
    def load(self, name: str) -> dict:
        return json.loads((ROOT / "profiles" / name).read_text(encoding="utf-8"))

    def test_current_registry_candidates_are_rev4_bound(self) -> None:
        objects = self.load("object_registry_rev4_candidate.json")
        aspects = self.load("aspect_registry_rev4_candidate.json")
        orbs = self.load("orb_registry_rev4_candidate.json")
        validate_registry_bundle(objects, aspects, orbs)

    def test_object_registry_is_exactly_13_unique_objects(self) -> None:
        validate_object_registry(self.load("object_registry_rev4_candidate.json"))

    def test_aspect_registry_is_exactly_five_branches(self) -> None:
        validate_aspect_registry(self.load("aspect_registry_rev4_candidate.json"))

    def test_orb_registry_has_a_and_b_profiles(self) -> None:
        validate_orb_registry(self.load("orb_registry_rev4_candidate.json"))

    def test_object_count_mutation_is_rejected(self) -> None:
        payload = self.load("object_registry_rev4_candidate.json")
        payload["objects"] = payload["objects"][:-1]
        with self.assertRaises(ValueError):
            validate_object_registry(payload)


if __name__ == "__main__":
    unittest.main()
