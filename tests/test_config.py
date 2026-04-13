"""Tests for RunbookConfig."""

from runbookgen.core.config import RunbookConfig, INDUSTRY_CONTEXT, RUNBOOK_SECTIONS


def test_config_defaults() -> None:
    config = RunbookConfig()
    assert config.industry == "fintech"
    assert config.output_dir == "runbooks"
    assert config.format == "markdown"
    assert config.dry_run is False


def test_config_custom() -> None:
    config = RunbookConfig(industry="manufacturing", output_dir="output")
    assert config.industry == "manufacturing"
    assert config.output_dir == "output"


def test_industry_context_fintech() -> None:
    assert "fintech" in INDUSTRY_CONTEXT
    assert "FFIEC" in INDUSTRY_CONTEXT["fintech"]
    assert "SOX" in INDUSTRY_CONTEXT["fintech"]


def test_industry_context_manufacturing() -> None:
    assert "manufacturing" in INDUSTRY_CONTEXT
    assert "IEC 62443" in INDUSTRY_CONTEXT["manufacturing"]


def test_runbook_sections_not_empty() -> None:
    assert len(RUNBOOK_SECTIONS) >= 6


def test_industry_context_property() -> None:
    config = RunbookConfig(industry="fintech")
    assert "FFIEC" in config.industry_context