"""miab-App: Mail-in-a-Box.

Stub-Implementation — Plan zeigt geplante Schritte. Apply kommt mit
erstem Apply-Sprint.

Referenz: <https://mailinabox.email/>
Plus: AI035-Memory `reference_curl_bash_process_substitution.md` (Mailinabox
ist DAS Pattern-Vorbild für interaktive curl-Bash-Installer).
"""

from __future__ import annotations

from rich.console import Console

from cca.apps.base import App

console = Console()


class MiabApp(App):
    """miab — Mail-in-a-Box (vollständiger Mail-Server-Stack)."""

    description = "Mail-in-a-Box (Postfix + Dovecot + Nextcloud + Roundcube + Z-Push)"
    is_implemented = False

    def plan(self) -> None:
        steps = [
            ("1.", "Pre-Flight: Public-IPv4, FQDN, DNS-Setup-Voraussetzungen"),
            ("2.", "Mailinabox-Bootstrap: bash <(curl -s https://mailinabox.email/setup.sh)"),
            ("3.", "Interaktive Konfig: PRIMARY_HOSTNAME, STORAGE_USER, STORAGE_ROOT"),
            ("4.", "Service-Stack: Postfix, Dovecot, OpenDKIM, Spamassassin"),
            ("5.", "Web-Stack: Roundcube (Webmail), Nextcloud (Cal/Cards/Files)"),
            ("6.", "Z-Push für Mobile-Sync (ActiveSync)"),
            ("7.", "Let's Encrypt für SMTP-/IMAP-/HTTPS-Zertifikate"),
        ]
        console.print("[bold]Geplante Schritte:[/bold]")
        for num, desc in steps:
            console.print(f"  {num} {desc}")
        console.print(
            "\n[dim]Hinweis: Mailinabox ist Process-Substitution-Vorbild "
            "(Memory 'reference_curl_bash_process_substitution.md'). Apply-"
            "Logic muss bash <(curl -s ...) statt curl|bash nutzen für TTY-"
            "Erhalt.[/dim]"
        )

    def apply(self) -> None:
        raise NotImplementedError(
            "miab.apply() ist noch ein Stub. "
            "Implementation kommt mit dem ersten Apply-Sprint."
        )
