"""Tests for runbook validation."""

import tempfile
from pathlib import Path
from runbookgen.core.validator import validate_runbook


GOOD_RUNBOOK = """# Payments Service Runbook

## Service overview
The payments service handles transactions.

## On-call contacts
- Primary: oncall@example.com

## Common alerts and responses
### HIGH_LATENCY
Check database connections.

## Rollback procedures
Run kubectl rollout undo.

## Escalation paths
Page the platform team.

## Compliance notes
SOX in-scope system. Log all changes.

## Revision history

| Date | Author | Change |
|------|--------|--------|
| 2026-04-12 | runbook-gen | Initial |

```bash
kubectl rollout undo deployment/payments
```
"""


def test_validate_good_runbook() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "runbook.md"
        path.write_text(GOOD_RUNBOOK)
        results = validate_runbook(path, industry="fintech")
        passed = [r for r in results if r.passed]
        assert len(passed) >= len(results) - 1


def test_validate_missing_file() -> None:
    results = validate_runbook(Path("/nonexistent/runbook.md"))
    assert results[0].passed is False
    assert "Not found" in results[0].detail


def test_validate_empty_runbook() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "empty.md"
        path.write_text("# Title\n\nToo short.")
        results = validate_runbook(path)
        length_check = next(r for r in results if "length" in r.name.lower())
        assert length_check.passed is False