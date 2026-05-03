"""wordops-App: WordOps NGINX-Stack-Manager (LEMP).

Stub-Implementation — Plan zeigt geplante Schritte. Apply kommt mit
erstem Apply-Sprint.

Referenz: <https://wordops.net/>
Plus: AI034-Memory `reference_wordops_install_quirks.md` (Codename-Conditional,
Bootstrap-Pattern, [KO]-Silent-Failure-Erkennung).
"""

from __future__ import annotations

from rich.console import Console

from cca.apps.base import App

console = Console()


class WordOpsApp(App):
    """wordops — WordOps NGINX-Stack-Manager (LEMP)."""

    description = "WordOps LEMP-Stack-Manager (NGINX + PHP-FPM + MariaDB + Let's Encrypt)"
    is_implemented = False

    def plan(self) -> None:
        steps = [
            ("1.", "Pre-Step: software-properties-common (Codename-conditional)"),
            ("2.", "WordOps-Bootstrap: bash <(curl -sSL wordops.net/install)"),
            ("3.", "Verifikation: command -v wo (Silent-Failure-Pattern beachten)"),
            ("4.", "wo stack install --nginx --php --mysql"),
            ("5.", "Optional: Let's Encrypt-Setup für Domain-SSL"),
        ]
        console.print("[bold]Geplante Schritte:[/bold]")
        for num, desc in steps:
            console.print(f"  {num} {desc}")
        console.print(
            "\n[dim]Hinweis: Codename-Conditional-Pattern aus AI034-Memory "
            "'reference_wordops_install_quirks.md' beachten — auf Resolute (26.04) "
            "ist Plain-NGINX-Fallback nötig wegen ABI-Bruch.[/dim]"
        )

    def apply(self) -> None:
        raise NotImplementedError(
            "wordops.apply() ist noch ein Stub. "
            "Implementation kommt mit dem ersten Apply-Sprint."
        )
