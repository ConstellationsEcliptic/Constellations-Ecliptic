from __future__ import annotations

import json
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, os.path.dirname(__file__))

from ce.calculation.evidence import EvidencePacket
from ce.foundation.hashing import sha256_bytes
from ce.foundation.serialization import canonical_json
from test_schema_contracts import _validate_schema_instance, SchemaContractTests


class EvidencePacketInstanceVerificationTests(unittest.TestCase):
    def _source_payload(self, reverse: bool = False) -> dict[str, object]:
        mappings = {
            "input_identity": {"source": "test", "profile": {"revision": 2, "id": "CE-CALC-V1-EP-001"}},
            "profile_version": {"revision": 2, "id": "CE-CALC-V1-EP-001"},
            "observation_instant_or_interval": {"start": "2000-01-01T00:00:00Z"},
            "timezone_context": {"version": "NOT_ESTABLISHED", "id": "UTC"},
            "numerical_tolerances": {"exact_tolerance_deg": 1e-4},
            "solver_metadata": {"mode": "development"},
            "actual_ephemeris_resolution": {"status": "NOT_ESTABLISHED"},
            "calculation_flags": {"authoritative": False},
        }
        if not reverse:
            return mappings
        return {
            key: value
            for key, value in reversed(list(mappings.items()))
        }

    def _packet(self, *, reverse: bool = False) -> EvidencePacket:
        m = self._source_payload(reverse=reverse)
        return EvidencePacket(
            evidence_packet_id="E-INSTANCE-001",
            input_identity=m["input_identity"],
            profile_version=m["profile_version"],
            observation_instant_or_interval=m["observation_instant_or_interval"],
            timezone_context=m["timezone_context"],
            execution_profile_id="CE-CALC-V1-EP-001",
            calculation_version="0.1.0",
            object_records=({"object_id": "sun"},),
            geometry_records=({"kind": "angular_separation"},),
            kinematics=({"object_id": "sun"},),
            warnings=("development-only",),
            errors=(),
            numerical_tolerances=m["numerical_tolerances"],
            solver_metadata=m["solver_metadata"],
            actual_ephemeris_resolution=m["actual_ephemeris_resolution"],
            calculation_flags=m["calculation_flags"],
        )

    def test_concrete_instance_validates_before_issuance(self) -> None:
        packet = self._packet()
        self.assertEqual(packet.validate(), ())

    def test_issuance_bytes_are_self_canonical_and_hash_exact(self) -> None:
        packet = self._packet()
        issued = packet.canonical_bytes()
        decoded = json.loads(issued.decode("utf-8"))

        self.assertEqual(issued, canonical_json(decoded))
        self.assertEqual(packet.content_sha256(), sha256_bytes(issued))
        self.assertNotIn("_canonical_bytes", decoded)
        self.assertNotIn("content_sha256", decoded)

    def test_issuance_instance_has_exact_established_top_level_shape(self) -> None:
        packet = self._packet()
        decoded = json.loads(packet.canonical_bytes().decode("utf-8"))
        expected = {
            "evidence_packet_id",
            "input_identity",
            "profile_version",
            "observation_instant_or_interval",
            "timezone_context",
            "execution_profile_id",
            "calculation_version",
            "object_records",
            "geometry_records",
            "kinematics",
            "warnings",
            "errors",
            "numerical_tolerances",
            "solver_metadata",
            "actual_ephemeris_resolution",
            "calculation_flags",
        }
        self.assertEqual(set(decoded), expected)

    def test_equivalent_mapping_order_produces_identical_instance_identity(self) -> None:
        left = self._packet(reverse=False)
        right = self._packet(reverse=True)
        self.assertEqual(left.canonical_bytes(), right.canonical_bytes())
        self.assertEqual(left.content_sha256(), right.content_sha256())

    def test_nested_source_mutation_cannot_change_issued_instance(self) -> None:
        source = self._source_payload()
        packet = EvidencePacket(
            evidence_packet_id="E-INSTANCE-002",
            input_identity=source["input_identity"],
            profile_version=source["profile_version"],
            observation_instant_or_interval=source["observation_instant_or_interval"],
            timezone_context=source["timezone_context"],
            execution_profile_id="CE-CALC-V1-EP-001",
            calculation_version="0.1.0",
            object_records=({"nested": {"value": "original"}},),
            geometry_records=(),
            kinematics=(),
            warnings=(),
            errors=(),
            numerical_tolerances=source["numerical_tolerances"],
            solver_metadata=source["solver_metadata"],
            actual_ephemeris_resolution=source["actual_ephemeris_resolution"],
            calculation_flags=source["calculation_flags"],
        )
        issued = packet.canonical_bytes()
        original_hash = packet.content_sha256()

        source["input_identity"]["profile"]["revision"] = 999
        source["numerical_tolerances"]["exact_tolerance_deg"] = 999.0

        self.assertEqual(packet.canonical_bytes(), issued)
        self.assertEqual(packet.content_sha256(), original_hash)
        self.assertEqual(packet.input_identity["profile"]["revision"], 2)
        self.assertEqual(packet.numerical_tolerances["exact_tolerance_deg"], 1e-4)

    def test_concrete_instance_matches_established_schema(self) -> None:
        schema = SchemaContractTests()._schema("evidence_packet.schema.json")
        packet = self._packet()
        decoded = json.loads(packet.canonical_bytes().decode("utf-8"))
        self.assertEqual(_validate_schema_instance(schema, decoded), [])


if __name__ == "__main__":
    unittest.main()
