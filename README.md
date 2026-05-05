# XED /CCA — cBOX@ /Container App-Installation

> **Atomare App-Stack-Installation für LXC-Boxen** — Pendant zu
> [xed-ccc](https://github.com/XED-dev/CCC) (Container-Lifecycle).
>
> Status: **v0.0.1 Skelett** — Stubs mit Plan-Output, Apply-Implementation kommt cycle-für-cycle
> Lizenz: MIT
> Distribution: <https://pypi.org/project/xed-cca/> (geplant: <https://cca.xed.dev>)

---

## Architektur — zwei Tools, klare Trennung

| Tool | Verantwortung | Beispiele |
|---|---|---|
| **`ccc`** | Container-Lifecycle + Rollen-Kompositionen | `ccc create pmDESK` (komponiert: gnome + xrdp + SysOps-User) |
| **`cca`** | Atomare App-Stack-Installation | `cca install gnome`, `cca install ghost`, `cca install miab` |

`ccc`-Rollen rufen intern `cca`-Apps auf. Wer eine maßgeschneiderte Box
will, nutzt `cca` direkt. Wer eine vorgefertigte Rolle will, nutzt `ccc create`.

---

## Schnellstart

```bash
# Variante A — automatisch via firstboot.sh Phase 7 (xed-ccc + xed-cca beide):
bash <(curl -s https://ccc.xed.dev/firstboot.sh)

# Variante B — PyPI direkt:
pipx install xed-cca
```

## Verben (analog `apt`)

```bash
cca list                     # verfügbare Apps mit Status
cca install gnome            # App installieren
cca install ghost --dry-run  # nur Plan zeigen
cca menu                     # interaktive TUI (Stub, Textual kommt später)
cca --version
cca --help
```

## Apps-Roadmap (v0.0.1 Stubs)

| App | Beschreibung | Status |
|---|---|---|
| `gnome` | Vanilla Gnome Desktop (Debian: `gnome-core`, Ubuntu: `vanilla-gnome-desktop`) | Stub |
| `ghost` | Ghost Headless CMS / Blog-Engine (Node + DB + nginx) | Stub |
| `wordops` | LEMP-Stack-Manager (NGINX + PHP-FPM + MariaDB) | Stub |
| `miab` | Mail-in-a-Box (vollständiger Mail-Server-Stack) | Stub |

Geplant für künftige Sessions: `nextcloud`, `gitea`, `xrdp`, `nginx-rp`, weitere.

---

## Lizenz

MIT — siehe [LICENSE](LICENSE).
