from __future__ import annotations

from datetime import date
import unittest

from ce.calculation.contracts import CalculationResultDraft, ObjectRecord, BirthInput, CalculationRequest, ObjectState
from ce.calculation.evidence_builder import EvidenceIssuanceError, issue_evidence_packet
from ce.foundation.identity import RuntimeIdentity
from ce.foundation.status import CalculationStatus, NatalBirthState, ScenarioState


class EvidenceBuilderR1Tests(unittest.TestCase):
    def _identity(self) -> RuntimeIdentity:
        return RuntimeIdentity(
            "CE-CALC-V1-EP-001", 4,
            "a" * 40, "b" * 64, "sha256:" + "c" * 64,
            "d" * 64, "e" * 64, "f" * 64,
        )

    def _request(self, request_id: str = "R-VALID") -> CalculationRequest:
        return CalculationRequest(
            request_id=request_id,
            birth=BirthInput(
                date(2026, 1, 1),
                "Test City",
                "UTC",
                "2026d",
                NatalBirthState.ZERO_BIRTH_TIME,
            ),
            target_interval_start_utc="2026-01-01T00:00:00Z",
            target_interval_end_utc="2026-01-02T00:00:00Z",
            execution_profile_id="CE-CALC-V1-EP-001",
        )

    def _draft(self, request_id: str, status: CalculationStatus, calculation_id: str = "C-VALID") -> CalculationResultDraft:
        return CalculationResultDraft(
            request_id=request_id,
            status=status,
            execution_profile_id="CE-CALC-V1-EP-001",
            scenario_state=ScenarioState.VARIABLE if status is CalculationStatus.NATAL_EVIDENCE_VARIABLE else ScenarioState.STABLE,
            normalized_time=None,
            calculation_id=calculation_id,
            observation_interval=("2026-01-01T00:00:00Z", "2026-01-02T00:00:00Z"),
            object_records=(),
        )

    def test_nonissuable_status_is_rejected(self) -> None:
        result = self._draft("R-ERR", CalculationStatus.NON_AUTHORIZED, "C-ERR")
        with self.assertRaisesRegex(EvidenceIssuanceError, "result_status_not_evidence_issuable"):
            issue_evidence_packet(
                result,
                request=self._request("R-ERR"),
                runtime_identity=self._identity(),
            )

    def test_variable_result_uses_request_and_runtime_provenance(self) -> None:
        request = self._request("R-VAR")
        result = self._draft("R-VAR", CalculationStatus.NATAL_EVIDENCE_VARIABLE, "C-VAR")
        issued = issue_evidence_packet(
            result,
            request=request,
            runtime_identity=self._identity(),
        )
        self.assertEqual(issued.calculation_id, "C-VAR")
        self.assertEqual(issued.input_identity["birth_date"], "2026-01-01")
        self.assertEqual(issued.input_identity["birth_city"], "Test City")
        self.assertEqual(issued.profile_version["implementation_plan_version"], "1.3.1")
        self.assertEqual(issued.timezone_context["database"], "IANA")
        self.assertEqual(len(issued.content_sha256()), 64)

    def test_request_mismatch_is_rejected(self) -> None:
        result = self._draft("R-OTHER", CalculationStatus.NATAL_EVIDENCE_VARIABLE, "C-OTHER")
        with self.assertRaisesRegex(EvidenceIssuanceError, "request_id_mismatch"):
            issue_evidence_packet(
                result,
                request=self._request("R-EXPECTED"),
                runtime_identity=self._identity(),
            )

    def test_observation_interval_mismatch_is_rejected(self) -> None:
        result = self._draft("R-VALID", CalculationStatus.NATAL_EVIDENCE_VARIABLE, "C-INTERVAL")
        result = CalculationResultDraft(
            request_id=result.request_id,
            status=result.status,
            execution_profile_id=result.execution_profile_id,
            scenario_state=result.scenario_state,
            normalized_time=None,
            calculation_id=result.calculation_id,
            observation_interval=("2026-01-01T01:00:00Z", "2026-01-02T00:00:00Z"),
        )
        with self.assertRaisesRegex(EvidenceIssuanceError, "observation_interval_request_mismatch"):
            issue_evidence_packet(
                result,
                request=self._request("R-VALID"),
                runtime_identity=self._identity(),
            )

    def test_valid_result_requires_real_object_record(self) -> None:
        request = self._request("R-VALID")
        result = self._draft("R-VALID", CalculationStatus.VALID, "C-VALID")
        with self.assertRaisesRegex(EvidenceIssuanceError, "valid_result_requires_object_records"):
            issue_evidence_packet(result, request=request, runtime_identity=self._identity())


if __name__ == "__main__":
    unittest.main()
