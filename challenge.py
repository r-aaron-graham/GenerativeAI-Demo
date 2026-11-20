"""Report broader synthetic paraphrases for inspection."""
import json
from benchmark import factual_support, SOURCES

CASES = [
    ("passive wording", "Audit logs are retained for 30 days.", True),
    ("retention period", "Audit logs have a retention period of 30 days.", True),
    ("number word", "Audit logs are kept for thirty days.", True),
    ("contradiction", "Audit logs are kept for 90 days.", False),
    ("extra claim", "Audit logs are kept for 30 days and encrypted.", False),
]


def run():
    rows = []
    for name, summary, expected in CASES:
        actual = factual_support({"summary": summary, "sources": ["retention"]}, SOURCES)["passed"]
        rows.append({"case": name, "expected": expected, "actual": actual,
                     "correct": actual == expected})
    return {"cases": rows, "correct": sum(row["correct"] for row in rows), "total": len(rows)}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
