"""Tests for source extraction."""

import tempfile
from pathlib import Path
from runbookgen.core.extractor import (
    extract_from_directory,
    extract_from_alerts,
    extract_from_incident,
    ServiceContext,
)


def test_extract_from_directory() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir)
        (path / "service.py").write_text("# ONCALL: page payments team\ndef process(): pass")
        (path / "config.yml").write_text("service: payments\nport: 8080")
        ctx = extract_from_directory(path)
        assert ctx.service_name == path.name
        assert len(ctx.source_files) == 2
        assert not ctx.is_empty


def test_extract_from_alerts() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "payments_alerts.yml"
        path.write_text("- alert: HighLatency\n  threshold: 2000ms")
        ctx = extract_from_alerts(path)
        assert not ctx.is_empty
        assert len(ctx.alert_definitions) == 1


def test_extract_from_incident() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "INC-001.md"
        path.write_text("# Incident INC-001\n\n## Summary\nPayments were slow.")
        ctx = extract_from_incident(path)
        assert not ctx.is_empty
        assert len(ctx.incident_history) == 1


def test_service_context_is_empty() -> None:
    ctx = ServiceContext(service_name="test", raw_content="")
    assert ctx.is_empty is True


def test_service_context_truncation() -> None:
    lines = [f"line {i}" for i in range(1000)]
    ctx = ServiceContext(service_name="test", raw_content="\n".join(lines))
    truncated = ctx.truncated(max_lines=100)
    assert "truncated" in truncated