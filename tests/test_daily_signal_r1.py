from __future__ import annotations

import unittest

from ce.foundation.status import CalculationStatus
from ce.signal.daily import (
    DailySignalState,
    aggregate_daily_signals,
    aggregate_qualified_signal_records,
    aggregate_completed_day,
)
from ce.signal.engine import SignalResult
from ce.signal.record import QualifiedSignalRecord


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


    def _record(self, signal_id: str = "CE-SIGNAL-" + "1" * 64) -> QualifiedSignalRecord:
        return QualifiedSignalRecord(
            schema_version="CE-QUALIFIED-SIGNAL-RECORD-V1",
            signal_id=signal_id,
            evidence_packet_ref="E-1:" + "2" * 64,
            timestamp_observation_utc="2026-01-01T00:00:00Z",
            qualification_status="VALID",
            classification="ROBUST_EXACT_SIGNAL",
            kinematic_phase="EXACT",
            phase_uniformity="UNIFORM",
            canon_input_valid=True,
            requires_uncertainty_disclaimer=False,
            environment_pin="sha256:" + "3" * 64,
        )

    def test_normative_aggregator_empty_completed_day_is_quiet_sky(self) -> None:
        result = aggregate_qualified_signal_records((), observation_completed=True)
        self.assertEqual(result.state, DailySignalState.QUIET_SKY)
        self.assertEqual(result.qualifying_signal_refs, ())

    def test_normative_aggregator_reports_qualifying_signal(self) -> None:
        result = aggregate_qualified_signal_records(
            (self._record(),),
            observation_completed=True,
        )
        self.assertEqual(result.state, DailySignalState.QUALIFYING_SIGNALS_PRESENT)
        self.assertEqual(result.qualifying_signal_refs, ("CE-SIGNAL-" + "1" * 64,))

    def test_normative_aggregator_rejects_uncompleted_observation(self) -> None:
        with self.assertRaisesRegex(ValueError, "daily_observation_not_completed"):
            aggregate_qualified_signal_records((), observation_completed=False)

    def test_normative_aggregator_rejects_non_record_input(self) -> None:
        with self.assertRaisesRegex(ValueError, "daily_qualified_signal_record_type_invalid"):
            aggregate_qualified_signal_records((object(),), observation_completed=True)

    def test_completed_day_rejects_unfinished_observation(self) -> None:
        with self.assertRaisesRegex(ValueError, "daily_observation_not_completed"):
            aggregate_completed_day((), observation_completed=False)

    def test_current_failure_remains_failure_after_prior_valid_day(self) -> None:
        prior = self._result(status=CalculationStatus.VALID, classification="ROBUST_EXACT_SIGNAL", canon_input_valid=True)
        self.assertEqual(prior.status, CalculationStatus.VALID)
        current = self._result(status=CalculationStatus.CALCULATION_FAILURE)
        with self.assertRaisesRegex(ValueError, "daily_signal_calculation_not_valid"):
            aggregate_completed_day((current,), observation_completed=True)

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
