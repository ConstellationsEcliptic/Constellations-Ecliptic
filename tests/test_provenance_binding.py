from __future__ import annotations

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from ce.calculation.contracts import (
    CalculationResult,
    ObjectState,
    _validate_result_provenance,
)
from ce.foundation.identity import RuntimeIdentity
from ce.foundation.status import CalculationStatus, ScenarioState


class ProvenanceBindingTests(unittest.TestCase):
    def _identity(self) -> RuntimeIdentity:
        return RuntimeIdentity(
            "CE-CALC-V1-EP-001",
            2,
            "a" * 40,
            "b" * 64,
            "sha256:" + "c" * 64,
            "d" * 64,
            "e" * 64,
            "f" * 64,
        )

    def _provenance(self) -> dict[str, str]:
        identity = self._identity()
        return {
            "source_commit": identity.source_commit,
            "source_tree_sha256_v2": identity.source_tree_sha256_v2,
            "dependency_lock_digest": identity.dependency_lock_digest,
            "timezone_bundle_digest": identity.timezone_bundle_digest,
            "ephemeris_bundle_digest": identity.ephemeris_bundle_digest,
            "runtime_image_digest": identity.runtime_image_digest,
            "calculation_version": "0.1.0",
        }

    def _nonvalid_result(self, provenance) -> CalculationResult:
        return CalculationResult(
            "R",
            CalculationStatus.NON_AUTHORIZED,
            "CE-CALC-V1-EP-001",
            ScenarioState.NONE,
            None,
            provenance=provenance,
        )

    def test_valid_provenance_requires_runtime_identity_binding(self) -> None:
        errors = _validate_result_provenance(self._provenance(), None)
        self.assertIn("provenance:binding_required", errors)

    def test_valid_provenance_accepts_exact_runtime_identity_binding(self) -> None:
        errors = _validate_result_provenance(self._provenance(), self._identity())
        self.assertEqual(errors, ())

    def test_valid_provenance_rejects_well_formed_unrelated_identity(self) -> None:
        for field_name, alternate in (
            ("source_commit", "9" * 40),
            ("source_tree_sha256_v2", "9" * 64),
            ("dependency_lock_digest", "8" * 64),
            ("timezone_bundle_digest", "7" * 64),
            ("ephemeris_bundle_digest", "6" * 64),
            ("runtime_image_digest", "sha256:" + "5" * 64),
        ):
            provenance = self._provenance()
            provenance[field_name] = alternate
            errors = _validate_result_provenance(provenance, self._identity())
            self.assertIn(f"provenance:mismatch:{field_name}", errors)

    def test_valid_result_rejects_nested_extra_provenance(self) -> None:
        provenance = self._provenance()
        provenance["trace"] = {"nested": "value"}
        errors = _validate_result_provenance(provenance, self._identity())
        self.assertIn("provenance:extra:trace:scalar_required", errors)

    def test_nonvalid_result_rejects_authority_identity_provenance(self) -> None:
        with self.assertRaisesRegex(ValueError, "provenance:nonvalid_forbidden:source_commit"):
            self._nonvalid_result({"source_commit": "a" * 40})

    def test_nonvalid_result_rejects_authorized_runtime_metadata(self) -> None:
        with self.assertRaisesRegex(
            ValueError, "provenance:nonvalid_runtime_authority_must_be_non_authorized"
        ):
            self._nonvalid_result({"runtime_authority": "AUTHORIZED"})

    def test_nonvalid_result_accepts_non_authorized_runtime_metadata(self) -> None:
        result = self._nonvalid_result({"runtime_authority": "NON_AUTHORIZED"})
        self.assertEqual(result.validate(), ())


if __name__ == "__main__":
    unittest.main()
