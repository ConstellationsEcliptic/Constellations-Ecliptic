from __future__ import annotations

import inspect
import unittest

from ce.calculation.evidence import EvidencePacket


class CER0A1IssuanceBoundaryTests(unittest.TestCase):
    def test_public_issue_api_is_absent(self) -> None:
        self.assertFalse(hasattr(EvidencePacket, "issue"))

    def test_constructor_does_not_accept_issuance_provenance(self) -> None:
        parameters = inspect.signature(EvidencePacket).parameters
        self.assertNotIn("runtime_identity_sha256", parameters)
        self.assertNotIn("provenance_root_sha256", parameters)

    def test_direct_constructor_creates_only_unissued_packet(self) -> None:
        packet = EvidencePacket(
            evidence_packet_id="UNISSUED-FIXTURE",
            calculation_id="FORGED-CALCULATION",
            input_identity={"request_id": "FORGED-REQUEST"},
            profile_version={
                "id": "CE-CALC-V1-EP-001",
                "revision": 4,
            },
            observation_instant_or_interval={
                "start": "2026-01-01T00:00:00Z",
                "end": "2026-01-02T00:00:00Z",
            },
            timezone_context={
                "database": "IANA",
                "id": "UTC",
                "version": "2026d",
            },
            execution_profile_id="CE-CALC-V1-EP-001",
            calculation_version="FORGED-VERSION",
            object_records=(),
            geometry_records=(),
            effective_orb_records=(),
            kinematics=(),
            exact_events=(),
            window_segments=(),
            scenario_stability_state="VARIABLE",
            scenario_window_state="NONE",
            warnings=(),
            errors=(),
            numerical_tolerances={},
            solver_metadata={},
            actual_ephemeris_resolution={},
            calculation_flags={},
        )

        self.assertEqual(packet.evidence_packet_id, "UNISSUED-FIXTURE")
        self.assertIsNone(packet.runtime_identity_sha256)
        self.assertIsNone(packet.provenance_root_sha256)

        self.assertIn(
            "evidence_packet_issuance_binding_missing",
            packet.validate(require_issued=True),
        )

    def test_constructor_rejects_issuance_provenance_arguments(self) -> None:
        common = {
            "evidence_packet_id": "FORGED-PACKET",
            "calculation_id": "FORGED-CALCULATION",
            "input_identity": {"request_id": "FORGED-REQUEST"},
            "profile_version": {
                "id": "CE-CALC-V1-EP-001",
                "revision": 4,
            },
            "observation_instant_or_interval": {
                "start": "2026-01-01T00:00:00Z",
            },
            "timezone_context": {
                "database": "IANA",
                "id": "UTC",
                "version": "2026d",
            },
            "execution_profile_id": "CE-CALC-V1-EP-001",
            "calculation_version": "FORGED-VERSION",
            "object_records": (),
            "geometry_records": (),
            "effective_orb_records": (),
            "kinematics": (),
            "exact_events": (),
            "window_segments": (),
            "scenario_stability_state": "VARIABLE",
            "scenario_window_state": "NONE",
            "warnings": (),
            "errors": (),
            "numerical_tolerances": {},
            "solver_metadata": {},
            "actual_ephemeris_resolution": {},
            "calculation_flags": {},
            "runtime_identity_sha256": "a" * 64,
            "provenance_root_sha256": "b" * 64,
        }

        with self.assertRaises(TypeError):
            EvidencePacket(**common)


if __name__ == "__main__":
    unittest.main()
