"""Source extraction — reads code comments, alerts, and incident files."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ServiceContext:
    """Extracted context from a service directory or file."""

    service_name: str
    source_files: list[str] = field(default_factory=list)
    code_comments: list[str] = field(default_factory=list)
    alert_definitions: list[str] = field(default_factory=list)
    incident_history: list[str] = field(default_factory=list)
    raw_content: str = ""

    @property
    def is_empty(self) -> bool:
        return not self.raw_content.strip()

    def truncated(self, max_lines: int = 800) -> str:
        lines = self.raw_content.splitlines()
        if len(lines) <= max_lines:
            return self.raw_content
        kept = lines[:max_lines]
        kept.append(f"\n... truncated at {max_lines} lines ({len(lines) - max_lines} more) ...")
        return "\n".join(kept)


def extract_from_directory(path: Path, max_files: int = 20) -> ServiceContext:
    """Extract context from a service source directory."""
    service_name = path.name
    source_files: list[str] = []
    code_comments: list[str] = []
    content_parts: list[str] = []

    extensions = {".py", ".ts", ".js", ".go", ".java", ".yaml", ".yml", ".md"}
    files = [f for f in path.rglob("*") if f.is_file() and f.suffix in extensions][:max_files]

    for file in files:
        try:
            text = file.read_text(errors="ignore")
            rel = str(file.relative_to(path))
            source_files.append(rel)
            content_parts.append(f"# File: {rel}\n{text[:2000]}")

            comments = re.findall(r'#\s*(?:TODO|FIXME|NOTE|ALERT|ONCALL|RUNBOOK):.*', text)
            code_comments.extend(comments)
        except Exception:
            pass

    return ServiceContext(
        service_name=service_name,
        source_files=source_files,
        code_comments=code_comments,
        raw_content="\n\n".join(content_parts),
    )


def extract_from_alerts(path: Path) -> ServiceContext:
    """Extract context from alert definition files (YAML/JSON)."""
    try:
        content = path.read_text(errors="ignore")
        service_name = path.stem.replace("-", "_").replace("_alerts", "")
        return ServiceContext(
            service_name=service_name,
            alert_definitions=[content],
            raw_content=f"# Alert definitions from: {path.name}\n\n{content}",
        )
    except Exception:
        return ServiceContext(service_name=path.stem, raw_content="")


def extract_from_incident(path: Path) -> ServiceContext:
    """Extract context from a past incident markdown file."""
    try:
        content = path.read_text(errors="ignore")
        service_name = path.stem
        return ServiceContext(
            service_name=service_name,
            incident_history=[content],
            raw_content=f"# Incident report: {path.name}\n\n{content}",
        )
    except Exception:
        return ServiceContext(service_name=path.stem, raw_content="")