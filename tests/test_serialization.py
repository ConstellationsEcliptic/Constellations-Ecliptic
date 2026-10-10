from __future__ import annotations

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from ce.foundation.serialization import canonical_json
from ce.foundation.hashing import sha256_bytes


class SerializationTests(unittest.TestCase):
    def test_mapping_order_does_not_change_bytes(self) -> None:
        a = canonical_json({"b": 2, "a": 1})
        b = canonical_json({"a": 1, "b": 2})
        self.assertEqual(a, b)

    def test_bytes_hash_is_deterministic(self) -> None:
        payload = canonical_json({"a": [1, 2, 3]})
        self.assertEqual(sha256_bytes(payload), sha256_bytes(payload))

    def test_non_string_mapping_key_is_rejected(self) -> None:
        with self.assertRaises(TypeError):
            canonical_json({1: "not-a-canonical-object"})

    def test_nonfinite_nested_float_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            canonical_json({"nested": [1.0, float("nan")]})
