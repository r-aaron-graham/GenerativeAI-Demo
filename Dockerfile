FROM python:3.12-slim
WORKDIR /app
COPY evaluate.py benchmark.py test_evaluate.py test_benchmark.py ./
USER 65534:65534
CMD ["python", "benchmark.py"]
