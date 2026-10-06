from __future__ import annotations

import json
from pathlib import Path
import unittest

from ce.runtime.profile import ExecutionProfileValidationError, validate_execution_profile


ROOT = Path(__file__).resolve().parents[1]


class CER0ExecutionProfileIdentityStrictnessTests(unittest.TestCase):
    def test_profile_rejects_unestablished_source_and_build_identity_sentinels(self):
        profile = json.loads((ROOT / "configs" / "runtime_profile.dev.json").read_text(encoding="utf-8"))
        # Current validator only checks non-empty strings. Any sentinel must be
        # rejected because this is an identity-bearing execution profile.
        with self.assertRaises(ExecutionProfileValidationError):
            validate_execution_profile(profile)
