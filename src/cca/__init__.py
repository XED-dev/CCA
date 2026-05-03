"""xed-cca — cBUZZ Container App-Installation.

Atomare App-Installation in LXC-Boxen. Pendant zu xed-ccc:
- ccc verwaltet Container-Lifecycle + Rollen-Kompositionen (lxcHOST/pmDESK/...)
- cca installiert atomare App-Stacks (gnome/ghost/wordops/miab/...)

Verben analog `pct` und `apt`:
  cca list                  # verfügbare Apps mit Status
  cca install <app>         # App-Stack installieren
  cca menu                  # interaktive TUI (Stub, Textual kommt später)
"""

from cca._version import __version__

__all__ = ["__version__"]
