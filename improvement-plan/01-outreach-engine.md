# 01 — Outreach Engine

**Goal:** make the cold-outreach that feeds `run-outreach-batch.sh` get more replies, without spamming or lying. Better copy, better targeting, a real follow-up sequence.

**Work in:** `/Users/juribuora/website-trust-security-mini-audit`
**Read first:** `templates/outreach-message.md`, `templates/follow-up-message.md`, `README.md` (the "Offerta" section).
**Reminder:** you never send. You only edit templates/files. A human approves real sends.

---

## Task 1 — Inventory the current outreach copy

**Do:** Read `templates/outreach-message.md` and `templates/follow-up-message.md`. Create `improvement-plan/outreach-notes.md` and write, in plain Italian: (a) the current first-message text, (b) the current follow-up text, (c) 3 concrete weaknesses you notice (e.g., too long, no clear reason-to-reply, weak subject).

**Test:** `test -f improvement-plan/outreach-notes.md && wc -l improvement-plan/outreach-notes.md` — must exist and have at least 10 lines.
**Double-check:** open the file and confirm it names both current messages AND lists exactly 3 weaknesses.
**If it fails:** re-run; make sure you actually read both template files first (`cat` them).

## Task 2 — Rewrite the first outreach email `[NEEDS-STRONGER-MODEL]`

**Do:** Write a new first-contact email into `templates/outreach-message.md` (back up the old one to `.bak` first). Requirements:
- Italian, max ~90 words, one clear idea.
- Subject line options: provide 3, each under 6 words, no clickbait, no ALL CAPS, no "gratis!!!".
- Body structure: 1 line that shows you actually looked at their site (leave a `{{OSSERVAZIONE}}` placeholder the run fills per-prospect), 1 line on the €49 check-up and what they get, 1 soft call to action ("posso mandarti un esempio senza impegno?").
- No alarmism, no "il tuo sito è a rischio", no GDPR/legal claims, no fake urgency. Signed "Juri".
- Keep the `{{OSSERVAZIONE}}` and (if useful) `{{NOME_ATTIVITA}}` / `{{URL}}` placeholders so automation can fill them.

**Test:** `python3 - <<'PY'` that opens the file, asserts it contains `{{OSSERVAZIONE}}`, contains at least 3 subject options, and body word count < 120. Print `OK` or the failing check.
**Double-check:** read it aloud in your head — would a busy shop owner reply? If it sounds like spam or a template, revise once.
**If it fails:** restore `.bak`, re-read the requirements, try again. If after 2 tries it still reads like spam, mark `[NEEDS-STRONGER-MODEL]` in `BLOCKERS.md` and leave the best draft.

## Task 3 — Build a 3-step follow-up sequence

**Do:** Replace `templates/follow-up-message.md` (back up first) with THREE short follow-ups, clearly separated with headers `## Follow-up 1 (dopo 3 giorni)`, `## Follow-up 2 (dopo 7 giorni)`, `## Follow-up 3 (dopo 14 giorni, ultimo)`. Each ≤ 60 words, Italian, adds a *new* angle (1: gentle bump; 2: offer the free mini-analysis instead; 3: polite last touch + easy "no"). Keep placeholders.

**Test:** file contains all three `## Follow-up` headers (`grep -c '^## Follow-up' templates/follow-up-message.md` returns 3).
**Double-check:** confirm follow-up 3 gives an explicit easy opt-out and is not pushy.
**If it fails:** restore `.bak`, redo. Never exceed 3 follow-ups (more = spam).

## Task 4 — Create 3 niche outreach variants

**Do:** Create `templates/outreach-variants/` and inside it three files: `ristoranti.md`, `artigiani.md`, `studi-professionali.md`. Each = the Task-2 email adapted with 1–2 niche-specific observations (e.g., restaurants: menu leggibile da telefono, prenotazioni; artigiani: portfolio/foto, contatti; studi: fiducia, privacy, chiarezza servizi). Keep placeholders and the same rules.

**Test:** `ls templates/outreach-variants/*.md | wc -l` returns 3.
**Double-check:** each variant mentions at least one thing specific to that niche (not generic).
**If it fails:** ensure the folder exists (`mkdir -p templates/outreach-variants`) and retry.

## Task 5 — Define the targeting rule (who to email)

**Do:** Write `improvement-plan/targeting-rules.md`: a short, concrete checklist for choosing prospects for a batch. Include: prefer businesses whose site plausibly has visible problems (no HTTPS, not mobile-friendly, slow, weak trust); avoid businesses with no public email; avoid huge chains; note the daily send cap (recommend **max 10–15/day** to protect deliverability); and a note that emails go out ONLY via the approval gate.

**Test:** `test -f improvement-plan/targeting-rules.md` and it mentions a daily cap number.
**Double-check:** the rules are usable by a non-marketer (concrete, not vague).
**If it fails:** re-read this task, keep it concrete.

## Task 6 — Wire variants into the run (small, careful)

**Do:** In `/Users/juribuora/ai-agent-laptop/scripts/make-outreach-draft.py`, the default body comes from `default_body()`. Add an **optional** `--variant ristoranti|artigiani|studi-professionali` flag that, if given, loads the matching text from `templates/outreach-variants/<variant>.md` (from the business repo) as the body, else keeps the current default. Back up the script first. Do NOT change existing behavior when `--variant` is not passed.

**Test:**
```bash
cd /Users/juribuora/ai-agent-laptop
python3 scripts/make-outreach-draft.py --batch TESTVAR --to webcheckup.online@gmail.com --company "X" --url https://x.it --variant ristoranti
python3 -c "import glob,json;print(json.load(open(sorted(glob.glob('/Users/juribuora/website-trust-security-mini-audit/operations/outbox/TESTVAR-*.json'))[-1]))['body'][:60])"
rm -f /Users/juribuora/website-trust-security-mini-audit/operations/outbox/TESTVAR-*.json
```
The printed body must reflect the restaurant variant. Also run WITHOUT `--variant` and confirm the old default still appears.
**Double-check:** `python3 -m py_compile scripts/make-outreach-draft.py` returns no error.
**If it fails:** restore the `.bak`, re-read; if you can't do it safely, log a blocker and leave the script unchanged — the variants still exist as templates for humans.

---

**When all 6 tasks are done:** append results to `PROGRESS.md`, and make sure every change is committed in the business repo (the script change is committed in the `ai-agent-laptop` repo). Do NOT send anything.
