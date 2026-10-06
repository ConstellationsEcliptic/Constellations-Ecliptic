from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
import re
from typing import Any

from ce.claim.manifest import AllowedClaimManifest
from ce.foundation.hashing import sha256_bytes
from ce.foundation.serialization import canonical_json

SemanticConformanceCheck = Callable[[str, AllowedClaimManifest], bool]

@dataclass(frozen=True)
class OutputValidationResult:
    valid: bool
    reasons: tuple[str, ...]

_GUARANTEE_PATTERNS=(
    re.compile(r"\bwill\s+definitely\b",re.I),
    re.compile(r"\bguarantee(?:d|s)?\b",re.I),
    re.compile(r"\bcertain(?:ly)?\s+to\b",re.I),
    re.compile(r"\bmust\s+be\s+true\b",re.I),
)
_TRUTH_PATTERNS=(
    re.compile(r"\bobjectively\b",re.I),
    re.compile(r"\bthis\s+is\s+true\b",re.I),
)
_DIAGNOSTIC_PATTERNS=(
    re.compile(r"\bdiagnos(?:is|e|ed|tic)\b",re.I),
    re.compile(r"\bmental\s+health\b",re.I),
)
_TYPE_PATTERNS={
    "guarantee":_GUARANTEE_PATTERNS,
    "objective truth":_TRUTH_PATTERNS,
    "unsupported causality":(
        re.compile(r"\bcauses?\b",re.I),
        re.compile(r"\bbecause\s+this\s+signal\b",re.I),
    ),
    "hidden profile":(
        re.compile(r"\byour\s+true\s+personality\b",re.I),
        re.compile(r"\byou\s+secretly\b",re.I),
    ),
    "fabricated fact":(
        re.compile(r"\bfactually\b",re.I),
        re.compile(r"\bthe\s+event\s+will\b",re.I),
    ),
}

def _phrases(value: Sequence[str]) -> set[str]:
    return {" ".join(item.casefold().replace("-"," ").split()) for item in value}

def _contains(text: str, value: str) -> bool:
    return " ".join(value.casefold().replace("-"," ").split()) in " ".join(text.casefold().replace("-"," ").split())

def _numbers(text: str)->tuple[str,...]:
    return tuple(re.findall(r"(?<![\w])[-+]?\d+(?:[.,]\d+)?%?",text))

def _subset(name: str, actual: Any, allowed: Sequence[str], reasons: list[str]) -> None:
    if not isinstance(actual, Sequence) or isinstance(actual,(str,bytes,bytearray)):
        reasons.append(f"claim_{name}_not_array")
        return
    values={str(x) for x in actual}
    allowed_set=_phrases(allowed)
    if not values or any(" ".join(v.casefold().replace("-"," ").split()) not in allowed_set for v in values):
        reasons.append(f"claim_{name}_outside_manifest")

def validate_claim_output(
    payload: Any,
    manifest: AllowedClaimManifest,
    *,
    expected_signal_reference: str | None = None,
    expected_evidence_refs: Sequence[str] = (),
    expected_provenance_root_sha256: str | None = None,
    semantic_conformance: SemanticConformanceCheck | None = None,
) -> OutputValidationResult:
    reasons:list[str]=[]
    if not isinstance(manifest,AllowedClaimManifest):
        return OutputValidationResult(False,("manifest_required",))
    if not isinstance(payload,Mapping):
        return OutputValidationResult(False,("output_not_object",))

    required_top={"manifest_id","provenance","claims"}
    if set(payload)!=required_top:
        reasons.append("output_schema_mismatch")
    if payload.get("manifest_id")!=manifest.manifest_id:
        reasons.append("manifest_identity_mismatch")
    expected_manifest_id="CE-ACM-"+sha256_bytes(canonical_json(manifest.canonical_payload()))
    if manifest.manifest_id!=expected_manifest_id:
        reasons.append("manifest_identity_digest_mismatch")

    provenance=payload.get("provenance")
    if not isinstance(provenance,Mapping):
        reasons.append("output_provenance_invalid")
    else:
        expected_keys={"manifest_id","manifest_version","canon_version","canon_registry_digest","canon_rule_id","signal_reference","evidence_refs","provenance_root_sha256"}
        if set(provenance)!=expected_keys:
            reasons.append("output_provenance_schema_mismatch")
        checks={
            "manifest_id":manifest.manifest_id,
            "manifest_version":manifest.manifest_version,
            "canon_version":manifest.canon_version,
            "canon_registry_digest":manifest.canon_registry_digest,
            "canon_rule_id":manifest.canon_rule_id,
            "signal_reference":expected_signal_reference or manifest.signal_reference,
        }
        for key,expected in checks.items():
            if provenance.get(key)!=expected:
                reasons.append(f"output_provenance_{key}_mismatch")
        ev=provenance.get("evidence_refs")
        if not isinstance(ev,Sequence) or isinstance(ev,(str,bytes,bytearray)):
            reasons.append("output_provenance_evidence_refs_invalid")
        else:
            ev_set={str(x) for x in ev}
            required_set=set(expected_evidence_refs) or set(manifest.required_evidence_refs)
            if not required_set.issubset(ev_set):
                reasons.append("output_provenance_missing_evidence_refs")
        if expected_provenance_root_sha256 is not None and provenance.get("provenance_root_sha256")!=expected_provenance_root_sha256:
            reasons.append("output_provenance_root_mismatch")

    claims=payload.get("claims")
    if not isinstance(claims,Sequence) or isinstance(claims,(str,bytes,bytearray)):
        reasons.append("claims_not_array"); claims=()
    if len(claims)!=1:
        reasons.append("claim_count_mismatch")

    if len(claims)==1:
        claim=claims[0]
        required_claim={"claim_id","text","subject","scope","modality","tense","epistemic_layer","certainty","evidence_refs","numeric_refs"}
        if not isinstance(claim,Mapping):
            reasons.append("claim_not_object")
        else:
            if set(claim)!=required_claim:
                reasons.append("claim_schema_mismatch")
            if claim.get("claim_id")!=manifest.claim_id:
                reasons.append("claim_id_mismatch")
            text=claim.get("text")
            if not isinstance(text,str) or not text.strip():
                reasons.append("claim_text_invalid")
            else:
                _subset("subject",claim.get("subject"),manifest.allowed_subject,reasons)
                _subset("scope",claim.get("scope"),manifest.allowed_scope,reasons)
                _subset("modality",claim.get("modality"),manifest.allowed_modality,reasons)
                _subset("tense",claim.get("tense"),manifest.allowed_tense,reasons)
                if claim.get("epistemic_layer")!=manifest.epistemic_layer:
                    reasons.append("claim_epistemic_layer_mismatch")
                if claim.get("certainty")!=manifest.certainty_ceiling:
                    reasons.append("claim_certainty_exceeds_or_mismatches_ceiling")

                evidence_refs=claim.get("evidence_refs")
                if not isinstance(evidence_refs,Sequence) or isinstance(evidence_refs,(str,bytes,bytearray)):
                    reasons.append("claim_evidence_refs_invalid")
                else:
                    ev_set={str(x) for x in evidence_refs}
                    required=set(expected_evidence_refs) or set(manifest.required_evidence_refs)
                    if not required.issubset(ev_set) or any(str(x) not in required for x in ev_set):
                        reasons.append("claim_evidence_refs_outside_manifest")

                numeric_refs=claim.get("numeric_refs")
                if not isinstance(numeric_refs,Sequence) or isinstance(numeric_refs,(str,bytes,bytearray)):
                    reasons.append("claim_numeric_refs_invalid")
                else:
                    allowed=set(manifest.allowed_numeric_refs)
                    if any(str(x) not in allowed for x in numeric_refs):
                        reasons.append("claim_numeric_reference_not_allowed")

                if any(p.search(text) for p in _GUARANTEE_PATTERNS):
                    reasons.append("forbidden_guarantee_language")
                if any(p.search(text) for p in _TRUTH_PATTERNS):
                    reasons.append("forbidden_objective_truth_language")
                if any(p.search(text) for p in _DIAGNOSTIC_PATTERNS):
                    reasons.append("forbidden_diagnostic_language")
                for claim_type in manifest.forbidden_claim_types:
                    patterns=_TYPE_PATTERNS.get(" ".join(claim_type.casefold().replace("-"," ").split()))
                    if patterns is None:
                        reasons.append(f"claim_type_semantics_unimplemented:{claim_type}")
                    elif any(p.search(text) for p in patterns):
                        reasons.append(f"forbidden_claim_type:{claim_type}")
                for domain in manifest.forbidden_domains:
                    if _contains(text,domain):
                        reasons.append(f"forbidden_domain:{domain}")
                for disclosure in manifest.required_disclosures:
                    if not _contains(text,disclosure):
                        reasons.append(f"required_disclosure_missing:{disclosure}")
                if semantic_conformance is None:
                    reasons.append("semantic_conformance_unavailable")
                else:
                    try:
                        if semantic_conformance(text,manifest) is not True:
                            reasons.append("semantic_nonconformance")
                    except Exception:
                        reasons.append("semantic_conformance_check_error")

    return OutputValidationResult(not reasons,tuple(dict.fromkeys(reasons)))
