from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP
from typing import Any
from pydantic import BaseModel, Field


def to_decimal(val: Any) -> Decimal:
    if val is None or val == "":
        return Decimal("0.00")
    if isinstance(val, Decimal):
        return val.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return Decimal(str(val)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def compute_statutory_interest(
    underpayment: Decimal,
    days_delinquent: int,
    rate: Decimal = Decimal("0.15"),
) -> Decimal:
    if underpayment <= Decimal("0.00") or days_delinquent <= 0:
        return Decimal("0.00")

    und = to_decimal(underpayment)
    r = to_decimal(rate)
    days = Decimal(str(days_delinquent))
    annual_days = Decimal("365")

    raw_interest = (und * r * days) / annual_days
    return raw_interest.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


class LineItemReconciliation(BaseModel):
    line_id: str = "LINE-1"
    billed_cpt: str | None = None
    allowed_cpt: str | None = None
    billed_amount: Decimal = Field(default_factory=lambda: Decimal("0.00"))
    allowed_amount: Decimal = Field(default_factory=lambda: Decimal("0.00"))
    paid_amount: Decimal = Field(default_factory=lambda: Decimal("0.00"))
    patient_responsibility: Decimal = Field(default_factory=lambda: Decimal("0.00"))
    sequestration_carc_253: Decimal = Field(default_factory=lambda: Decimal("0.00"))
    line_underpayment: Decimal = Field(default_factory=lambda: Decimal("0.00"))
    is_downcoded: bool = False
    carc_codes: list[str] = Field(default_factory=list)
    rarc_codes: list[str] = Field(default_factory=list)
    denial_category: str = "GENERAL"


class FinancialLedger(BaseModel):
    line_items: list[LineItemReconciliation] = Field(default_factory=list)
    total_billed: Decimal = Field(default_factory=lambda: Decimal("0.00"))
    total_allowed: Decimal = Field(default_factory=lambda: Decimal("0.00"))
    total_paid: Decimal = Field(default_factory=lambda: Decimal("0.00"))
    total_patient_responsibility: Decimal = Field(default_factory=lambda: Decimal("0.00"))
    total_sequestration_carc_253: Decimal = Field(default_factory=lambda: Decimal("0.00"))
    total_line_underpayment: Decimal = Field(default_factory=lambda: Decimal("0.00"))
    statutory_interest: Decimal = Field(default_factory=lambda: Decimal("0.00"))
    total_dollars_at_risk: Decimal = Field(default_factory=lambda: Decimal("0.00"))
    straight_through_eligible: bool = False
    has_downcoding: bool = False
    recommended_readiness_state: str = "READY_FOR_H3_REVIEW"
    metadata: dict[str, Any] = Field(default_factory=dict)


def reconcile_claim_case(
    case: Any,
    days_delinquent: int = 180,
    interest_rate: Decimal = Decimal("0.15"),
) -> FinancialLedger:
    if isinstance(case, dict):
        raw_lines = case.get("lines") or case.get("line_items") or []
        if not raw_lines:
            raw_lines = [{
                "line_id": "LINE-1",
                "billed_cpt": case.get("billed_cpt") or case.get("cpt_code"),
                "allowed_cpt": case.get("allowed_cpt") or case.get("cpt_code"),
                "billed_amount": case.get("billed_amount"),
                "allowed_amount": case.get("allowed_amount"),
                "paid_amount": case.get("paid_amount"),
                "patient_responsibility": case.get("patient_responsibility", 0.0),
                "sequestration_carc_253": case.get("sequestration_carc_253", 0.0),
                "carc_codes": case.get("denial_codes", []),
                "rarc_codes": case.get("rarc_codes", []),
            }]
    else:
        raw_lines = [{
            "line_id": "LINE-1",
            "billed_amount": getattr(case, "billed_amount", 0.0),
            "allowed_amount": getattr(case, "allowed_amount", 0.0),
            "paid_amount": getattr(case, "paid_amount", 0.0),
            "patient_responsibility": getattr(case, "patient_responsibility", 0.0),
            "sequestration_carc_253": getattr(case, "sequestration_carc_253", 0.0),
            "carc_codes": getattr(case, "denial_codes", []),
            "rarc_codes": getattr(case, "rarc_codes", []),
        }]

    reconciled_lines: list[LineItemReconciliation] = []
    tot_billed = Decimal("0.00")
    tot_allowed = Decimal("0.00")
    tot_paid = Decimal("0.00")
    tot_pr = Decimal("0.00")
    tot_carc253 = Decimal("0.00")
    tot_underpayment = Decimal("0.00")
    has_downcoding = False

    for idx, item in enumerate(raw_lines, 1):
        b_cpt = str(item.get("billed_cpt") or "")
        a_cpt = str(item.get("allowed_cpt") or "")
        is_down = bool(b_cpt and a_cpt and b_cpt != a_cpt)
        if is_down:
            has_downcoding = True

        b_amt = to_decimal(item.get("billed_amount"))
        a_amt = to_decimal(item.get("allowed_amount"))
        p_amt = to_decimal(item.get("paid_amount"))
        pr_amt = to_decimal(item.get("patient_responsibility"))
        s_amt = to_decimal(item.get("sequestration_carc_253"))

        net_carrier_due = a_amt - p_amt - pr_amt - s_amt
        line_und = max(Decimal("0.00"), net_carrier_due)

        reconciled_lines.append(
            LineItemReconciliation(
                line_id=str(item.get("line_id", f"LINE-{idx}")),
                billed_cpt=b_cpt or None,
                allowed_cpt=a_cpt or None,
                billed_amount=b_amt,
                allowed_amount=a_amt,
                paid_amount=p_amt,
                patient_responsibility=pr_amt,
                sequestration_carc_253=s_amt,
                line_underpayment=line_und,
                is_downcoded=is_down,
                carc_codes=item.get("carc_codes", []),
                rarc_codes=item.get("rarc_codes", []),
                denial_category=str(item.get("denial_category", "GENERAL")),
            )
        )

        tot_billed += b_amt
        tot_allowed += a_amt
        tot_paid += p_amt
        tot_pr += pr_amt
        tot_carc253 += s_amt
        tot_underpayment += line_und

    interest = compute_statutory_interest(tot_underpayment, days_delinquent, rate=interest_rate)
    tot_at_risk = (tot_underpayment + interest).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    stfa = bool(tot_underpayment == Decimal("0.00") and not has_downcoding)
    readiness = "READY_FOR_H3_REVIEW" if tot_underpayment > Decimal("0.00") else ("STRAIGHT_THROUGH_BALANCED" if stfa else "READY_FOR_SPECIALIST_REVIEW")

    return FinancialLedger(
        line_items=reconciled_lines,
        total_billed=tot_billed,
        total_allowed=tot_allowed,
        total_paid=tot_paid,
        total_patient_responsibility=tot_pr,
        total_sequestration_carc_253=tot_carc253,
        total_line_underpayment=tot_underpayment,
        statutory_interest=interest,
        total_dollars_at_risk=tot_at_risk,
        straight_through_eligible=stfa,
        has_downcoding=has_downcoding,
        recommended_readiness_state=readiness,
    )
