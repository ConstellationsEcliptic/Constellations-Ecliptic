from __future__ import annotations

from dataclasses import dataclass

from ce.canon.registry import CanonRegistry, CanonRegistryNotEstablished, CanonRuleNotFound
from ce.claim.manifest import AllowedClaimManifest, ManifestInvalid, build_allowed_claim_manifest
from ce.foundation.identity import RuntimeIdentity
from ce.foundation.status import CalculationStatus
from ce.output.validation import SemanticConformanceCheck, validate_claim_output
from ce.product.boundary import ProductBoundaryDecision
from ce.runtime.gates import authorize_runtime
from ce.signal.record import QualifiedSignalRecord


_SUPPORTED_RULE_CONDITION_FIELDS = {
    "classification",
    "kinematic_phase",
    "phase_uniformity",
    "requires_uncertainty_disclaimer",
}


def _rule_matches_signal(rule, signal: QualifiedSignalRecord) -> bool:
    condition = rule.condition
    if not isinstance(condition, dict) or not condition:
        return False
    signal_values = {
        "classification": signal.classification,
        "kinematic_phase": signal.kinematic_phase,
        "phase_uniformity": signal.phase_uniformity,
        "requires_uncertainty_disclaimer": signal.requires_uncertainty_disclaimer,
    }
    if any(key not in _SUPPORTED_RULE_CONDITION_FIELDS for key in condition):
        return False
    return all(signal_values[key] == value for key, value in condition.items())


@dataclass(frozen=True)
class ClaimReleaseDecision:
    authorized: bool
    reasons: tuple[str, ...]


def evaluate_claim_release(
    boundary: ProductBoundaryDecision,
    signal: QualifiedSignalRecord,
    manifest: AllowedClaimManifest,
    output_payload: object,
    runtime_identity: RuntimeIdentity,
    registry: CanonRegistry,
    *,
    semantic_conformance: SemanticConformanceCheck | None = None,
) -> ClaimReleaseDecision:
    """Evaluate release gates from the underlying inputs, not caller-made gate results."""

    reasons: list[str] = []

    if not isinstance(boundary, ProductBoundaryDecision):
        reasons.append("boundary_required")
    elif boundary.status is not CalculationStatus.VALID:
        if any(
            flag is not False
            for flag in (
                boundary.signal_processing_allowed,
                boundary.canon_claim_allowed,
                boundary.ai_release_allowed,
                boundary.quiet_sky_allowed,
            )
        ):
            reasons.append("product_boundary_contract_mismatch")
        reasons.append("calculation_not_valid")
    elif not (
        boundary.signal_processing_allowed is True
        and boundary.canon_claim_allowed is False
        and boundary.ai_release_allowed is False
        and boundary.quiet_sky_allowed is False
    ):
        reasons.append("product_boundary_contract_mismatch")

    if not isinstance(signal, QualifiedSignalRecord):
        reasons.append("qualified_signal_required")
    elif signal.qualification_status != CalculationStatus.VALID.value or not signal.canon_input_valid:
        reasons.append("qualified_signal_not_eligible")

    if not isinstance(manifest, AllowedClaimManifest):
        reasons.append("manifest_required")
    elif not isinstance(signal, QualifiedSignalRecord):
        reasons.append("manifest_signal_reference_unverifiable")
    else:
        if manifest.signal_reference != signal.signal_id:
            reasons.append("manifest_signal_reference_mismatch")
        if signal.evidence_packet_ref not in manifest.required_evidence_refs:
            reasons.append("manifest_missing_signal_evidence_reference")

    if isinstance(manifest, AllowedClaimManifest):
        output_validation = validate_claim_output(
            output_payload,
            manifest,
            semantic_conformance=semantic_conformance,
        )
        if not output_validation.valid:
            reasons.extend(output_validation.reasons or ("output_validation_failed",))
    else:
        reasons.append("output_validation_manifest_unavailable")

    if not isinstance(runtime_identity, RuntimeIdentity):
        reasons.append("runtime_identity_required")
    else:
        runtime_gate = authorize_runtime(runtime_identity)
        if runtime_gate.authority.value != "AUTHORIZED":
            reasons.append("runtime_not_authorized")

    if not isinstance(registry, CanonRegistry):
        reasons.append("canon_registry_required")
    elif isinstance(manifest, AllowedClaimManifest):
        try:
            rule = registry.get_rule(manifest.canon_rule_id)
            if isinstance(signal, QualifiedSignalRecord) and not _rule_matches_signal(rule, signal):
                reasons.append("canon_rule_signal_condition_mismatch")
            expected = build_allowed_claim_manifest(
                registry,
                rule_id=manifest.canon_rule_id,
                signal_reference=manifest.signal_reference,
                manifest_version=manifest.manifest_version,
            )
            if expected.manifest_id != manifest.manifest_id or expected.digest() != manifest.digest():
                reasons.append("manifest_registry_binding_mismatch")
            if expected.canon_version != manifest.canon_version:
                reasons.append("manifest_canon_version_mismatch")
        except (CanonRegistryNotEstablished, CanonRuleNotFound, ManifestInvalid, ValueError):
            reasons.append("manifest_registry_binding_failed")

    unique = tuple(dict.fromkeys(reasons))
    return ClaimReleaseDecision(authorized=not unique, reasons=unique)
