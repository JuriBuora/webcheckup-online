#!/usr/bin/env python3
"""Create a simple client audit folder structure and starter files."""

from __future__ import annotations

import argparse
from datetime import date
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = PROJECT_ROOT / "templates"
CHECKLISTS_DIR = PROJECT_ROOT / "checklists"
INTERNATIONAL_TEMPLATES_DIR = TEMPLATES_DIR / "international"
SUPPORTED_LANGUAGES = ("it", "en", "pl", "ro")
DEFAULT_PRICE = "€49"
DEFAULT_DELIVERY_PROMISE = "entro 2 giorni lavorativi dopo conferma pagamento"
DEFAULT_REVISION_PROMISE = "1 giro chiarimenti entro 7 giorni"

# The client-facing "message for your web developer" text, one per supported
# language. Everything else the operator sees (notes.md, handoff.md) stays in
# Italian on purpose, since that's Juri's own working language - only text
# that gets forwarded to the client or their web developer is localized.
WEBMASTER_MESSAGE_BY_LANG = {
    "it": {
        "heading": "# Messaggio per il webmaster",
        "intro": "Ciao, abbiamo fatto un check-up esterno e non invasivo del sito {website}.",
        "priorities_label": "Le priorita principali da verificare sono:",
        "closing": "Puoi controllare fattibilita, tempi, costi ed eventuali rischi di compatibilita?",
        "offer": "Se serve, posso condividere il report completo del check-up di {client_name}.",
    },
    "en": {
        "heading": "# Message for your web developer",
        "intro": "Hi, we've had an external, non-invasive check-up of the website {website} done.",
        "priorities_label": "The main priorities to check are:",
        "closing": "Could you check feasibility, timing, cost and any compatibility risks?",
        "offer": "If useful, I can share the full check-up report for {client_name}.",
    },
    "pl": {
        "heading": "# Wiadomość dla webmastera",
        "intro": "Cześć, zrobiliśmy zewnętrzny, nieinwazyjny check-up strony {website}.",
        "priorities_label": "Główne priorytety do sprawdzenia to:",
        "closing": "Możesz sprawdzić wykonalność, czas, koszt i ewentualne ryzyka związane z kompatybilnością?",
        "offer": "Jeśli przyda się, mogę udostępnić pełny raport z check-upu dla {client_name}.",
    },
    "ro": {
        "heading": "# Mesaj pentru webmaster",
        "intro": "Buna, am facut o verificare externa si neinvaziva a site-ului {website}.",
        "priorities_label": "Prioritatile principale de verificat sunt:",
        "closing": "Poti verifica fezabilitatea, timpul, costul si eventualele riscuri de compatibilitate?",
        "offer": "Daca e util, pot trimite raportul complet al verificarii pentru {client_name}.",
    },
}


def slugify(value: str) -> str:
    """Return a filesystem-friendly folder name."""
    value = value.strip().lower()
    value = re.sub(r"[^\w]+", "-", value, flags=re.UNICODE)
    value = re.sub(r"-{2,}", "-", value)
    return value.strip("-") or "cliente"


def normalize_website(value: str) -> str:
    website = value.strip()
    if not website:
        return "https://www.esempio.it"
    if "://" not in website:
        return f"https://{website}"
    return website


def replace_placeholders(template: str, client_name: str, website: str, audit_date: str) -> str:
    replacements = {
        "[Nome attività]": client_name,
        "[Nome attivita]": client_name,
        "[https://www.esempio.it]": website,
        "[GG/MM/AAAA]": audit_date,
        "{{BUSINESS}}": client_name,
        "{{URL}}": website,
        "{{DATA}}": audit_date,
    }
    content = template
    for source, target in replacements.items():
        content = content.replace(source, target)
    return content


def write_if_missing(path: Path, content: str) -> None:
    if not path.exists():
        path.write_text(content, encoding="utf-8")


def build_notes_content(
    client_name: str,
    website: str,
    contact_email: str,
    audit_date: str,
    price: str,
    contact_name: str,
    lead_source: str,
    language: str = "it",
) -> str:
    return "\n".join(
        [
            f"# {client_name}",
            "",
            "## Scheda cliente",
            "",
            "- Stato: lead confermato / audit da iniziare",
            f"- Sito: {website}",
            f"- Contatto: {contact_email or '[da inserire]'}",
            f"- Referente: {contact_name or '[da inserire]'}",
            f"- Fonte lead: {lead_source or '[da inserire]'}",
            f"- Lingua cliente: {language} (report, sintesi e messaggi vanno generati in questa lingua)",
            f"- Data apertura: {audit_date}",
            "- Obiettivo principale:",
            "",
            "## Commerciale",
            "",
            f"- Prezzo concordato: {price}",
            "- Pagamento: bonifico bancario (IBAN nel messaggio di conferma)",
            "- Data pagamento:",
            f"- Consegna standard promessa: {DEFAULT_DELIVERY_PROMISE}",
            "- Data consegna promessa:",
            f"- Revisione inclusa: {DEFAULT_REVISION_PROMISE}",
            "- PDF consegnato: no",
            "",
            "## Evidenze da raccogliere",
            "",
            "- Screenshot desktop:",
            "- Screenshot mobile:",
            "- Speed test:",
            "- HTTPS/TLS:",
            "- Header browser:",
            "- SEO base:",
            "- Privacy/cookie:",
            "- Link/CTA:",
            "",
            "## Post consegna",
            "",
            "- Testimonianza richiesta: no",
            "- Cliente ha inoltrato al webmaster:",
            "- Follow-up fissato per:",
            "",
            "## Note",
            "",
            "- ",
            "",
        ]
    )


def build_webmaster_message(client_name: str, website: str, language: str = "it") -> str:
    strings = WEBMASTER_MESSAGE_BY_LANG.get(language, WEBMASTER_MESSAGE_BY_LANG["it"])
    placeholder_lines = {
        "it": ["- [Priorita 1]", "- [Priorita 2]", "- [Priorita 3]"],
        "en": ["- [Priority 1]", "- [Priority 2]", "- [Priority 3]"],
        "pl": ["- [Priorytet 1]", "- [Priorytet 2]", "- [Priorytet 3]"],
        "ro": ["- [Prioritatea 1]", "- [Prioritatea 2]", "- [Prioritatea 3]"],
    }.get(language, ["- [Priorita 1]", "- [Priorita 2]", "- [Priorita 3]"])

    return "\n".join(
        [
            strings["heading"],
            "",
            strings["intro"].format(website=website),
            "",
            strings["priorities_label"],
            "",
            *placeholder_lines,
            "",
            strings["closing"],
            "",
            strings["offer"].format(client_name=client_name),
            "",
        ]
    )


def build_handoff_content(client_name: str, website: str, audit_date: str, language: str = "it") -> str:
    return "\n".join(
        [
            f"# Handoff - {client_name}",
            "",
            f"- Sito: {website}",
            f"- Lingua cliente: {language}",
            "- Stato: lead confermato / audit non iniziato",
            f"- Ultimo aggiornamento: {audit_date}",
            "- Obiettivo corrente: produrre il report PDF iniziale",
            "",
            "## Gia pronto",
            "",
            "- Cartella cliente creata",
            "- Template report creato",
            "- Template messaggi creati",
            "",
            "## Prossime azioni",
            "",
            "1. Aggiornare `notes.md` con dati reali e stato commerciale.",
            "2. Salvare screenshot e risultati tecnici in `screenshots/` e `raw-results/`.",
            "3. Compilare `report/report-completo.md`.",
            "4. Spuntare `report/checklist-prima-consegna.md` prima della generazione finale.",
            "5. Generare e controllare il PDF.",
            "",
            "## Da ricontrollare",
            "",
            "- Nessuna affermazione legale o di sicurezza assoluta.",
            "- Messaggi finali brevi e leggibili da telefono.",
            "- PDF verificato visivamente prima dell'invio.",
            "",
            "## Non fare",
            "",
            "- Non eseguire test invasivi.",
            "- Non inviare email automatiche senza approvazione umana.",
            "",
        ]
    )


def resolve_templates_dir(language: str) -> Path:
    """Return the template directory for the client's language.

    Italian keeps using the historical `templates/` root. Other supported
    languages read from `templates/international/<language>/`, which mirrors
    the same file names so the rest of this script doesn't need to branch."""
    if language == "it":
        return TEMPLATES_DIR
    lang_dir = INTERNATIONAL_TEMPLATES_DIR / language
    if not lang_dir.is_dir():
        raise SystemExit(
            f"No templates found for language '{language}' at {lang_dir}. "
            f"Supported languages: {', '.join(SUPPORTED_LANGUAGES)}."
        )
    return lang_dir


def create_client_folder(
    client_name: str,
    base_dir: Path,
    website: str,
    contact_email: str,
    price: str,
    contact_name: str,
    lead_source: str,
    language: str = "it",
) -> Path:
    client_dir = base_dir / slugify(client_name)
    subfolders = ["screenshots", "raw-results", "report"]
    audit_date = date.today().strftime("%d/%m/%Y")
    website = normalize_website(website)
    templates_dir = resolve_templates_dir(language)

    client_dir.mkdir(parents=True, exist_ok=True)
    for folder in subfolders:
        (client_dir / folder).mkdir(exist_ok=True)

    notes_file = client_dir / "notes.md"
    write_if_missing(
        notes_file,
        build_notes_content(
            client_name,
            website,
            contact_email,
            audit_date,
            price,
            contact_name,
            lead_source,
            language,
        ),
    )

    audit_template = (templates_dir / "audit-report-template.md").read_text(encoding="utf-8")
    phone_summary_template = (
        templates_dir / "summary-cliente-phone-template.md"
    ).read_text(encoding="utf-8")
    delivery_template = (templates_dir / "delivery-message-template.md").read_text(
        encoding="utf-8"
    )
    # The delivery QA gate stays Italian regardless of client language: Juri
    # is the one running this checklist himself before every send.
    report_ready_checklist = (
        CHECKLISTS_DIR / "report-ready-qa-checklist.md"
    ).read_text(encoding="utf-8")

    report_dir = client_dir / "report"
    write_if_missing(
        report_dir / "report-completo.md",
        replace_placeholders(audit_template, client_name, website, audit_date),
    )
    write_if_missing(
        report_dir / "summary-cliente-phone.md",
        replace_placeholders(phone_summary_template, client_name, website, audit_date),
    )
    write_if_missing(
        report_dir / "messaggio-consegna.md",
        replace_placeholders(delivery_template, client_name, website, audit_date),
    )
    write_if_missing(
        report_dir / "messaggio-webmaster.md",
        build_webmaster_message(client_name, website, language),
    )
    write_if_missing(
        report_dir / "checklist-prima-consegna.md",
        report_ready_checklist,
    )
    write_if_missing(
        client_dir / "handoff.md",
        build_handoff_content(client_name, website, audit_date, language),
    )

    return client_dir


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create folders for a website check-up client."
    )
    parser.add_argument("client_name", help='Client or business name, e.g. "Agriturismo Rossi"')
    parser.add_argument(
        "--base-dir",
        default="clients",
        help='Where to create the client folder. Default: "clients"',
    )
    parser.add_argument(
        "--website",
        default="https://www.esempio.it",
        help='Public website URL to prefill in starter files.',
    )
    parser.add_argument(
        "--contact-email",
        default="",
        help="Primary client email or empty if not yet known.",
    )
    parser.add_argument(
        "--contact-name",
        default="",
        help="Primary client contact person if already known.",
    )
    parser.add_argument(
        "--lead-source",
        default="",
        help="Where this lead came from (outreach, referral, landing page, etc.).",
    )
    parser.add_argument(
        "--price",
        default=DEFAULT_PRICE,
        help='Agreed price to write into `notes.md`. Default: "€49"',
    )
    parser.add_argument(
        "--language",
        choices=SUPPORTED_LANGUAGES,
        default="it",
        help="Client-facing language for the report and messages: match this to where the "
        "lead came from (e.g. Fonte: landing-page-en in the notification email -> --language en). "
        "Default: it.",
    )

    args = parser.parse_args()
    created_path = create_client_folder(
        args.client_name,
        Path(args.base_dir),
        args.website,
        args.contact_email,
        args.price,
        args.contact_name,
        args.lead_source,
        args.language,
    )
    print(f"Created client audit folder: {created_path}")


if __name__ == "__main__":
    main()
