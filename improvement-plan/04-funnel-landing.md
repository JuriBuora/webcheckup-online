# 04 — Funnel & Landing Page

**Goal:** make more of the people who reach webcheckup.online actually request the €49 check-up, and make the intake reliable. Small, safe, testable edits — do NOT redeploy the live site yourself; leave that for the human.

**Work in:** `/Users/juribuora/website-trust-security-mini-audit`
**Read first:** `landing-page/index.html`, `landing-page/styles.css`, `landing-page/intake.js`, `DEPLOY_GITHUB_PAGES.md`.
**Reminder:** this is a static site (GitHub Pages). You edit files locally and TEST locally. A human deploys.

---

## Task 1 — Snapshot + local preview

**Do:** Back up the three landing files (`cp landing-page/index.html landing-page/index.html.bak`, same for css/js). Serve locally and confirm it loads:
```bash
cd /Users/juribuora/website-trust-security-mini-audit/landing-page
python3 -m http.server 8899 >/tmp/lp.log 2>&1 &
sleep 1
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8899/index.html
```
**Test:** the curl prints `200`.
**Double-check:** `curl -s http://127.0.0.1:8899/index.html | grep -ci 'check-up'` is ≥ 1 (page has the expected content).
**If it fails:** kill any process on 8899 (`lsof -ti:8899 | xargs kill`), retry. Log a blocker if the page won't serve.
**Cleanup at end of this file:** `lsof -ti:8899 | xargs kill 2>/dev/null`.

## Task 2 — Sharpen the hero (headline + subhead + one CTA) `[NEEDS-STRONGER-MODEL]`

**Do:** In `index.html`, improve ONLY the hero section: a clear Italian headline (benefit, not jargon), one subhead line (what you get for €49, in 2 giorni), and ONE primary button ("Richiedi il check-up"). Remove competing CTAs above the fold. Do not touch the intake form logic. Keep existing CSS classes so styles still apply.

**Test:** reload `http://127.0.0.1:8899/index.html`; `curl -s http://127.0.0.1:8899/index.html | grep -c 'Richiedi il check-up'` ≥ 1. Page still returns 200.
**Double-check:** exactly one primary CTA above the fold; €49 and "2 giorni" appear; no broken HTML (`python3 -c "import html.parser,sys; ..."` or just visually confirm tags are balanced).
**If it fails:** restore `index.html.bak`, redo. Never break the form.

## Task 3 — Add a trust row (what's included / what's not)

**Do:** Add a short section below the hero: 3–4 bullets "Cosa ricevi" and 1 line "Analisi esterna e non invasiva — non è un pen-test." Pull wording from `offer/mini-audit-one-page.md` (do file 03 first if possible so they match). Reuse existing CSS classes.

**Test:** page returns 200 and contains "non invasiva".
**Double-check:** wording matches the one-pager (price, delivery, scope). No new legal claims.
**If it fails:** restore backup, redo.

## Task 4 — Verify the intake form still works end-to-end

**Do:** Read `intake.js` to see where the form submits (email, a form service, or a webhook). Do NOT change the submission target without human approval. Just confirm the form validates required fields and shows a success state. If the submission goes nowhere/misconfigured, DO NOT guess a new endpoint — log it in `BLOCKERS.md` as "intake submission target needs Juri's decision".

**Test:** load the page, fill the form in the browser preview if possible; otherwise statically confirm `intake.js` has validation and a success handler (`grep -iE 'require|valid|success|grazie' landing-page/intake.js`).
**Double-check:** no secret keys/tokens are hard-coded in `intake.js` (`grep -iE 'key|token|secret' landing-page/intake.js` — if found, log a blocker; do not print the value).
**If it fails:** log a blocker; do not invent an endpoint.

## Task 5 — Add the FAQ (from file 03) to the page

**Do:** If `offer/faq-obiezioni.md` exists (from file 03 Task 2), add a compact FAQ section to the landing page using 4–5 of the most important Q&As. Reuse existing styles; keep it collapsible only if the page already has a pattern for it (don't add new JS libraries).

**Test:** page returns 200 and contains at least 3 question strings from the FAQ.
**Double-check:** the privacy/GDPR answer on the page makes no legal guarantee.
**If it fails:** restore backup; if `faq-obiezioni.md` doesn't exist yet, skip this task and note it in `PROGRESS.md` to do after file 03.

## Task 6 — Pre-deploy checklist (do NOT deploy)

**Do:** Create `landing-page/PRE-DEPLOY-CHECK.md`: a checklist the human runs before publishing — local page returns 200, all links work (`grep -oE 'href="[^"]+"'` and eyeball), no `.bak` files committed, no secrets in JS, mobile view looks OK, price/delivery consistent with the one-pager. End with: "Deploy is a HUMAN step — see DEPLOY_GITHUB_PAGES.md."

**Test:** file exists with at least 6 checkboxes.
**Double-check:** it explicitly says the human deploys, not the model.
**If it fails:** redo.

---

**When done:** kill the local server (`lsof -ti:8899 | xargs kill 2>/dev/null`), remove any `.bak` files only AFTER commits are done (or leave them — they're gitignored if the repo ignores `*.bak`; if not, do not commit them). Update `PROGRESS.md`. Do NOT deploy the live site — that is a human step.
