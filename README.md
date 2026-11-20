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

Run `python benchmark.py`. The example checks cited evidence using exact matching and two controlled paraphrase grammars. It rejects invented durations, wrong citations, unknown sources, extra unsupported claims, missing citations, and duplicate citations. Wording outside the supported grammars is rejected. It establishes a reproducible baseline for testing citation handling.

The eleven labeled cases represent common structural and grounding failure modes. They are synthetic examples. Assessing a real deployment requires independently labeled examples from its actual documents, including supported paraphrases, contradictions, numerical claims, and unanswerable questions. Benchmark correctness measures agreement with these eleven labels.

## Deployment verification

Run from the repository root:

```sh
python -m unittest -v
python benchmark.py
docker build -t generative-evaluation .
docker run --rm --read-only --network none generative-evaluation
```

Expected benchmark output contains correct=11 and total=11, with exit status 0. The container runs as an unprivileged user and needs no network access. The deployment workflow builds and runs this image on GitHub Actions. A successful container check verifies this batch evaluation package. Operation within a target production service requires separate integration and monitoring.

## Paraphrase and contradiction benchmark

The benchmark includes a supported paraphrase, a direct contradiction, and an unsupported location. The original exact-match baseline rejected the supported paraphrase, recording one false negative. The original baseline precision was 1.0 and recall was 2/3 on this synthetic fixture. These values describe the fixed examples. The current behavior and benchmark gate are described below.

## Controlled paraphrase evaluation

The current evaluator recognizes complete retention-duration and operating-region statements using two explicit grammars. It compares extracted facts against the cited source text. The 11-case fixture now passes, including the supported paraphrase. Additional regression cases reject negation, changed durations, exceptions, and appended claims. The benchmark exits successfully only when every fixture label matches. This is a narrow rule-based example. General semantic entailment and independent real-document evaluation remain extension points.

The earlier exact-match baseline produced precision 1.0 and recall 2/3. The current controlled grammar produces precision 1.0 and recall 1.0 on the same fixed synthetic cases. These fixture results do not establish accuracy on unseen documents.

## Broader challenge report

Run `python challenge.py` to inspect five additional synthetic cases. The current evaluator matches three labels and misses two supported paraphrases, including a number written as a word. This exploratory report prints every outcome and exits normally. The separate strict benchmark remains the regression gate. Real-document accuracy remains unmeasured.

## Package installation

Run `python -m pip install .` from the repository root. The package has no runtime dependencies and requires Python 3.12 or later. Run `python -m benchmark` after installation.

## Security checks

The security workflow scans all three application modules with Bandit. See SECURITY.md for reporting guidance and deployment scope.
