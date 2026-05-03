"""ghost-App: Ghost Headless CMS / Blog-Engine.

Stub-Implementation — Plan zeigt geplante Schritte. Apply kommt mit
erstem Apply-Sprint.

Referenz: <https://ghost.org/docs/install/ubuntu/>
"""

from __future__ import annotations

from rich.console import Console

from cca.apps.base import App

console = Console()


class GhostApp(App):
    """ghost — Ghost Headless CMS / Blog-Engine."""

    description = "Ghost CMS / Blog-Engine (Node.js + MySQL/SQLite + nginx)"
    is_implemented = False

    def plan(self) -> None:
        steps = [
            ("1.", "Pre-Flight: nicht-root user, sudo, Distro-Check"),
            ("2.", "Node.js LTS via NodeSource-Repo (apt install nodejs)"),
            ("3.", "MySQL/MariaDB Server installieren + secure-install"),
            ("4.", "nginx installieren (oder Reverse-Proxy-Modus erkennen)"),
            ("5.", "Ghost-CLI installieren: npm install -g ghost-cli"),
            ("6.", "ghost install — interaktive Konfig"),
        ]
        console.print("[bold]Geplante Schritte:[/bold]")
        for num, desc in steps:
            console.print(f"  {num} {desc}")

    def apply(self) -> None:
        raise NotImplementedError(
            "ghost.apply() ist noch ein Stub. "
            "Implementation kommt mit dem ersten Apply-Sprint."
        )
