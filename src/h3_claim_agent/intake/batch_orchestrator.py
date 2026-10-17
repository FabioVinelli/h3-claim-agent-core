from __future__ import annotations

from typing import Any
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="H3-Claim-Agent Cloud Run Orchestrator", version="0.2.1")


class BatchIntakePayload(BaseModel):
    batch_id: str
    mode: str
    records: list[dict[str, Any]]


@app.get("/healthz")
def healthz():
    return {"status": "HEALTHY", "version": "0.2.1", "region": "us-west2"}


@app.post("/intake/batch")
def process_batch(payload: BatchIntakePayload):
    return {
        "batch_id": payload.batch_id,
        "mode": payload.mode,
        "record_count": len(payload.records),
        "status": "PROCESSING_QUEUED",
    }
