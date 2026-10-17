# H3-Claim-Agent™ (v0.2.1)
### Autonomous Forensic Claim Intelligence & Parity Defense Engine on Google Cloud & Vertex AI

[![Google Cloud Run](https://img.shields.io/badge/Google_Cloud-Cloud_Run-4285F4?logo=google-cloud&logoColor=white)](https://cloud.google.com/run)
[![Vertex AI](https://img.shields.io/badge/Vertex_AI-Gemini_2.5_Pro%2FFlash-blue?logo=google&logoColor=white)](https://cloud.google.com/vertex-ai)
[![Cloud DLP Zero-PHI](https://img.shields.io/badge/Security-Cloud_DLP_Zero--PHI-success?logo=google-cloud&logoColor=white)](https://cloud.google.com/sensitive-data-protection)
[![Pydantic v2](https://img.shields.io/badge/Validation-Pydantic_v2-E92063?logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)
[![LangGraph](https://img.shields.io/badge/Orchestration-LangGraph_StateGraph-black)](https://langchain-ai.github.io/langgraph/)

**Primary Production Target:** `h3-healthcare-prod` (`us-west2`)  
**Linked Billing Account ID:** `012A95-92AF92-F722F1`  
**Organization:** [Highland Health Hub (H3)](https://www.highlandhealthhub.com)  
**Whitepaper Specification:** [docs/h3-claim-agent-architecture.pdf](docs/h3-claim-agent-architecture.pdf)

---

## Core System Doctrine

> *"Give the model reasoning freedom inside a strictly bounded sandbox; govern all state, arithmetic, authority, and irreversible actions at the deterministic system boundary."*

Highland Health Hub's **H3-Claim-Agent™** is an enterprise-grade vertical AI SaaS engine designed for Behavioral Health & Substance Use Disorder (SUD) facilities (ASAM 1.0–3.7) and healthcare litigators. It ingests 835 ERA remittances, 837 claim files, and EHR clinical progress notes into a zero-PHI Google Cloud pipeline to overturn algorithmic denials (CARC 197 / CARC 50) and enforce the federal Mental Health Parity and Addiction Equity Act (MHPAEA).

---

## The 7-Stage Google Cloud Native Pipeline

```
[835/837P EDI & EHR Ingestion]
               │
               ▼
┌────────────────────────────────────────────────────────────────────────┐
│ Stage 1: CMEK Cloud Storage (gs://h3-claim-raw-intake · Cloud KMS)      │
├────────────────────────────────────────────────────────────────────────┤
│ Stage 2: Security Gates (Cloud DLP GATE-001 Fail-Closed & GATE-002)    │
├────────────────────────────────────────────────────────────────────────┤
│ Stage 3: Deterministic Financial Reconciler v2 (Pure Decimal Math)     │
├────────────────────────────────────────────────────────────────────────┤
│ Stage 4: JEV Decision Engine & Model Tier Router (Cloud Tasks Queue)   │
├────────────────────────────────────────────────────────────────────────┤
│ Stage 5: Bounded Vertex AI Reasoner (Gemini 2.5 Pro & Flash · ADC)    │
├────────────────────────────────────────────────────────────────────────┤
│ Stage 6: Two-Tier Evidence Admission vs. Quarantine (audit.py)         │
├────────────────────────────────────────────────────────────────────────┤
│ Stage 7: Sinks & Telemetry (Cloud Firestore · BigQuery · Zero-PHI Neo4j)│
└────────────────────────────────────────────────────────────────────────┘
```

---

## Benchmark Case Study: CASE-006

Every deployment and test suite verifies exact arithmetic on canonical benchmark fixture `CASE-006`:

| Attribute | Verified Value / Calculation | Legal / Mathematical Authority |
| :--- | :--- | :--- |
| **Case Identifier** | `CASE-006` | Synthetic Fixture Benchmark |
| **Payer & Plan** | Aetna Commercial PPO | Commercial Out-of-Network Parity |
| **Level of Care** | ASAM 3.7 Inpatient Medically Monitored Detox | Severe Fentanyl Withdrawal Protocol |
| **Denial Action** | CARC 197 / RARC N702 | Precertification Absent (Arbitrary Step-Down) |
| **Billed Charges** | `$2,500.00` | Submitted UB-04 / 837I Line |
| **Contract Allowed** | `$1,800.00` | Established Plan Benchmark |
| **Payer Paid** | `$1,200.00` | Remitted via 835 ERA |
| **Deterministic Underpayment**| **`$600.00`** | `max(0, $1800 - $1200 - $0 - $0)` via Pure Decimal |
| **CA § 1371.35 Interest** | **`$44.38`** | 15% p.a. over **180-Day Remittance Lag** |
| **Total Dollars at Risk** | **`$644.38`** | Direct Recoverable Carrier Liability |

$$\text{Daily Factor} = \frac{0.15}{365} \approx 0.0004109589$$
$$\text{Statutory Interest} = \$600.00 \times \left(\frac{0.15}{365}\right) \times 180 = \$44.38356... \xrightarrow{\text{ROUND\_HALF\_UP}} \mathbf{\$44.38}$$

---

## Dual SaaS Operating Modes

| Dimension | Mode A: Facility Recovery SaaS | Mode B: Legal Analytics-as-a-Service |
| :--- | :--- | :--- |
| **Client Target** | Behavioral Health & SUD Facilities | ERISA § 502 & Healthcare Litigation Counsel |
| **Storage Vault** | `gs://h3-vault-consulting/<CLIENT_ID>/` | `gs://h3-vault-litigation/<MATTER_ID>/` |
| **Deliverable** | Executive Claim Intelligence Records (CIR) | Master Damages Schedules & Trial Exhibits |
| **Boundary** | Administrative Dispute Support | Attorney Work Product / UPL Header Protection |
| **Impact** | Recovers operating cash flow for facilities | Quantifies carrier liability and speeds settlement |

---

## Quickstart & Verification

### 1. Local Testing
```bash
# Clone and enter showcase repo
git clone https://github.com/highlandhealthhub/h3-claim-agent-core.git
cd h3-claim-agent-core

# Setup virtual environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run deterministic test suite
PYTHONPATH=src pytest tests/ -v
```

### 2. Google Cloud Run Deployment
```bash
# Authenticate via Application Default Credentials (ADC)
gcloud auth application-default login

# Submit container build to Artifact Registry
gcloud builds submit --tag us-west2-docker.pkg.dev/h3-healthcare-prod/h3-claim-agent/service:latest .

# Deploy private managed service
gcloud run deploy h3-claim-agent-service \
  --image us-west2-docker.pkg.dev/h3-healthcare-prod/h3-claim-agent/service:latest \
  --region us-west2 \
  --platform managed \
  --no-allow-unauthenticated \
  --set-env-vars GOOGLE_CLOUD_PROJECT=h3-healthcare-prod,GOOGLE_GENAI_USE_ENTERPRISE=true,USE_LIVE_DLP=true
```

---

## License & Security
Proprietary & Confidential. All fixtures are synthetic (`SYNTHETIC_ONLY`). Zero protected health information (PHI) is processed or stored.
