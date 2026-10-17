from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from typing import Any


@dataclass
class DlpInspectionResult:
    passed: bool
    status: str  # "PASSED" or "BLOCKED_PHI_VIOLATION"
    detail: str
    findings: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


class Gate001DlpInspector:
    r"""Gate-001: Cloud Sensitive Data Protection (DLP) & Local Deterministic PHI Inspector.

    Enforces fail-closed Zero-PHI invariants:
    - If LOCAL_STORAGE_MOCK=true or USE_LIVE_DLP=false, executes local regex inspection
      for SSNs (\b\d{3}-\d{2}-\d{4}\b) and email addresses.
    - If live DLP is enabled (USE_LIVE_DLP=true and LOCAL_STORAGE_MOCK=false), invokes
      Google Cloud DLP API (dlp_v2.DlpServiceClient).
    - If sensitive data is detected or live check fails unexpectedly, trips to
      'BLOCKED_PHI_VIOLATION'.
    """

    SSN_REGEX = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
    EMAIL_REGEX = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")

    def __init__(
        self,
        local_mock: bool | None = None,
        use_live_dlp: bool | None = None,
        project_id: str | None = None,
    ):
        if local_mock is None:
            self.local_mock = os.getenv("LOCAL_STORAGE_MOCK", "true").lower() == "true"
        else:
            self.local_mock = local_mock

        if use_live_dlp is None:
            self.use_live_dlp = os.getenv("USE_LIVE_DLP", "false").lower() == "true"
        else:
            self.use_live_dlp = use_live_dlp

        self.project_id = (
            project_id
            or os.getenv("GOOGLE_CLOUD_PROJECT")
            or "h3-ao-dash-stg-2026"
        )

    def _extract_text(self, payload: Any) -> str:
        if isinstance(payload, str):
            return payload
        elif isinstance(payload, (dict, list)):
            return json.dumps(payload, default=str)
        return str(payload)

    def inspect(self, payload: Any) -> DlpInspectionResult:
        text = self._extract_text(payload)

        # Local Deterministic Regex Inspection
        if self.local_mock or not self.use_live_dlp:
            findings: list[str] = []

            ssn_matches = self.SSN_REGEX.findall(text)
            if ssn_matches:
                findings.extend([f"SSN pattern detected: {m}" for m in ssn_matches])

            email_matches = self.EMAIL_REGEX.findall(text)
            if email_matches:
                findings.extend([f"Email pattern detected: {m}" for m in email_matches])

            if findings:
                return DlpInspectionResult(
                    passed=False,
                    status="BLOCKED_PHI_VIOLATION",
                    detail=f"Detected sensitive data via local regex inspection: {len(findings)} finding(s)",
                    findings=findings,
                    metadata={"mode": "local_regex", "finding_count": len(findings)},
                )

            return DlpInspectionResult(
                passed=True,
                status="PASSED",
                detail="No sensitive PHI/PII detected by local regex inspection",
                findings=[],
                metadata={"mode": "local_regex"},
            )

        # Live Google Cloud DLP Inspection
        try:
            from google.cloud import dlp_v2

            dlp_client = dlp_v2.DlpServiceClient()
            parent = f"projects/{self.project_id}/locations/global"
            item = {"value": text}
            inspect_config = {
                "info_types": [
                    {"name": "US_SOCIAL_SECURITY_NUMBER"},
                    {"name": "EMAIL_ADDRESS"},
                    {"name": "PERSON_NAME"},
                    {"name": "DATE_OF_BIRTH"},
                ],
                "min_likelihood": dlp_v2.Likelihood.LIKELIHOOD_UNSPECIFIED,
                "include_quote": True,
            }
            response = dlp_client.inspect_content(
                request={"parent": parent, "inspect_config": inspect_config, "item": item}
            )

            findings = []
            if response.result and response.result.findings:
                for f in response.result.findings:
                    findings.append(f"{f.info_type.name} (likelihood={f.likelihood.name})")

            if findings:
                return DlpInspectionResult(
                    passed=False,
                    status="BLOCKED_PHI_VIOLATION",
                    detail=f"Cloud DLP detected sensitive data: {len(findings)} finding(s)",
                    findings=findings,
                    metadata={"mode": "cloud_dlp", "finding_count": len(findings)},
                )

            return DlpInspectionResult(
                passed=True,
                status="PASSED",
                detail="Cloud DLP verified payload clean of sensitive data",
                findings=[],
                metadata={"mode": "cloud_dlp"},
            )
        except Exception as exc:
            return DlpInspectionResult(
                passed=False,
                status="BLOCKED_PHI_VIOLATION",
                detail=f"Live Cloud DLP invocation failed (fail-closed policy): {exc}",
                findings=[str(exc)],
                metadata={"mode": "cloud_dlp_error"},
            )
