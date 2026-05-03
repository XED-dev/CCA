"""gnome-App: Vanilla Gnome Desktop für LXC-Boxen.

Stub-Implementation — Plan zeigt geplante Schritte mit distro-aware Paket-
Auswahl. Apply-Implementation kommt mit erstem Apply-Sprint.

Ziel: möglichst identischer Look auf Debian + Ubuntu (Vanilla Gnome ohne
distro-spezifische Customizations).
"""

from __future__ import annotations

from rich.console import Console

from cca.apps.base import App

console = Console()


class GnomeApp(App):
    """gnome — Vanilla Gnome Desktop (möglichst gleich auf Debian + Ubuntu)."""

    description = "Vanilla Gnome Desktop (Debian: gnome-core / Ubuntu: vanilla-gnome-desktop)"
    is_implemented = False

    def plan(self) -> None:
        """Zeigt die geplanten Schritte."""
        steps = [
            ("1.", "Distro-Erkennung (lsb_release / os-release)"),
            ("2.", "Distro-aware Paket-Auswahl:"),
            ("",  "    Debian: apt install gnome-core"),
            ("",  "    Ubuntu: apt install vanilla-gnome-desktop"),
            ("3.", "xrdp + dbus-x11 + xorgxrdp installieren (Remote-Access)"),
            ("4.", "xrdp-Konfig: listen auf 0.0.0.0:3389"),
            ("5.", "non-root SysOps-User (via 'useradd -m -G sudo,tsusers')"),
            ("6.", "Optional: Wayland-Socket-Bind-Mount-Stub (Phase 2)"),
        ]
        console.print("[bold]Geplante Schritte:[/bold]")
        for num, desc in steps:
            console.print(f"  {num} {desc}" if num else f"     {desc}")

    def apply(self) -> None:
        """Führt die Konfiguration aus — noch nicht implementiert."""
        raise NotImplementedError(
            "gnome.apply() ist noch ein Stub. "
            "Implementation kommt mit dem ersten Apply-Sprint."
        )
