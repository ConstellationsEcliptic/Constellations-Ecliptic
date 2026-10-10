from __future__ import annotations

from collections.abc import Mapping, Sequence
import re
from typing import Any

from ce.foundation.hashing import sha256_bytes
from ce.foundation.serialization import canonical_json


HOST_NATIVE_ENVIRONMENT_SCHEMA_VERSION = "CE-V1-HOST-NATIVE-ENV-R1"
HOST_NATIVE_ENVIRONMENT_KIND = "HOST_NATIVE"
_SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")


class HostRuntimeEnvironmentError(ValueError):
    """Host-native runtime identity manifest is malformed or inconsistent."""


def _require_text(value: Any, field: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise HostRuntimeEnvironmentError(f"invalid:{field}")


def _require_sha(value: Any, field: str) -> None:
    if not isinstance(value, str) or not _SHA256_RE.fullmatch(value):
        raise HostRuntimeEnvironmentError(f"invalid:{field}")


def _require_nonnegative_int(value: Any, field: str) -> None:
    if type(value) is not int or value < 0:
        raise HostRuntimeEnvironmentError(f"invalid:{field}")


def validate_host_native_environment_manifest(manifest: Mapping[str, Any]) -> None:
    if not isinstance(manifest, Mapping):
        raise HostRuntimeEnvironmentError("manifest_mapping_required")
    _require_text(manifest.get("schema_version"), "schema_version")
    if manifest.get("schema_version") != HOST_NATIVE_ENVIRONMENT_SCHEMA_VERSION:
        raise HostRuntimeEnvironmentError("schema_version_mismatch")
    if manifest.get("kind") != HOST_NATIVE_ENVIRONMENT_KIND:
        raise HostRuntimeEnvironmentError("kind_mismatch")

    os_info = manifest.get("os")
    if not isinstance(os_info, Mapping):
        raise HostRuntimeEnvironmentError("os_mapping_required")
    for key in ("system", "release", "version", "machine"):
        _require_text(os_info.get(key), f"os.{key}")

    python_info = manifest.get("python")
    if not isinstance(python_info, Mapping):
        raise HostRuntimeEnvironmentError("python_mapping_required")
    for key in ("implementation", "version", "platform"):
        _require_text(python_info.get(key), f"python.{key}")
    _require_sha(python_info.get("executable_sha256"), "python.executable_sha256")
    _require_nonnegative_int(python_info.get("executable_size_bytes"), "python.executable_size_bytes")

    components = manifest.get("components")
    if not isinstance(components, Sequence) or isinstance(components, (str, bytes, bytearray)):
        raise HostRuntimeEnvironmentError("components_sequence_required")
    names: list[str] = []
    for index, item in enumerate(components):
        if not isinstance(item, Mapping):
            raise HostRuntimeEnvironmentError(f"invalid:components[{index}]")
        _require_text(item.get("name"), f"components[{index}].name")
        _require_sha(item.get("sha256"), f"components[{index}].sha256")
        _require_nonnegative_int(item.get("size_bytes"), f"components[{index}].size_bytes")
        names.append(str(item["name"]))
    if len(names) != len(set(names)):
        raise HostRuntimeEnvironmentError("duplicate_component_name")
    if names != sorted(names):
        raise HostRuntimeEnvironmentError("components_not_sorted")


def host_native_environment_digest(manifest: Mapping[str, Any]) -> str:
    validate_host_native_environment_manifest(manifest)
    return sha256_bytes(canonical_json(manifest))
