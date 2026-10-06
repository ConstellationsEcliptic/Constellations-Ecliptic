from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import tempfile
import unittest
from zoneinfo import ZoneInfo
from hashlib import sha256

from ce.calculation.contracts import CalculationRequest, BirthInput, ObjectState, ObjectRecord
from ce.calculation.evidence import EvidencePacket
from ce.calculation.kernel import KernelFailure, calculate_aspect_window
from ce.calculation.scenario_evaluator import evaluate_zero_birth_scenarios
from ce.calculation.window_solver import solve_aspect_window
from ce.foundation.status import CalculationStatus, KinematicState, NatalBirthState, ScenarioState
from ce.runtime.gates import authorize_runtime
from ce.foundation.identity import RuntimeIdentity
from ce.timezone.runtime import TzifRuntime, TzifRuntimeError, compute_manifest_sha256


class PlannedCoreControlsR1(unittest.TestCase):
    # WIN-01
    def test_win_01_disjoint_possible_windows(self) -> None:
        result = solve_aspect_window(
            lambda x: min(abs(x - 15.0), abs(x - 45.0)),
            start=0.0,
            end=60.0,
            effective_orb=5.0,
            samples=600,
        )
        self.assertEqual(result.segments, ((10.0, 20.0), (40.0, 50.0)))
        self.assertEqual(
            tuple(round(event.instant, 9) for event in result.exact_events),
            (15.0, 45.0),
        )

    # WIN-02
    def test_win_02_continuous_multi_peak(self) -> None:
        result = solve_aspect_window(
            lambda x: 0.05 * __import__("math").sin(x),
            start=0.0,
            end=2.0 * __import__("math").pi,
            effective_orb=0.1,
            samples=720,
        )
        self.assertEqual(len(result.exact_events), 3)
        self.assertEqual(len(result.segments), 1)
        segment = result.segments[0]
        self.assertAlmostEqual(segment[0], 0.0, places=9)
        self.assertAlmostEqual(segment[1], 2.0 * __import__("math").pi, places=9)
        self.assertEqual(
            tuple(round(event.instant, 9) for event in result.exact_events),
            (0.0, round(__import__("math").pi, 9), round(2.0 * __import__("math").pi, 9)),
        )

    # WIN-03
    def test_win_03_tangential_contact(self) -> None:
        result = solve_aspect_window(
            lambda x: 1.0 + (x - 2.0) ** 2,
            start=0.0,
            end=4.0,
            effective_orb=1.0,
            samples=256,
        )
        self.assertEqual(result.exact_events, ())
        self.assertEqual(result.segments, ())
        self.assertTrue(result.tangential_contacts)
        self.assertAlmostEqual(result.tangential_contacts[0], 2.0, places=6)

    def _aggregate(self, sets: tuple[tuple[tuple[float, float], ...], ...]):
        from ce.calculation.scenario_windows import classify_sampled_windows
        return classify_sampled_windows(sets)

    # UNC-01
    def test_unc_01_stable_robust(self) -> None:
        state, possible, robust = self._aggregate(
            (((1.0, 3.0),), ((1.0, 3.0),), ((1.0, 3.0),))
        )
        self.assertIs(state, ScenarioState.ROBUST)
        self.assertEqual(possible, robust)

    # UNC-02
    def test_unc_02_variable_possible(self) -> None:
        state, possible, robust = self._aggregate(
            (((1.0, 2.0),), (), ())
        )
        self.assertIs(state, ScenarioState.POSSIBLE)
        self.assertTrue(possible)
        self.assertEqual(robust, ())

    # UNC-03
    def test_unc_03_variable_mixed_phase(self) -> None:
        state, possible, robust = self._aggregate(
            (((1.0, 3.0),), ((2.0, 4.0),))
        )
        self.assertIs(state, ScenarioState.MIXED)
        self.assertEqual(robust, ((2.0, 3.0),))

    # UNC-04
    def test_unc_04_variable_no_qualification(self) -> None:
        state, possible, robust = self._aggregate(((), (), ()))
        self.assertIs(state, ScenarioState.NONE)
        self.assertEqual(possible, ())
        self.assertEqual(robust, ())

    # EPH-01
    def test_eph_01_requested_actual_resolution_mismatch_is_failure(self) -> None:
        from ce.ephemeris.verification import classify_requested_actual_flags
        result = classify_requested_actual_flags(requested_flags=258, actual_flags=2)
        self.assertEqual(result, CalculationStatus.CALCULATION_FAILURE)

    def test_ephemeris_data_integrity_mismatch_remains_separate(self) -> None:
        from ce.ephemeris.verification import DataFileExpectation, EphemerisVerificationError, verify_data_files
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "seas_18.se1"
            path.write_bytes(b"abcd")
            with self.assertRaisesRegex(EphemerisVerificationError, "sha256_mismatch"):
                verify_data_files(
                    Path(directory),
                    (DataFileExpectation("seas_18.se1", 4, "0" * 64),),
                )

    # ERR-01
    def test_err_01_corrupt_evidence_packet(self) -> None:
        with self.assertRaises(ValueError):
            EvidencePacket(
                evidence_packet_id="E-CORRUPT",
                calculation_id="C-CORRUPT",
                input_identity={"x": float("nan")},
                profile_version={"id": "CE-CALC-V1-EP-001", "revision": 4},
                observation_instant_or_interval={"start": "2026-01-01T00:00:00Z"},
                timezone_context={"id": "UTC", "version": "2026d"},
                execution_profile_id="CE-CALC-V1-EP-001",
                calculation_version="v1",
                object_records=(),
                geometry_records=(),
                effective_orb_records=(),
                kinematics=(),
                exact_events=(),
                window_segments=(),
                scenario_stability_state="STABLE",
                warnings=(),
                errors=(),
                numerical_tolerances={},
                solver_metadata={},
                actual_ephemeris_resolution={},
                calculation_flags={},
            )

    # ERR-02
    def test_err_02_malformed_calculation_input(self) -> None:
        with self.assertRaises(ValueError):
            BirthInput(
                birth_date=datetime(2026, 1, 1),
                birth_city="X",
                timezone_id="UTC",
                timezone_version="2026d",
            )

    # ERR-05
    def test_err_05_failure_not_quiet_sky(self) -> None:
        class BadProvider:
            def object_state_at(self, object_id: str, instant_utc: datetime) -> ObjectRecord:
                return ObjectRecord(object_id, CalculationStatus.CALCULATION_FAILURE, 258, None, None, None, None, None, errors=("CALCULATION_FAILURE",))

        start = datetime(2026, 1, 1, tzinfo=timezone.utc)
        with self.assertRaisesRegex(KernelFailure, "natal_object_not_valid"):
            calculate_aspect_window(
                BadProvider(),
                birth_instant_utc=start,
                target_start_utc=start,
                target_end_utc=datetime(2026, 1, 2, tzinfo=timezone.utc),
                transit_object="SUN",
                natal_object="MOON",
                aspect="CONJUNCTION",
                samples=16,
            )

    # ERR-06
    def test_err_06_non_valid_boundary_preserved(self) -> None:
        class UnavailableProvider:
            def object_state_at(self, object_id: str, instant_utc: datetime) -> ObjectState:
                return ObjectRecord(object_id, CalculationStatus.KNOWN_UNAVAILABLE, 258, None, None, None, None, None, errors=("KNOWN_UNAVAILABLE",))

        start = datetime(2026, 1, 1, tzinfo=timezone.utc)
        with self.assertRaisesRegex(KernelFailure, "natal_object_not_valid"):
            calculate_aspect_window(
                UnavailableProvider(),
                birth_instant_utc=start,
                target_start_utc=start,
                target_end_utc=datetime(2026, 1, 2, tzinfo=timezone.utc),
                transit_object="SUN",
                natal_object="MOON",
                aspect="CONJUNCTION",
                samples=16,
            )

    # INT-01
    def test_int_01_quiet_sky(self) -> None:
        class QuietProvider:
            def object_state_at(self, object_id: str, instant_utc: datetime) -> ObjectState:
                return ObjectRecord(object_id, CalculationStatus.VALID, 258, 258, 200.0 if object_id == "MOON" else 100.0, 0.0, 1.0, 0.0)

        start = datetime(2026, 1, 1, tzinfo=timezone.utc)
        result = calculate_aspect_window(
            QuietProvider(),
            birth_instant_utc=start,
            target_start_utc=start,
            target_end_utc=datetime(2026, 1, 2, tzinfo=timezone.utc),
            transit_object="SUN",
            natal_object="MOON",
            aspect="CONJUNCTION",
            samples=32,
        )
        self.assertEqual(result.status, CalculationStatus.VALID)
        self.assertEqual(result.events, ())
        self.assertEqual(result.windows, ())


    # TIME-01
    def test_time_01_historical_timezone_normative_fixture(self) -> None:
        name = "Etc/UTC"
        data = self._controlled_tzif(name, "8b85846791ab2c8a5463c83a5be3c043e2570d7448434d41398969ed47e3e6f2")
        files = {name: data}
        runtime = TzifRuntime(
            version="2026d",
            files=files,
            expected_manifest_sha256=compute_manifest_sha256(files),
        )
        resolved = runtime.resolve_local_instant(datetime(2020, 1, 1, 12, 0), name)
        self.assertEqual(resolved.isoformat(), "2020-01-01T12:00:00+00:00")

    def test_time_02_ambiguous_rejected_normative_fixture(self) -> None:
        name = "Europe/Paris"
        data = self._controlled_tzif(name, "ab77a1488a2dd4667a4f23072236e0d2845fe208405eec1b4834985629ba7af8")
        files = {name: data}
        runtime = TzifRuntime(
            version="2026d",
            files=files,
            expected_manifest_sha256=compute_manifest_sha256(files),
        )
        with self.assertRaisesRegex(TzifRuntimeError, "ambiguous_local_time"):
            runtime.resolve_local_instant(datetime(2024, 10, 27, 2, 30), name)

    def test_time_03_nonexistent_rejected_normative_fixture(self) -> None:
        name = "Europe/Paris"
        data = self._controlled_tzif(name, "ab77a1488a2dd4667a4f23072236e0d2845fe208405eec1b4834985629ba7af8")
        files = {name: data}
        runtime = TzifRuntime(
            version="2026d",
            files=files,
            expected_manifest_sha256=compute_manifest_sha256(files),
        )
        with self.assertRaisesRegex(TzifRuntimeError, "nonexistent_local_time"):
            runtime.resolve_local_instant(datetime(2024, 3, 31, 2, 30), name)

    def _controlled_tzif(self, zone_name: str, expected_sha256: str) -> bytes:
        path = Path(__file__).resolve().parent / "fixtures" / "tzif" / zone_name
        if not path.is_file():
            self.fail(f"controlled fixture zone missing: {zone_name}")
        data = path.read_bytes()
        observed = sha256(data).hexdigest()
        self.assertEqual(observed, expected_sha256)
        return data

    def test_current_runtime_gate_is_fail_closed(self) -> None:
        identity = RuntimeIdentity(
            "CE-CALC-V1-EP-001", 4,
            "a" * 40, "b" * 64, "sha256:" + "c" * 64,
            "d" * 64, "e" * 64, "f" * 64,
        )
        result = authorize_runtime(identity)
        self.assertEqual(result.authority.value, "NON_AUTHORIZED")


if __name__ == "__main__":
    unittest.main()
