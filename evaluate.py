"""Evaluate structured model responses against explicit required fields."""
import json


def evaluate(response, known_sources=None):
    if not isinstance(response, dict):
        return {"passed": False, "errors": ["Response must be an object"]}
    errors = []
    if set(response) != {"summary", "sources"}:
        errors.append("Expected exactly summary and sources")
    if not isinstance(response.get("summary"), str) or not response["summary"].strip():
        errors.append("Summary must be nonempty text")
    sources = response.get("sources")
    if not isinstance(sources, list) or not sources or any(
        not isinstance(source, str) or not source.strip() for source in sources
    ):
        errors.append("Sources must be a nonempty list of source IDs")
    if not errors:
        if len(set(sources)) != len(sources):
            errors.append("Source IDs must be unique")
        if known_sources is not None:
            unknown = sorted(set(sources) - set(known_sources))
            if unknown:
                errors.append("Unknown source IDs: " + ", ".join(unknown))
    return {"passed": not errors, "errors": errors}


if __name__ == "__main__":
    samples = [
        {"summary": "Synthetic example summary.", "sources": ["example-1"]},
        {"summary": "", "sources": []},
    ]
    print(json.dumps([evaluate(sample) for sample in samples], indent=2))
