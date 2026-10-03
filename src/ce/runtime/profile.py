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

    canonical_lock = profile.get("canonical_data_lock")
    if not isinstance(canonical_lock, Mapping):
        raise ExecutionProfileValidationError("canonical_data_lock_missing")
    if canonical_lock.get("id") != CANONICAL_DATA_LOCK_ID:
        raise ExecutionProfileValidationError("canonical_data_lock_id_mismatch")
    if canonical_lock.get("revision") != 4:
        raise ExecutionProfileValidationError("canonical_data_lock_revision_mismatch")
