import unittest
from benchmark import run


class BenchmarkTests(unittest.TestCase):
    def test_supported_and_unsupported_cases(self):
        report = run()
        for case in report["cases"]:
            with self.subTest(case=case["case"]):
                if case["case"] == "supported paraphrase":
                    self.assertTrue(case["expected"])
                    self.assertFalse(case["actual"])
                else:
                    self.assertEqual(case["actual"], case["expected"])
        self.assertEqual(report["false_positives"], 0)
        self.assertEqual(report["false_negatives"], 1)


if __name__ == "__main__":
    unittest.main()
