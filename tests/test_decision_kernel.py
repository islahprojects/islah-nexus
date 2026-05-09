import unittest

from islah_nexus.decision_kernel import DecisionOption, choose_min_expected_error


class DecisionKernelTests(unittest.TestCase):
    def test_choose_lowest_total_risk(self):
        options = [
            DecisionOption(
                name="loud_answer",
                expected_error=0.2,
                harm_risk=0.3,
                falsehood_risk=0.2,
                governance_risk=0.1,
            ),
            DecisionOption(
                name="truthkind_answer",
                expected_error=0.1,
                harm_risk=0.05,
                falsehood_risk=0.05,
                governance_risk=0.05,
            ),
        ]

        chosen = choose_min_expected_error(options)

        self.assertEqual(chosen.name, "truthkind_answer")

    def test_empty_options_fail(self):
        with self.assertRaises(ValueError):
            choose_min_expected_error([])

    def test_negative_risk_fails(self):
        options = [
            DecisionOption(name="bad_input", expected_error=-0.1),
        ]

        with self.assertRaises(ValueError):
            choose_min_expected_error(options)

    def test_tie_breaks_by_name(self):
        options = [
            DecisionOption(name="z_option", expected_error=0.1),
            DecisionOption(name="a_option", expected_error=0.1),
        ]

        chosen = choose_min_expected_error(options)

        self.assertEqual(chosen.name, "a_option")


if __name__ == "__main__":
    unittest.main()
