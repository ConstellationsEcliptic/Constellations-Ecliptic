from __future__ import annotations

import unittest

from ce.foundation.status import CalculationStatus
from ce.signal.daily import DailySignalState, aggregate_daily_signals
from ce.signal.engine import SignalResult


class DailySignalR1Tests(unittest.TestCase):
    def _result(
        self,
        *,
        status: CalculationStatus = CalculationStatus.VALID,
        classification: str | None = None,
        canon_input_valid: bool = False,
        ref: str | None = "E-1:hash",
    ) -> SignalResult:
        return SignalResult(
            status=status,
            classification=classification,
            phase=None,
            uncertainty_state=None,
            evidence_packet_ref=ref,
            canon_input_valid=canon_input_valid,
        )

    def test_quiet_sky_requires_successful_completed_observations(self) -> None:
        result = aggregate_daily_signals(
            (
                self._result(
                    classification="DISQUALIFIED_OUT_OF_ORB",
                    canon_input_valid=False,
                ),
            )
        )
        self.assertEqual(result.state, DailySignalState.QUIET_SKY)
        self.assertEqual(result.qualifying_signal_refs, ())

    def test_qualifying_signal_prevents_quiet_sky(self) -> None:
        result = aggregate_daily_signals(
            (
                self._result(
                    classification="ROBUST_EXACT_SIGNAL",
                    canon_input_valid=True,
                    ref="E-1:hash",
                ),
            )
        )
        self.assertEqual(
            result.state,
            DailySignalState.QUALIFYING_SIGNALS_PRESENT,
        )
        self.assertEqual(result.qualifying_signal_refs, ("E-1:hash",))

    def test_mixed_daily_results_preserve_qualifying_signal(self) -> None:
        result = aggregate_daily_signals(
            (
                self._result(
                    classification="DISQUALIFIED_OUT_OF_ORB",
                    canon_input_valid=False,
                ),
                self._result(
                    classification="POSSIBLE_APPROACHING_SIGNAL",
                    canon_input_valid=True,
                    ref="E-2:hash",
                ),
            )
        )
        self.assertEqual(
            result.state,
            DailySignalState.QUALIFYING_SIGNALS_PRESENT,
        )
        self.assertEqual(result.qualifying_signal_refs, ("E-2:hash",))

    def test_failure_cannot_become_quiet_sky(self) -> None:
        with self.assertRaisesRegex(
            ValueError,
            "daily_signal_calculation_not_valid",
        ):
            aggregate_daily_signals(
                (
                    self._result(
                        status=CalculationStatus.CALCULATION_FAILURE,
                    ),
                )
            )

    def test_unknown_signal_result_type_is_rejected(self) -> None:
        with self.assertRaisesRegex(
            ValueError,
            "daily_signal_result_type_invalid",
        ):
            aggregate_daily_signals((object(),))


if __name__ == "__main__":
    unittest.main()
