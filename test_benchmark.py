import unittest
from benchmark import run


class BenchmarkTests(unittest.TestCase):
    def test_supported_and_unsupported_cases(self):
        report = run()
        for case in report["cases"]:
            with self.subTest(case=case["case"]):
                self.assertEqual(case["actual"], case["expected"])


if __name__ == "__main__":
    unittest.main()
