"""gnome-App: Vanilla Gnome Desktop für LXC-Boxen.

Atomar (cca §9): Display-Stack only. Distro-aware Paket-Auswahl
(Debian: gnome-core / Ubuntu: vanilla-gnome-desktop) plus xrdp +
xorgxrdp + dbus-x11 als Display-Server-Subset.

SysOps-User + Wayland-Bind-mount sind keine cca-Verantwortung —
gehören in ``ccc create pmDESK`` als Komposition.

v0.0.3: Self-Heal-Pre-Phase + Mozilla-APT-Repo für Firefox-deb statt
snap-Wrapper (snapd ist im LXC unzuverlässig — Squashfs/udev/cgroups).
Codename-Conditional folgt dem WordOps-Pattern aus AI034
(`reference_wordops_install_quirks.md`). Snap-LXC-Pattern in
`reference_no_snap_in_lxc.md`.
"""

from __future__ import annotations

import os
import subprocess
import urllib.request
from pathlib import Path
from typing import Iterable

from rich.console import Console

from ccc.system.self_heal import disable_pro_notice, self_heal_dpkg

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

# Codenames für die das Mozilla-APT-Repo gebraucht wird (Ubuntu mit snap-Falle).
# Debian (bookworm/bullseye) hat firefox-esr ohne snap-Wrapper, kein Repo nötig.
UBUNTU_CODENAMES: frozenset[str] = frozenset({"noble", "jammy", "focal"})

# SNAP_REDIRECT_PACKAGES + CRITICAL_PACKAGES_WHITELIST liegen ab v0.0.5
# in ccc.system.self_heal.constants (single source of truth fuer firstboot
# + ccc-Rollen + cca-Apps). Import oben.

# Mozilla Official APT-Repository für Firefox + Thunderbird als deb.
# Quelle: https://packages.mozilla.org/apt
MOZILLA_APT_KEY_URL = "https://packages.mozilla.org/apt/repo-signing-key.gpg"
MOZILLA_APT_KEYRING = "/etc/apt/keyrings/packages.mozilla.org.asc"
MOZILLA_APT_SOURCES_FILE = "/etc/apt/sources.list.d/mozilla.list"
MOZILLA_APT_PIN_FILE = "/etc/apt/preferences.d/mozilla"
MOZILLA_APT_SOURCES_LINE = (
    "deb [signed-by=/etc/apt/keyrings/packages.mozilla.org.asc] "
    "https://packages.mozilla.org/apt mozilla main"
)
MOZILLA_APT_PIN_CONTENT = (
    "Package: *\n"
    "Pin: origin packages.mozilla.org\n"
    "Pin-Priority: 1000\n"
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
            ("3.", "Self-Heal: snap-Redirect-Pakete entfernen"),
            ("",   "    firefox, thunderbird, chromium-browser,"),
            ("",   "    gnome-software-plugin-snap, snapd"),
            ("4.", "Self-Heal: dpkg --configure -a + apt install -f + autoremove"),
            ("5.", "Mozilla-APT-Repo (nur Ubuntu): Key + Sources + Pin (Priority 1000)"),
            ("6.", "apt-get update + apt-get install -y <Desktop-Meta> xrdp xorgxrdp dbus-x11"),
            ("7.", "systemctl enable --now xrdp"),
            ("8.", "Verifikation: dpkg-Status pro Paket + xrdp-Service aktiv"),
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

        self._self_heal_dpkg()
        self._disable_pro_notice()
        if codename in UBUNTU_CODENAMES:
            self._setup_mozilla_apt_repo()
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

    def _self_heal_dpkg(self) -> None:
        """Self-Heal-Pre-Phase via ccc.system.self_heal.self_heal_dpkg Composite.

        Lib uebernimmt: snap-Redirect-Purge mit Cascade-Schutz (safe_purge),
        dpkg --configure -a, apt-get install -f, apt-get autoremove --purge.
        DEBIAN_FRONTEND=noninteractive wird Lib-intern gesetzt (cca-Standalone-
        Path-Schutz). Defaults SNAP_REDIRECT_PACKAGES + CRITICAL_PACKAGES_WHITELIST
        kommen aus ccc.system.self_heal.constants.
        """
        console.print(
            "[cyan]→ Self-Heal: dpkg/apt-State "
            "(snap-purge + dpkg-cfg + apt-fix + autoremove via Lib)[/cyan]"
        )
        self_heal_dpkg()

    def _disable_pro_notice(self) -> None:
        """Ubuntu-Pro-Werbung non-destruktiv deaktivieren via Lib-Helper.

        Sub-Sprint 2 Modul #5: cca-Standalone-Path soll auch ohne firstboot
        vorab keine Pro-Werbung in apt update zeigen (Bash-firstboot Phase 6
        ruft self_heal_dpkg + self_heal_pro_notice IMMER zusammen — analog
        hier UX-Entkopplung von firstboot.sh).
        """
        console.print("[cyan]→ Self-Heal: Ubuntu-Pro-Werbung deaktivieren[/cyan]")
        disable_pro_notice()

    def _setup_mozilla_apt_repo(self) -> None:
        """Setup Mozilla Official APT-Repository für Firefox-deb statt
        snap-Wrapper. Idempotent: Files werden überschrieben, gleicher
        Inhalt = no-op effektiv. APT-Pin (Priority 1000) schlägt das
        Standard-Ubuntu-Archiv und verhindert dass der Wrapper-Wrapper-deb
        den Mozilla-deb verdrängt.
        """
        console.print("[cyan]→ Mozilla-Repo: Keyring herunterladen[/cyan]")
        Path("/etc/apt/keyrings").mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(MOZILLA_APT_KEY_URL, timeout=30) as response:
            Path(MOZILLA_APT_KEYRING).write_bytes(response.read())
        Path(MOZILLA_APT_KEYRING).chmod(0o644)

        console.print(f"[cyan]→ Mozilla-Repo: {MOZILLA_APT_SOURCES_FILE}[/cyan]")
        Path(MOZILLA_APT_SOURCES_FILE).write_text(MOZILLA_APT_SOURCES_LINE + "\n")

        console.print(f"[cyan]→ Mozilla-Repo: APT-Pin {MOZILLA_APT_PIN_FILE}[/cyan]")
        Path(MOZILLA_APT_PIN_FILE).write_text(MOZILLA_APT_PIN_CONTENT)

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
        # Recommends ON (Default) — vollständiger Desktop-Stack mit allen
        # Standard-Tools. Snap-Falle ist durch _self_heal_dpkg +
        # _setup_mozilla_apt_repo bereits abgewehrt.
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
