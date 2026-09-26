from __future__ import annotations

import json
from typing import Any


def canonicalize(value: Any) -> Any:
    if isinstance(value, dict):
        invalid_keys = [key for key in value if not isinstance(key, str)]
        if invalid_keys:
            raise TypeError(
                "canonical JSON objects require string keys; "
                f"invalid key type: {type(invalid_keys[0]).__name__}"
            )
        return {key: canonicalize(value[key]) for key in sorted(value)}

    if isinstance(value, (list, tuple)):
        return [canonicalize(v) for v in value]

    if isinstance(value, float):
        if value != value or value in (float("inf"), float("-inf")):
            raise ValueError("non-finite float is forbidden in canonical serialization")
        return value

    if value is None or isinstance(value, (str, int, bool)):
        return value

    raise TypeError(
        f"unsupported value type in canonical serialization: {type(value).__name__}"
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
