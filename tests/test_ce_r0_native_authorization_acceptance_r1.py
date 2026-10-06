from __future__ import annotations

import inspect
import unittest

from ce.ephemeris.native_runtime import NativeSwissEphemerisAdapter


class CER0NativeAuthorizationAcceptanceTests(unittest.TestCase):
    def test_native_adapter_must_not_accept_boolean_authorization(self) -> None:
        params = inspect.signature(NativeSwissEphemerisAdapter.__init__).parameters
        self.assertNotIn(
            "runtime_authorized",
            params,
            "native activation must consume a verified authority receipt, not a caller boolean",
        )


if __name__ == "__main__":
    unittest.main()
