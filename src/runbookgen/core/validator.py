"""Runbook validation against compliance standards."""

from __future__ import annotations

from pathlib import Path
from dataclasses import dataclass


REQUIRED_SECTIONS = {
    "fintech": [
        "service overview",
        "on-call",
        "alert",
        "rollback",
        "compliance",
        "escalation",
    ],
    "manufacturing": [
        "service overview",
        "on-call",
        "alert",
        "rollback",
        "compliance",
        "escalation",
    ],
    "regulated": [
        "service overview",
        "alert",
        "rollback",
        "compliance",
    ],
}


@dataclass
class ValidationResult:
    """Result of a runbook validation check."""

    name: str
    passed: bool
    detail: str = ""


def validate_runbook(path: Path, industry: str = "fintech") -> list[ValidationResult]:
    """Validate a runbook file against industry compliance standards."""
    if not path.exists():
        return [ValidationResult("File exists", False, f"Not found: {path}")]

    content = path.read_text(errors="ignore").lower()
    results: list[ValidationResult] = []

    results.append(ValidationResult("File exists", True))
    results.append(ValidationResult(
        "Minimum length",
        len(content) >= 500,
        f"{len(content)} chars" if len(content) >= 500 else f"Only {len(content)} chars — too short",
    ))

    required = REQUIRED_SECTIONS.get(industry, REQUIRED_SECTIONS["regulated"])
    for section in required:
        found = section.lower() in content
        results.append(ValidationResult(
            f"Contains '{section}' section",
            found,
            "" if found else f"Missing required section for {industry}",
        ))

    has_table = "|" in content and "---" in content
    results.append(ValidationResult(
        "Has revision history table",
        has_table,
        "" if has_table else "No markdown table found — revision history required",
    ))

    results.append(ValidationResult(
        "Has code blocks or commands",
        "```" in path.read_text(errors="ignore"),
        "" if "```" in path.read_text(errors="ignore") else "No command examples found",
    ))

    return results