from __future__ import annotations

from dataclasses import dataclass

from ce.canon.registry import CanonRegistry, CanonRegistryNotEstablished, CanonRuleNotFound
from ce.claim.manifest import AllowedClaimManifest, ManifestInvalid, build_allowed_claim_manifest
from ce.foundation.status import CalculationStatus, RuntimeAuthority
from ce.output.validation import OutputValidationResult
from ce.product.boundary import ProductBoundaryDecision
from ce.runtime.gates import RuntimeGateResult
from ce.signal.record import QualifiedSignalRecord

@dataclass(frozen=True)
class ClaimReleaseDecision:
    authorized: bool
    reasons: tuple[str, ...]

def evaluate_claim_release(
    boundary: ProductBoundaryDecision,
    signal: QualifiedSignalRecord,
    manifest: AllowedClaimManifest,
    output_validation: OutputValidationResult,
    runtime_gate: RuntimeGateResult,
    registry: CanonRegistry,
) -> ClaimReleaseDecision:
    reasons: list[str] = []

    if not isinstance(boundary, ProductBoundaryDecision):
        reasons.append("boundary_required")
    elif boundary.status is not CalculationStatus.VALID:
        reasons.append("calculation_not_valid")

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

    if not isinstance(output_validation, OutputValidationResult):
        reasons.append("output_validation_required")
    elif not output_validation.valid:
        reasons.extend(output_validation.reasons or ("output_validation_failed",))

    if not isinstance(runtime_gate, RuntimeGateResult):
        reasons.append("runtime_gate_required")
    elif runtime_gate.authority is not RuntimeAuthority.AUTHORIZED:
        reasons.append("runtime_not_authorized")

    if not isinstance(registry, CanonRegistry):
        reasons.append("canon_registry_required")
    elif isinstance(manifest, AllowedClaimManifest):
        try:
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
