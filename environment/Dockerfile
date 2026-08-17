# FinEdu-CodeGen — reproducibility container.
# Build context is the repository root:
#   docker build -t finedu-codegen -f environment/Dockerfile .
#   docker run --rm -it -v "$PWD":/app finedu-codegen
# Reproduces the main tables/figures from released logs (no API key needed;
# regenerating raw generations DOES need OPENROUTER_API_KEY — see README).
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

ENV PYTHONUNBUFFERED=1

CMD ["bash", "scripts/reproduce_main_results.sh"]
