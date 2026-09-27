from __future__ import annotations

import os
import sys
import tempfile
import unittest
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from zipfile import ZipFile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from build import build_source_tree_hash
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
from tools.package_source import build_archive, files, package_identity


ROOT = Path(__file__).resolve().parents[1]


class B4Item11RecoveryIntegrityTests(unittest.TestCase):
    def _packet_kwargs(self) -> dict[str, object]:
        return {
            "evidence_packet_id": "E-F11-REC-001",
            "input_identity": {"request": "F11", "nested": {"ok": True}},
            "profile_version": {"id": "CE-CALC-V1-EP-001", "revision": 2},
            "observation_instant_or_interval": {
                "start": "2026-01-01T00:00:00Z"
            },
            "timezone_context": {"id": "UTC", "version": "NOT_ESTABLISHED"},
            "execution_profile_id": "CE-CALC-V1-EP-001",
            "calculation_version": "0.1.0",
            "object_records": (
                {"object_id": "sun", "meta": {"enabled": True}},
            ),
            "geometry_records": (),
            "kinematics": (),
            "warnings": (),
            "errors": (),
            "numerical_tolerances": {"exact_tolerance_deg": 1e-4},
            "solver_metadata": {},
            "actual_ephemeris_resolution": {"status": "NOT_ESTABLISHED"},
            "calculation_flags": {"authoritative": False},
        }

    def _runtime_identity(self) -> RuntimeIdentity:
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

    def test_f11_1_all_nested_canonical_domain_rejections_are_preissuance(self) -> None:
        class Unsupported:
            pass

        invalid_values = (
            {"nested": {1: "bad"}},
            {"nested": {"unsupported"}},
            {"nested": datetime(2026, 1, 1)},
            {"nested": Decimal("1.25")},
            {"nested": Unsupported()},
            {"nested": {"value": float("nan")}},
            {"nested": {"value": float("inf")}},
            {"nested": {"value": float("-inf")}},
        )

        for invalid in invalid_values:
            with self.subTest(invalid=repr(invalid)):
                kwargs = self._packet_kwargs()
                kwargs["input_identity"] = invalid
                with self.assertRaisesRegex(ValueError, "invalid:"):
                    EvidencePacket(**kwargs)  # type: ignore[arg-type]

    def test_f11_1_valid_recursive_json_domain_is_issuable(self) -> None:
        kwargs = self._packet_kwargs()
        kwargs["input_identity"] = {
            "nested": {
                "list": [None, True, False, 1, 1.5, "ok"],
                "mapping": {"b": 2, "a": "ordered-canonically"},
            }
        }
        packet = EvidencePacket(**kwargs)
        self.assertEqual(packet.validate(), ())
        self.assertTrue(packet.canonical_bytes())

    def test_f11_2_geometry_rejects_bool_and_accepts_strict_numeric_types(self) -> None:
        for fn, args in (
            (normalize_longitude_deg, (True,)),
            (normalize_longitude_deg, (False,)),
            (circular_separation_deg, (1.0, True)),
            (signed_angular_deviation_deg, (1.0, 2.0, True)),
        ):
            with self.subTest(fn=fn.__name__):
                with self.assertRaises(ValueError):
                    fn(*args)

        self.assertEqual(normalize_longitude_deg(361), 1.0)
        self.assertEqual(normalize_longitude_deg(-1.0), 359.0)
        self.assertEqual(circular_separation_deg(359, 1.0), 2.0)

    def test_f11_3_ephemeris_request_is_the_only_adapter_input_shape(self) -> None:
        adapter = UnavailableSwissEphemerisAdapter()

        with self.assertRaises(TypeError):
            adapter.calculate_object("sun", 2451545.0, True)  # type: ignore[arg-type]

        invalid = adapter.calculate_object(object())  # type: ignore[arg-type]
        self.assertEqual(invalid.status, CalculationStatus.INVALID_INPUT)

        request = EphemerisRequest("sun", 2451545.0, True)
        self.assertEqual(
            adapter.calculate_object(request).status,
            CalculationStatus.NON_AUTHORIZED,
        )

    def test_f11_4_calculation_engine_closes_runtime_identity_type_boundary(self) -> None:
        adapter = UnavailableSwissEphemerisAdapter()
        with self.assertRaisesRegex(ValueError, "invalid:runtime_identity:type_required"):
            CalculationEngine(object(), adapter)  # type: ignore[arg-type]

        engine = CalculationEngine(self._runtime_identity(), adapter)
        self.assertIsNotNone(engine)

    def test_f11_5_package_scope_is_exactly_source_tree_scope(self) -> None:
        expected = [
            p.relative_to(ROOT).as_posix()
            for p in build_source_tree_hash.iter_files()
        ]
        self.assertEqual(
            [p.relative_to(ROOT).as_posix() for p in files()],
            expected,
        )

    def test_f11_5_package_identity_is_deterministic_and_source_bound(self) -> None:
        (ROOT / "dist").mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=ROOT / "dist") as temp:
            left = Path(temp) / "left.zip"
            right = Path(temp) / "right.zip"

            build_archive(left)
            build_archive(right)

            self.assertEqual(left.read_bytes(), right.read_bytes())

            with ZipFile(left, "r") as archive:
                self.assertEqual(
                    sorted(archive.namelist()),
                    [
                        p.relative_to(ROOT).as_posix()
                        for p in build_source_tree_hash.iter_files()
                    ],
                )
                self.assertEqual(
                    archive.comment.decode("ascii"),
                    f"CE_SOURCE_TREE_SHA256_V2={build_source_tree_hash.digest()}\n",
                )

            identity = package_identity(left)
            self.assertEqual(
                identity["source_tree_sha256_v2"],
                build_source_tree_hash.digest(),
            )
            self.assertRegex(
                identity["package_artifact_sha256"],
                r"^[0-9a-f]{64}$",
            )


if __name__ == "__main__":
    unittest.main()
