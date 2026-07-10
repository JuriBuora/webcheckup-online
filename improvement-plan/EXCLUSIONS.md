# EXCLUSIONS — who we must NEVER contact

**Hard rule (Juri, 2026-07-10):** never send any service or outreach email to **lawyers, banks, accountants/tax advisors, or any body connected to auditing our fiscal/tax position**. This is a risk-avoidance decision — do not second-guess it, do not make exceptions.

## What is excluded

- Lawyers / legal offices (avvocati, studi legali, notai, tribunali)
- Banks and credit institutions (banche, istituti di credito)
- Accountants / tax advisors (commercialisti, consulenti fiscali, CAF, patronati, revisori contabili)
- Tax authority & collection bodies (Agenzia delle Entrate, Guardia di Finanza, Equitalia/Riscossione)
- Government / institutional domains (`gov.it`)

## How it is enforced (you cannot bypass it)

- The keyword list lives at `/Users/juribuora/ai-agent-laptop/config/outreach-blocklist.txt`.
- `scripts/make-outreach-draft.py` checks every prospect's **company name + email + URL** against that list (case-insensitive substring). If it matches, the script prints `SKIPPED — exclusion rule matched '<keyword>'` and writes **no draft**, so nothing can be sent.
- `scripts/run-outreach-batch.sh` reports how many prospects were skipped.

## Rules for you (the executing model)

1. **Do not remove or weaken** entries in the blocklist. You may only ADD categories if Juri asks.
2. When researching/scraping prospects, still prefer to exclude these categories at the source — do not even add them to a prospects list. The code is a safety net, not a licence to be careless.
3. It intentionally **over-blocks** (e.g., "legale" is broad). That is on purpose: skipping a borderline business is fine; emailing a lawyer/bank/tax office is not.
4. If you think a legitimate prospect was wrongly blocked, do **not** override — log it in `BLOCKERS.md` for Juri to decide.

## Test the guard works (run this anytime)

```bash
cd /Users/juribuora/ai-agent-laptop
python3 scripts/make-outreach-draft.py --batch EXCLTEST --to info@studiolegalerossi.it --company "Studio Legale Rossi" --url https://studiolegalerossi.it
# expect: "SKIPPED — exclusion rule matched 'studio legale'..." and NO file created
ls /Users/juribuora/website-trust-security-mini-audit/operations/outbox/EXCLTEST-*.json 2>/dev/null && echo "FAIL: draft was created" || echo "OK: no draft created"
```
