from __future__ import annotations

import unittest

from ce.calculation.contracts import CalculationResult, ObjectRecord
from ce.calculation.evidence_builder import EvidenceIssuanceError, issue_evidence_packet
from ce.foundation.status import CalculationStatus, ScenarioState


class EvidenceBuilderR1Tests(unittest.TestCase):
    def test_nonissuable_status_is_rejected(self) -> None:
        result = CalculationResult(
            request_id="R-ERR",
            status=CalculationStatus.NON_AUTHORIZED,
            execution_profile_id="CE-CALC-V1-EP-001",
            scenario_state=ScenarioState.NONE,
            normalized_time=None,
        )
        with self.assertRaisesRegex(EvidenceIssuanceError, "result_status_not_evidence_issuable"):
            issue_evidence_packet(
                result,
                input_identity={},
                profile_version={"id": "CE-CALC-V1-EP-001", "revision": 4},
                timezone_context={"id": "UTC", "version": "2026d"},
            )

    def test_valid_result_requires_real_object_record(self) -> None:
        result = CalculationResult(
            request_id="R-VALID",
            status=CalculationStatus.VALID,
            execution_profile_id="CE-CALC-V1-EP-001",
            scenario_state=ScenarioState.STABLE,
            normalized_time="2026-01-01T00:00:00Z",
            calculation_id="C-VALID",
            observation_interval=("2026-01-01T00:00:00Z", "2026-01-01T01:00:00Z"),
            object_states=(),
            provenance={},
        )
        with self.assertRaisesRegex(EvidenceIssuanceError, "valid_result_requires_object_records"):
            issue_evidence_packet(
                result,
                input_identity={},
                profile_version={"id": "CE-CALC-V1-EP-001", "revision": 4},
                timezone_context={"id": "UTC", "version": "2026d"},
            )

    def test_variable_result_can_issue_packet_without_exact_natal_coordinate(self) -> None:
        identity = __import__(
            "ce.foundation.identity", fromlist=["RuntimeIdentity"]
        ).RuntimeIdentity(
            "CE-CALC-V1-EP-001", 4,
            "a" * 40, "b" * 64, "sha256:" + "c" * 64,
            "d" * 64, "e" * 64, "f" * 64,
        )
        result = CalculationResult(
            request_id="R-VAR",
            status=CalculationStatus.NATAL_EVIDENCE_VARIABLE,
            execution_profile_id="CE-CALC-V1-EP-001",
            scenario_state=ScenarioState.VARIABLE,
            normalized_time=None,
            calculation_id="C-VAR",
            observation_interval=("2026-01-01T00:00:00Z", "2026-01-02T00:00:00Z"),
            object_states=(),
            object_records=(),
            provenance={
                "source_commit": "a" * 40,
                "source_tree_sha256_v2": "b" * 64,
                "dependency_lock_digest": "d" * 64,
                "timezone_bundle_digest": "e" * 64,
                "ephemeris_bundle_digest": "f" * 64,
                "runtime_image_digest": "sha256:" + "c" * 64,
                "timezone_bundle_digest": "e" * 64,
                "ephemeris_bundle_digest": "f" * 64,
                "calculation_version": "CE-CALC-CORE-V1-R1-CONVERGENT",
            },
            _runtime_identity=identity,
        )
        packet = issue_evidence_packet(
            result,
            input_identity={"birth_date": "2026-01-01"},
            profile_version={"id": "CE-CALC-V1-EP-001", "revision": 4},
            timezone_context={"id": "UTC", "version": "2026d"},
        )
        self.assertEqual(packet.calculation_id, "C-VAR")
        self.assertEqual(packet.scenario_stability_state, "VARIABLE")


if __name__ == "__main__":
    unittest.main()
