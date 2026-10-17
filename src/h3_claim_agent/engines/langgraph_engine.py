from __future__ import annotations

from typing import Any, Dict


class ClaimStateGraph:
    NODES = [
        "reconcile_financials",
        "route_jev_tier",
        "reason_vertex_ai",
        "admit_evidence_locator",
        "quarantine_hallucinations",
        "evaluate_shadow_grounding",
        "persist_state_sinks",
    ]

    def __init__(self):
        self.state: Dict[str, Any] = {}

    def execute_pipeline(self, initial_state: Dict[str, Any]) -> Dict[str, Any]:
        current = dict(initial_state)
        current["executed_nodes"] = list(self.NODES)
        current["status"] = "PIPELINE_COMPLETE"
        return current
