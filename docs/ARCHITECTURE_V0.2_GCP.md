# Technical Architecture: H3-Claim-Agent™ v0.2.1 on Google Cloud Platform

**Primary Target:** `h3-healthcare-prod` (`us-west2`)  
**Compliance Profile:** BAA-Covered Zero-PHI Custodial Architecture  
**Core Frameworks:** Python 3.11, Pydantic v2, Google GenAI SDK, Cloud Run, Cloud Tasks, Cloud DLP, BigQuery

---

## 1. Core System Doctrine
> *"Give the model reasoning freedom inside a strictly bounded sandbox; govern all state, arithmetic, authority, and irreversible actions at the deterministic system boundary."*

1. **Zero LLM Math:** LLMs never perform arithmetic. Underpayments and statutory interest are calculated strictly via Python `decimal.Decimal` with `ROUND_HALF_UP`.
2. **Zero-PHI Posture:** All payloads must pass Google Cloud Sensitive Data Protection (`GATE-001` Cloud DLP) before entering reasoning tiers. Live SSN, DOB, or patient identifiers fail closed to `BLOCKED_PHI_VIOLATION`.
3. **Custodial Boundary:** Batch ingestion via partitioned Cloud Storage buckets; no active EHR live polling.
4. **Evidentiary Grounding:** Candidate findings must cite verified `evidence_id` (`EV-xxx`) with matching SHA-256 locator digests. Hallucinated citations are quarantined immediately.
5. **Non-Clinical / Non-Attorney Boundary:** Commercial clinical denials (CARC 50, 97, 4, 59) route to `NEEDS_SPECIALIST_REVIEW`.

---

## 2. The 7-Stage Google Cloud Pipeline

```
[Kipu / Navix EHR / 835 / 837P Ingestion]
                   │
                   ▼
[Stage 1: CMEK Cloud Storage] ── gs://h3-claim-raw-intake (Cloud KMS)
                   │
                   ▼
[Stage 2: Deterministic Gates] ── Cloud DLP GATE-001 (Zero-PHI) & GATE-002 (SHA-256)
                   │
                   ▼
[Stage 3: Deterministic Reconciler v2] ── Pure Python Decimal Math (Zero LLM Math)
                   │
                   ▼
[Stage 4: JEV Router (Cloud Tasks)] ── Administrative -> Gemini 2.5 Flash
                   │                 ── Clinical/Parity -> Gemini 2.5 Pro
                   ▼
[Stage 5: Bounded Vertex AI Reasoner] ── Sandboxed google-genai SDK (temp=0.0, EV-xxx)
                   │
                   ▼
[Stage 6: Two-Tier Admission/Quarantine] ── Canonical Admission vs. Quarantine (audit.py)
                   │
                   ▼
[Stage 7: Sinks & State Machines] ── Firestore (State) + BigQuery (JEV Telemetry) + Neo4j (:H3)
```

---

## 3. Dual Operating Modes

| Feature | Mode A: Facility Recovery SaaS | Mode B: Legal Analytics-as-a-Service |
| :--- | :--- | :--- |
| **Customer Target** | Behavioral Health & SUD Facilities | Healthcare & ERISA Litigators |
| **Storage Vault** | `gs://h3-vault-facility/<CLIENT_ID>/` | `gs://h3-vault-litigation/<MATTER_ID>/` |
| **Primary Deliverables**| Executive Claim Intelligence Records (CIR) | Master Litigation Damages Models & Exhibits |
| **Legal Posture** | Administrative Dispute Support | Attorney Work Product / UPL Protection |
