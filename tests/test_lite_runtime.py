import unittest

from islah_nexus.lite_runtime import (
    lite_evaluate,
    offline_queue_notice,
    simplify_terms,
    split_sms,
    validate_status_tag,
    validate_truth_gap,
)


class LiteRuntimeTests(unittest.TestCase):
    def test_truth_gap_accepts_valid_values(self):
        sigma, epsilon = validate_truth_gap(0.93, 0.07)
        self.assertEqual(sigma, 0.93)
        self.assertEqual(epsilon, 0.07)

    def test_truth_gap_rejects_overcertainty(self):
        with self.assertRaises(ValueError):
            validate_truth_gap(0.94, 0.06)

    def test_user_veto_halts(self):
        result = lite_evaluate(v_user=0, sigma=0.70, epsilon=0.30)
        self.assertEqual(result.verdict, "HALT_USER_VETO")
        self.assertEqual(result.omega_law, 0)
        self.assertIn("Itigil", result.message)

    def test_deepworlds_control_path_rejected(self):
        result = lite_evaluate(deepworlds_metadata_only=False)
        self.assertEqual(result.verdict, "HALT_CONSTITUTIONAL")
        self.assertEqual(result.status_tag, "REJECTED")

    def test_rf_delivery_guarantee_rejected(self):
        result = lite_evaluate(rf_delivery_guarantee=True)
        self.assertEqual(result.verdict, "HALT_CONSTITUTIONAL")
        self.assertIn("walang kasiguraduhan", result.message)

    def test_firmware_claim_requires_review(self):
        result = lite_evaluate(firmware_implementation_claim=True)
        self.assertEqual(result.verdict, "REVIEW_REQUIRED")
        self.assertEqual(result.status_tag, "UNVERIFIED")

    def test_status_tag_validation(self):
        self.assertEqual(validate_status_tag("partial"), "PARTIAL")
        with self.assertRaises(ValueError):
            validate_status_tag("MAGIC_DONE")

    def test_simplify_terms(self):
        text = simplify_terms("Truth Gap and Deepworlds metadata only")
        self.assertIn("May puwang", text)
        self.assertIn("Karagdagang konteksto", text)

    def test_sms_splitter_respects_limit(self):
        chunks = split_sms("word " * 100, max_len=80)
        self.assertTrue(chunks)
        self.assertTrue(all(len(chunk) <= 80 for chunk in chunks))

    def test_offline_queue_notice(self):
        msg = offline_queue_notice(2)
        self.assertIn("Naka-save sa device", msg)
        self.assertIn("Ipapadala kapag may signal", msg)


if __name__ == "__main__":
    unittest.main()
