from __future__ import annotations

import os
import sys
import unittest
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from ce.calculation.engine import CalculationEngine
from ce.calculation.evidence import EvidencePacket
from ce.calculation.geometry import (
    circular_separation_deg,
    normalize_longitude_deg,
    signed_angular_deviation_deg,
)
from ce.ephemeris.adapter import EphemerisRequest, UnavailableSwissEphemerisAdapter
from ce.foundation.identity import RuntimeIdentity
from ce.foundation.status import CalculationStatus


class B4Item11IntegrityTests(unittest.TestCase):
    def _packet_kwargs(self) -> dict[str, object]:
        return {
            "evidence_packet_id": "E-F11-001",
            "input_identity": {"request": "F11", "nested": {"ok": True}},
            "profile_version": {"id": "CE-CALC-V1-EP-001", "revision": 2},
            "observation_instant_or_interval": {"start": "2026-01-01T00:00:00Z"},
            "timezone_context": {"id": "UTC", "version": "NOT_ESTABLISHED"},
            "execution_profile_id": "CE-CALC-V1-EP-001",
            "calculation_version": "0.1.0",
            "object_records": ({"object_id": "sun", "meta": {"enabled": True}},),
            "geometry_records": (),
            "kinematics": (),
            "warnings": (),
            "errors": (),
            "numerical_tolerances": {"exact_tolerance_deg": 1e-4},
            "solver_metadata": {},
            "actual_ephemeris_resolution": {"status": "NOT_ESTABLISHED"},
            "calculation_flags": {"authoritative": False},
        }

    def test_f11_1_nested_invalid_domain_fails_contract_before_issuance(self) -> None:
        cases = (
            {"nested": {1: "bad"}},
            {"nested": {"unsupported"}},
            {"nested": datetime(2026, 1, 1)},
            {"nested": {"custom": object()}},
            {"nested": {"value": float("inf")}},
        )
        for invalid in cases:
            with self.subTest(invalid=repr(invalid)):
                values = self._packet_kwargs()
                values["input_identity"] = invalid
                with self.assertRaisesRegex(ValueError, "invalid:"):
                    EvidencePacket(**values)  # type: ignore[arg-type]

    def test_f11_1_nested_valid_domain_is_issuable(self) -> None:
        packet = EvidencePacket(**self._packet_kwargs())
        self.assertEqual(packet.validate(), ())
        self.assertTrue(packet.canonical_bytes())

    def test_f11_2_geometry_rejects_bool_numeric_input(self) -> None:
        for fn, args in (
            (normalize_longitude_deg, (True,)),
            (normalize_longitude_deg, (False,)),
            (circular_separation_deg, (1.0, True)),
            (signed_angular_deviation_deg, (1.0, 2.0, True)),
        ):
            with self.subTest(fn=fn.__name__):
                with self.assertRaises(ValueError):
                    fn(*args)

    def test_f11_3_ephemeris_adapter_requires_typed_request(self) -> None:
        adapter = UnavailableSwissEphemerisAdapter()
        with self.assertRaises(TypeError):
            adapter.calculate_object("sun", 2451545.0, True)  # type: ignore[arg-type]

        result = adapter.calculate_object(object())  # type: ignore[arg-type]
        self.assertEqual(result.status, CalculationStatus.INVALID_INPUT)

        request = EphemerisRequest("sun", 2451545.0, True)
        self.assertEqual(
            adapter.calculate_object(request).status,
            CalculationStatus.NON_AUTHORIZED,
        )

    def test_f11_4_engine_constructor_rejects_wrong_runtime_identity_type(self) -> None:
        with self.assertRaisesRegex(ValueError, "invalid:runtime_identity:type_required"):
            CalculationEngine(object(), UnavailableSwissEphemerisAdapter())  # type: ignore[arg-type]

    def test_f11_4_valid_runtime_identity_type_remains_constructible(self) -> None:
        identity = RuntimeIdentity(
            "CE-CALC-V1-EP-001",
            2,
            "a" * 40,
            "b" * 64,
            "sha256:" + "c" * 64,
            "d" * 64,
            "e" * 64,
            "f" * 64,
        )
        self.assertIsNotNone(
            CalculationEngine(identity, UnavailableSwissEphemerisAdapter())
        )


if __name__ == "__main__":
    unittest.main()
