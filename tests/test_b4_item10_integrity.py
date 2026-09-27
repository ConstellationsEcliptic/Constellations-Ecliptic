from __future__ import annotations

import os
import sys
from datetime import date, datetime, time
import runpy
import unittest
from types import MappingProxyType
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from ce.calculation.contracts import (
    BirthInput,
    CalculationRequest,
    CalculationResult,
    ObjectState,
)
from ce.calculation.evidence import EvidencePacket
from ce.calculation.engine import CalculationEngine
from ce.calculation.time import TimeResolution, resolve_exact_civil_time
from ce.ephemeris.adapter import UnavailableSwissEphemerisAdapter
from ce.foundation.identity import RuntimeIdentity
from ce.foundation.status import BirthTimeState, CalculationStatus, ScenarioState
from ce.signal.engine import SignalResult
from tools import package_source


class B4Item10IntegrityTests(unittest.TestCase):
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

    def _provenance(self, calculation_version: str = "0.1.0") -> dict[str, str]:
        identity = self._identity()
        return {
            "source_commit": identity.source_commit,
            "source_tree_sha256_v2": identity.source_tree_sha256_v2,
            "dependency_lock_digest": identity.dependency_lock_digest,
            "timezone_bundle_digest": identity.timezone_bundle_digest,
            "ephemeris_bundle_digest": identity.ephemeris_bundle_digest,
            "runtime_image_digest": identity.runtime_image_digest,
            "calculation_version": calculation_version,
        }

    def _packet(
        self,
        *,
        start: str = "2026-01-01T00:00:00Z",
        end: str | None = None,
        calculation_version: str = "0.1.0",
    ) -> EvidencePacket:
        observation = {"start": start}
        if end is not None:
            observation["end"] = end
        return EvidencePacket(
            evidence_packet_id="E-F10-001",
            input_identity={"request": "F10"},
            profile_version={"id": "CE-CALC-V1-EP-001", "revision": 2},
            observation_instant_or_interval=observation,
            timezone_context={"id": "UTC", "version": "NOT_ESTABLISHED"},
            execution_profile_id="CE-CALC-V1-EP-001",
            calculation_version=calculation_version,
            object_records=({"object_id": "sun"},),
            geometry_records=(),
            kinematics=(),
            warnings=(),
            errors=(),
            numerical_tolerances={"exact_tolerance_deg": 1e-4},
            solver_metadata={},
            actual_ephemeris_resolution={"status": "NOT_ESTABLISHED"},
            calculation_flags={"authoritative": False},
        )

    def _valid_result(self, packet: EvidencePacket) -> CalculationResult:
        return CalculationResult(
            request_id="R-F10",
            status=CalculationStatus.VALID,
            execution_profile_id="CE-CALC-V1-EP-001",
            scenario_state=ScenarioState.STABLE,
            normalized_time="2026-01-01T00:00:00Z",
            object_states=(ObjectState("sun", 12.5, 0.9, CalculationStatus.VALID),),
            warnings=(),
            errors=(),
            provenance=self._provenance(packet.calculation_version),
            _runtime_identity=self._identity(),
            _evidence_packet=packet,
        )

    def test_f10_1_valid_zero_birth_time_state_is_rejected(self) -> None:
        with self.assertRaisesRegex(
            ValueError, "valid_time_cannot_have_zero_birth_time_state"
        ):
            TimeResolution(
                CalculationStatus.VALID,
                BirthTimeState.ZERO_BIRTH_TIME,
                "2026-01-01T00:00:00Z",
                "UTC",
                "2026d",
                None,
            )

    def test_f10_2_malformed_birth_time_is_invalid_input_before_authority(self) -> None:
        result = resolve_exact_civil_time(
            date(2000, 1, 1),
            "12:00",  # type: ignore[arg-type]
            "UTC",
            "2026d",
            authoritative_timezone_version="2026d",
        )
        self.assertEqual(result.status, CalculationStatus.INVALID_INPUT)
        self.assertEqual(result.error, "invalid_birth_time")

    def test_f10_3_result_cross_binds_packet_semantics(self) -> None:
        packet = self._packet()
        result = self._valid_result(packet)
        self.assertEqual(result.evidence_packet_ref.evidence_packet_id, packet.evidence_packet_id)
        self.assertEqual(
            result.provenance["calculation_version"],
            packet.calculation_version,
        )

    def test_f10_3_result_rejects_calculation_version_mismatch(self) -> None:
        packet = self._packet(calculation_version="0.2.0")
        provenance = self._provenance("0.1.0")
        with self.assertRaisesRegex(
            ValueError, "evidence_packet:calculation_version_mismatch"
        ):
            CalculationResult(
                request_id="R-F10-MISMATCH",
                status=CalculationStatus.VALID,
                execution_profile_id="CE-CALC-V1-EP-001",
                scenario_state=ScenarioState.STABLE,
                normalized_time="2026-01-01T00:00:00Z",
                object_states=(ObjectState("sun", 12.5, 0.9, CalculationStatus.VALID),),
                provenance=provenance,
                _runtime_identity=self._identity(),
                _evidence_packet=packet,
            )

    def test_f10_3_result_rejects_observation_context_mismatch(self) -> None:
        packet = self._packet(start="2026-01-02T00:00:00Z")
        with self.assertRaisesRegex(
            ValueError, "evidence_packet:observation_context_mismatch"
        ):
            self._valid_result(packet)

    def test_f10_3_result_accepts_result_time_inside_observation_interval(self) -> None:
        packet = self._packet(
            start="2026-01-01T00:00:00Z",
            end="2026-01-02T00:00:00Z",
        )
        result = self._valid_result(packet)
        self.assertEqual(result.validate(), ())

    def test_f10_4_signal_valid_requires_runtime_bound_provenance(self) -> None:
        packet = self._packet()
        with self.assertRaisesRegex(ValueError, "provenance:binding_required"):
            SignalResult(
                CalculationStatus.VALID,
                "classification",
                "phase",
                "uncertain",
                packet,
                True,
            )

    def test_f10_4_signal_valid_accepts_exact_runtime_bound_provenance(self) -> None:
        packet = self._packet()
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
        self.assertEqual(result.validate(), ())
        self.assertEqual(
            result.provenance["calculation_version"],
            packet.calculation_version,
        )

    def test_f10_4_signal_nonvalid_rejects_authorized_runtime_metadata(self) -> None:
        with self.assertRaisesRegex(
            ValueError, "provenance:nonvalid_runtime_authority_must_be_non_authorized"
        ):
            SignalResult(
                CalculationStatus.NON_AUTHORIZED,
                None,
                None,
                None,
                None,
                False,
                provenance={"runtime_authority": "AUTHORIZED"},
            )

    def test_f10_5_packet_mapping_is_not_a_dict_subclass(self) -> None:
        packet = self._packet()
        self.assertIsInstance(packet.input_identity, MappingProxyType)
        self.assertNotIsInstance(packet.input_identity, dict)
        with self.assertRaises(TypeError):
            dict.__setitem__(packet.input_identity, "escaped", True)
        with self.assertRaises(TypeError):
            dict.update(packet.input_identity, {"escaped": True})

    def test_f10_6_hash_and_packaging_share_directory_scope(self) -> None:
        hash_ns = runpy.run_path(
            os.path.join(os.path.dirname(__file__), "..", "build", "build_source_tree_hash.py")
        )
        self.assertEqual(hash_ns["EXCLUDED_DIRS"], package_source.EXCLUDED_DIRS)
        self.assertNotIn("evidence", hash_ns["EXCLUDED_DIRS"])
        self.assertNotIn("provenance", hash_ns["EXCLUDED_DIRS"])

    def test_f10_7_result_warnings_and_errors_are_string_sequences(self) -> None:
        with self.assertRaisesRegex(ValueError, "invalid:warnings:sequence_required"):
            CalculationResult(
                "R-F10-W1",
                CalculationStatus.NON_AUTHORIZED,
                "CE-CALC-V1-EP-001",
                ScenarioState.NONE,
                None,
                warnings="not-a-sequence",  # type: ignore[arg-type]
                errors=(),
            )
        with self.assertRaisesRegex(ValueError, r"invalid:errors\[0\]:string_required"):
            CalculationResult(
                "R-F10-W2",
                CalculationStatus.NON_AUTHORIZED,
                "CE-CALC-V1-EP-001",
                ScenarioState.NONE,
                None,
                warnings=(),
                errors=(123,),  # type: ignore[arg-type]
            )

    def test_f10_8_engine_rejects_wrong_request_type_before_gate(self) -> None:
        identity = self._identity()
        engine = CalculationEngine(identity, UnavailableSwissEphemerisAdapter())
        with patch("ce.calculation.engine.authorize_runtime") as authorize:
            result = engine.calculate(object())  # type: ignore[arg-type]
        authorize.assert_not_called()
        self.assertEqual(result.status, CalculationStatus.INVALID_INPUT)
        self.assertEqual(result.errors, ("invalid_request_type",))
        self.assertEqual(result.request_id, "INVALID_INPUT")

    def test_f10_9_project_declares_same_python_as_ci(self) -> None:
        root = os.path.join(os.path.dirname(__file__), "..")
        pyproject = open(os.path.join(root, "pyproject.toml"), encoding="utf-8").read()
        workflow = open(
            os.path.join(root, ".github", "workflows", "b3-development-verification.yml"),
            encoding="utf-8",
        ).read()
        self.assertIn('requires-python = "==3.13.15"', pyproject)
        self.assertIn('python-version: "3.13.15"', workflow)


if __name__ == "__main__":
    unittest.main()
