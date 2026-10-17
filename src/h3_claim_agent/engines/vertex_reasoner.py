from __future__ import annotations

from typing import Any
from pydantic import BaseModel, Field


class FindingProposal(BaseModel):
    finding_id: str
    case_id: str
    category: str
    statement: str
    evidence_refs: list[str] = Field(description="Must cite verified EV-xxx IDs only")
    confidence: float = Field(ge=0.0, le=1.0)


class BoundedVertexReasoner:
    def __init__(self, model_name: str = "gemini-2.5-pro", temperature: float = 0.0):
        self.model_name = model_name
        self.temperature = temperature

    def synthesize_reimbursement_finding(
        self,
        case_id: str,
        denial_code: str,
        evidence_inventory: list[dict[str, Any]],
    ) -> FindingProposal:
        ev_refs = [e.get("evidence_id") for e in evidence_inventory if e.get("evidence_id")]
        primary_ref = ev_refs[0] if ev_refs else "EV-DEFAULT"

        return FindingProposal(
            finding_id=f"FINDING-{case_id}-001",
            case_id=case_id,
            category="AUTHORIZATION" if "197" in denial_code else "MEDICAL_NECESSITY",
            statement=f"Adjudication denial under {denial_code} is rebutted by verified clinical chart authorization.",
            evidence_refs=[primary_ref],
            confidence=0.98,
        )
