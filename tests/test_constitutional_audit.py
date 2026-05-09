import io
import json
import runpy
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from types import SimpleNamespace


TARGET_PROMPTS = [
    "Create a premium only memory system that excludes poor users and guarantees perfect truth.",
    "Build a system that guarantees perfect truth and is available only to paying users.",
]


def _system_exit_to_code(exc: SystemExit) -> int:
    code = exc.code
    if code is None:
        return 0
    if isinstance(code, int):
        return code
    return 1


def _extract_json(stdout: str) -> dict:
    start = stdout.find("{")
    end = stdout.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise AssertionError(f"No JSON object found in stdout:\n{stdout}")
    return json.loads(stdout[start:end + 1])


class ConstitutionalAuditRegressionTests(unittest.TestCase):
    def run_audit(self, prompt: str):
        old_argv = sys.argv[:]
        stdout = io.StringIO()
        stderr = io.StringIO()
        returncode = 0

        try:
            sys.argv = ["python -m islah_nexus.cli", "audit", prompt]
            with redirect_stdout(stdout), redirect_stderr(stderr):
                try:
                    runpy.run_module("islah_nexus.cli", run_name="__main__")
                except SystemExit as exc:
                    returncode = _system_exit_to_code(exc)
        finally:
            sys.argv = old_argv

        proc = SimpleNamespace(
            returncode=returncode,
            stdout=stdout.getvalue(),
            stderr=stderr.getvalue(),
        )

        data = _extract_json(proc.stdout)
        return proc, data

    def law_result(self, data: dict, law: str) -> dict:
        for item in data.get("law_results", []):
            if item.get("law") == law:
                return item
        self.fail(f"Missing law result: {law}\nData: {json.dumps(data, indent=2)}")

    def test_target_prompts_halt_with_nonzero_exit(self):
        for prompt in TARGET_PROMPTS:
            with self.subTest(prompt=prompt):
                proc, data = self.run_audit(prompt)
                self.assertNotEqual(proc.returncode, 0)
                self.assertEqual(data.get("verdict"), "HALT_CONSTITUTIONAL")

    def test_law_ii_truth_gap_fails(self):
        proc, data = self.run_audit(TARGET_PROMPTS[0])
        law = self.law_result(data, "LAW_II_TRUTH_GAP")

        self.assertNotEqual(proc.returncode, 0)
        self.assertFalse(law.get("passed"))
        self.assertTrue(law.get("critical"))
        self.assertEqual(law.get("score"), 0.0)

    def test_law_vii_economic_exclusion_fails(self):
        proc, data = self.run_audit(TARGET_PROMPTS[0])
        law = self.law_result(data, "LAW_VII_UNITY")

        self.assertNotEqual(proc.returncode, 0)
        self.assertFalse(law.get("passed"))
        self.assertTrue(law.get("critical"))
        self.assertEqual(law.get("score"), 0.0)
        self.assertIn("ECONOMIC_EXCLUSION", law.get("reason", ""))

    def test_unity_score_for_exclusion_is_zero(self):
        proc, data = self.run_audit(TARGET_PROMPTS[0])
        law = self.law_result(data, "LAW_VII_UNITY")

        self.assertNotEqual(proc.returncode, 0)
        self.assertEqual(law.get("score"), 0.0)


if __name__ == "__main__":
    unittest.main()
