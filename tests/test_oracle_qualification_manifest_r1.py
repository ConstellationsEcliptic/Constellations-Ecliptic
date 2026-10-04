from __future__ import annotations

import unittest

from tools.validate_oracle_qualification import EXPECTED_IDS, validate

class OracleQualificationManifestR1Tests(unittest.TestCase):
    def test_current_28_id_binding_manifest_is_valid(self) -> None:
        validate()

    def test_required_id_count_is_exactly_28(self) -> None:
        self.assertEqual(len(EXPECTED_IDS), 28)

if __name__ == "__main__":
    unittest.main()
