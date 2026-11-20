"""Run a synthetic exact-evidence support benchmark."""
import json
import re
from evaluate import evaluate

SOURCES = {
    "retention": "The fictional company retains audit logs for 30 days.",
    "region": "The fictional service operates in the EU region.",
}
CASES = [
    ("supported retention", SOURCES["retention"], ["retention"], True),
    ("supported region", SOURCES["region"], ["region"], True),
    ("supported paraphrase", "Audit logs are kept for 30 days.", ["retention"], True),
    ("contradiction", "Audit logs are never retained.", ["retention"], False),
    ("unsupported location", "The service operates in Asia.", ["region"], False),
    ("wrong citation", SOURCES["retention"], ["region"], False),
    ("invented duration", "Audit logs are retained for 90 days.", ["retention"], False),
    ("unknown source", SOURCES["region"], ["missing"], False),
    ("partially supported", SOURCES["region"] + " Data is always encrypted.", ["region"], False),
    ("missing citation", SOURCES["region"], [], False),
    ("duplicate citation", SOURCES["region"], ["region", "region"], False),
]


def canonical_fact(text):
    """Recognize only complete statements in two controlled policy grammars."""
    normalized = text.strip().lower().rstrip(".")
    retention = re.fullmatch(
        r"(?:the fictional company retains audit logs|audit logs are (?:retained|kept)) for (\d+) days",
        normalized,
    )
    if retention:
        return ("retention_days", int(retention.group(1)))
    region = re.fullmatch(
        r"(?:the fictional service|the service) operates in (?:the )?([a-z]+)(?: region)?",
        normalized,
    )
    if region:
        return ("region", region.group(1))
    return None


def factual_support(response, sources):
    result = evaluate(response, sources)
    if not result["passed"]:
        return result
    evidence = [sources[source].strip() for source in response["sources"]]
    claim = response["summary"].strip()
    fact = canonical_fact(claim)
    if claim not in evidence and (
        fact is None or not any(canonical_fact(text) == fact for text in evidence)
    ):
        return {"passed": False, "errors": ["Summary is outside the supported evidence grammar or conflicts with cited evidence"]}
    return result


def run():
    outcomes = []
    for name, summary, citations, expected in CASES:
        result = factual_support({"summary": summary, "sources": citations}, SOURCES)
        outcomes.append({"case": name, "expected": expected, "actual": result["passed"],
                         "correct": result["passed"] == expected})
    true_positives = sum(row["expected"] and row["actual"] for row in outcomes)
    false_positives = sum(not row["expected"] and row["actual"] for row in outcomes)
    false_negatives = sum(row["expected"] and not row["actual"] for row in outcomes)
    return {"cases": outcomes, "correct": sum(row["correct"] for row in outcomes),
            "total": len(outcomes), "true_positives": true_positives,
            "false_positives": false_positives, "false_negatives": false_negatives,
            "precision": true_positives / (true_positives + false_positives)
                         if true_positives + false_positives else None,
            "recall": true_positives / (true_positives + false_negatives)
                      if true_positives + false_negatives else None}


if __name__ == "__main__":
    report = run()
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report["correct"] == report["total"] else 1)
