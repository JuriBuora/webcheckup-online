# Repo Hardening Pass - 2026-07-10

## Main target

Look across the repo and implement another round of improvements beyond the earlier improvement-plan pass.

## What changed

- Tightened `.gitignore` so backup files, pycache, macOS clutter, and operational runtime folders stay out of git by default
- Kept the ignore cleanup intentionally scoped so older never-tracked repo files do not all flood into this commit at once
- Upgraded `scripts/create_client_folder.py` to:
  - normalize website URLs
  - default to `€49`
  - accept `--contact-name` and `--lead-source`
  - prefill the current report metadata placeholders (`{{BUSINESS}}`, `{{URL}}`, `{{DATA}}`)
  - copy a local `report/checklist-prima-consegna.md`
- Upgraded `scripts/generate_report_pdf.py` to refuse final PDF generation when `{{PLACEHOLDERS}}` are still open, unless `--allow-placeholders` is used for internal drafts
- Added `scripts/validate_business_repo.py` to validate key repo files and run a temporary smoke test of the scaffold flow
- Updated `README.md` to document the new scaffold checklist and validator command

## Files changed

- `.gitignore`
- `README.md`
- `scripts/create_client_folder.py`
- `scripts/generate_report_pdf.py`
- `scripts/validate_business_repo.py`

## Verification

- `python3 -m py_compile scripts/create_client_folder.py scripts/generate_report_pdf.py scripts/validate_business_repo.py`
- `python3 scripts/validate_business_repo.py`
- Verified PDF guard fails on `templates/audit-report-template.md` without `--allow-placeholders`
- Verified draft PDF still works with `--allow-placeholders`
- Verified scaffold output in `/tmp/repo-improve-clients/demo-locale/`

## Notes

- The previous repo layout had many important files effectively hidden by the old ignore rules. This pass improves that situation without auto-adding unrelated historical files.
- If you later want a dedicated pass to start versioning more of the business docs, do that as a separate intentional cleanup.

## Next sensible follow-up

- Add a client-package validator that checks a real client folder before delivery
- Decide whether more of `offer/`, `proof/`, and `operations/` should become first-class tracked source in a separate git hygiene pass
