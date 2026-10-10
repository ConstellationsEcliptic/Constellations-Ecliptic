from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

from ce.foundation.hashing import sha256_bytes
from ce.foundation.serialization import canonical_json

CANON_RULE_REQUIRED_FIELDS = (
    "rule_id","canon_version","tradition_track","source_reference","source_scope",
    "condition","allowed_interpretation","forbidden_extrapolation",
    "confidence_language_boundary","applicability_scope",
)

class CanonRegistryNotEstablished(RuntimeError):
    pass

class CanonRuleInvalid(ValueError):
    pass

class CanonRuleNotFound(CanonRegistryNotEstablished):
    pass

def _string_sequence(value: Any, field: str) -> tuple[str, ...]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        raise CanonRuleInvalid(f"canon_rule_invalid:{field}")
    result = tuple(value)
    if any(not isinstance(item, str) or not item.strip() for item in result):
        raise CanonRuleInvalid(f"canon_rule_invalid:{field}")
    return result

@dataclass(frozen=True)
class CanonRule:
    rule_id: str
    canon_version: str
    tradition_track: str
    source_reference: str
    source_scope: str
    condition: Mapping[str, Any]
    allowed_interpretation: Mapping[str, Any]
    forbidden_extrapolation: tuple[str, ...]
    confidence_language_boundary: Mapping[str, Any]
    applicability_scope: tuple[str, ...]

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "CanonRule":
        if not isinstance(value, Mapping):
            raise CanonRuleInvalid("canon_rule_not_object")
        required = set(CANON_RULE_REQUIRED_FIELDS)
        keys = set(value)
        missing = required - keys
        extra = keys - required
        if missing:
            raise CanonRuleInvalid("canon_rule_missing_fields:" + ",".join(sorted(missing)))
        if extra:
            raise CanonRuleInvalid("canon_rule_unknown_fields:" + ",".join(sorted(extra)))
        for key in ("rule_id","canon_version","tradition_track","source_reference","source_scope"):
            if not isinstance(value[key], str) or not value[key].strip():
                raise CanonRuleInvalid(f"canon_rule_invalid:{key}")
        for key in ("condition","allowed_interpretation","confidence_language_boundary"):
            if not isinstance(value[key], Mapping):
                raise CanonRuleInvalid(f"canon_rule_invalid:{key}")
        return cls(
            rule_id=value["rule_id"], canon_version=value["canon_version"],
            tradition_track=value["tradition_track"], source_reference=value["source_reference"],
            source_scope=value["source_scope"], condition=dict(value["condition"]),
            allowed_interpretation=dict(value["allowed_interpretation"]),
            forbidden_extrapolation=_string_sequence(value["forbidden_extrapolation"], "forbidden_extrapolation"),
            confidence_language_boundary=dict(value["confidence_language_boundary"]),
            applicability_scope=_string_sequence(value["applicability_scope"], "applicability_scope"),
        )

    def canonical_payload(self) -> dict[str, Any]:
        return {
            "rule_id": self.rule_id,"canon_version": self.canon_version,
            "tradition_track": self.tradition_track,"source_reference": self.source_reference,
            "source_scope": self.source_scope,"condition": dict(self.condition),
            "allowed_interpretation": dict(self.allowed_interpretation),
            "forbidden_extrapolation": list(self.forbidden_extrapolation),
            "confidence_language_boundary": dict(self.confidence_language_boundary),
            "applicability_scope": list(self.applicability_scope),
        }

    def digest(self) -> str:
        return sha256_bytes(canonical_json(self.canonical_payload()))

@dataclass(frozen=True)
class CanonRegistry:
    registry_version: str
    rules: tuple[CanonRule, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.registry_version, str) or not self.registry_version.strip():
            raise CanonRuleInvalid("canon_registry_version_invalid")
        if not isinstance(self.rules, tuple):
            raise CanonRuleInvalid("canon_registry_rules_invalid")
        ids=[]
        for rule in self.rules:
            if not isinstance(rule, CanonRule):
                raise CanonRuleInvalid("canon_registry_rule_type_invalid")
            CanonRule.from_mapping(rule.canonical_payload())
            ids.append(rule.rule_id)
        if len(ids)!=len(set(ids)):
            raise CanonRuleInvalid("canon_registry_duplicate_rule_id")

    @classmethod
    def from_records(cls, registry_version: str, records: Sequence[Mapping[str, Any]]) -> "CanonRegistry":
        if not isinstance(records, Sequence) or isinstance(records, (str, bytes, bytearray)):
            raise CanonRuleInvalid("canon_registry_rules_invalid")
        return cls(registry_version=registry_version, rules=tuple(CanonRule.from_mapping(item) for item in records))

    @classmethod
    def empty(cls, registry_version: str) -> "CanonRegistry":
        return cls.from_records(registry_version, ())

    def canonical_payload(self) -> dict[str, Any]:
        return {"registry_version": self.registry_version, "rules": [rule.canonical_payload() for rule in self.rules]}

    def digest(self) -> str:
        return sha256_bytes(canonical_json(self.canonical_payload()))

    def get_rule(self, rule_id: str) -> CanonRule:
        if not self.rules:
            raise CanonRegistryNotEstablished("canon_rule_registry_unpopulated")
        for rule in self.rules:
            if rule.rule_id == rule_id:
                return rule
        raise CanonRuleNotFound(f"canon_rule_not_found:{rule_id}")

def load_registry_json(path: str | Path) -> CanonRegistry:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        payload=json.load(handle)
    if not isinstance(payload, Mapping) or set(payload)!={"registry_version","rules"}:
        raise CanonRuleInvalid("canon_registry_schema_mismatch")
    return CanonRegistry.from_records(payload["registry_version"], payload["rules"])

def get_rule(rule_id: str) -> None:
    raise CanonRegistryNotEstablished(f"Canon rule registry is not materialized: {rule_id}")
