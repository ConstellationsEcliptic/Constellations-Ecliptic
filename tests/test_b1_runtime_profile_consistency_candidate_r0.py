from __future__ import annotations

import json
from pathlib import Path
import unittest

from ce.calculation.geometry import (
    ASPECT_BRANCHES,
    ORB_PROFILE_A,
    ORB_PROFILE_B,
    PROFILE_A_OBJECTS,
)
from ce.calculation.registry import (
    EXPECTED_ASPECTS,
    EXPECTED_OBJECTS,
    EXPECTED_OBJECT_PROFILES,
)


ROOT = Path(__file__).resolve().parents[1]


class B1RuntimeProfileConsistencyCandidateTests(unittest.TestCase):
    """Candidate-only drift checks. These tests do not confer source authority."""

    def load(self, name: str) -> dict:
        return json.loads((ROOT / "profiles" / name).read_text(encoding="utf-8"))

    def test_runtime_aspect_branches_match_candidate_profile(self) -> None:
        payload = self.load("aspect_registry_rev4_candidate.json")
        profile_branches = {
            item["aspect_id"]: tuple(float(value) for value in item["branches_deg"])
            for item in payload["aspects"]
        }
        profile_angles = {
            item["aspect_id"]: float(item["angle_deg"])
            for item in payload["aspects"]
        }

        self.assertEqual(ASPECT_BRANCHES, profile_branches)
        self.assertEqual(EXPECTED_ASPECTS, profile_angles)

    def test_runtime_orb_constants_match_candidate_profile(self) -> None:
        payload = self.load("orb_registry_rev4_candidate.json")
        profiles = payload["profiles"]

        self.assertEqual(ORB_PROFILE_A, profiles["A"])
        self.assertEqual(ORB_PROFILE_B, profiles["B"])

    def test_runtime_object_assignment_matches_candidate_profiles(self) -> None:
        objects_payload = self.load("object_registry_rev4_candidate.json")
        orb_payload = self.load("orb_registry_rev4_candidate.json")

        object_ids = {
            item["object_id"]: item["swiss_object_id"]
            for item in objects_payload["objects"]
        }
        object_profiles = {
            item["object_id"]: item["object_profile"]
            for item in objects_payload["objects"]
        }
        profile_assignment = {
            profile: set(object_ids)
            for profile, object_ids in orb_payload["object_profile_assignment"].items()
        }

        self.assertEqual(EXPECTED_OBJECTS, object_ids)
        self.assertEqual(EXPECTED_OBJECT_PROFILES, object_profiles)
        self.assertEqual(
            PROFILE_A_OBJECTS,
            frozenset(
                object_id
                for object_id, profile in object_profiles.items()
                if profile == "A"
            ),
        )
        self.assertEqual(
            profile_assignment["A"],
            {
                object_id
                for object_id, profile in object_profiles.items()
                if profile == "A"
            },
        )
        self.assertEqual(
            profile_assignment["B"],
            {
                object_id
                for object_id, profile in object_profiles.items()
                if profile == "B"
            },
        )

    def test_profile_authority_is_not_promoted_by_consistency_checks(self) -> None:
        for name in (
            "aspect_registry_rev4_candidate.json",
            "orb_registry_rev4_candidate.json",
            "object_registry_rev4_candidate.json",
        ):
            payload = self.load(name)
            self.assertEqual(payload.get("authority"), "NOT_ESTABLISHED")


if __name__ == "__main__":
    unittest.main()
