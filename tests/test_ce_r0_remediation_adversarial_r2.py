from __future__ import annotations

from datetime import date
import unittest

from ce.calculation.contracts import BirthInput, CalculationRequest
from ce.calculation.evidence import EvidencePacket
from ce.calculation.evidence_builder import issue_evidence_packet
from ce.foundation.identity import RuntimeIdentity
from ce.foundation.provenance import derive_provenance_root_sha256
from ce.foundation.status import CalculationStatus, NatalBirthState, ScenarioState
from ce.signal.record import issue_qualified_signal_record


class CER0DirectEvidenceIssuanceBypassTests(unittest.TestCase):
    """Adversarial proof: cryptographic self-consistency is not issuance authority."""

    def _runtime(self) -> RuntimeIdentity:
        return RuntimeIdentity(
            "CE-CALC-V1-EP-001", 4,
            "a" * 40, "b" * 64, "sha256:" + "c" * 64,
            "d" * 64, "e" * 64, "f" * 64,
        )

    def _forged_packet(self) -> EvidencePacket:
        # Deliberately omit any CalculationRequest/RuntimeIdentity object from
        # the packet issuance call. The caller supplies a synthetic runtime
        # digest and derives a matching provenance root from it.
        runtime_digest = "f" * 64
        input_identity = {
            "request_id": "FORGED-REQ-001",
            "birth_date": "2000-01-01",
            "birth_city": "Forged City",
            "timezone_id": "UTC",
            "timezone_version": "2026d",
            "natal_birth_state": "ZERO_BIRTH_TIME",
            "calendar_policy_id": "CE-V1-CALENDAR-GREGORIAN-ONLY",
        }
        profile = {
            "id": "CE-CALC-V1-EP-001",
            "revision": 4,
            "implementation_plan_version": "1.3.1",
            "technical_contracts_version": "1.1",
            "execution_profile_version": "1.3",
        }
        timezone_context = {"database": "IANA", "id": "UTC", "version": "2026d"}
        root = derive_provenance_root_sha256(
            calculation_id="FORGED-CALC-001",
            request_id=input_identity["request_id"],
            input_identity=input_identity,
            profile_version=profile,
            timezone_context=timezone_context,
            execution_profile_id="CE-CALC-V1-EP-001",
            calculation_version="CE-CALC-CORE-V1-R1-CONVERGENT",
            runtime_identity_digest=runtime_digest,
        )
        return EvidencePacket.issue(
            calculation_id="FORGED-CALC-001",
            input_identity=input_identity,
            profile_version=profile,
            observation_instant_or_interval={
                "start": "2026-01-01T00:00:00Z",
                "end": "2026-01-02T00:00:00Z",
            },
            timezone_context=timezone_context,
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
            warnings=("SYNTHETIC",),
            errors=(),
            numerical_tolerances={},
            solver_metadata={},
            actual_ephemeris_resolution={"ephemeris_resolution_status": "MATCH"},
            calculation_flags={"calculation_status": CalculationStatus.VALID.value},
            runtime_identity_sha256=runtime_digest,
            provenance_root_sha256=root,
        )

    def test_public_issue_path_cannot_materialize_publishable_signal_without_authoritative_request_runtime(self):
        packet = self._forged_packet()
        self.assertEqual(packet.evidence_packet_id, packet.content_sha256())
        with self.assertRaisesRegex(ValueError, r"qualified_signal_evidence|issuance|runtime_identity"):
            issue_qualified_signal_record(packet)

    def test_controlled_builder_still_requires_request_and_runtime(self):
        # Positive control: the intended builder path remains explicitly bound.
        from ce.calculation.contracts import CalculationResultDraft
        request = CalculationRequest(
            request_id="REQ-001",
            birth=BirthInput(
                date(2000, 1, 1), "Test City", "UTC", "2026d",
                NatalBirthState.ZERO_BIRTH_TIME,
            ),
            target_interval_start_utc="2026-01-01T00:00:00Z",
            target_interval_end_utc="2026-01-02T00:00:00Z",
            execution_profile_id="CE-CALC-V1-EP-001",
        )
        draft = CalculationResultDraft(
            request_id=request.request_id,
            status=CalculationStatus.NATAL_EVIDENCE_VARIABLE,
            execution_profile_id=request.execution_profile_id,
            scenario_state=ScenarioState.VARIABLE,
            normalized_time=None,
            calculation_id="CALC-001",
            observation_interval=(
                request.target_interval_start_utc,
                request.target_interval_end_utc,
            ),
        )
        packet = issue_evidence_packet(
            draft,
            request=request,
            runtime_identity=self._runtime(),
        )
        self.assertEqual(packet.input_identity["request_id"], request.request_id)


if __name__ == "__main__":
    unittest.main()
