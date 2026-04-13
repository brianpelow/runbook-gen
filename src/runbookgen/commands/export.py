"""export command — export runbooks to Markdown or Confluence."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from runbookgen.core.exporter import export_to_markdown, export_to_confluence

export_app = typer.Typer(help="Export runbooks to various targets.")
console = Console()


@export_app.callback(invoke_without_command=True)
def export(
    ctx: typer.Context,
    source: Path = typer.Argument(..., help="Runbook markdown file to export"),
    target: str = typer.Option("markdown", "--target", "-t", help="Export target: markdown or confluence"),
    output: Path = typer.Option(Path("runbooks/exported"), "--output", "-o", help="Output path"),
    space: str = typer.Option("ENG", "--space", help="Confluence space key"),
) -> None:
    """Export a runbook to Markdown or Confluence."""
    if ctx.invoked_subcommand is not None:
        return

    if not source.exists():
        console.print(f"[red]File not found: {source}[/red]")
        raise typer.Exit(1)

    content = source.read_text()

    if target == "confluence":
        title = source.stem.replace("-", " ").title()
        success = export_to_confluence(content, title=title, space_key=space)
        if success:
            console.print(f"[green]✓ Exported to Confluence: {title}[/green]")
        else:
            console.print("[red]Confluence export failed — check CONFLUENCE_URL and CONFLUENCE_TOKEN[/red]")
            raise typer.Exit(1)
    else:
        result = export_to_markdown(content, output / source.name)
        console.print(f"[green]✓ Exported to {result}[/green]")