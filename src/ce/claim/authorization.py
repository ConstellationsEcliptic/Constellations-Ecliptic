from __future__ import annotations

from dataclasses import dataclass

from ce.claim.manifest import AllowedClaimManifest
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
) -> ClaimReleaseDecision:
    reasons: list[str] = []
    if not isinstance(boundary, ProductBoundaryDecision):
        reasons.append("boundary_required")
    elif boundary.status is not CalculationStatus.VALID:
        reasons.append("calculation_not_valid")

    if not isinstance(signal, QualifiedSignalRecord):
        reasons.append("qualified_signal_required")
    else:
        if signal.qualification_status != CalculationStatus.VALID.value or not signal.canon_input_valid:
            reasons.append("qualified_signal_not_eligible")

    if not isinstance(manifest, AllowedClaimManifest):
        reasons.append("manifest_required")
    elif isinstance(signal, QualifiedSignalRecord):
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

    unique = tuple(dict.fromkeys(reasons))
    return ClaimReleaseDecision(authorized=not unique, reasons=unique)
