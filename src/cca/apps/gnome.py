"""gnome-App: Vanilla Gnome Desktop für LXC-Boxen.

Atomar (cca §9): Display-Stack only. Distro-aware Paket-Auswahl
(Debian: gnome-core / Ubuntu: vanilla-gnome-desktop) plus xrdp +
xorgxrdp + dbus-x11 als Display-Server-Subset.

SysOps-User + Wayland-Bind-mount sind keine cca-Verantwortung —
gehören in ``ccc create pmDESK`` als Komposition.

Codename-Conditional folgt dem WordOps-Pattern aus AI034
(`reference_wordops_install_quirks.md`).
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Iterable

from rich.console import Console

from cca.apps.base import App

console = Console()


CODENAME_DESKTOP_PACKAGE: dict[str, str] = {
    "noble":    "vanilla-gnome-desktop",
    "jammy":    "vanilla-gnome-desktop",
    "focal":    "vanilla-gnome-desktop",
    "bookworm": "gnome-core",
    "bullseye": "gnome-core",
}

DISPLAY_STACK_PACKAGES: tuple[str, ...] = (
    "xrdp",
    "xorgxrdp",
    "dbus-x11",
)


class GnomeApp(App):
    """gnome — Vanilla Gnome Desktop + xrdp Display-Stack (atomar)."""

    description = (
        "Vanilla Gnome Desktop "
        "(Debian: gnome-core / Ubuntu: vanilla-gnome-desktop) "
        "+ xrdp + dbus-x11"
    )
    is_implemented = True

    def plan(self) -> None:
        steps = [
            ("1.", "Distro-Erkennung via /etc/os-release ($VERSION_CODENAME)"),
            ("2.", "Codename-conditional Desktop-Meta-Paket:"),
            ("",   "    noble/jammy/focal  -> vanilla-gnome-desktop"),
            ("",   "    bookworm/bullseye  -> gnome-core"),
            ("3.", "apt-get update + apt-get install -y <Desktop-Meta> xrdp xorgxrdp dbus-x11"),
            ("4.", "systemctl enable --now xrdp"),
            ("5.", "Verifikation: dpkg-Status pro Paket + xrdp-Service aktiv"),
        ]
        console.print("[bold]Geplante Schritte (atomar, Display-Stack only):[/bold]")
        for num, desc in steps:
            console.print(f"  {num} {desc}" if num else f"     {desc}")

    def apply(self) -> None:
        self._require_root()
        codename = self._detect_codename()
        desktop_meta = self._select_desktop_meta(codename)
        all_packages: tuple[str, ...] = (desktop_meta,) + DISPLAY_STACK_PACKAGES

        console.print(f"[cyan]Distro-Codename:[/cyan] [bold]{codename}[/bold]")
        console.print(f"[cyan]Desktop-Meta:[/cyan]    {desktop_meta}")
        console.print(f"[cyan]Display-Stack:[/cyan]   {' '.join(DISPLAY_STACK_PACKAGES)}")
        console.print()

        self._apt_update()
        self._apt_install(all_packages)
        self._enable_xrdp_service()
        self._verify(all_packages)

    @staticmethod
    def _require_root() -> None:
        if os.geteuid() != 0:
            raise RuntimeError(
                "cca install gnome braucht root (apt install + systemctl). "
                "Aufruf via `sudo cca install gnome` oder direkt als root."
            )

    @staticmethod
    def _detect_codename() -> str:
        os_release = Path("/etc/os-release")
        if not os_release.exists():
            raise RuntimeError(
                "/etc/os-release fehlt — nur Debian/Ubuntu wird unterstützt."
            )
        for line in os_release.read_text(encoding="utf-8").splitlines():
            if line.startswith("VERSION_CODENAME="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
        raise RuntimeError(
            "VERSION_CODENAME fehlt in /etc/os-release — Distro nicht erkennbar."
        )

    @staticmethod
    def _select_desktop_meta(codename: str) -> str:
        package = CODENAME_DESKTOP_PACKAGE.get(codename)
        if package is None:
            supported = ", ".join(sorted(CODENAME_DESKTOP_PACKAGE.keys()))
            raise RuntimeError(
                f"Codename '{codename}' nicht unterstützt. "
                f"Bekannte Codenames: {supported}. "
                f"Erweitere CODENAME_DESKTOP_PACKAGE in cca/apps/gnome.py."
            )
        return package

    @staticmethod
    def _apt_env() -> dict[str, str]:
        env = os.environ.copy()
        env["DEBIAN_FRONTEND"] = "noninteractive"
        return env

    def _apt_update(self) -> None:
        console.print("[cyan]→ apt-get update[/cyan]")
        subprocess.run(
            ["apt-get", "update"],
            env=self._apt_env(),
            check=True,
        )

    def _apt_install(self, packages: Iterable[str]) -> None:
        pkgs = list(packages)
        console.print(f"[cyan]→ apt-get install -y {' '.join(pkgs)}[/cyan]")
        subprocess.run(
            ["apt-get", "install", "-y", *pkgs],
            env=self._apt_env(),
            check=True,
        )

    def _enable_xrdp_service(self) -> None:
        console.print("[cyan]→ systemctl enable --now xrdp[/cyan]")
        subprocess.run(
            ["systemctl", "enable", "--now", "xrdp"],
            env=self._apt_env(),
            check=True,
        )

    def _verify(self, packages: Iterable[str]) -> None:
        console.print("[cyan]→ Verifikation[/cyan]")
        for pkg in packages:
            result = subprocess.run(
                ["dpkg-query", "-W", "-f=${Status}", pkg],
                env=self._apt_env(),
                check=False,
                text=True,
                capture_output=True,
            )
            installed = (
                result.returncode == 0
                and "install ok installed" in result.stdout
            )
            mark = "[green]OK[/green]" if installed else "[red]FAIL[/red]"
            console.print(f"  {mark} {pkg}")
            if not installed:
                raise RuntimeError(
                    f"Paket '{pkg}' nicht 'install ok installed' "
                    f"(dpkg-Status: '{result.stdout.strip() or 'leer'}')."
                )

        result = subprocess.run(
            ["systemctl", "is-active", "xrdp"],
            check=False,
            text=True,
            capture_output=True,
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"xrdp.service nicht aktiv "
                f"(is-active: '{result.stdout.strip() or 'leer'}')."
            )
        console.print("  [green]OK[/green] xrdp.service aktiv")
        console.print()
        console.print("[green]Display-Stack installiert.[/green]")
