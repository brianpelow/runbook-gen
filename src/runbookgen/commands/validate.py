"""validate command — validate runbooks against compliance standards."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from runbookgen.core.validator import validate_runbook

validate_app = typer.Typer(help="Validate runbooks against compliance standards.")
console = Console()


@validate_app.callback(invoke_without_command=True)
def validate(
    ctx: typer.Context,
    path: Path = typer.Argument(..., help="Runbook file to validate"),
    industry: str = typer.Option("fintech", "--industry", "-i", help="Industry standard to validate against"),
) -> None:
    """Validate a runbook against regulated-industry compliance standards."""
    if ctx.invoked_subcommand is not None:
        return

    results = validate_runbook(path, industry)

    table = Table(title=f"Validation: {path.name} [{industry}]", border_style="dim")
    table.add_column("Check", style="bold")
    table.add_column("Status", justify="center")
    table.add_column("Detail", style="dim")

    passed = 0
    for result in results:
        status = "[green]✓[/green]" if result.passed else "[red]✗[/red]"
        if result.passed:
            passed += 1
        table.add_row(result.name, status, result.detail)

    console.print(table)
    score = int((passed / len(results)) * 100)
    color = "green" if score >= 80 else "yellow" if score >= 60 else "red"
    console.print(f"\n[bold]Score: [{color}]{score}%[/{color}][/bold] ({passed}/{len(results)} checks passed)\n")