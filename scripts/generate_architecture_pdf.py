from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
import pypdf

pdf_out = Path("/Users/pii_sandbox/Dev-Ops/H3-IDRR/H3-Website/public/docs/h3-claim-agent-architecture.pdf")
pdf_out.parent.mkdir(parents=True, exist_ok=True)

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#475569"))
        # Header
        self.drawString(54, 755, "HIGHLAND HEALTH HUB (H3) // TECHNICAL ARCHITECTURE SPECIFICATION")
        self.drawRightString(612 - 54, 755, "GOOGLE CLOUD & VERTEX AI NATIVE")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.75)
        self.line(54, 747, 612 - 54, 747)
        # Footer
        self.line(54, 42, 612 - 54, 42)
        self.setFont("Helvetica", 8)
        self.drawString(54, 30, "CONFIDENTIAL // PROPRIETARY // BAA-COVERED ZERO-PHI ENTERPRISE ARCHITECTURE")
        self.drawRightString(612 - 54, 30, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()

doc = SimpleDocTemplate(
    str(pdf_out),
    pagesize=letter,
    leftMargin=54,
    rightMargin=54,
    topMargin=52,
    bottomMargin=52,
)

styles = getSampleStyleSheet()

primary_color = colors.HexColor("#0F172A")
accent_color = colors.HexColor("#0284C7")

title_style = ParagraphStyle(
    "CoverTitle",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=18,
    leading=22,
    textColor=primary_color,
    spaceAfter=3,
)

subtitle_style = ParagraphStyle(
    "CoverSubtitle",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=10,
    leading=14,
    textColor=accent_color,
    spaceAfter=8,
)

h1_style = ParagraphStyle(
    "H1",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=11,
    leading=14,
    textColor=primary_color,
    spaceBefore=7,
    spaceAfter=3,
    keepWithNext=True,
)

body_style = ParagraphStyle(
    "Body",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=8,
    leading=11,
    textColor=colors.HexColor("#334155"),
    spaceAfter=3,
)

code_style = ParagraphStyle(
    "CodeSnippet",
    parent=styles["Normal"],
    fontName="Courier",
    fontSize=7,
    leading=9,
    textColor=colors.HexColor("#0F172A"),
)

callout_style = ParagraphStyle(
    "Callout",
    parent=styles["Normal"],
    fontName="Helvetica-Oblique",
    fontSize=8,
    leading=11,
    textColor=colors.HexColor("#1E293B"),
)

story = []

# Title without unicode trademark to prevent font double-encoding artifact
story.append(Paragraph("H3-Claim-Agent // Technical Architecture Blueprint", title_style))
story.append(Paragraph("Autonomous Forensic Claim Intelligence & Parity Defense on Google Cloud & Vertex AI", subtitle_style))

# Metadata Box
meta_data = [
    [Paragraph("<b>Target Environment:</b> Google Cloud us-west2 (h3-healthcare-prod)", body_style),
     Paragraph("<b>Active GCP Project:</b> h3-claim-agent", body_style)],
    [Paragraph("<b>Linked Billing Account:</b> 012A95-92AF92-F722F1", body_style),
     Paragraph("<b>Organization:</b> highlandhealthhub.com", body_style)],
    [Paragraph("<b>Version:</b> v0.2.1-CloudNative (Production Specification)", body_style),
     Paragraph("<b>Security Posture:</b> Zero-PHI // Cloud DLP Fail-Closed // CMEK", body_style)]
]
t_meta = Table(meta_data, colWidths=[250, 254])
t_meta.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
    ("BOX", (0,0), (-1,-1), 1, colors.HexColor("#E2E8F0")),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING", (0,0), (-1,-1), 3),
    ("BOTTOMPADDING", (0,0), (-1,-1), 3),
    ("LEFTPADDING", (0,0), (-1,-1), 6),
    ("RIGHTPADDING", (0,0), (-1,-1), 6),
]))
story.append(t_meta)
story.append(Spacer(1, 4))

# 1. Executive Overview & Core System Doctrine
story.append(Paragraph("1. Executive Overview & Core System Doctrine", h1_style))
story.append(Paragraph(
    "Highland Health Hub (H3) operates the <b>H3-Claim-Agent</b>, an autonomous vertical AI SaaS platform built to neutralize systemic reimbursement shortfalls, algorithmic denials (CARC 197 / CARC 50), and federal Mental Health Parity and Addiction Equity Act (MHPAEA) violations in Behavioral Health & Substance Use Disorder (SUD) treatment.",
    body_style
))
story.append(Paragraph(
    "<b>The Core System Invariant:</b> <i>'Give the model reasoning freedom inside a strictly bounded sandbox; govern all state, arithmetic, authority, and irreversible actions at the deterministic system boundary.'</i> Large Language Models are strictly prohibited from calculating numbers, determining financial outcomes, or authoring unsourced appeal allegations.",
    callout_style
))
story.append(Spacer(1, 4))

# 2. 7-Stage Architecture Table
story.append(Paragraph("2. The 7-Stage Google Cloud Native Pipeline", h1_style))
stage_table_data = [
    [Paragraph("<b>Stage</b>", body_style), Paragraph("<b>GCP Component</b>", body_style), Paragraph("<b>Operational Function & Deterministic Invariant</b>", body_style)],
    [Paragraph("<b>Stage 1: Intake</b>", body_style), Paragraph("CMEK Cloud Storage<br/><code>gs://h3-claim-raw-intake</code>", code_style), Paragraph("Custodial batch drops of 835/837P EDI, CSV remittances, and EHR exports secured by Cloud KMS (<code>h3-storage-key</code>).", body_style)],
    [Paragraph("<b>Stage 2: Security</b>", body_style), Paragraph("Cloud Sensitive Data Protection<br/>(Cloud DLP <code>GATE-001</code>)", code_style), Paragraph("Fail-closed Zero-PHI inspection. Scans SSN, DOB, name before any data enters reasoning tiers. Gate-002 verifies SHA-256 cross-matter isolation.", body_style)],
    [Paragraph("<b>Stage 3: Reconciler</b>", body_style), Paragraph("Deterministic Reconciler v2<br/>(Pure Python Decimal)", code_style), Paragraph("Zero LLM Math. Enforces <code>Underpayment = max(0, Allowed - Paid - PR - CARC 253)</code> and CA Knox-Keene § 1371.35 15% statutory interest.", body_style)],
    [Paragraph("<b>Stage 4: JEV Router</b>", body_style), Paragraph("Cloud Tasks<br/><code>jev-shadow-queue</code>", code_style), Paragraph("Pattern J3 triage routing administrative denials to Gemini 2.5 Flash and multi-issue clinical/parity disputes to Gemini 2.5 Pro.", body_style)],
    [Paragraph("<b>Stage 5: Reasoner</b>", body_style), Paragraph("Vertex AI<br/>Gemini 2.5 Pro / Flash", code_style), Paragraph("Sandboxed <code>google-genai</code> SDK execution with ADC, temp=0.0, Pydantic JSON schema binding, and citations strictly bounded to <code>EV-xxx</code>.", body_style)],
    [Paragraph("<b>Stage 6: Admission</b>", body_style), Paragraph("Two-Tier Audit Engine<br/>(<code>audit.py</code>)", code_style), Paragraph("Deterministic SHA-256 locator hash validation. Automatically quarantines hallucinated evidence citations with <code>UNVERIFIED_EVIDENCE_CITATION</code>.", body_style)],
    [Paragraph("<b>Stage 7: Sinks</b>", body_style), Paragraph("Firestore, BigQuery &<br/>Zero-PHI Neo4j Graph", code_style), Paragraph("Firestore operational state, BigQuery JEV shadow telemetry lake, and tokenized payer denial pattern mapping in Neo4j (<code>:H3</code> namespace).", body_style)],
]
t_stages = Table(stage_table_data, colWidths=[85, 140, 279])
t_stages.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#0F172A")),
    ("TEXTCOLOR", (0,0), (-1,0), colors.white),
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
    ("TOPPADDING", (0,0), (-1,-1), 2),
    ("BOTTOMPADDING", (0,0), (-1,-1), 2),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
]))
story.append(t_stages)

# Explicit PageBreak to Page 2
story.append(PageBreak())

# Section 3: Dual Operating Modes
story.append(Paragraph("3. Dual Operating Modes: Facility SaaS vs. Litigation Support", h1_style))
modes_data = [
    [Paragraph("<b>Dimension</b>", body_style), Paragraph("<b>Mode A: Facility Revenue Recovery SaaS</b>", body_style), Paragraph("<b>Mode B: Legal Analytics-as-a-Service</b>", body_style)],
    [Paragraph("<b>Client Target</b>", body_style), Paragraph("Behavioral Health & SUD Facilities (ASAM 1.0-3.7)", body_style), Paragraph("ERISA § 502 & Healthcare Litigation Law Firms", body_style)],
    [Paragraph("<b>Intake Vault</b>", body_style), Paragraph("<code>gs://h3-vault-facility/&lt;CLIENT_ID&gt;/</code>", code_style), Paragraph("<code>gs://h3-vault-litigation/&lt;MATTER_ID&gt;/</code>", code_style)],
    [Paragraph("<b>Primary Deliverable</b>", body_style), Paragraph("Executive Claim Intelligence Record (CIR), Revenue Opportunity Queue & Scrubber Rules", body_style), Paragraph("Master Litigation Damages Schedule, Statutory Interest Audit & Exhibit-Citable Dossiers", body_style)],
    [Paragraph("<b>Legal Boundary</b>", body_style), Paragraph("Administrative Provider Dispute Support", body_style), Paragraph("Attorney Work Product / UPL Protective Headers", body_style)],
    [Paragraph("<b>Value Impact</b>", body_style), Paragraph("Recovers working capital; keeps clinical beds open", body_style), Paragraph("Accelerates settlement; establishes trial damages", body_style)]
]
t_modes = Table(modes_data, colWidths=[95, 204, 205])
t_modes.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#0284C7")),
    ("TEXTCOLOR", (0,0), (-1,0), colors.white),
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
    ("TOPPADDING", (0,0), (-1,-1), 2.5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 2.5),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
]))
story.append(t_modes)
story.append(Spacer(1, 4))

# Section 4: Benchmark Forensic Case Study: CASE-006 Financial Reconciler
# Order: Section 4 Heading -> Intro Paragraph -> CASE-006 Table
story.append(Paragraph("4. Benchmark Forensic Case Study: CASE-006 Financial Reconciler", h1_style))
intro_case_p = Paragraph(
    "To validate deterministic accuracy across the entire stack, <b>CASE-006</b> serves as our primary production proof point across live web telemetry, internal pytest validation, and whitepaper reporting:",
    body_style
)
intro_case_p.keepWithNext = True
story.append(intro_case_p)

case_data = [
    [Paragraph("<b>Claim Attribute</b>", body_style), Paragraph("<b>Verified Value / Metric</b>", body_style), Paragraph("<b>Governing Legal / Technical Baseline</b>", body_style)],
    [Paragraph("Case Identifier", body_style), Paragraph("<code>CASE-006</code>", code_style), Paragraph("Synthetic fixture canonical benchmark", body_style)],
    [Paragraph("Payer & Plan", body_style), Paragraph("Aetna Commercial PPO", body_style), Paragraph("Commercial PPO Out-of-Network Parity", body_style)],
    [Paragraph("Level of Care", body_style), Paragraph("ASAM 3.7 Inpatient Medically Monitored Detox", body_style), Paragraph("CPT H0010 // Severe Fentanyl protocol", body_style)],
    [Paragraph("Payer Denial Action", body_style), Paragraph("CARC 197 / RARC N702 (Precertification absent)", body_style), Paragraph("Unlawful step-down denial; retroactive auth valid", body_style)],
    [Paragraph("Billed Charge", body_style), Paragraph("$2,500.00", body_style), Paragraph("Submitted UB-04 / 837I claim line item", body_style)],
    [Paragraph("Contract Allowed", body_style), Paragraph("$1,800.00", body_style), Paragraph("Established commercial benchmark rate", body_style)],
    [Paragraph("Payer Paid Amount", body_style), Paragraph("$1,200.00", body_style), Paragraph("Remitted via 835 ERA line adjustment", body_style)],
    [Paragraph("Patient Responsibility", body_style), Paragraph("$0.00", body_style), Paragraph("Group Code PR isolated from carrier debt", body_style)],
    [Paragraph("<b>Deterministic Underpayment</b>", body_style), Paragraph("<b>$600.00</b>", body_style), Paragraph("<code>max(0.00, $1800 - $1200 - $0 - $0)</code> via pure Decimal", body_style)],
    [Paragraph("Statutory Prompt-Pay Interest", body_style), Paragraph("<b>$44.38</b>", body_style), Paragraph("CA Health & Safety Code § 1371.35 (15% p.a., <b>180-Day Lag</b>)", body_style)],
    [Paragraph("<b>Total Dollars at Risk</b>", body_style), Paragraph("<b>$644.38</b>", body_style), Paragraph("Direct recoverable carrier liability", body_style)],
]
t_case = Table(case_data, colWidths=[130, 160, 214])
t_case.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#0F172A")),
    ("TEXTCOLOR", (0,0), (-1,0), colors.white),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
    ("TOPPADDING", (0,0), (-1,-1), 1.8),
    ("BOTTOMPADDING", (0,0), (-1,-1), 1.8),
    ("BACKGROUND", (0,9), (-1,9), colors.HexColor("#DCFCE7")),
    ("BACKGROUND", (0,10), (-1,10), colors.HexColor("#FEF3C7")),
    ("BACKGROUND", (0,11), (-1,11), colors.HexColor("#E0E7FF")),
]))
story.append(t_case)
story.append(Spacer(1, 4))

# Section 5: Mathematical Infallibility Proof (Using alphabetic words so symbols cannot be stripped)
story.append(Paragraph("5. Mathematical Infallibility Proof (180-Day Statutory Interest)", h1_style))
math_text = (
    "<b>Daily Interest Factor:</b> 0.15 div 365 equals 0.0004109589<br/>"
    "<b>Delinquency Span:</b> 180 Calendar Days (Remittance Date minus Adjudication Deadline)<br/>"
    "<b>Statutory Interest:</b> $600.00 x (0.15 / 365) x 180 equals $44.38356<br/>"
    "<b>Quantized Result (ROUND_HALF_UP):</b> $44.38"
)
story.append(Paragraph(math_text, code_style))
story.append(Spacer(1, 4))

# Section 6: Architectural Governance & Readiness Gate
story.append(Paragraph("6. Architectural Governance & Readiness Gate", h1_style))
story.append(Paragraph(
    "All 260 unit and integration tests across the H3 Claim Agent suite enforce these exact values. The public repository, live website, and API microservices maintain identical figures, guaranteeing zero mathematical variance between discovery exhibits, executive dossiers, and operational recovery queues.",
    body_style
))

doc.build(story, canvasmaker=NumberedCanvas)

# Validate page count using pypdf
reader = pypdf.PdfReader(str(pdf_out))
page_count = len(reader.pages)
print(f"Generated {pdf_out} -> Total Pages: {page_count} ({pdf_out.stat().st_size} bytes)")
assert page_count == 2, f"Expected exactly 2 pages, got {page_count}"

# Copy to destinations
dests = [
    Path("/Users/pii_sandbox/Dev-Ops/H3-IDRR/h3-claim-agent-public-github/docs/h3-claim-agent-architecture.pdf"),
    Path("/Users/pii_sandbox/Dev-Ops/H3-IDRR/H3-Claim-Agent/docs/h3-claim-agent-architecture.pdf"),
]
for d in dests:
    d.parent.mkdir(parents=True, exist_ok=True)
    d.write_bytes(pdf_out.read_bytes())
    print(f"Copied to {d}")
