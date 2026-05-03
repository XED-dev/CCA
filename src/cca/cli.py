"""xed-cca CLI — Typer-basiertes Pendant zu apt/snap für Container-App-Stacks.

Designprinzipien (analog xed-ccc):
- Vertrautheit > Eleganz: `cca install <app>` ist intuitiv
- Klare Architektur-Trennung zu ccc:
  * ccc = Container-Lifecycle + Rollen-Kompositionen
  * cca = atomare App-Stack-Installation
"""

from __future__ import annotations

import sys
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from cca._version import __version__
from cca.apps import AVAILABLE_APPS, get_app

app = typer.Typer(
    name="cca",
    help="cBUZZ Container App-Installation — App-Stack-Manager für LXC-Boxen.\n\n"
    "Atomare App-Installation in der aktuellen LXC-Box: gnome (Desktop),\n"
    "ghost (Blog/CMS), wordops (LEMP-Manager), miab (Mail-in-a-Box) usw.\n\n"
    "Pendant zu xed-ccc (Container-Lifecycle + Rollen): cca = atomare Apps.",
    no_args_is_help=True,
    add_completion=False,
)
console = Console()


def version_callback(value: bool) -> None:
    if value:
        console.print(f"xed-cca [bold]v{__version__}[/bold]")
        raise typer.Exit()


@app.callback()
def main_callback(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-V",
        help="Zeige Version und beende.",
        callback=version_callback,
        is_eager=True,
    ),
) -> None:
    """xed-cca Top-Level-Callback."""


@app.command("list")
def list_apps() -> None:
    """Listet verfügbare Apps mit Status (bereit/Stub).

    Beispiel:
        cca list
    """
    table = Table(
        title="Verfügbare Apps",
        show_header=True,
        header_style="bold cyan",
    )
    table.add_column("Name", style="bold")
    table.add_column("Beschreibung")
    table.add_column("Status", justify="center")

    for app_name, app_class in AVAILABLE_APPS.items():
        instance = app_class()
        status = (
            "[green]bereit[/green]"
            if instance.is_implemented
            else "[yellow]Stub[/yellow]"
        )
        table.add_row(app_name, instance.description, status)

    console.print(table)
    console.print()
    console.print(
        "[dim]Hinweis: Stub-Apps haben Skelett-Struktur, aber noch keine "
        "vollständige Apply-Implementation.[/dim]"
    )


@app.command("install")
def install_app(
    app_name: str = typer.Argument(
        ..., help="App, die in der aktuellen Box installiert werden soll."
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Zeige geplante Schritte, ohne sie auszuführen.",
    ),
) -> None:
    """Installiert eine App in der aktuellen LXC-Box.

    Beispiele:
        cca install gnome
        cca install ghost --dry-run
    """
    app_class = get_app(app_name)
    if app_class is None:
        console.print(f"[red]Unbekannte App:[/red] {app_name}")
        console.print(
            "Verfügbare Apps: " + ", ".join(AVAILABLE_APPS.keys())
        )
        raise typer.Exit(code=1)

    instance = app_class()
    console.print(
        f"[bold cyan]Installiere App:[/bold cyan] {app_name} — {instance.description}"
    )

    if dry_run:
        console.print("[yellow]Dry-Run:[/yellow] keine Änderungen am System.")
        instance.plan()
    else:
        if not instance.is_implemented:
            console.print(
                f"[yellow]Hinweis:[/yellow] App '{app_name}' ist noch ein Stub. "
                "Plan wird angezeigt; Apply ist noch nicht implementiert."
            )
            instance.plan()
            raise typer.Exit(code=2)
        instance.apply()
        console.print(f"[green]✔[/green] App '{app_name}' installiert.")


@app.command("menu")
def menu() -> None:
    """Startet die interaktive TUI (Textual-basiert).

    Stub: noch nicht implementiert. Kommt mit dem ersten Textual-Sprint.

    Beispiel:
        cca menu
    """
    console.print(
        "[yellow]TUI-Stub:[/yellow] `cca menu` ist noch nicht implementiert.\n"
        "Geplant: Textual-App mit App-Auswahl + Install-Status. Bis dahin:\n"
        "nutze `cca list` + `cca install <app>`."
    )
    raise typer.Exit(code=2)


def main() -> None:
    """Entry point für das `cca`-Script (siehe pyproject.toml [project.scripts])."""
    try:
        app()
    except KeyboardInterrupt:
        console.print("\n[red]Abgebrochen.[/red]")
        sys.exit(130)


if __name__ == "__main__":
    main()
