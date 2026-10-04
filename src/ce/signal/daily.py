from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable

from ce.foundation.status import CalculationStatus
from ce.signal.engine import SignalResult


class DailySignalState(str, Enum):
    QUIET_SKY = "QUIET_SKY"
    QUALIFYING_SIGNALS_PRESENT = "QUALIFYING_SIGNALS_PRESENT"


@dataclass(frozen=True)
class DailySignalAggregation:
    state: DailySignalState
    qualifying_signal_refs: tuple[str, ...]


def aggregate_daily_signals(signals: Iterable[SignalResult]) -> DailySignalAggregation:
    """Aggregate completed Signal Results without modifying signal/evidence state.

    QUIET_SKY is emitted only when every supplied result completed successfully
    and none is a qualifying Canon-eligible signal. Any calculation failure is
    terminal and is never coerced into QUIET_SKY.
    """
    items = tuple(signals)
    for item in items:
        if not isinstance(item, SignalResult):
            raise ValueError("daily_signal_result_type_invalid")
        if item.status is not CalculationStatus.VALID:
            raise ValueError("daily_signal_calculation_not_valid")

    qualifying = tuple(
        item.evidence_packet_ref
        for item in items
        if item.canon_input_valid and item.classification is not None
    )
    if qualifying:
        return DailySignalAggregation(
            state=DailySignalState.QUALIFYING_SIGNALS_PRESENT,
            qualifying_signal_refs=qualifying,
        )
    return DailySignalAggregation(
        state=DailySignalState.QUIET_SKY,
        qualifying_signal_refs=(),
    )
