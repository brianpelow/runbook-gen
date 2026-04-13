"""runbook-gen CLI entry point."""

from __future__ import annotations

import typer
from rich.console import Console

from runbookgen import __version__
from runbookgen.commands.generate import generate_app
from runbookgen.commands.export import export_app
from runbookgen.commands.validate import validate_app

app = typer.Typer(
    name="runbook-gen",
    help="AI-generated operational runbooks for regulated industries.",
    add_completion=True,
    rich_markup_mode="rich",
)
console = Console()

app.add_typer(generate_app, name="generate")
app.add_typer(export_app, name="export")
app.add_typer(validate_app, name="validate")


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool = typer.Option(False, "--version", "-v", help="Show version and exit."),
) -> None:
    """runbook-gen — AI-generated operational runbooks for regulated industries."""
    if version:
        console.print(f"runbook-gen v{__version__}")
        raise typer.Exit()
    if ctx.invoked_subcommand is None:
        console.print(ctx.get_help())