from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable

from ce.calculation.evidence import EvidencePacket
from ce.foundation.status import CalculationStatus
from ce.signal.engine import SignalEngine
from ce.signal.record import QualifiedSignalRecord, issue_qualified_signal_record


class DailySignalState(str, Enum):
    QUIET_SKY = "QUIET_SKY"
    QUALIFYING_SIGNALS_PRESENT = "QUALIFYING_SIGNALS_PRESENT"


@dataclass(frozen=True)
class DailySignalAggregation:
    state: DailySignalState
    qualifying_signal_refs: tuple[str, ...]


def _aggregate_issued_records(
    records: Iterable[QualifiedSignalRecord],
    *,
    observation_completed: bool,
) -> DailySignalAggregation:
    if not observation_completed:
        raise ValueError("daily_observation_not_completed")
    items = tuple(records)
    for item in items:
        if not isinstance(item, QualifiedSignalRecord):
            raise ValueError("daily_qualified_signal_record_type_invalid")
    qualifying = tuple(item.signal_id for item in items)
    if qualifying:
        return DailySignalAggregation(
            state=DailySignalState.QUALIFYING_SIGNALS_PRESENT,
            qualifying_signal_refs=qualifying,
        )
    return DailySignalAggregation(
        state=DailySignalState.QUIET_SKY,
        qualifying_signal_refs=(),
    )


def aggregate_daily_evidence_packets(
    packets: Iterable[EvidencePacket],
    *,
    observation_completed: bool,
) -> DailySignalAggregation:
    """Aggregate the completed observation directly from immutable evidence.

    Every supplied packet is evaluated by the Signal Engine. A VALID but
    disqualified packet contributes no signal and therefore permits QUIET_SKY.
    Any non-VALID packet is terminal and cannot be converted into QUIET_SKY.
    Only qualifying Signal Engine results are materialized as QSRs.
    """
    if not observation_completed:
        raise ValueError("daily_observation_not_completed")

    records: list[QualifiedSignalRecord] = []
    for packet in packets:
        if not isinstance(packet, EvidencePacket):
            raise ValueError("daily_evidence_packet_type_invalid")
        result = SignalEngine().evaluate(packet)
        if result.status is not CalculationStatus.VALID:
            raise ValueError("daily_signal_calculation_not_valid")
        if not result.canon_input_valid or result.classification is None:
            continue
        records.append(issue_qualified_signal_record(packet))

    return _aggregate_issued_records(records, observation_completed=True)


def aggregate_daily_signals(*args: object, **kwargs: object) -> DailySignalAggregation:
    """Removed unsafe SignalResult aggregation path."""
    raise ValueError("daily_signal_result_path_removed_use_evidence_packets")


def aggregate_qualified_signal_records(*args: object, **kwargs: object) -> DailySignalAggregation:
    """Removed unsafe caller-supplied QSR aggregation path."""
    raise ValueError("daily_qsr_path_removed_use_evidence_packets")


def aggregate_completed_day(
    packets: Iterable[EvidencePacket],
    *,
    observation_completed: bool,
) -> DailySignalAggregation:
    return aggregate_daily_evidence_packets(
        packets,
        observation_completed=observation_completed,
    )
