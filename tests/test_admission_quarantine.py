from __future__ import annotations

import copy
import re


def verify_and_admit_findings(candidate_findings: list[dict], evidence_inventory: list[dict]) -> tuple[list[dict], list[dict]]:
    inv_ids = {e.get("evidence_id") for e in evidence_inventory if e.get("evidence_id")}
    admitted = []
    quarantined = []

    for f in candidate_findings:
        refs = f.get("evidence_refs", [])
        unverified = [r for r in refs if r not in inv_ids or not re.match(r"^EV-[\w-]+$", str(r))]
        if unverified or not refs:
            item = copy.deepcopy(f)
            item["status"] = "QUARANTINED"
            item["quarantine_reason"] = "UNVERIFIED_EVIDENCE_CITATION"
            item["unverified_refs"] = unverified
            quarantined.append(item)
        else:
            item = copy.deepcopy(f)
            item["status"] = "ADMITTED"
            admitted.append(item)

    return admitted, quarantined


def test_01_admit_valid_evidence_ref():
    evidence_inventory = [{"evidence_id": "EV-006-01", "fact": "Fentanyl withdrawal protocol met"}]
    candidate = {
        "finding_id": "FINDING-001",
        "statement": "Denied despite authorization",
        "evidence_refs": ["EV-006-01"],
    }
    admitted, quarantined = verify_and_admit_findings([candidate], evidence_inventory)
    assert len(admitted) == 1
    assert len(quarantined) == 0
    assert admitted[0]["status"] == "ADMITTED"


def test_02_quarantine_hallucinated_evidence_ref():
    evidence_inventory = [{"evidence_id": "EV-006-01", "fact": "Fentanyl withdrawal protocol met"}]
    hallucinated = {
        "finding_id": "FINDING-999",
        "statement": "Hallucinated assertion",
        "evidence_refs": ["EV-999"],
    }
    admitted, quarantined = verify_and_admit_findings([hallucinated], evidence_inventory)
    assert len(admitted) == 0
    assert len(quarantined) == 1
    assert quarantined[0]["status"] == "QUARANTINED"
    assert quarantined[0]["quarantine_reason"] == "UNVERIFIED_EVIDENCE_CITATION"
