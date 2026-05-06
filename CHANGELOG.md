# Changelog

Alle bemerkenswerten Änderungen an `xed-cca` werden hier dokumentiert.

Format folgt [Keep a Changelog](https://keepachangelog.com/de/1.1.0/),
Versionierung folgt [Semantic Versioning](https://semver.org/lang/de/).

## [0.0.5] — 2026-05-06

### Geändert (Architektur-Refactor)

- **Self-Heal-Pre-Phase auf ccc-Lib refactored** — `_self_heal_dpkg` in
  `cca/apps/gnome.py` ist jetzt 1-Zeilen-Aufruf (`self_heal_dpkg()`) statt
  ~30-Zeilen-Methode mit 4 inline-subprocess-Aufrufen. Cross-Repo-Import:
  `from ccc.system.self_heal import disable_pro_notice, self_heal_dpkg`.
- Lokal-Konstante `SNAP_REDIRECT_PACKAGES` aus `gnome.py` entfernt
  (Single-Source-of-Truth jetzt in `ccc.system.self_heal.constants`). DRY-
  Hygiene via Cross-Repo-Lib statt Duplikation.

### Hinzugefügt

- **Pro-Notice-Integration für Standalone-Path** — `_disable_pro_notice`-
  Methode in `gnome.py`, in `apply()`-Sequenz nach `_self_heal_dpkg` + vor
  `_setup_mozilla_apt_repo`. cca-User die `cca install gnome` direkt ohne
  firstboot-Vorlauf aufrufen sehen jetzt keine Pro-Werbung in `apt update`.
- Cross-Repo-Smoke-Test `tests/apps/test_gnome_imports.py` (2 Cases:
  GnomeApp-Import + `ccc.system.self_heal` Re-Exports validieren).

### Geändert (Dependency-Bump)

- `pyproject.toml` dependencies: neu `xed-ccc>=0.1.0` (war ohne Constraint).
  Ermöglicht Cross-Repo-Lib-Imports im stable Release-Channel.

[0.0.5]: https://github.com/XED-dev/CCA/releases/tag/v0.0.5

## [0.0.4] — 2026-05-04

### Geändert

- **Branding aktualisiert** — `cBUZZ Container App-Installation` →
  `cBOX@ /Container App-Installation`. Konsistente Brand-Identität für
  cBOX.at/YOU by XED.dev Tools via Collective Context (CC).
- `pyproject.toml` description + Typer-CLI-Help + README.md + Pages-Landing
  (`docs/index.html`: Title + h1 + Footer) konsistent gebrandet.
- keyword in `pyproject.toml`: `cbuzz` → `cbox`.

### Architektur

Keine Code-Logic-Änderung — reines Brand-Update als Patch-Bump.

[0.0.4]: https://github.com/XED-dev/CCA/releases/tag/v0.0.4

## [0.0.3] — 2026-05-04

### Bug-Fix

- **Snap-Redirect-Falle behoben** — auf Ubuntu 22.04+ ist `firefox` (und
  auch `thunderbird` / `chromium-browser`) als snap-Redirect-deb publiziert.
  Im LXC ohne lauffähigen snapd scheitert das Konfigurations-Skript des
  Pakets, was `apt-get install vanilla-gnome-desktop` mit Recommends ON
  bricht. Live-Apply v0.0.2 brach an genau dieser Stelle (5521-pmDESK
  noble, AI036 Session 2026-05-04).

### Hinzugefügt

- **Self-Heal-Pre-Phase** in `apply()`:
  1. `apt-get purge` für snap-Redirect-Pakete (firefox, thunderbird,
     chromium-browser, gnome-software-plugin-snap, snapd)
  2. `dpkg --configure -a` (finalisiert halb-konfigurierte Pakete)
  3. `apt-get install -f -y` (fixt broken dependencies)
  4. `apt-get autoremove --purge -y` (räumt orphaned locale-Pakete)

  Idempotent: no-op auf sauberem System, voll-aktiv auf broken System.
- **Mozilla Official APT-Repository** für Firefox-deb statt snap-Wrapper
  via `_setup_mozilla_apt_repo()`. Codename-conditional: nur für Ubuntu
  (noble/jammy/focal); Debian (bookworm/bullseye) hat firefox-esr ohne
  snap-Wrapper und braucht das Repo nicht.
- Recommends bleibt ON — vollständiger Desktop-Stack mit allen
  Standard-Tools.

### Architektur-Notiz

`_setup_mozilla_apt_repo()` ist heute in `gnome.py` lokalisiert. Bei einem
zweiten Konsumenten (z.B. künftiges `cca install thunderbird-deb`)
extrahieren wir nach `cca/apt/repos.py` (Rule of Three).

Pattern-Stein-Meißel: `reference_no_snap_in_lxc.md` (AI036, 2026-05-04).

[0.0.3]: https://github.com/XED-dev/CCA/releases/tag/v0.0.3

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
