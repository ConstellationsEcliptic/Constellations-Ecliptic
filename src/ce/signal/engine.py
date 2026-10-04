from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Mapping
from datetime import datetime, timezone
from typing import Any

from ce.calculation.evidence import EvidencePacket
from ce.foundation.status import CalculationStatus


@dataclass(frozen=True)
class SignalResult:
    status: CalculationStatus
    classification: str | None
    phase: str | None
    uncertainty_state: str | None
    evidence_packet_ref: str | None
    canon_input_valid: bool


class SignalEngine:
    """Pure-read signal qualification boundary.

    All numerical/geometric state is consumed from an immutable EvidencePacket.
    This layer never recomputes coordinates, geometry, or kinematics.
    """

    @staticmethod
    def _failure() -> SignalResult:
        return SignalResult(
            status=CalculationStatus.CALCULATION_FAILURE,
            classification="DISQUALIFIED_CALCULATION_FAILURE",
            phase=None,
            uncertainty_state=None,
            evidence_packet_ref=None,
            canon_input_valid=False,
        )

    @staticmethod
    def _ref(packet: EvidencePacket) -> str:
        return f"{packet.evidence_packet_id}:{packet.content_sha256()}"

    @staticmethod
    def _observation_start(packet: EvidencePacket) -> datetime | None:
        start = packet.observation_instant_or_interval.get("start")
        if not isinstance(start, str) or not start.endswith("Z"):
            return None
        try:
            value = datetime.fromisoformat(start[:-1] + "+00:00")
        except ValueError:
            return None
        return value.astimezone(timezone.utc)

    @staticmethod
    def _future_exact_event_exists(packet: EvidencePacket) -> bool:
        start = SignalEngine._observation_start(packet)
        if start is None:
            return False
        for record in packet.exact_events:
            if not isinstance(record, Mapping):
                continue
            raw = record.get("event_time_utc")
            if not isinstance(raw, str) or not raw.endswith("Z"):
                continue
            try:
                event_time = datetime.fromisoformat(raw[:-1] + "+00:00").astimezone(timezone.utc)
            except ValueError:
                continue
            if event_time > start:
                return True
        return False

    @staticmethod
    def _phase(packet: EvidencePacket) -> str | None:
        states: set[str] = set()
        for record in packet.geometry_records:
            if isinstance(record, Mapping):
                state = record.get("kinematic_state")
                if isinstance(state, str) and state.strip():
                    states.add(state)
        if not states:
            for record in packet.kinematics:
                if isinstance(record, Mapping):
                    state = record.get("kinematic_state")
                    if isinstance(state, str) and state.strip():
                        states.add(state)

        if not states:
            return None
        if states == {"EXACT"}:
            return "EXACT"
        if states == {"APPLYING"}:
            return "APPLYING"
        if states == {"SEPARATING"}:
            return "SEPARATING"
        if states <= {"APPLYING", "SEPARATING"} and len(states) > 1:
            return "MIXED"
        if "NEAR_STATIONARY" in states:
            return "NEAR_STATIONARY"
        return None

    def evaluate(self, calculation_result: Any) -> SignalResult:
        if not isinstance(calculation_result, EvidencePacket):
            return self._failure()

        packet_errors = calculation_result.validate()
        if packet_errors:
            return self._failure()

        ref = self._ref(calculation_result)
        calculation_status = calculation_result.calculation_flags.get("calculation_status")
        if calculation_status != CalculationStatus.VALID.value:
            return SignalResult(
                status=CalculationStatus.CALCULATION_FAILURE,
                classification="DISQUALIFIED_CALCULATION_FAILURE",
                phase=None,
                uncertainty_state=None,
                evidence_packet_ref=ref,
                canon_input_valid=False,
            )

        resolution = calculation_result.actual_ephemeris_resolution
        resolution_status = resolution.get("ephemeris_resolution_status")
        if resolution_status is None:
            resolution_status = resolution.get("status")
        if resolution_status != "MATCH" or calculation_result.errors:
            return SignalResult(
                status=CalculationStatus.CALCULATION_FAILURE,
                classification="DISQUALIFIED_CALCULATION_FAILURE",
                phase=None,
                uncertainty_state=None,
                evidence_packet_ref=ref,
                canon_input_valid=False,
            )

        uncertainty = calculation_result.scenario_window_state
        if not isinstance(uncertainty, str) or uncertainty == "NONE":
            return SignalResult(
                status=CalculationStatus.VALID,
                classification="DISQUALIFIED_OUT_OF_ORB",
                phase=None,
                uncertainty_state="NONE",
                evidence_packet_ref=ref,
                canon_input_valid=False,
            )

        phase = self._phase(calculation_result)
        if phase == "NEAR_STATIONARY" or phase is None:
            return SignalResult(
                status=CalculationStatus.VALID,
                classification="DISQUALIFIED_KINEMATIC_STATE",
                phase=phase,
                uncertainty_state=uncertainty,
                evidence_packet_ref=ref,
                canon_input_valid=False,
            )

        # APPROACHING and SEPARATING are only publishable when the Evidence
        # Packet contains an exact event that is future relative to the
        # observation start. No event is inferred.
        if phase in {"APPLYING", "SEPARATING"} and not self._future_exact_event_exists(calculation_result):
            return SignalResult(
                status=CalculationStatus.VALID,
                classification=None,
                phase=phase,
                uncertainty_state=uncertainty,
                evidence_packet_ref=ref,
                canon_input_valid=False,
            )

        if uncertainty == "ROBUST":
            prefix = "ROBUST"
        elif uncertainty in {"POSSIBLE", "MIXED"}:
            prefix = "POSSIBLE"
        else:
            return SignalResult(
                status=CalculationStatus.VALID,
                classification=None,
                phase=phase,
                uncertainty_state=uncertainty,
                evidence_packet_ref=ref,
                canon_input_valid=False,
            )

        if phase == "EXACT":
            classification = f"{prefix}_EXACT_SIGNAL"
        elif phase == "APPLYING":
            classification = f"{prefix}_APPROACHING_SIGNAL"
        elif phase == "SEPARATING":
            classification = f"{prefix}_SEPARATING_SIGNAL"
        else:
            classification = "POSSIBLE_MIXED_SIGNAL" if prefix == "POSSIBLE" else None

        if classification is None:
            return SignalResult(
                status=CalculationStatus.VALID,
                classification=None,
                phase=phase,
                uncertainty_state=uncertainty,
                evidence_packet_ref=ref,
                canon_input_valid=False,
            )

        return SignalResult(
            status=CalculationStatus.VALID,
            classification=classification,
            phase=phase,
            uncertainty_state=uncertainty,
            evidence_packet_ref=ref,
            canon_input_valid=True,
        )
