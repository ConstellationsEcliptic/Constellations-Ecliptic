from __future__ import annotations

import unittest

from ce.foundation.status import CalculationStatus
from ce.product.boundary import preserve_calculation_truth


class ProductBoundaryFailClosedR1Tests(unittest.TestCase):
    def test_valid_allows_processing_but_not_claim_or_ai_release(self) -> None:
        decision = preserve_calculation_truth(CalculationStatus.VALID)

        self.assertTrue(decision.signal_processing_allowed)
        self.assertFalse(decision.canon_claim_allowed)
        self.assertFalse(decision.ai_release_allowed)
        self.assertFalse(decision.quiet_sky_allowed)
        self.assertEqual(
            decision.reason,
            "valid_state_requires_downstream_qualification",
        )

    def test_non_valid_states_never_imply_release(self) -> None:
        for status in CalculationStatus:
            if status is CalculationStatus.VALID:
                continue
            with self.subTest(status=status):
                decision = preserve_calculation_truth(status)
                self.assertFalse(decision.signal_processing_allowed)
                self.assertFalse(decision.canon_claim_allowed)
                self.assertFalse(decision.ai_release_allowed)
                self.assertFalse(decision.quiet_sky_allowed)

    def test_status_type_is_fail_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "product_boundary_status_invalid"):
            preserve_calculation_truth("VALID")  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
