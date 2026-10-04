from __future__ import annotations

from collections.abc import Mapping
from typing import Any


class ExecutionProfileValidationError(ValueError):
    """Execution profile violates a current CE V1 semantic invariant."""


CANONICAL_EXECUTION_PROFILE_ID = "CE-CALC-V1-EP-001"
CANONICAL_EXECUTION_PROFILE_REVISION = 4
CANONICAL_CALENDAR_POLICY = "CE-V1-CALENDAR-GREGORIAN-ONLY"
CANONICAL_TZ_VERSION = "2026d"
CANONICAL_DATA_LOCK_ID = "CE-V1-CANONICAL-DATA-2026D-SE-V2.10.3BFINAL"


def validate_execution_profile(profile: Mapping[str, Any]) -> None:
    if not isinstance(profile, Mapping):
        raise ExecutionProfileValidationError("profile_mapping_required")
    if profile.get("status") != "DEVELOPMENT_ONLY_NON_AUTHORITATIVE":
        raise ExecutionProfileValidationError("profile_status_mismatch")

    runtime = profile.get("runtime")
    if not isinstance(runtime, Mapping):
        raise ExecutionProfileValidationError("runtime_missing")
    if runtime.get("language") != "python":
        raise ExecutionProfileValidationError("runtime_language_mismatch")
    if runtime.get("version") != "3.13":
        raise ExecutionProfileValidationError("runtime_version_mismatch")
    if runtime.get("authority") != "development_only":
        raise ExecutionProfileValidationError("runtime_authority_mismatch")

    source = profile.get("source")
    if not isinstance(source, Mapping):
        raise ExecutionProfileValidationError("source_missing")
    for key in ("commit", "source_tree_sha256_v2"):
        if not isinstance(source.get(key), str) or not source.get(key).strip():
            raise ExecutionProfileValidationError(f"source_field_missing:{key}")

    build = profile.get("build")
    if not isinstance(build, Mapping):
        raise ExecutionProfileValidationError("build_missing")
    for key in ("dependency_lock_digest", "runtime_image_digest", "toolchain_identity"):
        if not isinstance(build.get(key), str) or not build.get(key).strip():
            raise ExecutionProfileValidationError(f"build_field_missing:{key}")

    if profile.get("execution_profile_id") != CANONICAL_EXECUTION_PROFILE_ID:
        raise ExecutionProfileValidationError("execution_profile_id_mismatch")
    if profile.get("execution_profile_revision") != CANONICAL_EXECUTION_PROFILE_REVISION:
        raise ExecutionProfileValidationError("execution_profile_revision_mismatch")

    inputs = profile.get("product_input_boundary")
    if not isinstance(inputs, Mapping):
        raise ExecutionProfileValidationError("product_input_boundary_missing")
    expected_inputs = {
        "birth_date": "USED",
        "birth_city": "USED",
        "birth_time_user_input": "NOT_USED",
        "calendar_policy": "GREGORIAN_ONLY",
    }
    for key, expected in expected_inputs.items():
        if inputs.get(key) != expected:
            raise ExecutionProfileValidationError(f"input_boundary_mismatch:{key}")

    if profile.get("natal_engine_state") != "ZERO_BIRTH_TIME":
        raise ExecutionProfileValidationError("natal_engine_state_mismatch")
    if profile.get("observation_time") != "SEPARATE_EXPLICIT_FEATURE_INPUT":
        raise ExecutionProfileValidationError("observation_time_boundary_mismatch")

    calendar = profile.get("calendar")
    if not isinstance(calendar, Mapping):
        raise ExecutionProfileValidationError("calendar_missing")
    if calendar.get("policy_id") != CANONICAL_CALENDAR_POLICY:
        raise ExecutionProfileValidationError("calendar_policy_mismatch")

    timezone = profile.get("timezone")
    if not isinstance(timezone, Mapping) or timezone.get("database") != "IANA":
        raise ExecutionProfileValidationError("timezone_database_mismatch")
    if timezone.get("version") != CANONICAL_TZ_VERSION:
        raise ExecutionProfileValidationError("timezone_version_mismatch")

    if profile.get("execution_profile_version") != "1.3":
        raise ExecutionProfileValidationError("execution_profile_version_mismatch")
    if profile.get("implementation_plan_version") != "1.3.1":
        raise ExecutionProfileValidationError("implementation_plan_version_mismatch")
    if profile.get("technical_contracts_version") != "1.1":
        raise ExecutionProfileValidationError("technical_contracts_version_mismatch")

    ephemeris = profile.get("ephemeris")
    if not isinstance(ephemeris, Mapping):
        raise ExecutionProfileValidationError("ephemeris_missing")
    if ephemeris.get("version") != "2.10.03":
        raise ExecutionProfileValidationError("ephemeris_version_mismatch")
    if ephemeris.get("library") != "Swiss Ephemeris":
        raise ExecutionProfileValidationError("ephemeris_library_mismatch")

    canonical_lock = profile.get("canonical_data_lock")
    if not isinstance(canonical_lock, Mapping):
        raise ExecutionProfileValidationError("canonical_data_lock_missing")
    if canonical_lock.get("id") != CANONICAL_DATA_LOCK_ID:
        raise ExecutionProfileValidationError("canonical_data_lock_id_mismatch")
    if canonical_lock.get("revision") != 4:
        raise ExecutionProfileValidationError("canonical_data_lock_revision_mismatch")
