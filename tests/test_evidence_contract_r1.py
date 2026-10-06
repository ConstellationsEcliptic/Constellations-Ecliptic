from __future__ import annotations

from datetime import date
import unittest

from ce.calculation.contracts import BirthInput, CalculationRequest, CalculationResultDraft, ObjectRecord, ObjectState
from ce.calculation.evidence_builder import issue_evidence_packet
from ce.calculation.evidence import EvidencePacket
from ce.canon.registry import CanonRegistry, CanonRegistryNotEstablished
from ce.claim.authorization import evaluate_claim_release
from ce.claim.manifest import AllowedClaimManifest, ManifestInvalid, build_allowed_claim_manifest
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
            birth=BirthInput(date(2000, 1, 1), "Test City", "UTC", "2026d", NatalBirthState.ZERO_BIRTH_TIME),
            target_interval_start_utc="2026-01-01T00:00:00Z",
            target_interval_end_utc="2026-01-02T00:00:00Z",
            execution_profile_id="CE-CALC-V1-EP-001",
        )

    def draft(self) -> CalculationResultDraft:
        request = self.request()
        runtime = self.runtime()
        obj = ObjectRecord("SUN", CalculationStatus.VALID, 258, 258, 12.5, 0.0, 1.0, 0.9)
        geometry = ({
            "transit_object": "SUN",
            "natal_object_or_scenario": "MOON",
            "aspect": "CONJUNCTION",
            "directed_branch": 0.0,
            "signed_deviation": 0.0,
            "absolute_deviation": 0.0,
            "effective_orb": 2.5,
            "qualification_state": "QUALIFIED",
            "kinematic_state": "EXACT",
        },)
        return CalculationResultDraft(
            request_id=request.request_id,
            status=CalculationStatus.VALID,
            execution_profile_id=request.execution_profile_id,
            scenario_state=ScenarioState.STABLE,
            normalized_time=request.target_interval_start_utc,
            calculation_id="CALC-FULL-1",
            observation_interval=(request.target_interval_start_utc, request.target_interval_end_utc),
            object_states=(ObjectState("SUN", 12.5, 0.9, CalculationStatus.VALID),),
            object_records=(obj,),
            geometry_records=geometry,
            window_classification=ScenarioState.ROBUST,
            solver_metadata={},
            actual_ephemeris_resolution={"ephemeris_resolution_status": "MATCH"},
            calculation_flags={"calculation_status": "VALID"},
            warnings=(),
            errors=(),
            provenance={},
        )

    def packet(self) -> EvidencePacket:
        return issue_evidence_packet(
            self.draft(),
            request=self.request(),
            runtime_identity=self.runtime(),
        )

    def valid_result(self, packet: EvidencePacket):
        return self.draft().to_final(
            runtime_identity=self.runtime(),
            evidence_packet=packet,
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

    def output(self, manifest: AllowedClaimManifest, packet: EvidencePacket, text: str = "This reflection may invite attention.") -> dict:
        ref = f"{packet.evidence_packet_id}:{packet.content_sha256()}"
        return {
            "manifest_id": manifest.manifest_id,
            "provenance": {
                "manifest_id": manifest.manifest_id,
                "manifest_version": manifest.manifest_version,
                "canon_version": manifest.canon_version,
                "canon_registry_digest": manifest.canon_registry_digest,
                "canon_rule_id": manifest.canon_rule_id,
                "signal_reference": manifest.signal_reference,
                "evidence_refs": [ref],
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
                "evidence_refs": [ref],
                "numeric_refs": [],
            }],
        }

    def test_output_validator_accepts_conforming_claim(self):
        packet = self.packet()
        signal = issue_qualified_signal_record(packet)
        manifest = build_allowed_claim_manifest(self.registry(signal.evidence_packet_ref), rule_id="TEST-RULE-001", signal_reference=signal.signal_id)
        result = validate_claim_output(
            self.output(manifest, packet),
            manifest,
            expected_signal_reference=signal.signal_id,
            expected_evidence_refs=(signal.evidence_packet_ref,),
            expected_provenance_root_sha256=packet.provenance_root_sha256,
            semantic_conformance=lambda text, manifest: True,
        )
        self.assertTrue(result.valid, result.reasons)

    def test_output_validator_rejects_forbidden_modality(self):
        packet = self.packet()
        signal = issue_qualified_signal_record(packet)
        manifest = build_allowed_claim_manifest(self.registry(signal.evidence_packet_ref), rule_id="TEST-RULE-001", signal_reference=signal.signal_id)
        payload = self.output(manifest, packet)
        payload["claims"][0]["modality"] = ["will"]
        result = validate_claim_output(payload, manifest, semantic_conformance=lambda text, manifest: True)
        self.assertFalse(result.valid)
        self.assertIn("claim_modality_outside_manifest", result.reasons)

    def test_claim_release_rederives_signal_and_blocks_runtime(self):
        packet = self.packet()
        signal = issue_qualified_signal_record(packet)
        registry = self.registry(signal.evidence_packet_ref)
        manifest = build_allowed_claim_manifest(registry, rule_id="TEST-RULE-001", signal_reference=signal.signal_id)
        result = evaluate_claim_release(
            self.valid_result(packet), packet, manifest, self.output(manifest, packet),
            self.runtime(), registry, semantic_conformance=lambda text, manifest: True,
        )
        self.assertFalse(result.authorized)
        self.assertIn("runtime_not_authorized", result.reasons)
        self.assertEqual(result.signal_id, signal.signal_id)

    def test_claim_release_rejects_unbound_evidence(self):
        packet = self.packet()
        signal = issue_qualified_signal_record(packet)
        registry = self.registry(signal.evidence_packet_ref)
        manifest = build_allowed_claim_manifest(registry, rule_id="TEST-RULE-001", signal_reference=signal.signal_id)
        other_packet = issue_evidence_packet(
            self.draft(),
            request=self.request(),
            runtime_identity=RuntimeIdentity(
                "CE-CALC-V1-EP-001", 4,
                "z" * 40, "y" * 64, "sha256:" + "x" * 64,
                "w" * 64, "v" * 64, "u" * 64,
            ),
        )
        result = evaluate_claim_release(
            self.valid_result(packet), other_packet, manifest, self.output(manifest, packet),
            self.runtime(), registry, semantic_conformance=lambda text, manifest: True,
        )
        self.assertFalse(result.authorized)
        self.assertTrue(any("mismatch" in reason or "binding" in reason for reason in result.reasons))

    def test_forged_manifest_identity_is_rejected_at_constructor(self):
        packet = self.packet()
        signal = issue_qualified_signal_record(packet)
        registry = self.registry(signal.evidence_packet_ref)
        manifest = build_allowed_claim_manifest(registry, rule_id="TEST-RULE-001", signal_reference=signal.signal_id)
        forged = dict(manifest.canonical_payload())
        forged["manifest_id"] = "CE-ACM-" + "0" * 64
        with self.assertRaisesRegex(ManifestInvalid, "identity_digest"):
            AllowedClaimManifest.from_mapping(forged)

    def test_empty_canon_registry_never_builds_manifest(self):
        packet = self.packet()
        signal = issue_qualified_signal_record(packet)
        empty = CanonRegistry.empty("CE-CANON-RULE-REGISTRY-V1")
        with self.assertRaisesRegex(CanonRegistryNotEstablished, "unpopulated"):
            build_allowed_claim_manifest(empty, rule_id="TEST-RULE-001", signal_reference=signal.signal_id)


if __name__ == "__main__":
    unittest.main()
