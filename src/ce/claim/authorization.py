from __future__ import annotations

from dataclasses import dataclass

from ce.calculation.contracts import CalculationResult
from ce.calculation.evidence import EvidencePacket
from ce.canon.registry import CanonRegistry, CanonRegistryNotEstablished, CanonRuleNotFound
from ce.claim.manifest import AllowedClaimManifest, ManifestInvalid, build_allowed_claim_manifest
from ce.foundation.identity import RuntimeIdentity
from ce.foundation.status import CalculationStatus
from ce.output.validation import SemanticConformanceCheck, validate_claim_output
from ce.product.boundary import preserve_calculation_truth
from ce.runtime.gates import authorize_runtime
from ce.signal.record import QualifiedSignalRecord, issue_qualified_signal_record


_SUPPORTED_RULE_CONDITION_FIELDS = {
    "classification",
    "kinematic_phase",
    "phase_uniformity",
    "requires_uncertainty_disclaimer",
}


@dataclass(frozen=True)
class ClaimReleaseDecision:
    authorized: bool
    reasons: tuple[str, ...]
    signal_id: str | None = None
    manifest_id: str | None = None


def _rule_matches_signal(rule: object, signal: QualifiedSignalRecord) -> bool:
    condition = getattr(rule, "condition", None)
    if not isinstance(condition, dict) or not condition:
        return False
    values = {
        "classification": signal.classification,
        "kinematic_phase": signal.kinematic_phase,
        "phase_uniformity": signal.phase_uniformity,
        "requires_uncertainty_disclaimer": signal.requires_uncertainty_disclaimer,
    }
    if any(key not in _SUPPORTED_RULE_CONDITION_FIELDS for key in condition):
        return False
    return all(values[key] == value for key, value in condition.items())


def evaluate_claim_release(
    calculation_result: CalculationResult,
    evidence_packet: EvidencePacket,
    manifest: AllowedClaimManifest,
    output_payload: object,
    runtime_identity: RuntimeIdentity,
    registry: CanonRegistry,
    *,
    semantic_conformance: SemanticConformanceCheck | None = None,
) -> ClaimReleaseDecision:
    reasons: list[str] = []

    if not isinstance(calculation_result, CalculationResult):
        reasons.append("calculation_result_required")
    if not isinstance(evidence_packet, EvidencePacket):
        reasons.append("evidence_packet_required")
    if not isinstance(runtime_identity, RuntimeIdentity):
        reasons.append("runtime_identity_required")
    if not isinstance(manifest, AllowedClaimManifest):
        reasons.append("manifest_required")
    if not isinstance(registry, CanonRegistry):
        reasons.append("canon_registry_required")
    if reasons:
        return ClaimReleaseDecision(False, tuple(dict.fromkeys(reasons)))

    assert isinstance(calculation_result, CalculationResult)
    assert isinstance(evidence_packet, EvidencePacket)
    assert isinstance(runtime_identity, RuntimeIdentity)
    assert isinstance(manifest, AllowedClaimManifest)
    assert isinstance(registry, CanonRegistry)

    result_errors = calculation_result.validate()
    if result_errors:
        reasons.extend(f"calculation_result:{item}" for item in result_errors)
    packet_errors = evidence_packet.validate(require_issued=True)
    if packet_errors:
        reasons.extend(f"evidence_packet:{item}" for item in packet_errors)

    try:
        derived_signal = issue_qualified_signal_record(evidence_packet)
    except (ValueError, TypeError) as exc:
        reasons.append(f"qualified_signal_derivation_failed:{exc}")
        derived_signal = None

    if derived_signal is not None:
        if calculation_result.evidence_packet_ref is None or not calculation_result.evidence_packet_ref.matches(evidence_packet):
            reasons.append("calculation_result_evidence_binding_missing")
        if manifest.signal_reference != derived_signal.signal_id:
            reasons.append("manifest_signal_reference_mismatch")

    if calculation_result.status is not CalculationStatus.VALID:
        reasons.append("calculation_not_valid")

    boundary = preserve_calculation_truth(calculation_result.status)
    if not (
        boundary.signal_processing_allowed
        and boundary.canon_claim_allowed is False
        and boundary.ai_release_allowed is False
        and boundary.quiet_sky_allowed is False
    ):
        reasons.append("product_boundary_contract_mismatch")

    try:
        rule = registry.get_rule(manifest.canon_rule_id)
        expected_manifest = build_allowed_claim_manifest(
            registry,
            rule_id=manifest.canon_rule_id,
            signal_reference=manifest.signal_reference,
            manifest_version=manifest.manifest_version,
        )
        if (
            expected_manifest.manifest_id != manifest.manifest_id
            or expected_manifest.digest() != manifest.digest()
            or expected_manifest.canon_registry_digest != registry.digest()
        ):
            reasons.append("manifest_registry_binding_mismatch")
        if derived_signal is not None and not _rule_matches_signal(rule, derived_signal):
            reasons.append("canon_rule_signal_condition_mismatch")
    except (CanonRegistryNotEstablished, CanonRuleNotFound, ManifestInvalid, ValueError):
        reasons.append("manifest_registry_binding_failed")

    if derived_signal is not None:
        actual_evidence_ref = f"{evidence_packet.evidence_packet_id}:{evidence_packet.content_sha256()}"
        if actual_evidence_ref not in manifest.required_evidence_refs:
            reasons.append("manifest_missing_signal_evidence_reference")

    output_validation = validate_claim_output(
        output_payload,
        manifest,
        expected_signal_reference=derived_signal.signal_id if derived_signal else None,
        expected_evidence_refs=(
            (f"{evidence_packet.evidence_packet_id}:{evidence_packet.content_sha256()}",)
            if derived_signal is not None
            else ()
        ),
        expected_provenance_root_sha256=(
            calculation_result.provenance_root_sha256
            if calculation_result.provenance_root_sha256 is not None
            else evidence_packet.provenance_root_sha256
        ),
        semantic_conformance=semantic_conformance,
    )
    if not output_validation.valid:
        reasons.extend(output_validation.reasons or ("output_validation_failed",))

    gate = authorize_runtime(runtime_identity)
    if gate.authority.value != "AUTHORIZED":
        reasons.append("runtime_not_authorized")

    unique = tuple(dict.fromkeys(reasons))
    return ClaimReleaseDecision(
        authorized=not unique,
        reasons=unique,
        signal_id=derived_signal.signal_id if derived_signal else None,
        manifest_id=manifest.manifest_id,
    )
