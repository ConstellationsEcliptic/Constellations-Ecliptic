from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Mapping, Sequence
from typing import Any

from ce.canon.registry import CanonRule
from ce.foundation.hashing import sha256_bytes
from ce.foundation.serialization import canonical_json

ALLOWED_EPISTEMIC_LAYERS = (
    "ASTRONOMICAL_FACT",
    "GEOMETRIC_DERIVATION",
    "ASTROLOGICAL_INTERPRETATION",
    "POSSIBILITY",
    "USER_REPORTED",
)

class ManifestInvalid(ValueError):
    pass

def _strings(name: str, value: Any) -> tuple[str, ...]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise ManifestInvalid(f"manifest_invalid:{name}")
    result = tuple(value)
    if any(not isinstance(item, str) or not item.strip() for item in result):
        raise ManifestInvalid(f"manifest_invalid:{name}")
    return result

@dataclass(frozen=True)
class CanonApprovedInterpretation:
    claim_id: str
    allowed_subject: tuple[str, ...]
    allowed_scope: tuple[str, ...]
    epistemic_layer: str
    certainty_ceiling: str
    allowed_modality: tuple[str, ...]
    allowed_tense: tuple[str, ...]
    forbidden_domains: tuple[str, ...]
    forbidden_claim_types: tuple[str, ...]
    required_evidence_refs: tuple[str, ...]
    allowed_numeric_refs: tuple[str, ...]
    required_disclosures: tuple[str, ...]

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "CanonApprovedInterpretation":
        if not isinstance(value, Mapping):
            raise ManifestInvalid("canon_interpretation_not_object")
        required = (
            "claim_id","allowed_subject","allowed_scope","epistemic_layer",
            "certainty_ceiling","allowed_modality","allowed_tense","forbidden_domains",
            "forbidden_claim_types","required_evidence_refs","allowed_numeric_refs",
            "required_disclosures",
        )
        missing = [key for key in required if key not in value]
        if missing:
            raise ManifestInvalid("canon_interpretation_missing_fields:" + ",".join(missing))
        if not isinstance(value["claim_id"], str) or not value["claim_id"].strip():
            raise ManifestInvalid("manifest_invalid:claim_id")
        if value["epistemic_layer"] not in ALLOWED_EPISTEMIC_LAYERS:
            raise ManifestInvalid("manifest_invalid:epistemic_layer")
        if not isinstance(value["certainty_ceiling"], str) or not value["certainty_ceiling"].strip():
            raise ManifestInvalid("manifest_invalid:certainty_ceiling")
        return cls(
            claim_id=value["claim_id"],
            allowed_subject=_strings("allowed_subject", value["allowed_subject"]),
            allowed_scope=_strings("allowed_scope", value["allowed_scope"]),
            epistemic_layer=value["epistemic_layer"],
            certainty_ceiling=value["certainty_ceiling"],
            allowed_modality=_strings("allowed_modality", value["allowed_modality"]),
            allowed_tense=_strings("allowed_tense", value["allowed_tense"]),
            forbidden_domains=_strings("forbidden_domains", value["forbidden_domains"]),
            forbidden_claim_types=_strings("forbidden_claim_types", value["forbidden_claim_types"]),
            required_evidence_refs=_strings("required_evidence_refs", value["required_evidence_refs"]),
            allowed_numeric_refs=_strings("allowed_numeric_refs", value["allowed_numeric_refs"]),
            required_disclosures=_strings("required_disclosures", value["required_disclosures"]),
        )

    def canonical_payload(self) -> dict[str, Any]:
        return {
            "claim_id": self.claim_id,
            "allowed_subject": list(self.allowed_subject),
            "allowed_scope": list(self.allowed_scope),
            "epistemic_layer": self.epistemic_layer,
            "certainty_ceiling": self.certainty_ceiling,
            "allowed_modality": list(self.allowed_modality),
            "allowed_tense": list(self.allowed_tense),
            "forbidden_domains": list(self.forbidden_domains),
            "forbidden_claim_types": list(self.forbidden_claim_types),
            "required_evidence_refs": list(self.required_evidence_refs),
            "allowed_numeric_refs": list(self.allowed_numeric_refs),
            "required_disclosures": list(self.required_disclosures),
        }

@dataclass(frozen=True)
class AllowedClaimManifest:
    manifest_version: str
    manifest_id: str
    claim_id: str
    canon_version: str
    canon_rule_id: str
    signal_reference: str
    allowed_subject: tuple[str, ...]
    allowed_scope: tuple[str, ...]
    epistemic_layer: str
    certainty_ceiling: str
    allowed_modality: tuple[str, ...]
    allowed_tense: tuple[str, ...]
    forbidden_domains: tuple[str, ...]
    forbidden_claim_types: tuple[str, ...]
    required_evidence_refs: tuple[str, ...]
    allowed_numeric_refs: tuple[str, ...]
    required_disclosures: tuple[str, ...]

    def canonical_payload(self) -> dict[str, Any]:
        return {
            "manifest_version": self.manifest_version,
            "claim_id": self.claim_id,
            "canon_version": self.canon_version,
            "canon_rule_id": self.canon_rule_id,
            "signal_reference": self.signal_reference,
            "allowed_subject": list(self.allowed_subject),
            "allowed_scope": list(self.allowed_scope),
            "epistemic_layer": self.epistemic_layer,
            "certainty_ceiling": self.certainty_ceiling,
            "allowed_modality": list(self.allowed_modality),
            "allowed_tense": list(self.allowed_tense),
            "forbidden_domains": list(self.forbidden_domains),
            "forbidden_claim_types": list(self.forbidden_claim_types),
            "required_evidence_refs": list(self.required_evidence_refs),
            "allowed_numeric_refs": list(self.allowed_numeric_refs),
            "required_disclosures": list(self.required_disclosures],
        }

    def digest(self) -> str:
        return sha256_bytes(canonical_json(self.canonical_payload()))

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "AllowedClaimManifest":
        if not isinstance(value, Mapping):
            raise ManifestInvalid("manifest_not_object")
        required = (
            "manifest_version","manifest_id","claim_id","canon_version","canon_rule_id",
            "signal_reference","allowed_subject","allowed_scope","epistemic_layer",
            "certainty_ceiling","allowed_modality","allowed_tense","forbidden_domains",
            "forbidden_claim_types","required_evidence_refs","allowed_numeric_refs",
            "required_disclosures",
        )
        missing = [key for key in required if key not in value]
        if missing:
            raise ManifestInvalid("manifest_missing_fields:" + ",".join(missing))
        for key in (
            "manifest_version","manifest_id","claim_id","canon_version",
            "canon_rule_id","signal_reference","certainty_ceiling",
        ):
            if not isinstance(value[key], str) or not value[key].strip():
                raise ManifestInvalid(f"manifest_invalid:{key}")
        interpretation = CanonApprovedInterpretation.from_mapping(value)
        candidate = cls(
            manifest_version=value["manifest_version"],
            manifest_id=value["manifest_id"],
            claim_id=value["claim_id"],
            canon_version=value["canon_version"],
            canon_rule_id=value["canon_rule_id"],
            signal_reference=value["signal_reference"],
            allowed_subject=interpretation.allowed_subject,
            allowed_scope=interpretation.allowed_scope,
            epistemic_layer=interpretation.epistemic_layer,
            certainty_ceiling=interpretation.certainty_ceiling,
            allowed_modality=interpretation.allowed_modality,
            allowed_tense=interpretation.allowed_tense,
            forbidden_domains=interpretation.forbidden_domains,
            forbidden_claim_types=interpretation.forbidden_claim_types,
            required_evidence_refs=interpretation.required_evidence_refs,
            allowed_numeric_refs=interpretation.allowed_numeric_refs,
            required_disclosures=interpretation.required_disclosures,
        )
        expected_id = "CE-ACM-" + sha256_bytes(canonical_json(candidate.canonical_payload()))
        if candidate.manifest_id != expected_id:
            raise ManifestInvalid("manifest_identity_digest_mismatch")
        return candidate

def build_allowed_claim_manifest(
    rule: CanonRule,
    *,
    signal_reference: str,
    interpretation: CanonApprovedInterpretation,
    manifest_version: str = "CE-ALLOWED-CLAIM-MANIFEST-V1",
) -> AllowedClaimManifest:
    if not isinstance(rule, CanonRule):
        raise ManifestInvalid("manifest_canon_rule_required")
    if not isinstance(signal_reference, str) or not signal_reference.strip():
        raise ManifestInvalid("manifest_signal_reference_invalid")
    if not isinstance(interpretation, CanonApprovedInterpretation):
        raise ManifestInvalid("manifest_interpretation_required")

    identity = {
        "manifest_version": manifest_version,
        "claim_id": interpretation.claim_id,
        "canon_version": rule.canon_version,
        "canon_rule_id": rule.rule_id,
        "signal_reference": signal_reference,
        **interpretation.canonical_payload(),
    }
    manifest_id = "CE-ACM-" + sha256_bytes(canonical_json(identity))
    return AllowedClaimManifest(
        manifest_version=manifest_version,
        manifest_id=manifest_id,
        claim_id=interpretation.claim_id,
        canon_version=rule.canon_version,
        canon_rule_id=rule.rule_id,
        signal_reference=signal_reference,
        allowed_subject=interpretation.allowed_subject,
        allowed_scope=interpretation.allowed_scope,
        epistemic_layer=interpretation.epistemic_layer,
        certainty_ceiling=interpretation.certainty_ceiling,
        allowed_modality=interpretation.allowed_modality,
        allowed_tense=interpretation.allowed_tense,
        forbidden_domains=interpretation.forbidden_domains,
        forbidden_claim_types=interpretation.forbidden_claim_types,
        required_evidence_refs=interpretation.required_evidence_refs,
        allowed_numeric_refs=interpretation.allowed_numeric_refs,
        required_disclosures=interpretation.required_disclosures,
    )
