from __future__ import annotations

import unittest

from ce.foundation.status import CalculationStatus
from ce.product.boundary import preserve_calculation_truth


class ProductBoundaryR1Tests(unittest.TestCase):
    def test_every_non_valid_status_is_preserved_and_blocks_claim_paths(self) -> None:
        non_valid = (
            CalculationStatus.KNOWN_UNAVAILABLE,
            CalculationStatus.CALCULATION_FAILURE,
            CalculationStatus.INPUT_UNSUPPORTED,
            CalculationStatus.NATAL_EVIDENCE_VARIABLE,
            CalculationStatus.NOT_IMPLEMENTED,
            CalculationStatus.NON_AUTHORIZED,
            CalculationStatus.INVALID_INPUT,
        )
        for status in non_valid:
            with self.subTest(status=status):
                decision = preserve_calculation_truth(status)
                self.assertIs(decision.status, status)
                self.assertFalse(decision.signal_processing_allowed)
                self.assertFalse(decision.canon_claim_allowed)
                self.assertFalse(decision.ai_release_allowed)
                self.assertFalse(decision.quiet_sky_allowed)

    def test_unknown_type_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "product_boundary_status_invalid"):
            preserve_calculation_truth("VALID")  # type: ignore[arg-type]

    def test_valid_status_allows_processing_but_blocks_claim_paths(self) -> None:
        decision = preserve_calculation_truth(CalculationStatus.VALID)
        self.assertTrue(decision.signal_processing_allowed)
        self.assertFalse(decision.canon_claim_allowed)
        self.assertFalse(decision.ai_release_allowed)
        self.assertFalse(decision.quiet_sky_allowed)
        self.assertEqual(
            decision.reason,
            "valid_state_requires_downstream_qualification",
        )


if __name__ == "__main__":
    unittest.main()
