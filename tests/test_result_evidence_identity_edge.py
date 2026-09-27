from __future__ import annotations

import json
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from ce.calculation.contracts import CalculationResult, ObjectState
from ce.calculation.evidence import EvidencePacket, EvidencePacketRef
from ce.foundation.identity import RuntimeIdentity
from ce.foundation.status import CalculationStatus, ScenarioState
from ce.signal.engine import SignalResult


class ResultEvidenceIdentityEdgeTests(unittest.TestCase):
    def _identity(self) -> RuntimeIdentity:
        return RuntimeIdentity(
            "CE-CALC-V1-EP-001",
            2,
            "a" * 40,
            "b" * 64,
            "sha256:" + "c" * 64,
            "d" * 64,
            "e" * 64,
            "f" * 64,
        )

    def _provenance(self) -> dict[str, str]:
        identity = self._identity()
        return {
            "source_commit": identity.source_commit,
            "source_tree_sha256_v2": identity.source_tree_sha256_v2,
            "dependency_lock_digest": identity.dependency_lock_digest,
            "timezone_bundle_digest": identity.timezone_bundle_digest,
            "ephemeris_bundle_digest": identity.ephemeris_bundle_digest,
            "runtime_image_digest": identity.runtime_image_digest,
            "calculation_version": "0.1.0",
        }

    def _packet(self, value: str, packet_id: str = "E-EDGE-001") -> EvidencePacket:
        return EvidencePacket(
            evidence_packet_id=packet_id,
            input_identity={"value": value},
            profile_version={"id": "CE-CALC-V1-EP-001", "revision": 2},
            observation_instant_or_interval={"start": "2000-01-01T00:00:00Z"},
            timezone_context={"id": "UTC", "version": "NOT_ESTABLISHED"},
            execution_profile_id="CE-CALC-V1-EP-001",
            calculation_version="0.1.0",
            object_records=({"object_id": "sun"},),
            geometry_records=({"kind": "angular_separation"},),
            kinematics=({"object_id": "sun"},),
            warnings=(),
            errors=(),
            numerical_tolerances={"exact_tolerance_deg": 1e-4},
            solver_metadata={},
            actual_ephemeris_resolution={"status": "NOT_ESTABLISHED"},
            calculation_flags={"authoritative": False},
        )

    def _valid_result(self, packet: EvidencePacket) -> CalculationResult:
        return CalculationResult(
            request_id="R-EDGE-001",
            status=CalculationStatus.VALID,
            execution_profile_id="CE-CALC-V1-EP-001",
            scenario_state=ScenarioState.STABLE,
            normalized_time="2026-01-01T00:00:00Z",
            object_states=(ObjectState("sun", 12.5, 0.9, CalculationStatus.VALID),),
            errors=(),
            provenance=self._provenance(),
            _runtime_identity=self._identity(),
            _evidence_packet=packet,
        )

    def test_ref_is_compound_identity_derived_from_concrete_packet(self) -> None:
        packet = self._packet("x")
        ref = EvidencePacketRef.from_packet(packet)
        self.assertEqual(ref.evidence_packet_id, packet.evidence_packet_id)
        self.assertEqual(ref.content_sha256, packet.content_sha256())
        self.assertEqual(ref.as_dict(), {
            "evidence_packet_id": packet.evidence_packet_id,
            "content_sha256": packet.content_sha256(),
        })
        self.assertTrue(ref.matches(packet))

    def test_same_packet_id_with_different_content_is_not_the_same_reference(self) -> None:
        left = self._packet("left", "E-SAME-ID")
        right = self._packet("right", "E-SAME-ID")
        left_ref = EvidencePacketRef.from_packet(left)
        right_ref = EvidencePacketRef.from_packet(right)
        self.assertNotEqual(left_ref.content_sha256, right_ref.content_sha256)
        self.assertNotEqual(left_ref, right_ref)
        self.assertFalse(left_ref.matches(right))

    def test_malformed_compound_reference_is_constructor_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "invalid:evidence_packet_ref:evidence_packet_id"):
            EvidencePacketRef("", "a" * 64)
        with self.assertRaisesRegex(ValueError, "invalid:evidence_packet_ref:content_sha256"):
            EvidencePacketRef("E-1", "not-a-sha256")

    def test_calculation_result_derives_reference_from_packet(self) -> None:
        packet = self._packet("x")
        result = self._valid_result(packet)
        expected = EvidencePacketRef.from_packet(packet)
        self.assertEqual(result.evidence_packet_ref, expected)
        payload = json.loads(result.canonical_bytes().decode("utf-8"))
        self.assertEqual(payload["evidence_packet_ref"], expected.as_dict())

    def test_calculation_result_does_not_accept_caller_supplied_reference(self) -> None:
        packet = self._packet("x")
        with self.assertRaises(TypeError):
            CalculationResult(
                request_id="R-EDGE-002",
                status=CalculationStatus.VALID,
                execution_profile_id="CE-CALC-V1-EP-001",
                scenario_state=ScenarioState.STABLE,
                normalized_time="2026-01-01T00:00:00Z",
                object_states=(ObjectState("sun", 12.5, 0.9, CalculationStatus.VALID),),
                errors=(),
                provenance=self._provenance(),
                _runtime_identity=self._identity(),
                _evidence_packet=packet,
                evidence_packet_ref=EvidencePacketRef.from_packet(packet),  # type: ignore[call-arg]
            )

    def test_calculation_result_detects_swapped_or_stale_packet(self) -> None:
        packet = self._packet("x", "E-SWAP")
        result = self._valid_result(packet)
        replacement = self._packet("y", "E-SWAP")
        object.__setattr__(result, "_evidence_packet", replacement)
        self.assertIn("evidence_packet:reference_mismatch", result.validate())

    def test_calculation_result_nonvalid_state_has_no_evidence_reference(self) -> None:
        result = CalculationResult(
            request_id="R-NONVALID",
            status=CalculationStatus.NON_AUTHORIZED,
            execution_profile_id="CE-CALC-V1-EP-001",
            scenario_state=ScenarioState.NONE,
            normalized_time=None,
            errors=("development-only",),
        )
        self.assertIsNone(result.evidence_packet_ref)
        payload = json.loads(result.canonical_bytes().decode("utf-8"))
        self.assertIsNone(payload["evidence_packet_ref"])

    def test_signal_result_derives_reference_from_packet(self) -> None:
        packet = self._packet("signal")
        result = SignalResult(
            CalculationStatus.VALID,
            "classification",
            "phase",
            "uncertain",
            packet,
            True,
            provenance=self._provenance(),
            _runtime_identity=self._identity(),
        )
        expected = EvidencePacketRef.from_packet(packet)
        self.assertEqual(result.evidence_packet_ref, expected)
        payload = json.loads(result.canonical_bytes().decode("utf-8"))
        self.assertEqual(payload["evidence_packet_ref"], expected.as_dict())

    def test_signal_result_does_not_accept_string_reference(self) -> None:
        with self.assertRaises(ValueError):
            SignalResult(
                CalculationStatus.VALID,
                "classification",
                "phase",
                "uncertain",
                "E-EDGE-001",
                True,
            )

    def test_signal_result_detects_swapped_packet(self) -> None:
        packet = self._packet("signal", "E-SIGNAL-SWAP")
        result = SignalResult(
            CalculationStatus.VALID,
            "classification",
            "phase",
            "uncertain",
            packet,
            True,
        )
        replacement = self._packet("changed", "E-SIGNAL-SWAP")
        object.__setattr__(result, "evidence_packet", replacement)
        self.assertIn("evidence_packet:reference_mismatch", result.validate())

    def test_nonvalid_signal_cannot_carry_evidence_packet(self) -> None:
        with self.assertRaisesRegex(ValueError, "nonvalid_signal_requires_null_evidence_packet"):
            SignalResult(
                CalculationStatus.NON_AUTHORIZED,
                None,
                None,
                None,
                self._packet("forbidden"),
                False,
            )

    def test_issuance_identity_is_stable_and_frozen(self) -> None:
        source = {"nested": {"value": "original"}}
        packet = EvidencePacket(
            evidence_packet_id="E-STABLE",
            input_identity=source,
            profile_version={"id": "CE-CALC-V1-EP-001", "revision": 2},
            observation_instant_or_interval={"start": "2000-01-01T00:00:00Z"},
            timezone_context={"id": "UTC", "version": "NOT_ESTABLISHED"},
            execution_profile_id="CE-CALC-V1-EP-001",
            calculation_version="0.1.0",
            object_records=(),
            geometry_records=(),
            kinematics=(),
            warnings=(),
            errors=(),
            numerical_tolerances={"exact_tolerance_deg": 1e-4},
            solver_metadata={},
            actual_ephemeris_resolution={"status": "NOT_ESTABLISHED"},
            calculation_flags={},
        )
        ref = EvidencePacketRef.from_packet(packet)
        source["nested"]["value"] = "changed-outside"
        self.assertEqual(ref, EvidencePacketRef.from_packet(packet))
        self.assertEqual(ref.content_sha256, packet.content_sha256())

    def test_direct_schema_shape_rejects_bad_hash_and_extra_field(self) -> None:
        # The schema-level checks are exercised independently in test_schema_contracts.
        # This test asserts the Python edge is equally strict at construction.
        with self.assertRaises(ValueError):
            EvidencePacketRef("E-EDGE-001", "0" * 63)
        with self.assertRaises(ValueError):
            EvidencePacketRef("E-EDGE-001", "0" * 64 + "extra")


if __name__ == "__main__":
    unittest.main()
