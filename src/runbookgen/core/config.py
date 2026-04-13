"""Configuration models for runbook-gen."""

from __future__ import annotations

import os
from pydantic import BaseModel, Field


INDUSTRY_CONTEXT = {
    "fintech": (
        "Regulated financial services environment. Runbooks must align with "
        "FFIEC IT examination handbooks, SOX ITGC controls, and PCI-DSS "
        "operational requirements. Include compliance notes and audit trail guidance."
    ),
    "manufacturing": (
        "Regulated manufacturing environment. Runbooks must align with "
        "IEC 62443 operational procedures, ISO 9001 work instructions, "
        "and ISO 27001 incident management controls."
    ),
    "regulated": (
        "Regulated environment. Runbooks must include SOC 2 change management "
        "evidence, ISO 27001 incident response procedures, and audit trail requirements."
    ),
}

RUNBOOK_SECTIONS = [
    "Service overview",
    "On-call contacts",
    "Architecture summary",
    "Common alerts and responses",
    "Step-by-step remediation procedures",
    "Escalation paths",
    "Rollback procedures",
    "Compliance notes",
    "Revision history",
]


class RunbookConfig(BaseModel):
    """Runtime configuration for runbook-gen."""

    industry: str = Field("fintech", description="Industry context for compliance sections")
    output_dir: str = Field("runbooks", description="Output directory for generated runbooks")
    format: str = Field("markdown", description="Output format: markdown or confluence")
    service_name: str = Field("", description="Service name for the runbook")
    max_input_lines: int = Field(800, description="Max lines to send to AI")
    dry_run: bool = Field(False, description="Print output without writing files")

    @classmethod
    def from_env(cls) -> "RunbookConfig":
        return cls(
            industry=os.environ.get("RUNBOOK_INDUSTRY", "fintech"),
        )

    @property
    def industry_context(self) -> str:
        return INDUSTRY_CONTEXT.get(self.industry, INDUSTRY_CONTEXT["regulated"])