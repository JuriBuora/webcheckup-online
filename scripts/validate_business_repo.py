#!/usr/bin/env python3
"""Validate repo consistency and scaffold behavior for the mini-audit business."""

from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CREATE_CLIENT_SCRIPT = PROJECT_ROOT / "scripts" / "create_client_folder.py"

CORE_FILES = [
    PROJECT_ROOT / "README.md",
    PROJECT_ROOT / "offer" / "mini-audit-one-page.md",
    PROJECT_ROOT / "offer" / "faq-obiezioni.md",
    PROJECT_ROOT / "offer" / "scala-servizi.md",
    PROJECT_ROOT / "operations" / "payment-and-delivery-flow.md",
    PROJECT_ROOT / "landing-page" / "index.html",
    PROJECT_ROOT / "landing-page" / "PRE-DEPLOY-CHECK.md",
    PROJECT_ROOT / "checklists" / "report-ready-qa-checklist.md",
    PROJECT_ROOT / "scripts" / "create_client_folder.py",
    PROJECT_ROOT / "scripts" / "generate_report_pdf.py",
    PROJECT_ROOT / "landing-page" / "robots.txt",
    PROJECT_ROOT / "landing-page" / "sitemap.xml",
    PROJECT_ROOT / "SECURITY.md",
]

LANDING_PAGES = [
    PROJECT_ROOT / "landing-page" / "index.html",
    PROJECT_ROOT / "landing-page" / "en" / "index.html",
    PROJECT_ROOT / "landing-page" / "pl" / "index.html",
    PROJECT_ROOT / "landing-page" / "ro" / "index.html",
]

CONTENT_CHECKS = {
    PROJECT_ROOT / "offer" / "mini-audit-one-page.md": [
        "€49",
        "2 giorni lavorativi dopo conferma pagamento",
        "Check-up del Sito Web",
        "bonifico bancario",
        "ricevuta semplice",
    ],
    PROJECT_ROOT / "operations" / "payment-and-delivery-flow.md": [
        "€49",
        "2 giorni lavorativi",
        "bonifico bancario",
        "ricevuta semplice",
    ],
    PROJECT_ROOT / "landing-page" / "index.html": [
        "Richiedi il check-up",
        "Analisi esterna e non invasiva - non e un pen-test.",
        "2 giorni lavorativi",
    ],
    PROJECT_ROOT / "landing-page" / "PRE-DEPLOY-CHECK.md": [
        "Deploy is a HUMAN step",
        "€49",
    ],
}


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def validate_core_files() -> None:
    missing = [str(path.relative_to(PROJECT_ROOT)) for path in CORE_FILES if not path.exists()]
    if missing:
        fail(f"missing core files: {', '.join(missing)}")
    print("OK core files exist")


def validate_content_checks() -> None:
    for path, snippets in CONTENT_CHECKS.items():
        text = path.read_text(encoding="utf-8")
        for snippet in snippets:
            if snippet not in text:
                fail(f"{path.relative_to(PROJECT_ROOT)} is missing expected text: {snippet}")
    print("OK repo content checks")


def validate_landing_page_hardening() -> None:
    for page in LANDING_PAGES:
        text = page.read_text(encoding="utf-8")
        for snippet in [
            'http-equiv="Content-Security-Policy"',
            'name="referrer" content="strict-origin-when-cross-origin"',
            'name="Conferma sito pubblico"',
            'name="Conferma informativa privacy"',
            'id="privacy-ack"',
            'href="privacy.html"',
        ]:
            if snippet not in text:
                fail(f"{page.relative_to(PROJECT_ROOT)} is missing hardening: {snippet}")

        privacy_page = page.parent / "privacy.html"
        if not privacy_page.exists():
            fail(f"{page.relative_to(PROJECT_ROOT)} is missing matching privacy page")

    intake_script = (PROJECT_ROOT / "landing-page" / "intake.js").read_text(encoding="utf-8")
    for snippet in ["summaryBox.replaceChildren", "new URLSearchParams", "submissionNonceKey"]:
        if snippet not in intake_script:
            fail(f"landing-page/intake.js is missing hardening: {snippet}")
    if "summaryBox.innerHTML" in intake_script:
        fail("landing-page/intake.js must not render request data with innerHTML")

    sitemap = (PROJECT_ROOT / "landing-page" / "sitemap.xml").read_text(encoding="utf-8")
    for url in ["https://www.webcheckup.online/", "/en/", "/pl/", "/ro/"]:
        if url not in sitemap:
            fail(f"landing-page/sitemap.xml is missing URL: {url}")
    print("OK landing-page hardening checks")


def validate_scaffold() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        base_dir = Path(tmpdir) / "clients"
        cmd = [
            sys.executable,
            str(CREATE_CLIENT_SCRIPT),
            "Attivita Demo",
            "--base-dir",
            str(base_dir),
            "--website",
            "demo.example.it",
            "--contact-email",
            "demo@example.it",
            "--contact-name",
            "Mario Demo",
            "--lead-source",
            "landing page",
        ]
        subprocess.run(cmd, check=True, capture_output=True, text=True)

        client_dir = base_dir / "attivita-demo"
        required_paths = [
            client_dir / "notes.md",
            client_dir / "handoff.md",
            client_dir / "report" / "report-completo.md",
            client_dir / "report" / "summary-cliente-phone.md",
            client_dir / "report" / "messaggio-consegna.md",
            client_dir / "report" / "messaggio-webmaster.md",
            client_dir / "report" / "checklist-prima-consegna.md",
        ]
        missing = [str(path.relative_to(client_dir)) for path in required_paths if not path.exists()]
        if missing:
            fail(f"scaffold missing files: {', '.join(missing)}")

        notes = (client_dir / "notes.md").read_text(encoding="utf-8")
        report = (client_dir / "report" / "report-completo.md").read_text(encoding="utf-8")
        summary = (client_dir / "report" / "summary-cliente-phone.md").read_text(encoding="utf-8")
        delivery = (client_dir / "report" / "messaggio-consegna.md").read_text(encoding="utf-8")

        for snippet in [
            "https://demo.example.it",
            "demo@example.it",
            "Mario Demo",
            "landing page",
            "€49",
            "2 giorni lavorativi dopo conferma pagamento",
        ]:
            if snippet not in notes:
                fail(f"notes scaffold missing expected value: {snippet}")

        for snippet in [
            "**Cliente:** Attivita Demo",
            "**Sito analizzato:** https://demo.example.it",
        ]:
            if snippet not in report:
                fail(f"report scaffold missing expected value: {snippet}")

        if "{{BUSINESS}}" in report or "{{URL}}" in report or "{{DATA}}" in report:
            fail("report scaffold still contains top-level metadata placeholders")

        if "Attivita Demo" not in summary or "https://demo.example.it" not in delivery:
            fail("summary or delivery scaffold was not personalized")

    print("OK scaffold smoke test")


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate the mini-audit repo and scaffold behavior.")
    parser.add_argument(
        "--scaffold-only",
        action="store_true",
        help="Run only the client scaffold smoke test.",
    )
    parser.add_argument(
        "--repo-only",
        action="store_true",
        help="Run only repo/document consistency checks.",
    )
    args = parser.parse_args()

    if args.scaffold_only and args.repo_only:
        fail("use either --scaffold-only or --repo-only, not both")

    if not args.scaffold_only:
        validate_core_files()
        validate_content_checks()
        validate_landing_page_hardening()

    if not args.repo_only:
        validate_scaffold()

    print("All checks passed")


if __name__ == "__main__":
    main()
