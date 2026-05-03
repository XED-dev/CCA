"""App-Registry für xed-cca.

Jede App ist eine Klasse mit:
- description: Kurze Beschreibung der App
- is_implemented: True wenn Apply-Logik vollständig
- plan(): zeigt geplante Schritte (Dry-Run)
- apply(): führt die Schritte aus

Apps werden hier zentral registriert — `cca list` und `cca install <name>`
nutzen die `AVAILABLE_APPS`-Map.
"""

from __future__ import annotations

from typing import Optional, Type

from cca.apps.base import App
from cca.apps.gnome import GnomeApp
from cca.apps.ghost import GhostApp
from cca.apps.wordops import WordOpsApp
from cca.apps.miab import MiabApp

AVAILABLE_APPS: dict[str, Type[App]] = {
    "gnome": GnomeApp,
    "ghost": GhostApp,
    "wordops": WordOpsApp,
    "miab": MiabApp,
    # Geplant für künftige Sessions:
    # "nextcloud":   NextcloudApp,
    # "gitea":       GiteaApp,
    # "xrdp":        XrdpApp,
    # "nginx-rp":    NginxReverseProxyApp,
}


def get_app(name: str) -> Optional[Type[App]]:
    """Gibt die App-Klasse zum Namen zurück, oder None wenn unbekannt.

    Case-insensitiv beim Lookup, aber Display bleibt case-sensitive.
    """
    for registered_name, app_class in AVAILABLE_APPS.items():
        if registered_name.lower() == name.lower():
            return app_class
    return None
