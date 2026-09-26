from __future__ import annotations

from enum import Enum


class CalculationStatus(str, Enum):
    VALID = "VALID"
    NOT_IMPLEMENTED = "NOT_IMPLEMENTED"
    NON_AUTHORIZED = "NON_AUTHORIZED"
    INVALID_INPUT = "INVALID_INPUT"
    CALCULATION_FAILURE = "CALCULATION_FAILURE"


class RuntimeAuthority(str, Enum):
    AUTHORIZED = "AUTHORIZED"
    NON_AUTHORIZED = "NON_AUTHORIZED"


class BirthTimeState(str, Enum):
    EXACT = "EXACT"
    ZERO_BIRTH_TIME = "ZERO_BIRTH_TIME"


class ScenarioState(str, Enum):
    STABLE = "STABLE"
    VARIABLE = "VARIABLE"
    POSSIBLE = "POSSIBLE"
    ROBUST = "ROBUST"
    MIXED = "MIXED"
    NONE = "NONE"
