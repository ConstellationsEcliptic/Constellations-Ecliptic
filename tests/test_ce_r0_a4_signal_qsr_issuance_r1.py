from __future__ import annotations

from datetime import date
import unittest

from ce.calculation.evidence import EvidencePacket
from ce.foundation.status import CalculationStatus
from ce.foundation.identity import RuntimeIdentity
from ce.foundation.provenance import derive_provenance_root_sha256, runtime_identity_sha256
from ce.signal.daily import _aggregate_issued_records
from ce.signal.engine import SignalEngine, SignalResult
from ce.signal.record import QualifiedSignalRecord, issue_qualified_signal_record
from tests.evidence_test_factory_r1 import build_test_bound_evidence_packet


class CER0A4SignalQsrIssuanceTests(unittest.TestCase):
    def _packet(self) -> EvidencePacket:
        runtime = RuntimeIdentity(
            "CE-CALC-V1-EP-001", 4,
            "a" * 40, "b" * 64, "sha256:" + "c" * 64,
            "d" * 64, "e" * 64, "f" * 64,
            control_plane_sha256="9" * 64,
        )
        input_identity = {
            "request_id": "R-A4",
            "birth_date": "2000-01-01",
            "birth_city": "Test City",
            "timezone_id": "UTC",
            "timezone_version": "2026d",
            "natal_birth_state": "ZERO_BIRTH_TIME",
            "calendar_policy_id": "CE-V1-CALENDAR-GREGORIAN-ONLY",
        }
        profile = {"id": "CE-CALC-V1-EP-001", "revision": 4}
        timezone_context = {"id": "UTC", "version": "2026d"}
        runtime_digest = runtime_identity_sha256(runtime)
        provenance_root = derive_provenance_root_sha256(
            calculation_id="C-A4",
            request_id="R-A4",
            input_identity=input_identity,
            profile_version=profile,
            timezone_context=timezone_context,
            execution_profile_id="CE-CALC-V1-EP-001",
            calculation_version="CE-CALC-CORE-V1-R1-CONVERGENT",
            runtime_identity_digest=runtime_digest,
        )
        return build_test_bound_evidence_packet(
            evidence_packet_id="fixture",
            calculation_id="C-A4",
            input_identity={
                "request_id": "R-A4",
                "birth_date": "2000-01-01",
                "birth_city": "Test City",
                "timezone_id": "UTC",
                "timezone_version": "2026d",
                "natal_birth_state": "ZERO_BIRTH_TIME",
                "calendar_policy_id": "CE-V1-CALENDAR-GREGORIAN-ONLY",
            },
            profile_version={"id": "CE-CALC-V1-EP-001", "revision": 4},
            observation_instant_or_interval={
                "start": "2026-01-01T00:00:00Z",
                "end": "2026-01-02T00:00:00Z",
            },
            timezone_context={"id": "UTC", "version": "2026d"},
            execution_profile_id="CE-CALC-V1-EP-001",
            calculation_version="CE-CALC-CORE-V1-R1-CONVERGENT",
            object_records=(),
            geometry_records=(
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
            ),
            effective_orb_records=(),
            kinematics=(
                {
                    "transit_object": "SUN",
                    "aspect": "CONJUNCTION",
                    "kinematic_state": "EXACT",
                    "transit_speed": 1.0,
                },
            ),
            exact_events=(),
            window_segments=(),
            scenario_stability_state="STABLE",
            scenario_window_state="ROBUST",
            warnings=(),
            errors=(),
            numerical_tolerances={},
            solver_metadata={},
            actual_ephemeris_resolution={"ephemeris_resolution_status": "MATCH"},
            calculation_flags={"calculation_status": "VALID"},
            runtime_identity_sha256=runtime_digest,
            provenance_root_sha256=provenance_root,
        )

    def test_signal_result_direct_constructor_is_not_issuance_path(self) -> None:
        with self.assertRaisesRegex(ValueError, "signal_result_must_be_issued"):
            SignalResult(
                CalculationStatus.VALID,
                "ROBUST_EXACT_SIGNAL",
                "EXACT",
                "ROBUST",
                "E:hash",
                True,
            )

    def test_qsr_direct_constructor_is_not_issuance_path(self) -> None:
        with self.assertRaisesRegex(ValueError, "qualified_signal_record_must_be_issued"):
            QualifiedSignalRecord(
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

    def test_signal_engine_returns_issued_result(self) -> None:
        result = SignalEngine().evaluate(self._packet())
        self.assertEqual(result.status, CalculationStatus.VALID)
        self.assertEqual(result.validate(), ())

    def test_qsr_issuance_returns_issued_record(self) -> None:
        record = issue_qualified_signal_record(self._packet())
        self.assertEqual(record.validate(), ())

    def test_daily_internal_aggregation_rejects_unissued_record(self) -> None:
        record = object.__new__(QualifiedSignalRecord)
        with self.assertRaisesRegex(ValueError, "daily_qualified_signal_record_not_issued"):
            _aggregate_issued_records((record,), observation_completed=True)


if __name__ == "__main__":
    unittest.main()
