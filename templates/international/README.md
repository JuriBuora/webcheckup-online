# International Outreach Templates

Translated versions of `templates/outreach-message.md` and `templates/follow-up-message.md` for markets beyond Italy, to go with the `landing-page/en/`, `landing-page/pl/` and `landing-page/ro/` site versions.

Structure:

- `en/outreach-message.md`, `en/follow-up-message.md` - English
- `pl/outreach-message.md`, `pl/follow-up-message.md` - Polish
- `ro/outreach-message.md`, `ro/follow-up-message.md` - Romanian

Placeholders (`{{OSSERVAZIONE}}`, `{{NOME_ATTIVITA}}`, `{{URL}}`) are kept identical to the Italian originals on purpose, so any future automation that fills them (e.g. `make-outreach-draft.py` in `ai-agent-laptop`) does not need separate logic per language.

Price is kept at `€49` in every language for now, matching the Italian offer, rather than converting to local currency (PLN, RON, and eventually NOK/SEK/DKK). `[DECISIONE-JURI]`: confirm whether to keep a single €-denominated price across all markets or localize it later - Poland and Romania are not eurozone, so a converted local-currency price may read as more natural to a local business owner, at the cost of needing to update it whenever exchange rates move materially.

## Before sending anything in these languages - read this first

The existing Italian rules in `improvement-plan/EXCLUSIONS.md` and `improvement-plan/targeting-rules.md` still apply everywhere (no lawyers, banks, accountants, tax bodies; daily send cap; approval gate only).

On top of that, cold B2B email rules differ by country and are **not** all identical to Italy's:

- Poland and Romania are both EU/GDPR countries with ePrivacy-style rules similar in spirit to Italy's, but local implementation details (e.g. what counts as legitimate interest for a first unsolicited business email) differ - worth a quick check before a real batch, not just an assumption of "same as Italy".
- The Nordic countries (Norway, Sweden, Denmark) are generally considered **stricter** on unsolicited commercial email, including B2B, under their national marketing-control acts. A daily cap and a clean opt-out are not automatically sufficient there.
- None of this is legal advice - it is a flag to get a real, current answer (a lawyer, or at minimum up-to-date official guidance for the target country) before running outreach into a new country, not to block translating the templates themselves.

**Until Juri confirms this per country, treat these translated templates as drafts ready for review, not as cleared for sending.** Nothing in this folder is wired into the outreach automation - they are plain Markdown files, same as the Italian ones, requiring the same human approval before anything goes out.
