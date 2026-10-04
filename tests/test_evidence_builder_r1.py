from __future__ import annotations

import unittest

from ce.calculation.contracts import CalculationResult, ObjectRecord, ObjectState
from ce.calculation.evidence import EvidencePacket
from ce.calculation.evidence_builder import EvidenceIssuanceError, issue_evidence_packet
from ce.foundation.identity import RuntimeIdentity
from ce.foundation.status import CalculationStatus, ScenarioState


class EvidenceBuilderR1Tests(unittest.TestCase):
    def _identity(self) -> RuntimeIdentity:
        return RuntimeIdentity(
            "CE-CALC-V1-EP-001", 4,
            "a" * 40, "b" * 64, "sha256:" + "c" * 64,
            "d" * 64, "e" * 64, "f" * 64,
        )

    def _packet(self, calculation_id: str) -> EvidencePacket:
        return EvidencePacket(
            evidence_packet_id="E-INPUT",
            calculation_id=calculation_id,
            input_identity={"birth_date": "2026-01-01"},
            profile_version={"id": "CE-CALC-V1-EP-001", "revision": 4},
            observation_instant_or_interval={
                "start": "2026-01-01T00:00:00Z",
                "end": "2026-01-02T00:00:00Z",
            },
            timezone_context={"id": "UTC", "version": "2026d"},
            execution_profile_id="CE-CALC-V1-EP-001",
            calculation_version="CE-CALC-CORE-V1-R1-CONVERGENT",
            object_records=(),
            geometry_records=(),
            effective_orb_records=(),
            kinematics=(),
            exact_events=(),
            window_segments=(),
            scenario_stability_state="STABLE",
            warnings=(),
            errors=(),
            numerical_tolerances={},
            solver_metadata={},
            actual_ephemeris_resolution={"status": "NOT_ESTABLISHED"},
            calculation_flags={},
        )

    def _valid_result(
        self,
        calculation_id: str,
        *,
        object_records: tuple[ObjectRecord, ...],
        packet: EvidencePacket,
    ) -> CalculationResult:
        return CalculationResult(
            request_id="R-" + calculation_id,
            status=CalculationStatus.VALID,
            execution_profile_id="CE-CALC-V1-EP-001",
            scenario_state=ScenarioState.STABLE,
            normalized_time="2026-01-01T00:00:00Z",
            calculation_id=calculation_id,
            observation_interval=("2026-01-01T00:00:00Z", "2026-01-01T01:00:00Z"),
            object_states=(
                ObjectState("SUN", 12.5, 0.9, CalculationStatus.VALID),
            ),
            object_records=object_records,
            provenance={
                "source_commit": "a" * 40,
                "source_tree_sha256_v2": "b" * 64,
                "dependency_lock_digest": "d" * 64,
                "timezone_bundle_digest": "e" * 64,
                "ephemeris_bundle_digest": "f" * 64,
                "runtime_image_digest": "sha256:" + "c" * 64,
                "calculation_version": "CE-CALC-CORE-V1-R1-CONVERGENT",
            },
            _runtime_identity=self._identity(),
            _evidence_packet=packet,
        )

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
        packet = self._packet("C-VALID")
        result = self._valid_result("C-VALID", object_records=(), packet=packet)
        with self.assertRaisesRegex(EvidenceIssuanceError, "valid_result_requires_object_records"):
            issue_evidence_packet(
                result,
                input_identity={},
                profile_version={"id": "CE-CALC-V1-EP-001", "revision": 4},
                timezone_context={"id": "UTC", "version": "2026d"},
            )

    def test_variable_result_can_issue_packet_without_exact_natal_coordinate(self) -> None:
        packet = self._packet("C-VAR")
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
                "calculation_version": "CE-CALC-CORE-V1-R1-CONVERGENT",
            },
            _runtime_identity=self._identity(),
            _evidence_packet=packet,
        )
        issued = issue_evidence_packet(
            result,
            input_identity={"birth_date": "2026-01-01"},
            profile_version={"id": "CE-CALC-V1-EP-001", "revision": 4},
            timezone_context={"id": "UTC", "version": "2026d"},
        )
        self.assertEqual(issued.calculation_id, "C-VAR")
        self.assertEqual(issued.scenario_stability_state, "VARIABLE")
        self.assertEqual(len(issued.content_sha256()), 64)


if __name__ == "__main__":
    unittest.main()
