from __future__ import annotations

import unittest

from ce.calculation.evidence import EvidencePacket
from ce.foundation.identity import RuntimeIdentity
from ce.foundation.provenance import derive_provenance_root_sha256, runtime_identity_sha256
from ce.foundation.status import CalculationStatus
from ce.signal.daily import (
    DailySignalState,
    aggregate_daily_evidence_packets,
    aggregate_daily_signals,
    aggregate_qualified_signal_records,
    aggregate_completed_day,
)
from ce.signal.engine import SignalResult
from ce.signal.record import QualifiedSignalRecord


class DailySignalR1Tests(unittest.TestCase):
    def _packet(self, *, calculation_status: str = "VALID", qualifying: bool = True) -> EvidencePacket:
        runtime = RuntimeIdentity(
            "CE-CALC-V1-EP-001", 4,
            "a" * 40, "b" * 64, "sha256:" + "c" * 64,
            "d" * 64, "e" * 64, "f" * 64,
        )
        input_identity = {
            "request_id": "R-DAY",
            "birth_date": "2000-01-01",
            "birth_city": "Test City",
            "timezone_id": "UTC",
            "timezone_version": "2026d",
            "natal_birth_state": "ZERO_BIRTH_TIME",
            "calendar_policy_id": "CE-V1-CALENDAR-GREGORIAN-ONLY",
        }
        profile = {"id": "CE-CALC-V1-EP-001", "revision": 4}
        timezone_context = {"id": "UTC", "version": "2026d", "database": "IANA"}
        runtime_digest = runtime_identity_sha256(runtime)
        root = derive_provenance_root_sha256(
            calculation_id="C-DAY",
            request_id="R-DAY",
            input_identity=input_identity,
            profile_version=profile,
            timezone_context=timezone_context,
            execution_profile_id="CE-CALC-V1-EP-001",
            calculation_version="CE-CALC-CORE-V1-R1-CONVERGENT",
            runtime_identity_digest=runtime_digest,
        )
        geometry = (
            {
                "transit_object": "SUN",
                "natal_object_or_scenario": "MOON",
                "aspect": "CONJUNCTION",
                "directed_branch": 0.0,
                "signed_deviation": 0.0,
                "absolute_deviation": 0.0,
                "effective_orb": 2.5,
                "qualification_state": "QUALIFIED",
                "kinematic_state": "EXACT",
            },
        ) if qualifying else ()
        return EvidencePacket.issue(
            calculation_id="C-DAY",
            input_identity=input_identity,
            profile_version=profile,
            observation_instant_or_interval={"start": "2026-01-01T00:00:00Z", "end": "2026-01-02T00:00:00Z"},
            timezone_context=timezone_context,
            execution_profile_id="CE-CALC-V1-EP-001",
            calculation_version="CE-CALC-CORE-V1-R1-CONVERGENT",
            object_records=(),
            geometry_records=geometry,
            effective_orb_records=(),
            kinematics=(
                {
                    "transit_object": "SUN",
                    "aspect": "CONJUNCTION",
                    "kinematic_state": "EXACT",
                    "transit_speed": 1.0,
                },
            ) if qualifying else (),
            exact_events=(),
            window_segments=(),
            scenario_stability_state="STABLE",
            scenario_window_state="ROBUST" if qualifying else "NONE",
            warnings=(),
            errors=(),
            numerical_tolerances={},
            solver_metadata={},
            actual_ephemeris_resolution={"ephemeris_resolution_status": "MATCH"},
            calculation_flags={"calculation_status": calculation_status},
            runtime_identity_sha256=runtime_digest,
            provenance_root_sha256=root,
        )

    def _result(self, *, status: CalculationStatus = CalculationStatus.VALID) -> SignalResult:
        return SignalResult(status, None, None, None, "R:hash", False)

    def _record(self) -> QualifiedSignalRecord:
        return QualifiedSignalRecord(
            "CE-QUALIFIED-SIGNAL-RECORD-V1",
            "CE-SIGNAL-" + "1" * 64,
            "E-1:" + "2" * 64,
            "2026-01-01T00:00:00Z",
            "VALID",
            "ROBUST_EXACT_SIGNAL",
            "EXACT",
            "UNIFORM",
            True,
            False,
            "sha256:" + "3" * 64,
        )

    def test_empty_completed_day_is_quiet_sky(self) -> None:
        result = aggregate_daily_evidence_packets((), observation_completed=True)
        self.assertEqual(result.state, DailySignalState.QUIET_SKY)

    def test_qualifying_packet_prevents_quiet_sky(self) -> None:
        result = aggregate_daily_evidence_packets(
            (self._packet(),),
            observation_completed=True,
        )
        self.assertEqual(result.state, DailySignalState.QUALIFYING_SIGNALS_PRESENT)
        self.assertEqual(len(result.qualifying_signal_refs), 1)

    def test_non_qualifying_packet_produces_quiet_sky(self) -> None:
        result = aggregate_daily_evidence_packets(
            (self._packet(qualifying=False),),
            observation_completed=True,
        )
        self.assertEqual(result.state, DailySignalState.QUIET_SKY)

    def test_failed_packet_never_becomes_quiet_sky(self) -> None:
        with self.assertRaisesRegex(ValueError, "qualified_signal_result_not_eligible"):
            aggregate_daily_evidence_packets(
                (self._packet(calculation_status="CALCULATION_FAILURE", qualifying=False),),
                observation_completed=True,
            )

    def test_legacy_signal_result_aggregation_path_is_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "daily_signal_result_path_removed"):
            aggregate_daily_signals((self._result(),))

    def test_legacy_qsr_aggregation_path_is_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "daily_qsr_path_removed"):
            aggregate_qualified_signal_records((self._record(),), observation_completed=True)

    def test_completed_day_rejects_unfinished_observation(self) -> None:
        with self.assertRaisesRegex(ValueError, "daily_observation_not_completed"):
            aggregate_completed_day((), observation_completed=False)

    def test_completed_day_uses_evidence_packets(self) -> None:
        result = aggregate_completed_day(
            (self._packet(),),
            observation_completed=True,
        )
        self.assertEqual(result.state, DailySignalState.QUALIFYING_SIGNALS_PRESENT)


if __name__ == "__main__":
    unittest.main()
