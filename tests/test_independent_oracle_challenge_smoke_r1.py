from __future__ import annotations

import unittest

class IndependentOracleChallengeSmokeR1(unittest.TestCase):
    def test_module_is_intentionally_challenge_layer(self) -> None:
        import tests.test_independent_oracle_challenge_r1 as mod
        self.assertIn("does not import CE production geometry", mod.__doc__)
        self.assertTrue(callable(mod.ref_geometry))
        self.assertTrue(callable(mod.ref_wrap180))

if __name__ == "__main__":
    unittest.main()
