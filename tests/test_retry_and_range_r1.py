from __future__ import annotations

import unittest

from ce.ephemeris.range import ObjectRangeStatus, map_native_range_result
from ce.foundation.status import CalculationStatus
from ce.runtime.retry import (
    FailureClass,
    NonRetryableCalculationError,
    RetryableCalculationError,
    execute_with_retry,
)


class RetryAndRangeR1Tests(unittest.TestCase):
    # ERR-03
    def test_err_03_retryable_worker_failure(self) -> None:
        attempts = []
        def operation(attempt: int) -> str:
            attempts.append(attempt)
            if attempt == 0:
                raise RetryableCalculationError("worker timeout")
            return "fresh-result"

        result = execute_with_retry(operation, max_retries=1)
        self.assertEqual(result.retry_attempt, 1)
        self.assertEqual(result.final_status, CalculationStatus.VALID)
        self.assertFalse(result.stale_result_substitution)
        self.assertEqual(result.value, "fresh-result")
        self.assertEqual(attempts, [0, 1])

    # ERR-04
    def test_err_04_non_retryable_failure(self) -> None:
        result = execute_with_retry(
            lambda attempt: (_ for _ in ()).throw(
                NonRetryableCalculationError("hard failure")
            ),
            max_retries=1,
        )
        self.assertEqual(result.final_status, CalculationStatus.CALCULATION_FAILURE)
        self.assertFalse(result.stale_result_substitution)
        self.assertIn(FailureClass.NON_RETRYABLE_FAILURE.value, result.errors)

    # EPH-02
    def test_eph_02_chiron_out_of_range_is_known_unavailable(self) -> None:
        result = map_native_range_result(
            "CHIRON",
            range_status=ObjectRangeStatus.OUTSIDE_SUPPORTED_RANGE,
            native_return_code=0,
        )
        self.assertIsNotNone(result)
        assert result is not None
        self.assertEqual(result.status, CalculationStatus.KNOWN_UNAVAILABLE)
        self.assertIsNone(result.longitude_deg)
        self.assertIsNone(result.speed_deg_per_day)


if __name__ == "__main__":
    unittest.main()
