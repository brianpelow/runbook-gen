"""Nightly agent — automated maintenance for runbook-gen."""

from __future__ import annotations

import json
import sys
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

REPO_ROOT = Path(__file__).parent.parent


def update_section_stats() -> None:
    """Write a summary of required runbook sections to docs."""
    from runbookgen.core.config import RUNBOOK_SECTIONS
    from runbookgen.core.validator import REQUIRED_SECTIONS
    stats = {
        "generated_at": datetime.utcnow().isoformat(),
        "date": date.today().isoformat(),
        "total_sections": len(RUNBOOK_SECTIONS),
        "sections": RUNBOOK_SECTIONS,
        "required_by_industry": {k: v for k, v in REQUIRED_SECTIONS.items()},
    }
    out = REPO_ROOT / "docs" / "section-stats.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(stats, indent=2))
    print(f"[agent] Updated section stats -> {out}")


def refresh_changelog() -> None:
    changelog = REPO_ROOT / "CHANGELOG.md"
    if not changelog.exists():
        return
    today = date.today().isoformat()
    content = changelog.read_text()
    if today not in content:
        content = content.replace("## [Unreleased]", f"## [Unreleased]\n\n_Last checked: {today}_", 1)
        changelog.write_text(content)
    print("[agent] Refreshed CHANGELOG timestamp")


def validate_example_runbook() -> None:
    """Run validation against the example runbook and save report."""
    from runbookgen.core.validator import validate_runbook
    example = REPO_ROOT / "docs" / "examples" / "payments-runbook.md"
    if not example.exists():
        print("[agent] No example runbook found, skipping validation")
        return
    results = validate_runbook(example, industry="fintech")
    passed = sum(1 for r in results if r.passed)
    report = {
        "generated_at": datetime.utcnow().isoformat(),
        "file": str(example.name),
        "score": int((passed / len(results)) * 100),
        "passed": passed,
        "total": len(results),
        "results": [{"name": r.name, "passed": r.passed, "detail": r.detail} for r in results],
    }
    out = REPO_ROOT / "docs" / "example-validation.json"
    out.write_text(json.dumps(report, indent=2))
    print(f"[agent] Example runbook validation score: {report['score']}% -> {out}")


if __name__ == "__main__":
    print(f"[agent] Starting nightly agent - {date.today().isoformat()}")
    update_section_stats()
    refresh_changelog()
    validate_example_runbook()
    print("[agent] Done.")