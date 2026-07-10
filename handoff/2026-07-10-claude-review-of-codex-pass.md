# Claude Review Of Codex Improvement-Plan Pass - 2026-07-10

## Main target

Double-check the work codex did executing `improvement-plan/01-04` plus the
separate repo-hardening pass, fix anything found, run the tests myself, and
commit/push cleanly.

## What I found on review

- The actual content produced by codex (outreach copy, niche variants,
  targeting rules, checklist rubric, report template, finding examples,
  offer one-pager, FAQ, service ladder, landing page hero/trust strip/FAQ,
  pre-deploy checklist) is solid, internally consistent, and matches the
  plan's requirements task by task. Price (`€49`), delivery (`2 giorni
  lavorativi`), and revision policy (`1 revisione minore entro 7 giorni`)
  agree everywhere I checked (grep across all client-facing `.md` files).
- One real gap: the "repo hardening pass" tightened `.gitignore` to a
  blanket-ignore-then-allowlist pattern, but the allowlist never covered
  `templates/`, `checklists/`, `offer/`, `proof/`, `operations/`,
  `handoff/`, or `improvement-plan/`. Files already tracked before that
  change stayed tracked (git doesn't untrack existing files), but several
  important files had **never** been committed at all, most notably
  `templates/audit-report-template.md` - the actual report template the
  whole €49 product is built on. Also missing: the delivery message and
  phone-summary templates, the testimonial request, the case study, both
  folder READMEs, and the improvement-plan task files themselves.

## What I changed

- Extended `.gitignore` to explicitly track those directories as source,
  while still excluding real runtime/PII data: `operations/logs`,
  `operations/outbox`, `operations/prospects`, `operations/plans`,
  `operations/delivery-log.csv`, `clients/`, `output/`, `tmp/`, plus the
  usual `*.bak` / `.DS_Store` / `__pycache__` noise.
- Committed the previously-untracked safe source files (see commit
  `d3bb0a4`).
- Updated `improvement-plan/PROGRESS.md` with this review pass.

## Commands and checks re-run

- `python3 scripts/validate_business_repo.py` - all checks pass
- `python3 -m py_compile scripts/create_client_folder.py scripts/generate_report_pdf.py scripts/validate_business_repo.py`
- Filled every placeholder in `templates/audit-report-template.md` and ran
  `scripts/generate_report_pdf.py` -> valid 6-page PDF (`/tmp/sample-check.pdf`)
- Confirmed the placeholder guard refuses `templates/audit-report-template.md`
  as-is (unfilled placeholders) and only proceeds with `--allow-placeholders`
- Served `landing-page/` on `127.0.0.1:8899`: HTTP 200, page contains
  "Richiedi il check-up" (CTA), "non invasiva", and "check-up" repeatedly
- `grep -rniE '49|giorni|revision|pagament'` across all client-facing docs:
  no inconsistent price/delivery claims outside the intentional
  `[DECISIONE-JURI]` Tier 2 price range and old client-specific work in
  `clients/` (not part of the offer, not tracked in git)

## Not verified (out of reach from this environment)

- `ai-agent-laptop/scripts/make-outreach-draft.py --variant` wiring (task
  01-06) lives in a different folder not mounted in this session; PROGRESS.md
  already logs it done under commit `4976865` in that other repo.

## Commits from this pass

- `d3bb0a4` `harden: track core report templates, offer/proof docs, handoff history and plan files`

## Next steps for Juri

- Confirm the `[DECISIONE-JURI]` items: payment method, receipt/invoice
  wording, and the Tier 2 price range (`€99-149`) in `offer/scala-servizi.md`
  and `operations/payment-and-delivery-flow.md`.
- Review `proof/public-sample-report.md` before it's ever linked publicly.
- Deploy is still a human step - see `landing-page/PRE-DEPLOY-CHECK.md` and
  `DEPLOY_GITHUB_PAGES.md`.
