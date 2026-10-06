from __future__ import annotations

from datetime import date
import unittest

from ce.calculation.contracts import (
    BirthInput,
    CalculationRequest,
    CalculationResult,
    CalculationResultDraft,
    ObjectRecord,
    ObjectState,
)
from ce.calculation.evidence_builder import issue_evidence_packet
from ce.canon.registry import CanonRegistry
from ce.claim.authorization import evaluate_claim_release
from ce.claim.manifest import build_allowed_claim_manifest
from ce.foundation.identity import RuntimeIdentity
from ce.foundation.provenance import runtime_identity_sha256
from ce.foundation.status import CalculationStatus, NatalBirthState, ScenarioState
from ce.output.validation import validate_claim_output
from ce.signal.record import issue_qualified_signal_record


class CER0FullBoundaryTests(unittest.TestCase):
    def runtime(self) -> RuntimeIdentity:
        return RuntimeIdentity(
            "CE-CALC-V1-EP-001", 4,
            "a" * 40, "b" * 64, "sha256:" + "c" * 64,
            "d" * 64, "e" * 64, "f" * 64,
        )

    def request(self) -> CalculationRequest:
        return CalculationRequest(
            request_id="REQ-FULL-1",
            birth=BirthInput(
                date(2000, 1, 1), "Test City", "UTC", "2026d",
                NatalBirthState.ZERO_BIRTH_TIME,
            ),
            target_interval_start_utc="2026-01-01T00:00:00Z",
            target_interval_end_utc="2026-01-02T00:00:00Z",
            execution_profile_id="CE-CALC-V1-EP-001",
        )

    def packet(self):
        request = self.request()
        runtime = self.runtime()
        draft = CalculationResultDraft(
            request_id=request.request_id,
            status=CalculationStatus.NATAL_EVIDENCE_VARIABLE,
            execution_profile_id=request.execution_profile_id,
            scenario_state=ScenarioState.VARIABLE,
            window_classification=ScenarioState.ROBUST,
            normalized_time=None,
            calculation_id="CALC-FULL-1",
            observation_interval=(
                request.target_interval_start_utc,
                request.target_interval_end_utc,
            ),
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
            actual_ephemeris_resolution={"ephemeris_resolution_status": "MATCH"},
            calculation_flags={"calculation_status": "VALID"},
            solver_metadata={"solver": "test"},
        )
        return issue_evidence_packet(
            draft,
            request=request,
            runtime_identity=runtime,
        )

    def valid_result(self, packet):
        runtime = self.runtime()
        return CalculationResult(
            request_id="REQ-FULL-1",
            status=CalculationStatus.VALID,
            execution_profile_id="CE-CALC-V1-EP-001",
            scenario_state=ScenarioState.STABLE,
            normalized_time="2026-01-01T00:00:00Z",
            calculation_id=packet.calculation_id,
            observation_interval=(
                "2026-01-01T00:00:00Z",
                "2026-01-02T00:00:00Z",
            ),
            object_states=(
                ObjectState("SUN", 12.5, 0.9, CalculationStatus.VALID),
            ),
            object_records=(
                ObjectRecord(
                    "SUN", CalculationStatus.VALID, 258, 258,
                    12.5, 0.0, 1.0, 0.9,
                ),
            ),
            provenance={
                "source_commit": runtime.source_commit,
                "source_tree_sha256_v2": runtime.source_tree_sha256_v2,
                "dependency_lock_digest": runtime.dependency_lock_digest,
                "timezone_bundle_digest": runtime.timezone_bundle_digest,
                "ephemeris_bundle_digest": runtime.ephemeris_bundle_digest,
                "runtime_image_digest": runtime.runtime_image_digest,
                "calculation_version": "CE-CALC-CORE-V1-R1-CONVERGENT",
                "runtime_identity_sha256": runtime_identity_sha256(runtime),
                "provenance_root_sha256": packet.provenance_root_sha256,
            },
            provenance_root_sha256=packet.provenance_root_sha256,
            _runtime_identity=runtime,
            _evidence_packet=packet,
        )

    def registry(self, evidence_ref: str) -> CanonRegistry:
        return CanonRegistry.from_records(
            "CE-CANON-RULE-REGISTRY-TEST-V1",
            [{
                "rule_id": "TEST-RULE-001",
                "canon_version": "CE-CANON-TEST-1",
                "tradition_track": "TEST_ONLY",
                "source_reference": "TEST-SOURCE",
                "source_scope": "TEST-SCOPE",
                "condition": {"classification": "ROBUST_EXACT_SIGNAL"},
                "allowed_interpretation": {
                    "claim_id": "TEST-CLAIM-001",
                    "allowed_subject": ["reflection"],
                    "allowed_scope": ["self-reflection"],
                    "epistemic_layer": "ASTROLOGICAL_INTERPRETATION",
                    "certainty_ceiling": "possibility_or_reflection",
                    "allowed_modality": ["may"],
                    "allowed_tense": ["present"],
                    "forbidden_domains": ["medical", "diagnosis"],
                    "forbidden_claim_types": ["guarantee"],
                    "required_evidence_refs": [evidence_ref],
                    "allowed_numeric_refs": [],
                    "required_disclosures": [],
                },
                "forbidden_extrapolation": ["guarantee"],
                "confidence_language_boundary": {"ceiling": "possibility"},
                "applicability_scope": ["self-reflection"],
            }],
        )

    def output(self, manifest, packet, *, text="This reflection may invite attention.") -> dict:
        return {
            "manifest_id": manifest.manifest_id,
            "provenance": {
                "manifest_id": manifest.manifest_id,
                "manifest_version": manifest.manifest_version,
                "canon_version": manifest.canon_version,
                "canon_registry_digest": manifest.canon_registry_digest,
                "canon_rule_id": manifest.canon_rule_id,
                "signal_reference": manifest.signal_reference,
                "evidence_refs": [f"{packet.evidence_packet_id}:{packet.content_sha256()}"],
                "provenance_root_sha256": packet.provenance_root_sha256,
            },
            "claims": [{
                "claim_id": manifest.claim_id,
                "text": text,
                "subject": ["reflection"],
                "scope": ["self-reflection"],
                "modality": ["may"],
                "tense": ["present"],
                "epistemic_layer": "ASTROLOGICAL_INTERPRETATION",
                "certainty": "possibility_or_reflection",
                "evidence_refs": [f"{packet.evidence_packet_id}:{packet.content_sha256()}"],
                "numeric_refs": [],
            }],
        }

    def test_output_validator_accepts_structurally_conforming_claim(self):
        packet = self.packet()
        signal = issue_qualified_signal_record(packet)
        evidence_ref = signal.evidence_packet_ref
        registry = self.registry(evidence_ref)
        manifest = build_allowed_claim_manifest(
            registry,
            rule_id="TEST-RULE-001",
            signal_reference=signal.signal_id,
        )
        result = validate_claim_output(
            self.output(manifest, packet),
            manifest,
            expected_signal_reference=signal.signal_id,
            expected_evidence_refs=(evidence_ref,),
            expected_provenance_root_sha256=packet.provenance_root_sha256,
            semantic_conformance=lambda text, manifest: True,
        )
        self.assertTrue(result.valid)
        self.assertEqual(result.reasons, ())

    def test_output_rejects_field_outside_manifest(self):
        packet = self.packet()
        signal = issue_qualified_signal_record(packet)
        registry = self.registry(signal.evidence_packet_ref)
        manifest = build_allowed_claim_manifest(registry, rule_id="TEST-RULE-001", signal_reference=signal.signal_id)
        payload = self.output(manifest, packet)
        payload["claims"][0]["modality"] = ["will"]
        result = validate_claim_output(payload, manifest, semantic_conformance=lambda text, manifest: True)
        self.assertFalse(result.valid)
        self.assertIn("claim_modality_outside_manifest", result.reasons)

    def test_result_rejects_replicated_packet_content_mismatch(self):
        from dataclasses import replace
        packet = self.packet()
        runtime = self.runtime()
        mismatched = replace(
            packet,
            calculation_flags={"calculation_status": "VALID"},
        )
        with self.assertRaisesRegex(ValueError, "packet_calculation_flags_result_mismatch"):
            CalculationResult(
                request_id="REQ-FULL-1",
                status=CalculationStatus.NATAL_EVIDENCE_VARIABLE,
                execution_profile_id="CE-CALC-V1-EP-001",
                scenario_state=ScenarioState.VARIABLE,
                normalized_time=None,
                calculation_id="CALC-FULL-1",
                observation_interval=("2026-01-01T00:00:00Z", "2026-01-02T00:00:00Z"),
                object_states=(),
                object_records=(),
                geometry_records=packet.geometry_records,
                event_records=packet.exact_events,
                window_segments=packet.window_segments,
                window_classification=ScenarioState.ROBUST,
                possible_window_segments=(),
                robust_window_segments=(),
                scenario_observations=(),
                solver_metadata={},
                actual_ephemeris_resolution=packet.actual_ephemeris_resolution,
                calculation_flags={"calculation_status": "CALCULATION_FAILURE"},
                warnings=(),
                errors=(),
                provenance={
                    "source_commit": runtime.source_commit,
                    "source_tree_sha256_v2": runtime.source_tree_sha256_v2,
                    "dependency_lock_digest": runtime.dependency_lock_digest,
                    "timezone_bundle_digest": runtime.timezone_bundle_digest,
                    "ephemeris_bundle_digest": runtime.ephemeris_bundle_digest,
                    "runtime_image_digest": runtime.runtime_image_digest,
                    "calculation_version": "CE-CALC-CORE-V1-R1-CONVERGENT",
                    "runtime_identity_sha256": runtime_identity_sha256(runtime),
                    "provenance_root_sha256": packet.provenance_root_sha256,
                },
                provenance_root_sha256=packet.provenance_root_sha256,
                _runtime_identity=runtime,
                _evidence_packet=mismatched,
            )
        self.assertTrue(True)

    def test_claim_release_rederives_signal_and_blocks_runtime(self):
        packet = self.packet()
        signal = issue_qualified_signal_record(packet)
        registry = self.registry(signal.evidence_packet_ref)
        manifest = build_allowed_claim_manifest(registry, rule_id="TEST-RULE-001", signal_reference=signal.signal_id)
        result = evaluate_claim_release(
            self.valid_result(packet),
            packet,
            manifest,
            self.output(manifest, packet),
            self.runtime(),
            registry,
            semantic_conformance=lambda text, manifest: True,
        )
        self.assertFalse(result.authorized)
        self.assertIn("runtime_not_authorized", result.reasons)
        self.assertEqual(result.signal_id, signal.signal_id)

    def test_claim_release_rejects_forged_manifest(self):
        packet = self.packet()
        signal = issue_qualified_signal_record(packet)
        registry = self.registry(signal.evidence_packet_ref)
        manifest = build_allowed_claim_manifest(registry, rule_id="TEST-RULE-001", signal_reference=signal.signal_id)
        forged = type(manifest)(**{**manifest.__dict__, "canon_version": "FORGED"})
        result = evaluate_claim_release(
            self.valid_result(packet),
            packet,
            forged,
            self.output(forged, packet),
            self.runtime(),
            registry,
            semantic_conformance=lambda text, manifest: True,
        )
        self.assertFalse(result.authorized)
        self.assertIn("manifest_registry_binding_mismatch", result.reasons)

    def test_claim_release_rejects_wrong_evidence_packet(self):
        packet = self.packet()
        signal = issue_qualified_signal_record(packet)
        registry = self.registry(signal.evidence_packet_ref)
        manifest = build_allowed_claim_manifest(registry, rule_id="TEST-RULE-001", signal_reference=signal.signal_id)
        other_packet = self.packet()
        result = evaluate_claim_release(
            self.valid_result(packet),
            other_packet,
            manifest,
            self.output(manifest, packet),
            self.runtime(),
            registry,
            semantic_conformance=lambda text, manifest: True,
        )
        self.assertFalse(result.authorized)
        self.assertTrue(any("qualified_signal_derivation_failed" in x or "calculation_result_evidence_binding_missing" in x for x in result.reasons))

    def test_empty_canon_registry_never_releases(self):
        packet = self.packet()
        signal = issue_qualified_signal_record(packet)
        empty = CanonRegistry.empty("CE-CANON-RULE-REGISTRY-V1")
        from ce.claim.authorization import evaluate_claim_release
        result = evaluate_claim_release(
            self.valid_result(packet),
            packet,
            None,  # type: ignore[arg-type]
            {},
            self.runtime(),
            empty,
        )
        self.assertFalse(result.authorized)
        self.assertIn("manifest_required", result.reasons)


if __name__ == "__main__":
    unittest.main()
