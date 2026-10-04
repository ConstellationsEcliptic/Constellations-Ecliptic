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
            calculation_id="C-001",
            calculation_id="C-001",
            input_identity={"value": value},
            profile_version={"id": "CE-CALC-V1-EP-001", "revision": 4},
            observation_instant_or_interval={"start": "2000-01-01T00:00:00Z"},
            timezone_context={"id": "UTC", "version": "NOT_ESTABLISHED"},
            execution_profile_id="CE-CALC-V1-EP-001",
            calculation_version="0.1.0",
            object_records=(),
            geometry_records=(),
            effective_orb_records=(),
            kinematics=(),
            exact_events=(),
            window_segments=(),
            scenario_stability_state="STABLE",
            warnings=(),
            errors=(),
            numerical_tolerances={"exact_tolerance_deg": 1e-4},
            solver_metadata={},
            actual_ephemeris_resolution={"status": "NOT_ESTABLISHED"},
            calculation_flags={},
        )

    def test_same_payload_same_hash(self) -> None:
        self.assertEqual(self._packet("x").content_sha256(), self._packet("x").content_sha256())

    def test_mutation_changes_hash(self) -> None:
        self.assertNotEqual(self._packet("x").content_sha256(), self._packet("y").content_sha256())
