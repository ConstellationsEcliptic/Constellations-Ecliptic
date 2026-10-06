from __future__ import annotations

import inspect
import unittest

from ce.claim.authorization import evaluate_claim_release
from ce.output.validation import validate_claim_output


class PR14VerifierAuthorityAcceptanceTests(unittest.TestCase):
    def test_output_validator_must_not_accept_caller_supplied_semantic_callback(self) -> None:
        self.assertNotIn(
            "semantic_conformance",
            inspect.signature(validate_claim_output).parameters,
            "semantic verification must be CE-owned or fail closed; caller predicates cannot be authority",
        )

    def test_release_evaluator_must_not_accept_caller_supplied_semantic_callback(self) -> None:
        self.assertNotIn(
            "semantic_conformance",
            inspect.signature(evaluate_claim_release).parameters,
            "release authorization must not depend on a caller-supplied semantic predicate",
        )


if __name__ == "__main__":
    unittest.main()
