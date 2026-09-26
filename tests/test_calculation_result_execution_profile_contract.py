from __future__ import annotations

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from ce.calculation.contracts import CalculationResult
from ce.foundation.identity import CANONICAL_EXECUTION_PROFILE_ID
from ce.foundation.status import CalculationStatus, ScenarioState


class CalculationResultExecutionProfileContractTests(unittest.TestCase):
    def _result(self, profile_id: str | None) -> CalculationResult:
        return CalculationResult(
            request_id="B4-ITEM4-001",
            status=CalculationStatus.NON_AUTHORIZED,
            execution_profile_id=profile_id,  # type: ignore[arg-type]
            scenario_state=ScenarioState.NONE,
            normalized_time=None,
            object_states=(),
            warnings=(),
            errors=("development-only",),
            provenance={},
        )

    def test_canonical_profile_is_accepted(self) -> None:
        result = self._result(CANONICAL_EXECUTION_PROFILE_ID)
        self.assertEqual(result.validate(), ())

    def test_alternate_profile_is_rejected(self) -> None:
        result = self._result("CE-CALC-V1-EP-ALT")
        self.assertIn(
            "invalid:execution_profile_id:canonical_required",
            result.validate(),
        )

    def test_missing_profile_is_rejected(self) -> None:
        result = self._result(None)
        self.assertIn(
            "invalid:execution_profile_id:canonical_required",
            result.validate(),
        )


if __name__ == "__main__":
    unittest.main()
