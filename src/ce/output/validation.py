from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Callable, Mapping, Sequence
import re
from typing import Any

from ce.claim.manifest import AllowedClaimManifest

SemanticConformanceCheck = Callable[[str, AllowedClaimManifest], bool]

@dataclass(frozen=True)
class OutputValidationResult:
    valid: bool
    reasons: tuple[str, ...]

_GUARANTEE_PATTERNS = (
    re.compile(r"\bwill\s+definitely\b", re.I),
    re.compile(r"\bguarantee(?:d|s)?\b", re.I),
    re.compile(r"\bcertain(?:ly)?\s+to\b", re.I),
    re.compile(r"\bmust\s+be\s+true\b", re.I),
)
_TRUTH_PATTERNS = (
    re.compile(r"\bobjectively\b", re.I),
    re.compile(r"\bthis\s+is\s+true\b", re.I),
)
_DIAGNOSTIC_PATTERNS = (
    re.compile(r"\bdiagnos(?:is|e|ed|tic)\b", re.I),
    re.compile(r"\bmental\s+health\b", re.I),
)
_TYPE_PATTERNS = {
    "guarantee": _GUARANTEE_PATTERNS,
    "objective truth": _TRUTH_PATTERNS,
    "unsupported causality": (
        re.compile(r"\bcauses?\b", re.I),
        re.compile(r"\bbecause\s+this\s+signal\b", re.I),
    ),
    "hidden profile": (
        re.compile(r"\byour\s+true\s+personality\b", re.I),
        re.compile(r"\byou\s+secretly\b", re.I),
    ),
    "fabricated fact": (
        re.compile(r"\bfactually\b", re.I),
        re.compile(r"\bthe\s+event\s+will\b", re.I),
    ),
}

def _phrase(value: str) -> str:
    return " ".join(value.casefold().replace("-", " ").split())

def _contains(text: str, value: str) -> bool:
    return _phrase(value) in _phrase(text)

def _numbers(text: str) -> tuple[str, ...]:
    return tuple(re.findall(r"(?<![\w])[-+]?\d+(?:[.,]\d+)?%?", text))

def validate_claim_output(
    payload: Any,
    manifest: AllowedClaimManifest,
    semantic_conformance: SemanticConformanceCheck | None = None,
) -> OutputValidationResult:
    reasons: list[str] = []
    if not isinstance(manifest, AllowedClaimManifest):
        return OutputValidationResult(False, ("manifest_required",))
    if not isinstance(payload, Mapping):
        return OutputValidationResult(False, ("output_not_object",))

    if set(payload) != {"manifest_id", "claims"}:
        reasons.append("output_schema_mismatch")
    if payload.get("manifest_id") != manifest.manifest_id:
        reasons.append("manifest_identity_mismatch")

    claims = payload.get("claims")
    if not isinstance(claims, Sequence) or isinstance(claims, (str, bytes)):
        reasons.append("claims_not_array")
        claims = ()
    if len(claims) != 1:
        reasons.append("claim_count_mismatch")

    if len(claims) == 1:
        claim = claims[0]
        if not isinstance(claim, Mapping):
            reasons.append("claim_not_object")
        elif set(claim) != {"claim_id", "text"}:
            reasons.append("claim_schema_mismatch")
        else:
            if claim.get("claim_id") != manifest.claim_id:
                reasons.append("claim_id_mismatch")
            text = claim.get("text")
            if not isinstance(text, str) or not text.strip():
                reasons.append("claim_text_invalid")
            else:
                if any(p.search(text) for p in _GUARANTEE_PATTERNS):
                    reasons.append("forbidden_guarantee_language")
                if any(p.search(text) for p in _TRUTH_PATTERNS):
                    reasons.append("forbidden_objective_truth_language")
                if any(p.search(text) for p in _DIAGNOSTIC_PATTERNS):
                    reasons.append("forbidden_diagnostic_language")

                for claim_type in manifest.forbidden_claim_types:
                    patterns = _TYPE_PATTERNS.get(_phrase(claim_type))
                    if patterns is None:
                        reasons.append(f"claim_type_semantics_unimplemented:{_phrase(claim_type)}")
                    elif any(p.search(text) for p in patterns):
                        reasons.append(f"forbidden_claim_type:{_phrase(claim_type)}")

                for domain in manifest.forbidden_domains:
                    if _contains(text, domain):
                        reasons.append(f"forbidden_domain:{_phrase(domain)}")

                for disclosure in manifest.required_disclosures:
                    if not _contains(text, disclosure):
                        reasons.append(f"required_disclosure_missing:{_phrase(disclosure)}")

                for number in _numbers(text):
                    if number not in manifest.allowed_numeric_refs:
                        reasons.append("numeric_reference_not_allowed")
                        break

                if semantic_conformance is None:
                    reasons.append("semantic_conformance_unavailable")
                else:
                    try:
                        if semantic_conformance(text, manifest) is not True:
                            reasons.append("semantic_nonconformance")
                    except Exception:
                        reasons.append("semantic_conformance_check_error")

    return OutputValidationResult(not reasons, tuple(dict.fromkeys(reasons)))
