"""generate command — AI runbook generation from multiple sources."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

from runbookgen.core.config import RunbookConfig
from runbookgen.core.extractor import (
    extract_from_directory,
    extract_from_alerts,
    extract_from_incident,
)
from runbookgen.core.generator import generate_runbook, write_runbook

generate_app = typer.Typer(help="Generate runbooks from various sources.")
console = Console()


@generate_app.callback(invoke_without_command=True)
def generate(
    ctx: typer.Context,
    source: Path = typer.Argument(..., help="Source path — directory, alert file, or incident file"),
    output: str = typer.Option("runbooks", "--output", "-o", help="Output directory"),
    industry: str = typer.Option("fintech", "--industry", "-i", help="Industry context"),
    service: Optional[str] = typer.Option(None, "--service", "-s", help="Override service name"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Print without writing files"),
    from_alerts: bool = typer.Option(False, "--from-alerts", help="Treat source as alert definitions"),
    from_incident: bool = typer.Option(False, "--from-incident", help="Treat source as incident report"),
) -> None:
    """Generate an operational runbook from source code, alerts, or incidents.

    Examples:

        runbook-gen generate src/payments/ --industry fintech

        runbook-gen generate alerts/critical.yml --from-alerts

        runbook-gen generate incidents/INC-001.md --from-incident
    """
    if ctx.invoked_subcommand is not None:
        return

    if not source.exists():
        console.print(f"[red]Source not found: {source}[/red]")
        raise typer.Exit(1)

    console.print(f"[dim]Extracting context from {source}...[/dim]")

    if from_alerts:
        context = extract_from_alerts(source)
    elif from_incident:
        context = extract_from_incident(source)
    elif source.is_dir():
        context = extract_from_directory(source)
    else:
        context = extract_from_incident(source)

    if service:
        context.service_name = service

    if context.is_empty:
        console.print("[yellow]No content extracted from source.[/yellow]")
        raise typer.Exit(1)

    config = RunbookConfig(
        industry=industry,
        output_dir=output,
        service_name=context.service_name,
        dry_run=dry_run,
    )

    console.print(f"[dim]Generating runbook for [cyan]{context.service_name}[/cyan]...[/dim]")
    runbook = generate_runbook(context, config)

    if dry_run:
        console.print(Panel(
            Syntax(runbook[:2000], "markdown", theme="monokai", word_wrap=True),
            title=f"Runbook preview — {context.service_name}",
            border_style="blue",
        ))
    else:
        output_path = write_runbook(runbook, config)
        console.print(f"[green]✓[/green] Runbook written to [cyan]{output_path}[/cyan]")