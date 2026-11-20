import unittest
from evaluate import evaluate


class ResponseTests(unittest.TestCase):
    def test_source_registry(self):
        response = {"summary": "Example", "sources": ["s1"]}
        self.assertTrue(evaluate(response, ["s1"])["passed"])
        self.assertFalse(evaluate(response, ["s2"])["passed"])
        self.assertFalse(evaluate(response, [])["passed"])

    def test_duplicate_sources(self):
        self.assertFalse(evaluate({"summary": "Example", "sources": ["s1", "s1"]})["passed"])

    def test_valid_response(self):
        self.assertTrue(evaluate({"summary": "Example", "sources": ["s1"]})["passed"])

    def test_invalid_responses(self):
        for response in (None, [], {}, {"summary": "", "sources": []},
                         {"summary": "Text", "sources": [3]},
                         {"summary": "Text", "sources": ["s1"], "extra": True}):
            with self.subTest(response=response):
                self.assertFalse(evaluate(response)["passed"])


if __name__ == "__main__":
    unittest.main()
