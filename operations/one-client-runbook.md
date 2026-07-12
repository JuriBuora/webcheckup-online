# One Client Runbook

This is the simplest safe path for one operator to go from lead to PDF report without confusion.

## Goal

Produce one clear deliverable package for one real client:

- one report PDF
- one short client summary readable on a phone
- one ready-to-forward message for the webmaster
- one handoff note so the next agent or session can resume cleanly

## Stop Conditions

Pause the workflow if any of these happen:

- the prospect asks for a penetration test
- the site requires login to evaluate the requested area
- the website is clearly broken or offline
- there is no public website URL
- the client asks for legal/privacy certification wording

In those cases, do not improvise. Re-scope the job first.

## The Only Workflow To Follow

### 1. Capture the lead

Use one of these:

- `templates/outreach-message.md`
- `templates/follow-up-message.md`
- `/Users/juribuora/ai-agent-laptop/scripts/draft-website-audit-outreach.sh`

Minimum info to collect:

- business name
- public website URL
- contact email if available
- whether the lead is still cold, warm, or confirmed

### 2. If the lead is interested, create the client package

Run:

```bash
cd /Users/juribuora/webcheckup
python3 scripts/create_client_folder.py "Nome Attivita" \
  --website "https://www.esempio.it" \
  --contact-email "email@example.com"
```

This creates:

- the folder structure
- a prefilled report draft
- a phone-friendly client summary
- a delivery message draft
- a webmaster-forward message draft
- a client handoff file
- commercial notes with payment and revision fields

### 3. Fill `notes.md` first

Before collecting evidence, update:

- status
- website
- contact
- lead source
- price agreed
- delivery target date

If `notes.md` is not updated, the rest of the workflow gets messy later.

### 4. Collect evidence

Use only the checklist in `checklists/website-audit-checklist.md`.

Before delivery, also pass:

- `checklists/report-ready-qa-checklist.md`
- `operations/too-few-findings-policy.md`

Save everything in the client folder only:

- screenshots in `screenshots/`
- tool outputs in `raw-results/`
- working notes in `notes.md`

Do not leave evidence in Downloads, Desktop, or random temp folders.

### 5. Write the report

Open `report/report-completo.md` and replace placeholders.

Keep it simple:

- 2-3 real strengths
- 2-5 real issues
- clear priority table
- plain Italian
- business impact, not technical drama

Do not pad the report just to make it look longer.

### 6. Generate the PDF

Run:

```bash
/Users/juribuora/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  scripts/generate_report_pdf.py clients/nome-attivita/report/report-completo.md \
  --output clients/nome-attivita/report/report-completo.pdf \
  --title "Check-up Sito Web - Nome Attivita"
```

Then do one visual check of the PDF before delivery.

### 7. Prepare the phone-friendly outputs

Update these three files:

- `report/summary-cliente-phone.md`
- `report/messaggio-consegna.md`
- `report/messaggio-webmaster.md`

Rule:

- the client summary should fit comfortably on a phone screen
- the delivery message should be short enough to send without editing much
- the webmaster message should be easy to forward as-is

### 8. Close the case cleanly

Update `handoff.md` with:

- current stage
- what was done
- files ready to send
- remaining task
- anything risky or still unverified

Then update `operations/delivery-log.csv`.

## Operator Checklist

Use this exact order every time:

1. Lead captured
2. Client folder created
3. Notes updated
4. Evidence saved
5. Report written
6. PDF generated
7. Phone summary updated
8. Delivery message updated
9. Webmaster message updated
10. Handoff updated

## What To Avoid

- running too many tools for a €49 service
- writing security theater
- mixing free mini-analysis and paid report files
- creating custom folder structures per client
- skipping the phone summary
- skipping the final handoff
