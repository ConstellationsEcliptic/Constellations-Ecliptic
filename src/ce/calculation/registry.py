from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any


class RegistryValidationError(ValueError):
    """Registry data violates the current CE V1 contract."""


EXPECTED_OBJECT_COUNT = 13
EXPECTED_ASPECTS = {
    "CONJUNCTION": 0.0,
    "SEXTILE": 60.0,
    "SQUARE": 90.0,
    "TRINE": 120.0,
    "OPPOSITION": 180.0,
}
REQUIRED_ORB_PROFILES = {"A", "B"}


def validate_object_registry(payload: Mapping[str, Any]) -> None:
    objects = payload.get("objects")
    if not isinstance(objects, Sequence) or isinstance(objects, (str, bytes)):
        raise RegistryValidationError("objects_sequence_required")
    if len(objects) != EXPECTED_OBJECT_COUNT:
        raise RegistryValidationError("object_count_mismatch")
    ids: set[str] = set()
    swiss_ids: set[int] = set()
    for item in objects:
        if not isinstance(item, Mapping):
            raise RegistryValidationError("object_entry_mapping_required")
        object_id = item.get("object_id")
        swiss_id = item.get("swiss_object_id")
        profile = item.get("object_profile")
        if not isinstance(object_id, str) or not object_id.strip():
            raise RegistryValidationError("object_id_invalid")
        if object_id in ids:
            raise RegistryValidationError("duplicate_object_id")
        ids.add(object_id)
        if type(swiss_id) is not int or swiss_id < 0:
            raise RegistryValidationError("swiss_object_id_invalid")
        if swiss_id in swiss_ids:
            raise RegistryValidationError("duplicate_swiss_object_id")
        swiss_ids.add(swiss_id)
        if profile not in REQUIRED_ORB_PROFILES:
            raise RegistryValidationError("object_profile_invalid")


def validate_aspect_registry(payload: Mapping[str, Any]) -> None:
    aspects = payload.get("aspects")
    if not isinstance(aspects, Sequence) or isinstance(aspects, (str, bytes)):
        raise RegistryValidationError("aspects_sequence_required")
    observed: dict[str, float] = {}
    for item in aspects:
        if not isinstance(item, Mapping):
            raise RegistryValidationError("aspect_entry_mapping_required")
        aspect_id = item.get("aspect_id")
        angle = item.get("angle_deg")
        branches = item.get("branches_deg")
        if not isinstance(aspect_id, str) or not aspect_id:
            raise RegistryValidationError("aspect_id_invalid")
        if type(angle) not in (int, float):
            raise RegistryValidationError("aspect_angle_invalid")
        if not isinstance(branches, Sequence) or isinstance(branches, (str, bytes)):
            raise RegistryValidationError("aspect_branches_invalid")
        if aspect_id in observed:
            raise RegistryValidationError("duplicate_aspect_id")
        observed[aspect_id] = float(angle)
        if not all(type(v) in (int, float) for v in branches):
            raise RegistryValidationError("aspect_branch_value_invalid")
    if observed != EXPECTED_ASPECTS:
        raise RegistryValidationError("aspect_set_mismatch")


def validate_orb_registry(payload: Mapping[str, Any]) -> None:
    profiles = payload.get("profiles")
    if not isinstance(profiles, Mapping) or set(profiles) != REQUIRED_ORB_PROFILES:
        raise RegistryValidationError("orb_profile_set_mismatch")
    for name in REQUIRED_ORB_PROFILES:
        values = profiles[name]
        if not isinstance(values, Mapping):
            raise RegistryValidationError("orb_profile_mapping_required")
        if set(values) != set(EXPECTED_ASPECTS):
            raise RegistryValidationError("orb_aspect_set_mismatch")
        for value in values.values():
            if type(value) not in (int, float) or float(value) <= 0.0:
                raise RegistryValidationError("orb_value_invalid")


def validate_registry_bundle(
    object_registry: Mapping[str, Any],
    aspect_registry: Mapping[str, Any],
    orb_registry: Mapping[str, Any],
) -> None:
    for payload in (object_registry, aspect_registry, orb_registry):
        revision = payload.get("execution_profile_revision")
        profile_id = payload.get("execution_profile_id")
        if profile_id != "CE-CALC-V1-EP-001" or revision != 4:
            raise RegistryValidationError("registry_profile_binding_mismatch")
    validate_object_registry(object_registry)
    validate_aspect_registry(aspect_registry)
    validate_orb_registry(orb_registry)
