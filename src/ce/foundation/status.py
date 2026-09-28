from __future__ import annotations

from enum import Enum


class CalculationStatus(str, Enum):
    VALID = "VALID"
    KNOWN_UNAVAILABLE = "KNOWN_UNAVAILABLE"
    CALCULATION_FAILURE = "CALCULATION_FAILURE"
    INPUT_UNSUPPORTED = "INPUT_UNSUPPORTED"
    NATAL_EVIDENCE_VARIABLE = "NATAL_EVIDENCE_VARIABLE"
    NOT_IMPLEMENTED = "NOT_IMPLEMENTED"
    NON_AUTHORIZED = "NON_AUTHORIZED"
    INVALID_INPUT = "INVALID_INPUT"


CALENDAR_POLICY_GREGORIAN_ONLY = "CE-V1-CALENDAR-GREGORIAN-ONLY"


class RuntimeAuthority(str, Enum):
    AUTHORIZED = "AUTHORIZED"
    NON_AUTHORIZED = "NON_AUTHORIZED"


class NatalBirthState(str, Enum):
    """V1 Personal Sky natal input state.

    CE V1 does not accept an exact user-supplied birth time.
    """

    ZERO_BIRTH_TIME = "ZERO_BIRTH_TIME"
    INVALID = "INVALID"


class ObservationTimeState(str, Enum):
    """Time-state for explicit observation/evaluation calculations."""

    EXACT = "EXACT"
    INVALID = "INVALID"


class ScenarioState(str, Enum):
    STABLE = "STABLE"
    VARIABLE = "VARIABLE"
    POSSIBLE = "POSSIBLE"
    ROBUST = "ROBUST"
    MIXED = "MIXED"
    NONE = "NONE"
