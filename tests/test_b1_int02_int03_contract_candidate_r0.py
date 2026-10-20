from __future__ import annotations

import unittest
from unittest.mock import patch

from ce.calculation.engine import CalculationEngine
from ce.signal.engine import SignalEngine
import tests.test_no_commercial_dependency as commercial_test_module
import tests.test_signal_no_recomputation_r1 as no_recomputation_test_module


class B1Int02Int03ContractCandidateTests(unittest.TestCase):
    """Candidate-only oracle-strengthening checks; not an official ID rebinding."""

    def test_int02_evidence_reference_and_qualification_are_identical(self) -> None:
        helper = commercial_test_module.CommercialIndependenceTests()
        zero_credits = helper._evaluate_fixture(commercial_state="ZERO_CREDITS")
        purchased_credits = helper._evaluate_fixture(commercial_state="CREDITS_PURCHASED")

        self.assertEqual(zero_credits.evidence_packet_ref, purchased_credits.evidence_packet_ref)
        self.assertEqual(zero_credits.status, purchased_credits.status)
        self.assertEqual(zero_credits.classification, purchased_credits.classification)
        self.assertEqual(zero_credits.phase, purchased_credits.phase)
        self.assertEqual(zero_credits.uncertainty_state, purchased_credits.uncertainty_state)
        self.assertTrue(zero_credits.canon_input_valid)
        self.assertTrue(purchased_credits.canon_input_valid)

    def test_int03_signal_uses_issued_packet_without_calculation_engine_reentry(self) -> None:
        helper = no_recomputation_test_module.SignalNoRecomputationR1Tests()
        packet, source = helper._packet()
        issued_ref = f"{packet.evidence_packet_id}:{packet.content_sha256()}"
        issued_digest = packet.content_sha256()
        engine = SignalEngine()

        with patch.object(
            CalculationEngine,
            "calculate",
            side_effect=AssertionError("signal layer must not invoke astronomical calculation"),
        ):
            before = engine.evaluate(packet)
            source["geometry_state"] = "APPLYING"
            source["calculation_status"] = "CALCULATION_FAILURE"
            source["ephemeris_status"] = "MISMATCH"
            after = engine.evaluate(packet)

        self.assertEqual(before.evidence_packet_ref, issued_ref)
        self.assertEqual(after.evidence_packet_ref, issued_ref)
        self.assertEqual(packet.content_sha256(), issued_digest)
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
