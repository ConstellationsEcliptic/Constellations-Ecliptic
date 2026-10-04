from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
import math
import re
from typing import Any

from ce.foundation.hashing import sha256_bytes
from ce.foundation.identity import CANONICAL_EXECUTION_PROFILE_ID, CANONICAL_EXECUTION_PROFILE_REVISION
from ce.foundation.serialization import canonical_json


_COMMIT_RE = re.compile(r"^[0-9a-fA-F]{40}$")
_SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")
_RUNTIME_IMAGE_RE = re.compile(r"^sha256:[0-9a-fA-F]{64}$")
_UTC_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?Z$")


class ReproducibilityCaptureError(ValueError):
    """A reproducibility capture is incomplete or internally inconsistent."""


@dataclass(frozen=True)
class RuntimeCapture:
    capture_id: str
    captured_at_utc: str
    platform: str
    python_version: str
    execution_profile_id: str
    execution_profile_revision: int
    source_commit: str
    source_tree_sha256_v2: str
    dependency_lock_digest: str
    runtime_image_digest: str
    timezone_bundle_digest: str
    ephemeris_bundle_digest: str
    native_library_sha256: str
    native_runtime_version: str
    swiss_source_commit: str
    calling_convention: str
    fixtures: tuple[dict[str, Any], ...]

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []
        if not isinstance(self.capture_id, str) or not self.capture_id.strip():
            errors.append("invalid:capture_id")
        if not isinstance(self.captured_at_utc, str) or not _UTC_RE.fullmatch(self.captured_at_utc):
            errors.append("invalid:captured_at_utc")
        for name, value in (
            ("platform", self.platform),
            ("python_version", self.python_version),
            ("native_runtime_version", self.native_runtime_version),
        ):
            if not isinstance(value, str) or not value.strip():
                errors.append(f"invalid:{name}")
        if self.execution_profile_id != CANONICAL_EXECUTION_PROFILE_ID:
            errors.append("invalid:execution_profile_id")
        if self.execution_profile_revision != CANONICAL_EXECUTION_PROFILE_REVISION:
            errors.append("invalid:execution_profile_revision")
        for name, value in (
            ("source_commit", self.source_commit),
            ("swiss_source_commit", self.swiss_source_commit),
        ):
            if not isinstance(value, str) or not _COMMIT_RE.fullmatch(value):
                errors.append(f"invalid:{name}")
        for name, value in (
            ("source_tree_sha256_v2", self.source_tree_sha256_v2),
            ("dependency_lock_digest", self.dependency_lock_digest),
            ("timezone_bundle_digest", self.timezone_bundle_digest),
            ("ephemeris_bundle_digest", self.ephemeris_bundle_digest),
            ("native_library_sha256", self.native_library_sha256),
        ):
            if not isinstance(value, str) or not _SHA256_RE.fullmatch(value):
                errors.append(f"invalid:{name}")
        if not isinstance(self.runtime_image_digest, str) or not _RUNTIME_IMAGE_RE.fullmatch(self.runtime_image_digest):
            errors.append("invalid:runtime_image_digest")
        if self.calling_convention not in {"__cdecl", "__stdcall"}:
            errors.append("invalid:calling_convention")
        if not isinstance(self.fixtures, (tuple, list)):
            errors.append("invalid:fixtures:sequence_required")
        else:
            for index, fixture in enumerate(self.fixtures):
                if not isinstance(fixture, Mapping):
                    errors.append(f"invalid:fixtures[{index}]:mapping_required")
                    continue
                fixture_id = fixture.get("fixture_id")
                if not isinstance(fixture_id, str) or not fixture_id.strip():
                    errors.append(f"invalid:fixtures[{index}]:fixture_id")
                if "records" not in fixture or not isinstance(fixture.get("records"), (Mapping, list, tuple)):
                    errors.append(f"invalid:fixtures[{index}]:records")
                errors.extend(_domain_errors(fixture, f"fixtures[{index}]"))
        return tuple(errors)

    def __post_init__(self) -> None:
        errors = self.validate()
        if errors:
            raise ReproducibilityCaptureError(";".join(errors))

    def canonical_bytes(self) -> bytes:
        payload = {
            "capture_id": self.capture_id,
            "captured_at_utc": self.captured_at_utc,
            "platform": self.platform,
            "python_version": self.python_version,
            "execution_profile_id": self.execution_profile_id,
            "execution_profile_revision": self.execution_profile_revision,
            "source_commit": self.source_commit,
            "source_tree_sha256_v2": self.source_tree_sha256_v2,
            "dependency_lock_digest": self.dependency_lock_digest,
            "runtime_image_digest": self.runtime_image_digest,
            "timezone_bundle_digest": self.timezone_bundle_digest,
            "ephemeris_bundle_digest": self.ephemeris_bundle_digest,
            "native_library_sha256": self.native_library_sha256,
            "native_runtime_version": self.native_runtime_version,
            "swiss_source_commit": self.swiss_source_commit,
            "calling_convention": self.calling_convention,
            "fixtures": self.fixtures,
        }
        return canonical_json(payload)

    def content_sha256(self) -> str:
        return sha256_bytes(self.canonical_bytes())


def _domain_errors(value: Any, path: str) -> tuple[str, ...]:
    if isinstance(value, Mapping):
        errors: list[str] = []
        for key, item in value.items():
            if not isinstance(key, str):
                errors.append(f"invalid:{path}:mapping_key_string_required")
                continue
            errors.extend(_domain_errors(item, f"{path}.{key}"))
        return tuple(errors)
    if isinstance(value, (list, tuple)):
        errors: list[str] = []
        for index, item in enumerate(value):
            errors.extend(_domain_errors(item, f"{path}[{index}]"))
        return tuple(errors)
    if value is None or isinstance(value, (str, int, bool)):
        return ()
    if isinstance(value, float):
        return () if math.isfinite(value) else (f"invalid:{path}:finite_number_required",)
    return (f"invalid:{path}:canonical_json_value_required",)


def _compare_values(
    left: Any,
    right: Any,
    *,
    path: str,
    numeric_tolerances: Mapping[str, float],
) -> list[str]:
    if isinstance(left, Mapping) and isinstance(right, Mapping):
        errors: list[str] = []
        if set(left) != set(right):
            errors.append(f"{path}:keys_mismatch")
            return errors
        for key in sorted(left):
            errors.extend(_compare_values(
                left[key],
                right[key],
                path=f"{path}.{key}",
                numeric_tolerances=numeric_tolerances,
            ))
        return errors
    if isinstance(left, (list, tuple)) and isinstance(right, (list, tuple)):
        errors = []
        if len(left) != len(right):
            return [f"{path}:length_mismatch"]
        for index, (a, b) in enumerate(zip(left, right)):
            errors.extend(_compare_values(
                a,
                b,
                path=f"{path}[{index}]",
                numeric_tolerances=numeric_tolerances,
            ))
        return errors
    if type(left) in (int, float) and type(right) in (int, float) and not isinstance(left, bool) and not isinstance(right, bool):
        if not math.isfinite(float(left)) or not math.isfinite(float(right)):
            return [f"{path}:nonfinite_numeric"]
        field = path.rsplit(".", 1)[-1]
        tolerance = numeric_tolerances.get(field)
        if tolerance is None:
            return [] if left == right else [f"{path}:numeric_mismatch"]
        if not isinstance(tolerance, (int, float)) or isinstance(tolerance, bool) or not math.isfinite(float(tolerance)) or float(tolerance) < 0.0:
            return [f"{path}:invalid_tolerance"]
        return [] if abs(float(left) - float(right)) <= float(tolerance) else [f"{path}:numeric_mismatch"]
    return [] if left == right and type(left) is type(right) else [f"{path}:value_mismatch"]


def compare_capture_outputs(
    left: RuntimeCapture,
    right: RuntimeCapture,
    *,
    numeric_tolerances: Mapping[str, float] | None = None,
) -> tuple[str, ...]:
    """Compare two captures without rounding or inventing expected astronomy."""

    numeric_tolerances = numeric_tolerances or {}
    errors: list[str] = []

    identity_fields = (
        "execution_profile_id",
        "execution_profile_revision",
        "source_commit",
        "source_tree_sha256_v2",
        "dependency_lock_digest",
        "runtime_image_digest",
        "timezone_bundle_digest",
        "ephemeris_bundle_digest",
        "native_library_sha256",
        "native_runtime_version",
        "swiss_source_commit",
        "calling_convention",
    )
    for field in identity_fields:
        if getattr(left, field) != getattr(right, field):
            errors.append(f"identity_mismatch:{field}")

    left_by_id = {str(item["fixture_id"]): item for item in left.fixtures}
    right_by_id = {str(item["fixture_id"]): item for item in right.fixtures}
    if set(left_by_id) != set(right_by_id):
        errors.append("fixture_set_mismatch")
        return tuple(errors)

    for fixture_id in sorted(left_by_id):
        errors.extend(
            _compare_values(
                left_by_id[fixture_id]["records"],
                right_by_id[fixture_id]["records"],
                path=f"fixtures[{fixture_id}].records",
                numeric_tolerances=numeric_tolerances,
            )
        )
    return tuple(dict.fromkeys(errors))
