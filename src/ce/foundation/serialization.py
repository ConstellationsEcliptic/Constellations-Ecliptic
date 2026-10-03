from __future__ import annotations

import json
import math
from collections.abc import Mapping, Sequence
from typing import Any


def canonicalize(value: Any) -> Any:
    """Return the only JSON value domain accepted by CE canonical hashing.

    Mapping keys are part of the identity domain and therefore must already be
    strings; coercion would make distinct inputs collide.
    """
    if isinstance(value, Mapping):
        for key in value:
            if not isinstance(key, str):
                raise TypeError(
                    "canonical JSON objects require string keys; "
                    f"invalid key type: {type(key).__name__}"
                )
        return {key: canonicalize(value[key]) for key in sorted(value)}

    if isinstance(value, (list, tuple)):
        return [canonicalize(item) for item in value]

    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("non-finite float is forbidden in canonical serialization")
        return value

    if value is None or isinstance(value, (str, int, bool)):
        return value

    raise TypeError(
        "unsupported value type in canonical serialization: "
        f"{type(value).__name__}"
    )


def canonical_json(value: Any) -> bytes:
    normalized = canonicalize(value)
    return json.dumps(
        normalized,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
        allow_nan=False,
    ).encode("utf-8")
