from __future__ import annotations

import json
from pathlib import Path
import unittest

from ce.runtime.profile import ExecutionProfileValidationError, validate_execution_profile


ROOT = Path(__file__).resolve().parents[1]


class ExecutionProfileR1Tests(unittest.TestCase):
    def test_current_development_profile_is_rev4_compatible(self) -> None:
        profile = json.loads(
            (ROOT / "configs" / "runtime_profile.dev.json").read_text(encoding="utf-8")
        )
        validate_execution_profile(profile)

    def test_profile_root_and_nested_runtime_shape_is_required(self) -> None:
        profile = json.loads(
            (ROOT / "configs" / "runtime_profile.dev.json").read_text(encoding="utf-8")
        )
        profile.pop("runtime")
        with self.assertRaisesRegex(ExecutionProfileValidationError, "runtime_missing"):
            validate_execution_profile(profile)

    def test_profile_cannot_claim_authorized_runtime(self) -> None:
        profile = json.loads(
            (ROOT / "configs" / "runtime_profile.dev.json").read_text(encoding="utf-8")
        )
        profile["runtime"]["authority"] = "production"
        with self.assertRaisesRegex(ExecutionProfileValidationError, "runtime_authority_mismatch"):
            validate_execution_profile(profile)

    def test_stale_revision_is_rejected(self) -> None:
        profile = json.loads(
            (ROOT / "configs" / "runtime_profile.dev.json").read_text(encoding="utf-8")
        )
        profile["execution_profile_revision"] = 2
        with self.assertRaisesRegex(ExecutionProfileValidationError, "execution_profile_revision_mismatch"):
            validate_execution_profile(profile)


if __name__ == "__main__":
    unittest.main()
