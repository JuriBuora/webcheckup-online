# Website-Audit Business — Improvement Plan (operator instructions for a local LLM)

**Read this whole file before doing anything.** You (the executing model) are less capable than the model that wrote this plan, so follow the steps **literally and in order**. Do not improvise. Do not skip the TEST and DOUBLE-CHECK steps.

## What this is

A set of task files that improve the "Website Trust & Security Mini-Audit" business (€49 website check-up for small Italian businesses). There are four area files, each a numbered list of small tasks:

1. `01-outreach-engine.md` — cold-email copy, targeting, follow-up sequence (feeds the automated `run-outreach-batch.sh`).
2. `02-deliverable-and-proof.md` — the €49 report: checklist depth, report template, PDF, public sample/proof.
3. `03-offer-packaging.md` — terms, pricing tiers, objections FAQ, upsell ladder.
4. `04-funnel-landing.md` — landing page + intake conversion at webcheckup.online.

Do the files in the order **01 → 02 → 03 → 04** unless the human says otherwise. Inside each file, do tasks in number order.

## Where things live

- **Business repo (do the work here):** `/Users/juribuora/website-trust-security-mini-audit`
- **This plan (also mirrored here):** `/Users/juribuora/ai-agent-laptop/business/website-audit/improvement-plan/`
- **Automation you must NOT bypass:** sending real emails is gated. You never send. You only create/edit files and drafts. A human approves sends on their phone via the approval gate (`scripts/run-outreach-batch.sh` + Telegram/email). See `/Users/juribuora/ai-agent-laptop/docs/N8N_SETUP.md`.

## Which model / how to run a task

- **Default:** run each file-producing task through the orchestrator, which checks the file was really written and retries:
  ```bash
  /Users/juribuora/ai-agent-laptop/scripts/orchestrate "TASK TEXT, including the exact output file path"
  ```
- **Only if a task is tagged `[NEEDS-STRONGER-MODEL]`** (customer-facing Italian sales prose): either start DS4 and use it, or leave a clear draft and ask the human to review/upgrade it. Do not assume your first draft of sales copy is good enough to send to real clients.
  ```bash
  START_DS4=1 /Users/juribuora/ai-agent-laptop/scripts/start-local-ai-stack.sh
  /Users/juribuora/ai-agent-laptop/scripts/local-agent --provider ds4 --model deepseek-v4-flash "TASK TEXT"
  ```
- **Never** send email, publish the website, take payment, or contact a real business yourself. Those are human-approved steps.

## The rules you must follow for EVERY task

1. **One task at a time, in order.** Finish and verify a task before starting the next.
2. **After writing/editing, run the task's TEST step.** If the test fails, do the RECOVERY step, then run the TEST again. Do **not** move on until the TEST passes.
3. **Then run the DOUBLE-CHECK step** (a second, different check). If it disagrees with the TEST, trust neither — stop and log a blocker.
4. **Commit after each verified task** (in the business repo), touching only the files that task changed:
   ```bash
   cd /Users/juribuora/website-trust-security-mini-audit
   git add <the exact files you changed>
   git commit -m "improve: <short description of the task>"
   ```
   Do **not** `git add -A` or `git add .`. Do **not** push unless the human says to.
5. **If a step is ambiguous, a file is missing, or something breaks you can't fix in one recovery attempt: STOP.** Append a note to `improvement-plan/BLOCKERS.md` (create it if missing) with: the file, the task number, exactly what you tried, and the exact error. Then move to the next *independent* task if there is one; otherwise stop and wait for the human.
6. **Never delete or overwrite an existing file without first copying it to `<name>.bak`.** Example: `cp templates/audit-report-template.md templates/audit-report-template.md.bak` before editing.
7. **Keep all customer-facing text in Italian**, matching the existing tone: practical, honest, non-alarmist, no legal/GDPR compliance claims, no invented statistics, signed "Juri".
8. **Do not invent facts** (no fake testimonials, fake client names, fake stats, fake certifications). If a task needs real data you don't have, log a blocker.
9. **NEVER contact excluded categories.** Do not draft or send outreach to lawyers, banks, accountants/tax advisors, or any fiscal/tax-audit body. This is enforced in code (`config/outreach-blocklist.txt` + `make-outreach-draft.py`), but you must also avoid adding them to prospect lists in the first place. Full rule: `improvement-plan/EXCLUSIONS.md`. Never weaken the blocklist.

## Definition of done for the whole plan

Every task in 01–04 is either (a) completed, tested, double-checked, and committed, or (b) logged in `BLOCKERS.md` with a clear reason. Nothing is left half-done and unlogged.

## Progress tracking

Keep a running log at `improvement-plan/PROGRESS.md`. After each task, append one line:
`YYYY-MM-DD  <file> task <n>  DONE|BLOCKED  <commit hash or blocker note>`
Create the file if it does not exist.

## IMPORTANT — runner & write access (learned from a live test 2026-07-10)

1. **Use `scripts/local-agent` for prose/doc tasks, NOT `scripts/orchestrate`.** `orchestrate` misclassifies "write a markdown file" as a *code* task and escalates without writing. For docs/copy/checklists run:
   `scripts/local-agent --max-steps 8 "…SAVE the file at <path>…"`
   then ALWAYS verify: `ls -la <path>`. If it printed but didn't save, re-run once saying "use your file-writing tool to SAVE the file". Use `orchestrate` only for real code edits.
2. **`local-agent` is sandboxed:** it can READ the business repo but only WRITE inside `/Users/juribuora/ai-agent-laptop/` (e.g. `workspace/website-audit-staging/`) and the business `operations/` folder. Pattern: the model saves output to `workspace/website-audit-staging/<file>`, then a human (or aider/Codex run inside the business repo) reviews and copies it to the real target path. It CANNOT write directly into `website-trust-security-mini-audit/templates|offer|checklists|landing-page`.

Verified: `local-agent` read the outreach templates and produced `workspace/website-audit-staging/outreach-notes.md` (file 01, task 1). ✓
