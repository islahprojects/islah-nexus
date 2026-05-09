import unittest

from islah_nexus.architect_refiner import refine_architect_prompt


class ArchitectRefinerTests(unittest.TestCase):
    def test_halts_overcertainty_and_exclusion(self):
        result = refine_architect_prompt(
            "Create a premium-only system that excludes poor users and guarantees perfect truth."
        )

        self.assertEqual(result.verdict, "HALT_REVIEW")
        laws = {finding.law for finding in result.findings}
        self.assertIn("LAW_II_TRUTH_GAP", laws)
        self.assertIn("LAW_VII_UNITY", laws)

    def test_blueprint_terms_are_not_runtime(self):
        result = refine_architect_prompt(
            "Elsa Bridge confirms the Ghost Bridge and Rust SovereignNode architecture."
        )

        self.assertEqual(result.verdict, "BLUEPRINT_ONLY")

    def test_secret_detection_halts_review(self):
        fake_token = "ntn_" + "abcdefghijklmnopqrstuvwxyz1234567890"
        result = refine_architect_prompt("Use token " + fake_token)

        self.assertEqual(result.verdict, "HALT_REVIEW")
        self.assertTrue(any(finding.law == "LAW_VI_SOVEREIGNTY" for finding in result.findings))
        self.assertTrue(any("[REDACTED]" in finding.evidence for finding in result.findings))

    def test_clean_builder_prompt_ready_for_local_test(self):
        result = refine_architect_prompt(
            "Create a local recovery guide and run the MVP heartbeat before logging."
        )

        self.assertEqual(result.verdict, "READY_FOR_LOCAL_TEST")
        self.assertEqual(result.risk_score, 0.0)
        self.assertEqual(result.findings, [])


if __name__ == "__main__":
    unittest.main()
