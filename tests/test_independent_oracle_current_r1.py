from __future__ import annotations

from datetime import datetime
from hashlib import sha256
from pathlib import Path
import math
import unittest

from ce.calculation.geometry import aspect_geometry, circular_span_deg, effective_orb
from ce.calculation.window_solver import solve_aspect_window
from ce.ephemeris.verification import classify_requested_actual_flags
from ce.foundation.status import CalculationStatus, KinematicState, ScenarioState
from ce.signal.daily import aggregate_qualified_signal_records
from ce.signal.engine import SignalEngine
from ce.signal.record import QualifiedSignalRecord
from ce.timezone.runtime import TzifRuntime, compute_manifest_sha256


class IndependentOracleCurrentR1Tests(unittest.TestCase):
    """Candidate independent reference checks.

    The expected values below are derived by this test module's own mathematical
    rules. They are not imported from CE production implementations.
    """

    def test_geo_and_kinematics_from_independent_math(self) -> None:
        def ref_wrap180(value: float) -> float:
            normalized = value % 360.0
            return normalized - 360.0 if normalized >= 180.0 else normalized

        def reference(transit: float, natal: float, branch: float, speed: float | None):
            delta = ref_wrap180((transit - natal) % 360.0)
            error = ref_wrap180(delta - branch)
            abs_error = abs(error)
            if abs_error <= 1.0e-4:
                phase = "EXACT"
            else:
                derivative = (-1.0 if error < 0.0 else 1.0) * speed if speed is not None else 0.0
                if derivative < -1.0e-6:
                    phase = "APPLYING"
                elif derivative > 1.0e-6:
                    phase = "SEPARATING"
                else:
                    phase = "NEAR_STATIONARY"
            return error, abs_error, phase

        expected = (
            ("GEO-01", 359.5, 0.5, 0.0, None, -1.0, 1.0),
            ("GEO-02", 10.0, 100.0, -90.0, None, 0.0, 0.0),
        )
        for case, transit, natal, branch, speed, e, d in expected:
            with self.subTest(case=case):
                got_branch, got_e, got_d, _, _ = aspect_geometry(
                    "SUN", "MOON", transit, natal, speed, "SQUARE" if case == "GEO-02" else "CONJUNCTION"
                )
                self.assertEqual(got_branch, branch)
                self.assertAlmostEqual(got_e, e, places=12)
                self.assertAlmostEqual(got_d, d, places=12)
                ref_e, ref_d, _ = reference(transit, natal, branch, speed)
                self.assertAlmostEqual(ref_e, e, places=12)
                self.assertAlmostEqual(ref_d, d, places=12)

        kinematics = (
            ("KIN-01", 59.5, 0.0, 1.2, "SEXTILE", "APPLYING"),
            ("KIN-02", 60.5, 0.0, 1.2, "SEXTILE", "SEPARATING"),
            ("KIN-03", 59.5, 0.0, -0.8, "SEXTILE", "SEPARATING"),
            ("KIN-04", 60.00005, 0.0, -20.0, "SEXTILE", "EXACT"),
        )
        for case, transit, natal, speed, aspect, expected_phase in kinematics:
            with self.subTest(case=case):
                _, _, _, phase, _ = aspect_geometry("SUN", "MOON", transit, natal, speed, aspect)
                self.assertEqual(phase.value, expected_phase)

    def test_orb_and_span_reference_values(self) -> None:
        self.assertEqual(effective_orb("SUN", "CONJUNCTION"), 2.5)
        self.assertEqual(effective_orb("JUPITER", "CONJUNCTION"), 1.5)
        self.assertAlmostEqual(circular_span_deg(359.8, 0.2), 0.4, places=12)

    def test_window_normative_vectors_from_independent_expected_topology(self) -> None:
        r1 = solve_aspect_window(
            lambda x: min(abs(x - 15.0), abs(x - 45.0)),
            start=0.0, end=60.0, effective_orb=5.0, samples=600,
        )
        self.assertEqual(r1.segments, ((10.0, 20.0), (40.0, 50.0)))
        self.assertEqual(tuple(round(e.instant, 9) for e in r1.exact_events), (15.0, 45.0))

        r2 = solve_aspect_window(
            lambda x: 0.05 * math.sin(x),
            start=0.0, end=2.0 * math.pi, effective_orb=0.1, samples=720,
        )
        self.assertEqual(len(r2.segments), 1)
        self.assertEqual(
            tuple(round(e.instant, 9) for e in r2.exact_events),
            (0.0, round(math.pi, 9), round(2.0 * math.pi, 9)),
        )

        r3 = solve_aspect_window(
            lambda x: 1.0 + (x - 2.0) ** 2,
            start=0.0, end=4.0, effective_orb=1.0, samples=256,
        )
        self.assertEqual(r3.segments, ())
        self.assertEqual(r3.exact_events, ())
        self.assertEqual(len(r3.tangential_contacts), 1)

    def test_ephemeris_requested_actual_reference_rule(self) -> None:
        self.assertEqual(
            classify_requested_actual_flags(258, 2),
            CalculationStatus.CALCULATION_FAILURE,
        )
        self.assertEqual(
            classify_requested_actual_flags(2, 258),
            CalculationStatus.VALID,
        )

    def _controlled_zone(self, zone: str, expected_sha: str) -> bytes:
        path = Path("/usr/share/zoneinfo") / zone
        if not path.is_file():
            self.skipTest(zone)
        data = path.read_bytes()
        self.assertEqual(sha256(data).hexdigest(), expected_sha)
        return data

    def test_time_normative_vectors_use_exact_controlled_zone_bytes(self) -> None:
        utc_fixture = "Etc/UTC"
        utc_data = self._controlled_zone(
            utc_fixture, "8b85846791ab2c8a5463c83a5be3c043e2570d7448434d41398969ed47e3e6f2"
        )
        runtime = TzifRuntime(
            version="2026d",
            files={utc_fixture: utc_data},
            expected_manifest_sha256=compute_manifest_sha256({utc_fixture: utc_data}),
        )
        self.assertEqual(
            runtime.resolve_local_instant(datetime(2020, 1, 1, 12, 0), utc_fixture).isoformat(),
            "2020-01-01T12:00:00+00:00",
        )

        paris = "Europe/Paris"
        paris_data = self._controlled_zone(
            paris, "ab77a1488a2dd4667a4f23072236e0d2845fe208405eec1b4834985629ba7af8"
        )
        runtime = TzifRuntime(
            version="2026d",
            files={paris: paris_data},
            expected_manifest_sha256=compute_manifest_sha256({paris: paris_data}),
        )
        with self.assertRaisesRegex(ValueError, "ambiguous_local_time"):
            runtime.resolve_local_instant(datetime(2024, 10, 27, 2, 30), paris)
        with self.assertRaisesRegex(ValueError, "nonexistent_local_time"):
            runtime.resolve_local_instant(datetime(2024, 3, 31, 2, 30), paris)

    def test_signal_and_daily_boundaries_are_not_self_proving(self) -> None:
        # This test validates independently derived downstream invariants using
        # only a minimal deterministic packet; it does not calculate astronomy.
        packet = self._packet()
        result = SignalEngine().evaluate(packet)
        self.assertEqual(result.classification, "ROBUST_EXACT_SIGNAL")
        record = QualifiedSignalRecord(
            schema_version="CE-QUALIFIED-SIGNAL-RECORD-V1",
            signal_id="CE-SIGNAL-" + "1" * 64,
            evidence_packet_ref=result.evidence_packet_ref or f"{packet.evidence_packet_id}:{packet.content_sha256()}",
            timestamp_observation_utc="2026-01-01T00:00:00Z",
            qualification_status="VALID",
            classification="ROBUST_EXACT_SIGNAL",
            kinematic_phase="EXACT",
            phase_uniformity="UNIFORM",
            canon_input_valid=True,
            requires_uncertainty_disclaimer=False,
            environment_pin="sha256:" + "2" * 64,
        )
        agg = aggregate_qualified_signal_records((record,), observation_completed=True)
        self.assertEqual(agg.qualifying_signal_refs, (record.signal_id,))

    def _packet(self):
        from ce.calculation.evidence import EvidencePacket
        return EvidencePacket(
            evidence_packet_id="E-IND-001",
            calculation_id="C-IND-001",
            input_identity={"fixture": "independent-oracle"},
            profile_version={"id": "CE-CALC-V1-EP-001", "revision": 4},
            observation_instant_or_interval={"start": "2026-01-01T00:00:00Z"},
            timezone_context={"id": "UTC", "version": "2026d"},
            execution_profile_id="CE-CALC-V1-EP-001",
            calculation_version="CE-CALC-CORE-V1-R1-CONVERGENT",
            object_records=(),
            geometry_records=({
                "transit_object": "SUN",
                "natal_object_or_scenario": "MOON",
                "aspect": "CONJUNCTION",
                "directed_branch": 0.0,
                "signed_deviation": 0.0,
                "absolute_deviation": 0.0,
                "effective_orb": 2.5,
                "qualification_state": "QUALIFIED",
                "kinematic_state": "EXACT",
            },),
            effective_orb_records=(),
            kinematics=({"transit_object": "SUN", "aspect": "CONJUNCTION", "kinematic_state": "EXACT"},),
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


if __name__ == "__main__":
    unittest.main()
