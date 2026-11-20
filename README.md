# Structured Response Evaluation Demo

A local evaluation example for structured generative AI responses. It validates a summary and source identifiers using Python 3.12 and the standard library.

## Run

```sh
python evaluate.py
python -m unittest -v
```

The demo evaluates two synthetic responses. The first passes. The second reports an empty summary and missing source identifiers. Tests cover valid responses, wrong types, missing fields, empty values, and extra fields.

## Integration and limitations

Call `evaluate(response)` with a parsed model response. It returns a passed flag and validation errors. Pass an explicit registry with `evaluate(response, known_sources=["example-1"])` to reject unknown source IDs. Duplicate source IDs also fail validation. Omitting the registry performs structural checks. Factual accuracy, source existence, citation support, and answer relevance require additional evaluation against a trusted corpus. Model-provider integration is an extension point. The included examples are synthetic.

## Factual-support example

Run `python benchmark.py`. The example checks whether the complete summary exactly matches a cited source in a small fictional policy corpus. It rejects invented durations, wrong citations, unknown sources, extra unsupported claims, missing citations, and duplicate citations. This conservative exact-evidence check rejects paraphrases. It establishes a reproducible baseline for testing citation handling.

The eight labeled cases represent common structural and grounding failure modes. They are synthetic examples. Assessing a real deployment requires independently labeled examples from its actual documents, including supported paraphrases, contradictions, numerical claims, and unanswerable questions. Benchmark correctness measures agreement with these eight labels.

## Deployment verification

Run from the repository root:

```sh
python -m unittest -v
python benchmark.py
docker build -t generative-evaluation .
docker run --rm --read-only --network none generative-evaluation
```

Expected benchmark output contains correct=8 and total=8, with exit status 0. The container runs as an unprivileged user and needs no network access. The deployment workflow builds and runs this image on GitHub Actions. A successful container check verifies this batch evaluation package. Operation within a target production service requires separate integration and monitoring.
