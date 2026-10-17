from __future__ import annotations

from typing import Any


class StorageSinks:
    @staticmethod
    def write_firestore_run(run_id: str, case_data: dict[str, Any]) -> dict[str, Any]:
        return {"collection": "claim_runs", "doc_id": run_id, "status": "PERSISTED"}

    @staticmethod
    def write_bigquery_telemetry(eval_record: dict[str, Any]) -> dict[str, Any]:
        return {"table": "h3_analytics.jev_shadow_evaluations", "rows_inserted": 1}
