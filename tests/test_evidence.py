from __future__ import annotations

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from ce.calculation.evidence import EvidencePacket


class EvidenceTests(unittest.TestCase):
    def _packet(self, value: str) -> EvidencePacket:
        return EvidencePacket(
            evidence_packet_id="E-001",
            input_identity={"value": value},
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

    def test_same_payload_same_hash(self) -> None:
        self.assertEqual(self._packet("x").content_sha256(), self._packet("x").content_sha256())

    def test_mutation_changes_hash_for_distinct_packets(self) -> None:
        self.assertNotEqual(self._packet("x").content_sha256(), self._packet("y").content_sha256())

    def test_packet_mapping_is_immutable(self) -> None:
        packet = self._packet("x")
        with self.assertRaises(TypeError):
            packet.input_identity["value"] = "mutated"

    def test_packet_mapping_rejects_in_place_union(self) -> None:
        packet = self._packet("x")
        mapping = packet.input_identity
        with self.assertRaises(TypeError):
            mapping |= {"new": "value"}
        self.assertEqual(mapping, {"value": "x"})

    def test_content_identity_is_stable_after_source_input_mutation(self) -> None:
        source = {"value": "x"}
        packet = EvidencePacket(
            evidence_packet_id="E-002",
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
        original_hash = packet.content_sha256()
        source["value"] = "changed-outside-packet"
        self.assertEqual(packet.content_sha256(), original_hash)
        self.assertEqual(packet.input_identity["value"], "x")
