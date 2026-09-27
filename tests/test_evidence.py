from __future__ import annotations

import os
import sys
import unittest
from datetime import datetime
from decimal import Decimal

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from ce.calculation.evidence import EvidencePacket


class EvidenceTests(unittest.TestCase):
    def _packet(self, value: str, **overrides: object) -> EvidencePacket:
        values = dict(
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
        values.update(overrides)
        return EvidencePacket(**values)

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

    def test_invalid_scalar_fields_are_rejected(self) -> None:
        for field_name, value, token in (
            ("evidence_packet_id", 123, "invalid:evidence_packet_id"),
            ("evidence_packet_id", "   ", "invalid:evidence_packet_id"),
            ("calculation_version", 123, "invalid:calculation_version"),
            ("calculation_version", "", "invalid:calculation_version"),
        ):
            with self.assertRaisesRegex(ValueError, token):
                self._packet("x", **{field_name: value})

    def test_noncanonical_execution_profile_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "unrecognized:execution_profile_id"):
            self._packet("x", execution_profile_id="CE-CALC-V1-EP-ALT")

    def test_mapping_fields_require_mapping_values(self) -> None:
        for field_name in (
            "input_identity",
            "profile_version",
            "observation_instant_or_interval",
            "timezone_context",
            "numerical_tolerances",
            "solver_metadata",
            "actual_ephemeris_resolution",
            "calculation_flags",
        ):
            with self.assertRaisesRegex(ValueError, f"invalid:{field_name}:mapping_required"):
                self._packet("x", **{field_name: ("not-a-mapping",)})

    def test_record_fields_require_mapping_members(self) -> None:
        for field_name in ("object_records", "geometry_records", "kinematics"):
            with self.assertRaisesRegex(ValueError, f"invalid:{field_name}\\[0\\]:mapping_required"):
                self._packet("x", **{field_name: (1,)})

    def test_message_fields_require_string_members(self) -> None:
        for field_name in ("warnings", "errors"):
            with self.assertRaisesRegex(ValueError, f"invalid:{field_name}\\[0\\]:string_required"):
                self._packet("x", **{field_name: (123,)})

    def test_empty_record_and_message_sequences_remain_valid(self) -> None:
        packet = self._packet("x")
        self.assertEqual(packet.object_records, ())
        self.assertEqual(packet.geometry_records, ())
        self.assertEqual(packet.kinematics, ())
        self.assertEqual(packet.warnings, ())
        self.assertEqual(packet.errors, ())


    def test_nested_canonical_domain_rejects_non_string_mapping_key(self) -> None:
        with self.assertRaisesRegex(ValueError, "mapping_key_string_required"):
            self._packet("x", input_identity={"nested": {1: "invalid"}})

    def test_nested_canonical_domain_rejects_set(self) -> None:
        with self.assertRaisesRegex(ValueError, "canonical_json_value_required"):
            self._packet("x", input_identity={"nested": {"unsupported"}})

    def test_nested_canonical_domain_rejects_datetime_and_decimal(self) -> None:
        for value in (
            {"nested": datetime(2026, 1, 1)},
            {"nested": Decimal("1.25")},
        ):
            with self.assertRaisesRegex(ValueError, "canonical_json_value_required"):
                self._packet("x", input_identity=value)

    def test_nested_canonical_domain_rejects_nonfinite_float(self) -> None:
        with self.assertRaisesRegex(ValueError, "finite_number_required"):
            self._packet("x", input_identity={"nested": {"value": float("inf")}})

