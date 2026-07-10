# Improvement Plan Pass - 2026-07-10

## Main target

Execute the website-audit improvement plan files `02`, `03`, and `04`, while respecting the earlier completed `01` work already present in the repo.

## What was done

- Verified `01-outreach-engine` was already completed and logged in `improvement-plan/PROGRESS.md`
- Added reusable finding examples and tightened the report QA and public sample assets
- Rewrote the one-page offer in Italian, added FAQ objections and service ladder, and aligned core terms around `€49`, `2 giorni lavorativi`, and the revision default
- Tightened the landing-page hero, added the trust/include scope strip, refreshed the FAQ section, and added a pre-deploy checklist
- Updated `improvement-plan/PROGRESS.md` with task-by-task status for files `02`, `03`, and `04`

## Files changed

- `checklists/finding-examples.md`
- `checklists/report-ready-qa-checklist.md`
- `proof/public-sample-report.md`
- `offer/mini-audit-one-page.md`
- `offer/faq-obiezioni.md`
- `offer/scala-servizi.md`
- `operations/payment-and-delivery-flow.md`
- `README.md`
- `operations/too-few-findings-policy.md`
- `operations/service-audit-2026-07-03.md`
- `operations/one-client-runbook.md`
- `templates/outreach-message.md`
- `templates/follow-up-message.md`
- `templates/outreach-variants/ristoranti.md`
- `templates/outreach-variants/artigiani.md`
- `templates/outreach-variants/studi-professionali.md`
- `CODEX_CONTEXT.md`
- `landing-page/index.html`
- `landing-page/styles.css`
- `landing-page/PRE-DEPLOY-CHECK.md`
- `improvement-plan/PROGRESS.md`

## Commands and checks

- Verified checklist rubric count with `grep -c 'OK / Migliorabile / Problema'`
- Generated throwaway PDF with `scripts/generate_report_pdf.py` to `/tmp/sample-check.pdf`
- Double-checked rendered PDF content with `pdftotext /tmp/sample-check.pdf -`
- Served the landing page locally on `http://127.0.0.1:8899/index.html`
- Verified landing copy with `curl` and HTML parse check
- Confirmed intake validation/success logic by reading `landing-page/intake.js`

## Commits

- `d780d53` `improve: strengthen audit proof and QA assets`
- `f1ac269` `improve: productize offer and align terms`
- `1ee5a7f` `improve: tighten landing page funnel copy`
- `d894a56` `improve: record plan progress`

## Current state

- Plan files `02`, `03`, and `04` are marked done in `improvement-plan/PROGRESS.md`
- No blockers were logged
- Backups remain locally as `.bak` files under `landing-page/` and other touched paths where required before overwriting

## Next steps

- Human review of `[DECISIONE-JURI]` items in `offer/mini-audit-one-page.md` and `operations/payment-and-delivery-flow.md`
- Human review before publishing `proof/public-sample-report.md`
- Human-only deploy step for the landing page after checking `landing-page/PRE-DEPLOY-CHECK.md`

## Double-check later

- Decide whether the repo should keep force-tracked business docs or whether `.gitignore` should be revisited explicitly later
- If the landing page is deployed, smoke-test the live FormSubmit flow once on production

## Do not do

- Do not send outreach emails directly
- Do not publish the landing page automatically
- Do not turn the service into a legal/GDPR or invasive-security offer
