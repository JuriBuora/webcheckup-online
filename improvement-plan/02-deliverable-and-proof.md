# 02 — The €49 Deliverable & Proof

**Goal:** make each report more valuable and consistent, and make the public proof stronger, so a €49 report clearly feels worth it.

**Work in:** `/Users/juribuora/website-trust-security-mini-audit`
**Read first:** `checklists/website-audit-checklist.md`, `checklists/report-ready-qa-checklist.md`, `templates/audit-report-template.md`, `operations/too-few-findings-policy.md`, `proof/public-sample-report.md`.
**Reminder:** no invented findings, no fake clients/testimonials, no legal claims.

---

## Task 1 — Turn the audit checklist into a scored, repeatable rubric

**Do:** Back up `checklists/website-audit-checklist.md`, then expand it so every area (trust/first impression, mobile, speed, HTTPS/TLS, hardening headers, SEO base, broken links, privacy/cookie, contact/conversion path) has: (a) exactly what to look at, (b) how to judge it as `OK / Migliorabile / Problema`, (c) the business impact in one plain sentence, (d) who typically fixes it (owner / webmaster / hosting). Keep it non-invasive (no login, no scanning tools that hit the server hard).

**Test:** `grep -c 'OK / Migliorabile / Problema' checklists/website-audit-checklist.md` returns at least 9 (one per area).
**Double-check:** a non-technical operator could follow it and produce the same verdicts twice. If two runs would disagree wildly, the criteria are too vague — tighten them.
**If it fails:** restore `.bak`, redo one area at a time.

## Task 2 — Strengthen the report template structure

**Do:** Back up `templates/audit-report-template.md`. Ensure it has, in this order: cover (business, site, date), 1-paragraph plain-language summary, a **priority table** (Problema | Impatto | Priorità Alta/Media/Bassa | Chi lo sistema), one section per finding (what/why-it-matters/what-to-do), a "quick wins" box (3 things fixable this week), and a technical appendix. Use clear placeholders like `{{BUSINESS}}`, `{{URL}}`, `{{DATA}}`, `{{FINDINGS}}`. Do not remove fields the PDF generator relies on — check `scripts/generate_report_pdf.py` first to see which placeholders/sections it expects.

**Test:** `python3 -c "print('ok')"` after generating a sample PDF from the template with dummy content (see Task 3). The template must contain a priority table header row.
**Double-check:** open `scripts/generate_report_pdf.py`; confirm no placeholder it requires was renamed/removed. If unsure, do not rename existing placeholders.
**If it fails:** restore `.bak`. Never break the PDF generator to improve the template.

## Task 3 — Prove the PDF still generates end-to-end

**Do:** Using the existing generator, produce a throwaway PDF from the template with obviously-fake sample content into `/tmp/sample-check.pdf`:
```bash
cd /Users/juribuora/website-trust-security-mini-audit
python3 scripts/generate_report_pdf.py --help 2>/dev/null | head -30   # learn its real interface FIRST
```
Then run it the way `--help` shows, with a dummy filled report, output to `/tmp/sample-check.pdf`.

**Test:** `test -s /tmp/sample-check.pdf` (file exists and is non-empty) and `file /tmp/sample-check.pdf` says PDF.
**Double-check:** the PDF has more than 1 page and the priority table rendered (open it if a viewer is available; otherwise check byte size > 20 KB).
**If it fails:** read the generator's error; fix only the template/content you fed it, not the generator, unless the generator itself errors on valid input — then log a blocker with the exact traceback.

## Task 4 — Add "before/after" mini examples to the checklist knowledge

**Do:** Create `checklists/finding-examples.md` with 6–8 concrete, generic example findings (no real client), each written as: the problem, the one-line business impact, the recommended fix, and who fixes it. These are reusable phrasings so reports read consistently. Keep them realistic and non-alarmist.

**Test:** `grep -c '^### ' checklists/finding-examples.md` returns at least 6.
**Double-check:** none of the examples name a real business or invent statistics.
**If it fails:** redo; keep examples generic and honest.

## Task 5 — Upgrade the public sample report `[NEEDS-STRONGER-MODEL]`

**Do:** Improve `proof/public-sample-report.md` so it reads like a credible, anonymised real audit (business named e.g. "Attività di esempio"), using the new template structure and 3–4 example findings from Task 4. Keep it honest and non-alarmist. Do NOT regenerate the PDF for the public site yet — leave that for a human to review and publish.

**Test:** file exists, uses the priority table, and contains 3–4 findings.
**Double-check:** nothing in it could embarrass a real business or make a false claim. Flag for human review by adding a line at the top: `<!-- DA RIVEDERE DA JURI PRIMA DELLA PUBBLICAZIONE -->`.
**If it fails:** leave the previous version intact (`.bak`) and log a blocker.

## Task 6 — Tighten the report-ready QA checklist

**Do:** Back up and update `checklists/report-ready-qa-checklist.md` so it is a hard gate before any report is delivered: PDF generates, ≥ the minimum findings from `too-few-findings-policy.md`, no placeholders left (`grep '{{' report`), priority table filled, phone summary written, delivery message written, no legal/GDPR claims, spelling pass. Make each item a checkbox.

**Test:** `grep -c '\- \[ \]' checklists/report-ready-qa-checklist.md` returns at least 8.
**Double-check:** the checklist explicitly forbids delivering a report that still contains `{{` placeholders.
**If it fails:** restore `.bak`, redo.

---

**When done:** update `PROGRESS.md`, commit each change in the business repo. Do not publish anything to the public site.
