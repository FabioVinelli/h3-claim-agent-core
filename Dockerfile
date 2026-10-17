# Google Cloud Run Managed Container (Port 8080)
FROM python:3.11-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /app/src/
COPY docs/ /app/docs/

ENV PYTHONPATH=/app/src

EXPOSE 8080

CMD ["uvicorn", "h3_claim_agent.intake.batch_orchestrator:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "2"]
