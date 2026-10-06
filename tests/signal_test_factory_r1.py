from __future__ import annotations

from typing import Any

from ce.foundation.status import CalculationStatus
from ce.signal.engine import SignalResult
from ce.signal.record import QualifiedSignalRecord


def build_test_signal_result(**kwargs: Any) -> SignalResult:
    result = object.__new__(SignalResult)
    defaults = {
        "status": CalculationStatus.CALCULATION_FAILURE,
        "classification": None,
        "phase": None,
        "uncertainty_state": None,
        "evidence_packet_ref": None,
        "canon_input_valid": False,
    }
    defaults.update(kwargs)
    for name, value in defaults.items():
        object.__setattr__(result, name, value)
    object.__setattr__(result, "_issued", True)
    errors = result.validate()
    if errors:
        raise AssertionError("invalid test SignalResult: " + ";".join(errors))
    return result


def build_test_qsr(**kwargs: Any) -> QualifiedSignalRecord:
    record = object.__new__(QualifiedSignalRecord)
    for name, value in kwargs.items():
        object.__setattr__(record, name, value)
    object.__setattr__(record, "_issued", True)
    errors = record.validate()
    if errors:
        raise AssertionError("invalid test QSR: " + ";".join(errors))
    return record
