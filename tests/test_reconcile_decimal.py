from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path

from h3_claim_agent.engines.reconcile import reconcile_claim_case, compute_statutory_interest


def test_01_case_006_exact_underpayment_and_180d_interest():
    """Verify exact deterministic math on CASE-006:
    Billed: $2,500.00
    Allowed: $1,800.00
    Paid: $1,200.00
    Underpayment = max(0.00, $1800 - $1200) = $600.00
    CA § 1371.35 Interest (15% p.a., 180 days) = round(600 * 0.15 * 180 / 365, 2) = $44.38
    Total At Risk = $644.38
    """
    fixture_path = Path(__file__).resolve().parent.parent / "fixtures" / "synthetic_cases" / "CASE-006_detox_carc197.json"
    with open(fixture_path, "r", encoding="utf-8") as f:
        case_data = json.load(f)

    ledger = reconcile_claim_case(case_data, days_delinquent=180, interest_rate=Decimal("0.15"))

    assert ledger.total_billed == Decimal("2500.00")
    assert ledger.total_allowed == Decimal("1800.00")
    assert ledger.total_paid == Decimal("1200.00")
    assert ledger.total_line_underpayment == Decimal("600.00")
    assert ledger.statutory_interest == Decimal("44.38")
    assert ledger.total_dollars_at_risk == Decimal("644.38")
    assert ledger.recommended_readiness_state == "READY_FOR_H3_REVIEW"


def test_02_pure_interest_formula_boundary():
    # Direct formula check: $600 * 0.15 * 180 / 365 = 44.3835616... -> Decimal('44.38')
    interest = compute_statutory_interest(Decimal("600.00"), days_delinquent=180, rate=Decimal("0.15"))
    assert interest == Decimal("44.38")
