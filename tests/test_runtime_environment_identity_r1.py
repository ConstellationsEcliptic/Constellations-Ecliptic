from __future__ import annotations

import tempfile
from pathlib import Path
import unittest

from ce.runtime.environment_identity import (
    HOST_NATIVE_ENVIRONMENT_KIND,
    HOST_NATIVE_ENVIRONMENT_SCHEMA_VERSION,
    HostRuntimeEnvironmentError,
    host_native_environment_digest,
)
from ce.foundation.hashing import sha256_file


class RuntimeEnvironmentIdentityR1Tests(unittest.TestCase):
    def _manifest(self, first: bytes = b"abc", second: bytes = b"def") -> dict:
        return {
            "schema_version": HOST_NATIVE_ENVIRONMENT_SCHEMA_VERSION,
            "kind": HOST_NATIVE_ENVIRONMENT_KIND,
            "os": {
                "system": "Windows",
                "release": "11",
                "version": "10.0.26200",
                "machine": "AMD64",
            },
            "python": {
                "implementation": "CPython",
                "version": "3.13.15",
                "platform": "Windows-11-10.0.26200-SP0",
                "executable_sha256": "1" * 64,
                "executable_size_bytes": 100,
            },
            "components": [
                {"name": "cl", "size_bytes": len(first), "sha256": __import__("hashlib").sha256(first).hexdigest()},
                {"name": "link", "size_bytes": len(second), "sha256": __import__("hashlib").sha256(second).hexdigest()},
            ],
        }

    def test_digest_is_content_based(self) -> None:
        self.assertEqual(host_native_environment_digest(self._manifest()), host_native_environment_digest(self._manifest()))

    def test_component_order_is_identity_normalized_by_contract(self) -> None:
        manifest = self._manifest()
        reversed_components = {**manifest, "components": list(reversed(manifest["components"]))}
        with self.assertRaisesRegex(HostRuntimeEnvironmentError, "components_not_sorted"):
            host_native_environment_digest(reversed_components)

    def test_component_mutation_changes_digest(self) -> None:
        left = self._manifest()
        right = self._manifest(first=b"abcd")
        self.assertNotEqual(host_native_environment_digest(left), host_native_environment_digest(right))

    def test_environment_digest_without_kind_is_rejected(self) -> None:
        from ce.foundation.identity import RuntimeIdentity
        identity = RuntimeIdentity(
            "CE-CALC-V1-EP-001", 4,
            None, None, None, None, None, None,
            runtime_environment_digest="f" * 64,
        )
        self.assertIn("missing:runtime_environment_kind", identity.validate_shape())

    def test_duplicate_component_name_fails_closed(self) -> None:
        manifest = self._manifest()
        manifest["components"] = manifest["components"] + [dict(manifest["components"][0])]
        with self.assertRaisesRegex(HostRuntimeEnvironmentError, "duplicate_component_name"):
            host_native_environment_digest(manifest)


if __name__ == "__main__":
    unittest.main()
