from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Callable, TypeVar

from ce.foundation.status import CalculationStatus


class FailureClass(str, Enum):
    RETRYABLE_TIMEOUT = "RETRYABLE_TIMEOUT"
    NON_RETRYABLE_FAILURE = "NON_RETRYABLE_FAILURE"


@dataclass(frozen=True)
class RetryExecution:
    final_status: CalculationStatus
    retry_attempt: int
    attempts_total: int
    stale_result_substitution: bool
    value: object | None
    errors: tuple[str, ...]


T = TypeVar("T")


class RetryableCalculationError(RuntimeError):
    failure_class = FailureClass.RETRYABLE_TIMEOUT


class NonRetryableCalculationError(RuntimeError):
    failure_class = FailureClass.NON_RETRYABLE_FAILURE


def execute_with_retry(
    operation: Callable[[int], T],
    *,
    max_retries: int = 1,
) -> RetryExecution:
    if max_retries < 0:
        raise ValueError("max_retries_must_be_nonnegative")

    attempts = 0
    last_error: str | None = None

    while True:
        try:
            value = operation(attempts)
            return RetryExecution(
                final_status=CalculationStatus.VALID,
                retry_attempt=attempts,
                attempts_total=attempts + 1,
                stale_result_substitution=False,
                value=value,
                errors=(),
            )
        except RetryableCalculationError as exc:
            last_error = str(exc) or FailureClass.RETRYABLE_TIMEOUT.value
            if attempts >= max_retries:
                return RetryExecution(
                    final_status=CalculationStatus.CALCULATION_FAILURE,
                    retry_attempt=attempts,
                    attempts_total=attempts + 1,
                    stale_result_substitution=False,
                    value=None,
                    errors=(FailureClass.RETRYABLE_TIMEOUT.value, last_error),
                )
            attempts += 1
        except NonRetryableCalculationError as exc:
            return RetryExecution(
                final_status=CalculationStatus.CALCULATION_FAILURE,
                retry_attempt=attempts,
                attempts_total=attempts + 1,
                stale_result_substitution=False,
                value=None,
                errors=(FailureClass.NON_RETRYABLE_FAILURE.value, str(exc)),
            )
        except Exception as exc:
            return RetryExecution(
                final_status=CalculationStatus.CALCULATION_FAILURE,
                retry_attempt=attempts,
                attempts_total=attempts + 1,
                stale_result_substitution=False,
                value=None,
                errors=(FailureClass.NON_RETRYABLE_FAILURE.value, str(exc)),
            )
