from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from ce.canon.registry import CanonRegistry, CanonRule
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
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        raise ManifestInvalid(f"manifest_invalid:{name}")
    result=tuple(value)
    if any(not isinstance(item,str) or not item.strip() for item in result):
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
        required=(
            "claim_id","allowed_subject","allowed_scope","epistemic_layer",
            "certainty_ceiling","allowed_modality","allowed_tense",
            "forbidden_domains","forbidden_claim_types","required_evidence_refs",
            "allowed_numeric_refs","required_disclosures",
        )
        if not isinstance(value, Mapping): raise ManifestInvalid("canon_interpretation_not_object")
        missing=[k for k in required if k not in value]
        extra=[k for k in value if k not in required]
        if missing: raise ManifestInvalid("canon_interpretation_missing_fields:"+",".join(missing))
        if extra: raise ManifestInvalid("canon_interpretation_unknown_fields:"+",".join(sorted(extra)))
        if not isinstance(value["claim_id"],str) or not value["claim_id"].strip():
            raise ManifestInvalid("manifest_invalid:claim_id")
        if value["epistemic_layer"] not in ALLOWED_EPISTEMIC_LAYERS:
            raise ManifestInvalid("manifest_invalid:epistemic_layer")
        if not isinstance(value["certainty_ceiling"],str) or not value["certainty_ceiling"].strip():
            raise ManifestInvalid("manifest_invalid:certainty_ceiling")
        return cls(
            value["claim_id"], _strings("allowed_subject",value["allowed_subject"]),
            _strings("allowed_scope",value["allowed_scope"]), value["epistemic_layer"],
            value["certainty_ceiling"], _strings("allowed_modality",value["allowed_modality"]),
            _strings("allowed_tense",value["allowed_tense"]),
            _strings("forbidden_domains",value["forbidden_domains"]),
            _strings("forbidden_claim_types",value["forbidden_claim_types"]),
            _strings("required_evidence_refs",value["required_evidence_refs"]),
            _strings("allowed_numeric_refs",value["allowed_numeric_refs"]),
            _strings("required_disclosures",value["required_disclosures"]),
        )

    @classmethod
    def from_rule(cls, rule: CanonRule) -> "CanonApprovedInterpretation":
        if not isinstance(rule,CanonRule): raise ManifestInvalid("canon_rule_required")
        return cls.from_mapping(rule.allowed_interpretation)

    def canonical_payload(self)->dict[str,Any]:
        return {
            "claim_id":self.claim_id,"allowed_subject":list(self.allowed_subject),
            "allowed_scope":list(self.allowed_scope),"epistemic_layer":self.epistemic_layer,
            "certainty_ceiling":self.certainty_ceiling,"allowed_modality":list(self.allowed_modality),
            "allowed_tense":list(self.allowed_tense),"forbidden_domains":list(self.forbidden_domains),
            "forbidden_claim_types":list(self.forbidden_claim_types),
            "required_evidence_refs":list(self.required_evidence_refs),
            "allowed_numeric_refs":list(self.allowed_numeric_refs),
            "required_disclosures":list(self.required_disclosures),
        }

@dataclass(frozen=True)
class AllowedClaimManifest:
    manifest_version: str
    manifest_id: str
    claim_id: str
    canon_version: str
    canon_registry_digest: str
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

    def canonical_payload(self)->dict[str,Any]:
        return {
            "manifest_version":self.manifest_version,"claim_id":self.claim_id,
            "canon_version":self.canon_version,"canon_registry_digest":self.canon_registry_digest,
            "canon_rule_id":self.canon_rule_id,"signal_reference":self.signal_reference,
            "allowed_subject":list(self.allowed_subject),"allowed_scope":list(self.allowed_scope),
            "epistemic_layer":self.epistemic_layer,"certainty_ceiling":self.certainty_ceiling,
            "allowed_modality":list(self.allowed_modality),"allowed_tense":list(self.allowed_tense),
            "forbidden_domains":list(self.forbidden_domains),"forbidden_claim_types":list(self.forbidden_claim_types),
            "required_evidence_refs":list(self.required_evidence_refs),
            "allowed_numeric_refs":list(self.allowed_numeric_refs),
            "required_disclosures":list(self.required_disclosures),
        }

    def digest(self)->str:
        return sha256_bytes(canonical_json(self.canonical_payload()))

    def __post_init__(self)->None:
        if not all(isinstance(x,str) and x.strip() for x in (
            self.manifest_version,self.manifest_id,self.claim_id,self.canon_version,
            self.canon_registry_digest,self.canon_rule_id,self.signal_reference,self.certainty_ceiling
        )):
            raise ManifestInvalid("manifest_identity_fields_invalid")
        if len(self.canon_registry_digest)!=64:
            raise ManifestInvalid("manifest_invalid:canon_registry_digest")
        if self.epistemic_layer not in ALLOWED_EPISTEMIC_LAYERS:
            raise ManifestInvalid("manifest_invalid:epistemic_layer")
        for name,value in (
            ("allowed_subject",self.allowed_subject),("allowed_scope",self.allowed_scope),
            ("allowed_modality",self.allowed_modality),("allowed_tense",self.allowed_tense),
            ("forbidden_domains",self.forbidden_domains),("forbidden_claim_types",self.forbidden_claim_types),
            ("required_evidence_refs",self.required_evidence_refs),("allowed_numeric_refs",self.allowed_numeric_refs),
            ("required_disclosures",self.required_disclosures),
        ):
            _strings(name,value)
        expected="CE-ACM-"+sha256_bytes(canonical_json(self.canonical_payload()))
        if self.manifest_id!=expected:
            raise ManifestInvalid("manifest_identity_digest_mismatch")

    @classmethod
    def from_mapping(cls, value: Mapping[str,Any])->"AllowedClaimManifest":
        required=(
            "manifest_version","manifest_id","claim_id","canon_version","canon_registry_digest",
            "canon_rule_id","signal_reference","allowed_subject","allowed_scope","epistemic_layer",
            "certainty_ceiling","allowed_modality","allowed_tense","forbidden_domains",
            "forbidden_claim_types","required_evidence_refs","allowed_numeric_refs","required_disclosures",
        )
        if not isinstance(value,Mapping): raise ManifestInvalid("manifest_not_object")
        missing=[k for k in required if k not in value]
        extra=[k for k in value if k not in required]
        if missing: raise ManifestInvalid("manifest_missing_fields:"+",".join(missing))
        if extra: raise ManifestInvalid("manifest_unknown_fields:"+",".join(sorted(extra)))
        interp=CanonApprovedInterpretation.from_mapping(value)
        return cls(
            manifest_version=value["manifest_version"], manifest_id=value["manifest_id"],
            claim_id=interp.claim_id, canon_version=value["canon_version"],
            canon_registry_digest=value["canon_registry_digest"], canon_rule_id=value["canon_rule_id"],
            signal_reference=value["signal_reference"], allowed_subject=interp.allowed_subject,
            allowed_scope=interp.allowed_scope, epistemic_layer=interp.epistemic_layer,
            certainty_ceiling=interp.certainty_ceiling, allowed_modality=interp.allowed_modality,
            allowed_tense=interp.allowed_tense, forbidden_domains=interp.forbidden_domains,
            forbidden_claim_types=interp.forbidden_claim_types, required_evidence_refs=interp.required_evidence_refs,
            allowed_numeric_refs=interp.allowed_numeric_refs, required_disclosures=interp.required_disclosures,
        )

def build_allowed_claim_manifest(
    registry: CanonRegistry, *, rule_id: str, signal_reference: str,
    manifest_version: str="CE-ALLOWED-CLAIM-MANIFEST-V1",
)->AllowedClaimManifest:
    if not isinstance(registry,CanonRegistry): raise ManifestInvalid("manifest_canon_registry_required")
    rule=registry.get_rule(rule_id)
    interp=CanonApprovedInterpretation.from_rule(rule)
    candidate=AllowedClaimManifest(
        manifest_version=manifest_version, manifest_id="",
        claim_id=interp.claim_id, canon_version=rule.canon_version,
        canon_registry_digest=registry.digest(), canon_rule_id=rule.rule_id,
        signal_reference=signal_reference, allowed_subject=interp.allowed_subject,
        allowed_scope=interp.allowed_scope, epistemic_layer=interp.epistemic_layer,
        certainty_ceiling=interp.certainty_ceiling, allowed_modality=interp.allowed_modality,
        allowed_tense=interp.allowed_tense, forbidden_domains=interp.forbidden_domains,
        forbidden_claim_types=interp.forbidden_claim_types, required_evidence_refs=interp.required_evidence_refs,
        allowed_numeric_refs=interp.allowed_numeric_refs, required_disclosures=interp.required_disclosures,
    )
    manifest_id="CE-ACM-"+sha256_bytes(canonical_json(candidate.canonical_payload()))
    return AllowedClaimManifest(**{**candidate.__dict__,"manifest_id":manifest_id})
