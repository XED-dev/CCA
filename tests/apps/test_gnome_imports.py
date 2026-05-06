"""Smoke-Tests fuer cca.apps.gnome — Cross-Repo-Import-Verifikation.

Sub-Sprint 2 Modul #5: validiert dass cca.apps.gnome die ccc.system.self_heal
Lib-Composites (self_heal_dpkg, disable_pro_notice) sauber importiert. Plus
Re-Export-Verifikation der Lib selbst.

PYTHONPATH muss src + ../XED-CCC/src enthalten (Cross-Repo-Editable-Modus).
"""

from __future__ import annotations


def test_gnome_imports():
    from cca.apps.gnome import GnomeApp

    assert GnomeApp.is_implemented


def test_self_heal_lib_reexports():
    """Re-Exports validieren — safe_purge + disable_pro_notice + self_heal_dpkg."""
    from ccc.system.self_heal import (
        disable_pro_notice,
        safe_purge,
        self_heal_dpkg,
    )

    assert callable(safe_purge)
    assert callable(disable_pro_notice)
    assert callable(self_heal_dpkg)
