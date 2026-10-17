from __future__ import annotations

import json
from pathlib import Path
from h3_claim_agent.harness.gate_001_gcp_dlp import Gate001DlpInspector


def test_01_gate_001_dlp_fail_closed_on_mock_ssn():
    inspector = Gate001DlpInspector(local_mock=True)

    dirty_payload = {
        "case_id": "CASE-TEST-001",
        "notes": "Patient Social Security Number is 123-45-6789 for intake verification",
    }

    result = inspector.inspect(dirty_payload)
    assert result.passed is False
    assert result.status == "BLOCKED_PHI_VIOLATION"
    assert any("123-45-6789" in f for f in result.findings)


def test_02_gate_001_pass_on_clean_synthetic_case_006():
    fixture_path = Path(__file__).resolve().parent.parent / "fixtures" / "synthetic_cases" / "CASE-006_detox_carc197.json"
    with open(fixture_path, "r", encoding="utf-8") as f:
        case_data = json.load(f)

    inspector = Gate001DlpInspector(local_mock=True)
    result = inspector.inspect(case_data)
    assert result.passed is True
    assert result.status == "PASSED"
    assert len(result.findings) == 0
