from __future__ import annotations

"""Additional CE-R0 adversarial acceptance tests."""

from dataclasses import replace
from pathlib import Path
import unittest
import tempfile

from ce.calculation.evidence import EvidencePacket
from ce.ephemeris.native_runtime import NativeRuntimeError, NativeSwissEphemerisAdapter
from ce.signal.daily import aggregate_qualified_signal_records
from ce.signal.record import QualifiedSignalRecord
from ce.foundation.status import CalculationStatus


def packet() -> EvidencePacket:
    return EvidencePacket(
        evidence_packet_id="FORGED-ID",
        calculation_id="C-R0-ID",
        input_identity={"birth_date": "2026-01-01"},
        profile_version={"id": "CE-CALC-V1-EP-001", "revision": 4},
        observation_instant_or_interval={"start": "2026-01-01T00:00:00Z"},
        timezone_context={"id": "UTC", "version": "2026d"},
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
        warnings=(),
        errors=(),
        numerical_tolerances={},
        solver_metadata={},
        actual_ephemeris_resolution={"ephemeris_resolution_status": "MATCH"},
        calculation_flags={"calculation_status": "VALID"},
    )


class CER0AdditionalAcceptanceTests(unittest.TestCase):
    def test_evidence_packet_id_must_be_content_addressed(self) -> None:
        value = packet()
        # A packet constructor must not accept an arbitrary ID that is unrelated
        # to the canonical content-addressed identity.
        expected_id = __import__("hashlib").sha256(value.canonical_bytes()).hexdigest()
        self.assertEqual(value.evidence_packet_id, expected_id)

    def test_daily_aggregator_must_reject_unissued_record(self) -> None:
        record = QualifiedSignalRecord(
            schema_version="CE-QUALIFIED-SIGNAL-RECORD-V1",
            signal_id="CE-SIGNAL-" + "1" * 64,
            evidence_packet_ref="E-1:" + "2" * 64,
            timestamp_observation_utc="2026-01-01T00:00:00Z",
            qualification_status="VALID",
            classification="ROBUST_EXACT_SIGNAL",
            kinematic_phase="EXACT",
            phase_uniformity="UNIFORM",
            canon_input_valid=True,
            requires_uncertainty_disclaimer=False,
            environment_pin="sha256:" + "3" * 64,
        )
        with self.assertRaises(ValueError):
            aggregate_qualified_signal_records((record,), observation_completed=True)

    def test_native_adapter_must_require_verified_authorization_receipt_not_bool(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaises((TypeError, NativeRuntimeError, ValueError)):
                NativeSwissEphemerisAdapter(
                    library_path=root / "missing.dll",
                    ephemeris_root=root,
                    calling_convention="__cdecl",
                    runtime_authorized=True,
                )

    def test_source_identity_scope_must_cover_control_plane_files(self) -> None:
        # This documents the required future invariant: mutation of a workflow
        # file must alter the canonical CE identity if that workflow participates
        # in build/release trust.
        identity_module = __import__(
            "ce.foundation.source_tree_identity",
            fromlist=["source_tree_sha256"],
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ("src", "build", "tools", "tests", "schemas", "profiles", "manifests", ".github"):
                (root / name).mkdir(parents=True)
            (root / "src" / "x.py").write_text("x\n", encoding="utf-8")
            (root / ".github" / "workflow.yml").write_text("version: 1\n", encoding="utf-8")
            first = identity_module.source_tree_sha256(root)
            (root / ".github" / "workflow.yml").write_text("version: 2\n", encoding="utf-8")
            second = identity_module.source_tree_sha256(root)
            self.assertNotEqual(first, second)


if __name__ == "__main__":
    unittest.main()
