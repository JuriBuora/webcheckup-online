# Handoff - WebCheckup

## Purpose

This project is a lightweight monetization project for Juri Buora.

The service is a low-cost, non-invasive website check-up for small Italian businesses. It is positioned as:

> WebCheckup — Sicurezza, Fiducia e Visibilità

The goal is to sell practical website audits for **€49** and deliver a simple PDF report with clear findings, screenshots, priorities, business impact, and practical recommendations.

This is **not** a penetration test.

## Important Safety Constraints

Always keep the audit external and non-invasive.

Allowed:

- visit public pages
- capture screenshots
- inspect visible HTML/rendered DOM
- check HTTP/HTTPS headers
- check TLS certificate metadata
- run Lighthouse/PageSpeed-style tests
- manually review visible SEO, cookie/privacy, trust and conversion elements
- check main public links lightly

Do not do:

- exploitation
- brute forcing
- login testing
- password testing
- directory fuzzing
- vulnerability exploitation
- aggressive crawling
- intrusive scanners
- sqlmap
- Nessus
- Burp Suite intrusive testing
- legal/GDPR compliance claims

Use this disclaimer in reports:

> Nota importante: questo check-up è un'analisi esterna e non invasiva del sito web. Non include penetration test, scansioni aggressive, accesso ad aree riservate, test su login, exploit o verifiche legali complete. Le osservazioni su privacy/cookie non costituiscono consulenza legale, ma indicano elementi visibili che possono essere verificati con il proprio consulente o fornitore web.

## Project Location

Canonical project folder:

```text
/Users/juribuora/webcheckup
```

For compatibility, `/Users/juribuora/website-trust-security-mini-audit` is a symlink to this canonical folder. Historical notes below may use the legacy path.

Important files:

```text
/Users/juribuora/website-trust-security-mini-audit/README.md
/Users/juribuora/website-trust-security-mini-audit/CODEX_CONTEXT.md
/Users/juribuora/website-trust-security-mini-audit/HANDOFF.md
/Users/juribuora/website-trust-security-mini-audit/AGENTS.md
/Users/juribuora/website-trust-security-mini-audit/CLAUDE.md
/Users/juribuora/website-trust-security-mini-audit/landing-page/index.html
/Users/juribuora/website-trust-security-mini-audit/landing-page/styles.css
/Users/juribuora/website-trust-security-mini-audit/landing-page/intake.js
/Users/juribuora/website-trust-security-mini-audit/landing-page/CNAME
/Users/juribuora/website-trust-security-mini-audit/landing-page/.nojekyll
/Users/juribuora/website-trust-security-mini-audit/landing-page/assets/sample-report-page.png
/Users/juribuora/website-trust-security-mini-audit/landing-page/assets/public-sample-report.pdf
/Users/juribuora/website-trust-security-mini-audit/DEPLOY_GITHUB_PAGES.md
/Users/juribuora/website-trust-security-mini-audit/templates/audit-report-template.md
/Users/juribuora/website-trust-security-mini-audit/templates/summary-cliente-phone-template.md
/Users/juribuora/website-trust-security-mini-audit/templates/delivery-message-template.md
/Users/juribuora/website-trust-security-mini-audit/templates/outreach-message.md
/Users/juribuora/website-trust-security-mini-audit/templates/follow-up-message.md
/Users/juribuora/website-trust-security-mini-audit/templates/testimonial-request.md
/Users/juribuora/website-trust-security-mini-audit/checklists/website-audit-checklist.md
/Users/juribuora/website-trust-security-mini-audit/checklists/report-ready-qa-checklist.md
/Users/juribuora/website-trust-security-mini-audit/scripts/create_client_folder.py
/Users/juribuora/website-trust-security-mini-audit/scripts/generate_report_pdf.py
/Users/juribuora/website-trust-security-mini-audit/operations/
/Users/juribuora/website-trust-security-mini-audit/offer/mini-audit-one-page.md
/Users/juribuora/website-trust-security-mini-audit/operations/payment-and-delivery-flow.md
/Users/juribuora/website-trust-security-mini-audit/operations/too-few-findings-policy.md
/Users/juribuora/website-trust-security-mini-audit/operations/delivery-log.csv
/Users/juribuora/website-trust-security-mini-audit/operations/one-client-runbook.md
/Users/juribuora/website-trust-security-mini-audit/operations/service-audit-2026-07-03.md
/Users/juribuora/website-trust-security-mini-audit/proof/README.md
/Users/juribuora/website-trust-security-mini-audit/proof/public-sample-report.md
/Users/juribuora/website-trust-security-mini-audit/proof/public-sample-report.pdf
/Users/juribuora/website-trust-security-mini-audit/proof/case-study-local-business-checkup.md
```

## Local Agent Integration

Juri's local laptop agent is configured to understand this business and can help with prospect research, outreach drafts, and operations notes.

Local agent root:

```text
/Users/juribuora/ai-agent-laptop
```

Important local-agent files:

```text
/Users/juribuora/ai-agent-laptop/prompts/local-agent-system.md
/Users/juribuora/ai-agent-laptop/memory/website-audit-business.md
/Users/juribuora/ai-agent-laptop/memory/autonomy-policy.md
/Users/juribuora/ai-agent-laptop/scripts/local-agent
/Users/juribuora/ai-agent-laptop/scripts/website-audit-agent
/Users/juribuora/ai-agent-laptop/scripts/draft-website-audit-outreach.sh
/Users/juribuora/ai-agent-laptop/scripts/send-approved-email.py
```

Useful commands:

```bash
/Users/juribuora/ai-agent-laptop/scripts/website-audit-agent "summarize this business and suggest next actions"

/Users/juribuora/ai-agent-laptop/scripts/draft-website-audit-outreach.sh \
  "Nome Attività" "https://example.com" "email@example.com"
```

The outreach helper creates prospect notes and email drafts in:

```text
/Users/juribuora/website-trust-security-mini-audit/operations/prospects
/Users/juribuora/website-trust-security-mini-audit/operations/outbox
```

Business email:

```text
webcheckup.online@gmail.com
```

Email drafts are approval-gated. The local agent must not send emails directly. Draft JSON starts as:

```text
draft_requires_human_approval
```

Sending is only possible through:

```bash
/Users/juribuora/ai-agent-laptop/scripts/send-approved-email.py /path/to/draft.json --send
```

That script refuses to send unless the draft JSON has `"status": "approved"` and SMTP environment variables are configured. This is intentional.

## Client Folder Structure

Client audits live here:

```text
/Users/juribuora/website-trust-security-mini-audit/clients
```

Each client should have this structure:

```text
clients/client-site-name/
  screenshots/
  raw-results/
  report/
  notes.md
```

The helper script creates the basic structure:

```bash
cd /Users/juribuora/website-trust-security-mini-audit
python3 scripts/create_client_folder.py "example.com" --base-dir clients
```

The script slugifies domains into readable folder names, for example:

```text
aziendaagricolafarina.com -> aziendaagricolafarina-com
```

## Work Already Done

### 1. Project scaffold created

Created:

- README
- project context
- static landing page
- audit report template
- outreach and follow-up templates
- audit checklist
- client folder helper script

### 2. Landing page improved

Landing page:

```text
/Users/juribuora/website-trust-security-mini-audit/landing-page/index.html
```

Styles:

```text
/Users/juribuora/website-trust-security-mini-audit/landing-page/styles.css
```

Current landing page improvements:

- Italian accents corrected
- stronger sales copy
- more visual/colorful design
- real report preview asset added
- "Come funziona" section added
- price clearly shown as €49
- contact email set to `webcheckup.online@gmail.com`

Important: `webcheckup.online@gmail.com` is the dedicated business Gmail address from Juri's Google account setup. If Juri creates a domain email later, update all `mailto:` links in `landing-page/index.html`.

### 3. First sample audit completed

Audited site:

```text
https://www.aziendaagricolafarina.com/
```

Client folder:

```text
/Users/juribuora/website-trust-security-mini-audit/clients/aziendaagricolafarina-com
```

Generated reports:

```text
/Users/juribuora/website-trust-security-mini-audit/clients/aziendaagricolafarina-com/report/mini-analisi-outreach.md
/Users/juribuora/website-trust-security-mini-audit/clients/aziendaagricolafarina-com/report/report-completo.md
/Users/juribuora/website-trust-security-mini-audit/clients/aziendaagricolafarina-com/report/report-completo.pdf
/Users/juribuora/website-trust-security-mini-audit/clients/aziendaagricolafarina-com/report/messaggio-webmaster.md
```

Advanced/local security assessment artifacts:

```text
/Users/juribuora/website-trust-security-mini-audit/clients/aziendaagricolafarina-com/advanced-security/
/Users/juribuora/website-trust-security-mini-audit/clients/aziendaagricolafarina-com/advanced-security/report/advanced-security-assessment.md
/Users/juribuora/website-trust-security-mini-audit/clients/aziendaagricolafarina-com/advanced-security/raw-results/
```

The advanced assessment used the local codebase:

```text
/Users/juribuora/Projects/farina-farm-website
```

### 4. Operator workflow tightened

Added a repo-specific operating layer so the service is easier to run repeatedly and easier to resume across agents.

Key additions:

- `AGENTS.md` and `CLAUDE.md` for repo-local guidance
- `operations/one-client-runbook.md` as the default lead-to-PDF workflow
- `operations/service-audit-2026-07-03.md` with the current business verdict
- new phone-friendly delivery templates
- improved `scripts/create_client_folder.py` so it scaffolds:
  - `report/report-completo.md`
  - `report/summary-cliente-phone.md`
  - `report/messaggio-consegna.md`
  - `report/messaggio-webmaster.md`
  - `handoff.md`

Preferred command now:

```bash
cd /Users/juribuora/website-trust-security-mini-audit
python3 scripts/create_client_folder.py "Nome Attivita" \
  --website "https://www.esempio.it" \
  --contact-email "email@example.com"
```

### 5. Productization gaps tightened

The repo now includes concrete assets for the main missing business pieces:

- one-page offer definition with scope, turnaround, payment, and revision defaults
- standard payment and delivery workflow
- final QA checklist
- weak-findings policy so low-value reports are not forced
- delivery log
- public sample report and anonymized case study
- testimonial request template

### 6. GitHub Pages deployment prepared

The landing page is now prepared for GitHub Pages with custom domain support for:

- `www.webcheckup.online`

Added:

- `.github/workflows/deploy-pages.yml`
- `landing-page/CNAME`
- `landing-page/.nojekyll`
- `DEPLOY_GITHUB_PAGES.md`

The workflow is set up for the GitHub account:

- `JuriBuora`

So the DNS target for `www` should be:

- `JuriBuora.github.io`

Important boundary: do not run intrusive exploit/brute-force/sqlmap/Nessus/Burp-active traffic against the live GitHub Pages site. Use local/staging copies for learning, or require written authorization, scope, rate limits and provider-compatible rules before any live active testing.

The full PDF report has been polished after review:

- desktop and mobile screenshots are on separate, larger pages
- the recommended action plan starts on its own page
- an evidence appendix was added for the main technical claims
- PDF metadata title, author and subject are set
- wording now says "header di hardening" instead of implying an active security issue

The PDF is generated from the Markdown file with:

```bash
cd /Users/juribuora/website-trust-security-mini-audit
/Users/juribuora/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  scripts/generate_report_pdf.py clients/aziendaagricolafarina-com/report/report-completo.md \
  --output clients/aziendaagricolafarina-com/report/report-completo.pdf \
  --title "Check-up Sito Web - Società Agricola Farina 2.0" \
  --author "Juri Buora" \
  --subject "Analisi esterna e non invasiva del sito web"
```

Collected evidence:

```text
/Users/juribuora/website-trust-security-mini-audit/clients/aziendaagricolafarina-com/screenshots/
/Users/juribuora/website-trust-security-mini-audit/clients/aziendaagricolafarina-com/raw-results/
```

Key findings from the first audit:

- HTTPS works.
- HTTP redirects to HTTPS.
- TLS certificate is valid.
- Site is served by GitHub Pages.
- Lighthouse local test was strong:
  - mobile performance 93
  - mobile accessibility 96
  - mobile best practices 100
  - mobile SEO 100
  - desktop 100 across main categories
- Main visible links returned 200.
- robots.txt and sitemap.xml are present.
- SEO basics are good.
- Cookie banner is present with accept/reject.
- Google Analytics appears consent-gated in the visible code.
- Main improvement: common browser hardening headers are not present.
- Other improvements: mobile contrast, image optimization, cache lifetime, privacy/cookie legal validation.

Note: Google PageSpeed Insights API returned quota/rate-limit 429, so the audit used local Lighthouse instead. Raw PageSpeed API error JSON files were kept in `raw-results/`.

### 4. Mini audit refresh completed

On 26 June 2026 Juri asked for a fresh mini audit because the live site had changed. A new dated audit folder was created instead of overwriting the original audit:

```text
/Users/juribuora/website-trust-security-mini-audit/clients/aziendaagricolafarina-com/audits/2026-06-26-1840-mini-refresh
```

Generated refresh reports:

```text
/Users/juribuora/website-trust-security-mini-audit/clients/aziendaagricolafarina-com/audits/2026-06-26-1840-mini-refresh/report/mini-audit-refresh.md
/Users/juribuora/website-trust-security-mini-audit/clients/aziendaagricolafarina-com/audits/2026-06-26-1840-mini-refresh/report/mini-audit-refresh.pdf
```

Collected refresh evidence:

```text
/Users/juribuora/website-trust-security-mini-audit/clients/aziendaagricolafarina-com/audits/2026-06-26-1840-mini-refresh/raw-results/
/Users/juribuora/website-trust-security-mini-audit/clients/aziendaagricolafarina-com/audits/2026-06-26-1840-mini-refresh/screenshots/
```

Key refresh findings:

- Live homepage `Last-Modified`: `Fri, 26 Jun 2026 16:33:42 GMT`.
- Sitemap now has 7 public URLs and includes `/ordina-legna-da-ardere/`.
- New "Ordina Legna" page is public, indexed in sitemap, and has dedicated title/meta/H1.
- Lighthouse mobile: performance 87, accessibility 100, best practices 100, SEO 100.
- Lighthouse desktop: 100 across performance/accessibility/best-practices/SEO.
- The original mobile contrast finding is no longer present in Lighthouse.
- Header hardening recommendations still apply because the GitHub Pages response still lacks common hardening headers.
- Light link check returned `200` for all main public pages; `/.well-known/security.txt` returned `404`.
- Suggested refinements: mobile LCP/hero asset optimization, reduce cookie banner impact on the order page first viewport, add native `required` attributes to required form controls if compatible with existing validation.

The PDF generator was also improved so table header text renders white on dark header rows. This change is in:

```text
/Users/juribuora/website-trust-security-mini-audit/scripts/generate_report_pdf.py
```

## Recommended Workflow For Future Audits

For every new site:

1. Create client folder:

```bash
cd /Users/juribuora/website-trust-security-mini-audit
python3 scripts/create_client_folder.py "domain.com" --base-dir clients
```

2. Save public evidence:

```text
clients/client-site-name/screenshots/
clients/client-site-name/raw-results/
```

Useful raw result files:

```text
homepage.html
homepage-headers.txt
http-redirect-headers.txt
tls-certificate.txt
lighthouse-mobile.json
lighthouse-desktop.json
lighthouse-findings.txt
link-check-main.txt
robots.txt
sitemap.xml
privacy-policy.html
cookie-policy.html
```

3. Check these areas:

- first impression and trust
- mobile usability
- website speed
- HTTPS / SSL / TLS
- browser hardening headers
- SEO basics
- broken/main links
- privacy/cookie basics
- contact and conversion path
- priority remediation plan

4. Produce:

```text
report/mini-analisi-outreach.md
report/report-completo.md
report/report-completo.pdf
report/messaggio-webmaster.md
```

5. Generate the PDF with the reusable script:

```bash
cd /Users/juribuora/website-trust-security-mini-audit
/Users/juribuora/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  scripts/generate_report_pdf.py clients/client-site-name/report/report-completo.md \
  --output clients/client-site-name/report/report-completo.pdf \
  --title "Check-up Sito Web - Nome Cliente"
```

6. Render and visually inspect the PDF before delivery. Check that screenshots are readable, page breaks are clean, tables do not overflow and the evidence appendix is present.

7. Keep language simple, practical and Italian.

Avoid legal claims such as:

- "il sito è sicuro"
- "il sito è GDPR compliant"
- "il sito è vulnerabile"

Prefer cautious language:

- "risulta migliorabile"
- "da verificare con il webmaster"
- "da validare con il consulente privacy"
- "non significa che il sito sia compromesso"
- "è una buona pratica tecnica"

## Suggested Commands

Run local static server for the landing page:

```bash
cd /Users/juribuora/website-trust-security-mini-audit
python3 -m http.server 8765 --bind 127.0.0.1 --directory landing-page
```

Then open:

```text
http://127.0.0.1:8765/
```

Check headers:

```bash
curl -L -sS --max-time 30 -D raw-results/homepage-headers.txt -o raw-results/homepage.html https://example.com/
curl -I -L -sS --max-time 20 http://example.com/ > raw-results/http-redirect-headers.txt
```

Check TLS certificate:

```bash
echo | openssl s_client -connect example.com:443 -servername example.com 2>/dev/null | openssl x509 -noout -issuer -subject -dates -fingerprint -sha256 > raw-results/tls-certificate.txt
```

Run Lighthouse if available:

```bash
npx -y lighthouse https://example.com/ --quiet --output=json --output-path=raw-results/lighthouse-mobile.json --only-categories=performance,accessibility,best-practices,seo --chrome-flags="--headless --disable-gpu"
npx -y lighthouse https://example.com/ --quiet --preset=desktop --output=json --output-path=raw-results/lighthouse-desktop.json --only-categories=performance,accessibility,best-practices,seo --chrome-flags="--headless --disable-gpu"
```

Generate the PDF report:

```bash
cd /Users/juribuora/website-trust-security-mini-audit
/Users/juribuora/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  scripts/generate_report_pdf.py clients/client-site-name/report/report-completo.md \
  --output clients/client-site-name/report/report-completo.pdf \
  --title "Check-up Sito Web - Nome Cliente" \
  --author "Juri Buora" \
  --subject "Analisi esterna e non invasiva del sito web"
```

If the bundled Codex Python is not available, use another Python with ReportLab installed:

```bash
python3 -m pip install reportlab
python3 scripts/generate_report_pdf.py clients/client-site-name/report/report-completo.md
```

## Email Recommendation

Do not use Juri's personal email for outreach.

Recommended short-term setup:

- create a dedicated Gmail for this business
- current dedicated Gmail: `webcheckup.online@gmail.com`
- add a simple signature
- keep all outreach, replies and reports separate from personal mail

Recommended later setup after validation:

- buy/use a domain
- create a more professional address such as `audit@domain.it` or `info@domain.it`

## Suggested Handoff Prompt For Another LLM

Copy/paste this into another LLM:

```text
You are helping me continue a small Italian business project called "Check-up Sito Web: Sicurezza, Fiducia e Visibilità".

The project lives at:
/Users/juribuora/website-trust-security-mini-audit

Read these first:
/Users/juribuora/website-trust-security-mini-audit/HANDOFF.md
/Users/juribuora/website-trust-security-mini-audit/CODEX_CONTEXT.md
/Users/juribuora/website-trust-security-mini-audit/README.md

This business sells non-invasive website mini-audits for Italian small businesses at €49. The audit checks public, visible issues only: HTTPS, browser hardening headers, performance, mobile usability, SEO basics, broken/main links, privacy/cookie basics, trust and conversion.

Never do penetration testing, exploit testing, login testing, brute forcing, directory fuzzing, aggressive crawling, or legal/GDPR compliance claims.

When I give you a website URL, create a client folder under:
/Users/juribuora/website-trust-security-mini-audit/clients

Then produce:
- report/mini-analisi-outreach.md
- report/report-completo.md
- report/report-completo.pdf using scripts/generate_report_pdf.py if possible
- report/messaggio-webmaster.md
- screenshots and raw-results evidence

Keep the language clear, professional and practical Italian. Use priorities Alta / Media / Bassa. Include business impact, practical recommendations, who should fix each issue and a short evidence appendix for technical claims.
```

## Next Good Improvements

Useful next tasks:

- Add a `scripts/run_basic_audit.py` helper to automate non-invasive checks.
- Add an anonymized sample report package for sharing with prospects.
- Consider tagged/accessible PDF generation later if the service becomes more formal.
- Decide and create the dedicated Gmail address, then update the landing page mail links.
- For the Farina codebase, add anti-spam controls to `/ordina-legna-da-ardere/` and update dependencies flagged by `npm audit`.
