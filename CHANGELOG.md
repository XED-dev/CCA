# Changelog

Alle bemerkenswerten Änderungen an `xed-cca` werden hier dokumentiert.

Format folgt [Keep a Changelog](https://keepachangelog.com/de/1.1.0/),
Versionierung folgt [Semantic Versioning](https://semver.org/lang/de/).

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
