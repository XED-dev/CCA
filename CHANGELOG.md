# Changelog

Alle bemerkenswerten Änderungen an `xed-cca` werden hier dokumentiert.

Format folgt [Keep a Changelog](https://keepachangelog.com/de/1.1.0/),
Versionierung folgt [Semantic Versioning](https://semver.org/lang/de/).

## [0.0.2] — 2026-05-03

### Hinzugefügt

- **`gnome.apply()` implementiert** — `cca install gnome` ist nicht mehr Stub.
  Atomar (cca §9): nur Display-Stack. Codename-conditional Desktop-Meta-Paket
  (`vanilla-gnome-desktop` für noble/jammy/focal, `gnome-core` für
  bookworm/bullseye) plus `xrdp` + `xorgxrdp` + `dbus-x11`.
  Apply-Schritte: Distro-Erkennung → apt-Install → `systemctl enable --now xrdp`
  → Verifikation (dpkg-Status + service-active-Check).
- **Pre-Flight-Check:** `apply()` wirft RuntimeError mit klarer Meldung wenn
  nicht-root, wenn `/etc/os-release` fehlt, oder wenn der Codename nicht in
  `CODENAME_DESKTOP_PACKAGE` registriert ist.

### Geändert

- `GnomeApp.is_implemented = True` (vorher `False`)
- `GnomeApp.plan()` zeigt reduzierten atomaren Scope (5 Schritte statt 6:
  SysOps-User + Wayland-Bind-mount entfernt — gehören in `ccc create pmDESK`).

### Architektur-Notiz

`cca`-Apps sind atomar (eine App, ein Stack). Container-Lifecycle-Aufgaben
wie SysOps-User-Setup oder Wayland-Bind-mount gehören in `ccc`-Rollen-
Kompositionen, nicht in `cca`-Apps.

[0.0.2]: https://github.com/XED-dev/CCA/releases/tag/v0.0.2

## [0.0.1] — 2026-05-03

### Hinzugefügt

- **PyPI-Skelett** — Name-Reservierung auf <https://pypi.org/project/xed-cca/>
- **CLI-Skelett** mit drei Top-Level-Commands (analog `apt` und xed-ccc):
  - `cca list` — verfügbare Apps mit Status
  - `cca install <app> [--dry-run]` — App installieren (heute Plan-Output)
  - `cca menu` — TUI-Stub (Textual kommt später)
- **App-Registry** in `src/cca/apps/`:
  - `gnome` — Vanilla Gnome Desktop (Debian/Ubuntu, Distro-aware)
  - `ghost` — Ghost CMS / Blog-Engine (Node + DB + nginx)
  - `wordops` — LEMP-Stack-Manager (referenziert AI034-Memory)
  - `miab` — Mail-in-a-Box (referenziert AI035-Memory zu Process-Substitution)
- **Architektur-Trennung zu xed-ccc:**
  - `ccc` = Container-Lifecycle + Rollen-Kompositionen
  - `cca` = atomare App-Stack-Installation

### Architektur-Hinweise

- Python ≥ 3.11, hatchling-Build-Backend, Typer + Rich als Dependencies
- `pyproject.toml` mit dynamischer Versionierung aus `src/cca/_version.py`
- Optional-Dependencies: `tui` (Textual), `dev` (pytest)

[0.0.1]: https://github.com/XED-dev/CCA/releases/tag/v0.0.1
