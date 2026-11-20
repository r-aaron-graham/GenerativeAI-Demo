# Structured Response Evaluation Demo

A local evaluation example for structured generative AI responses. It validates a summary and source identifiers using Python 3.12 and the standard library.

## Run

```sh
python evaluate.py
python -m unittest -v
```

The demo evaluates two synthetic responses. The first passes. The second reports an empty summary and missing source identifiers. Tests cover valid responses, wrong types, missing fields, empty values, and extra fields.

## Integration and limitations

Call `evaluate(response)` with a parsed model response. It returns a passed flag and validation errors. Source IDs are checked for structure only. Factual accuracy, source existence, citation support, and answer relevance require additional evaluation against a trusted corpus. Model-provider integration is an extension point. The included examples are synthetic.
