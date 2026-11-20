import unittest
from benchmark import run, factual_support, SOURCES


class BenchmarkTests(unittest.TestCase):
    def test_adversarial_claims(self):
        for claim in (
            "Audit logs are kept for 90 days.",
            "Audit logs are not kept for 30 days.",
            "Audit logs are kept for 30 days. Everything is encrypted.",
            "Audit logs are kept for 30 days except when deleted.",
        ):
            with self.subTest(claim=claim):
                self.assertFalse(factual_support(
                    {"summary": claim, "sources": ["retention"]}, SOURCES
                )["passed"])

    def test_supported_and_unsupported_cases(self):
        report = run()
        for case in report["cases"]:
            with self.subTest(case=case["case"]):
                self.assertEqual(case["actual"], case["expected"])
        self.assertEqual(report["false_positives"], 0)
        self.assertEqual(report["false_negatives"], 0)


if __name__ == "__main__":
    unittest.main()
