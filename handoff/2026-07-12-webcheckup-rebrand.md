# Handoff - WebCheckup Rebrand (2026-07-12)

## Outcome

The service is now branded **WebCheckup**. The canonical local repository is:

```text
/Users/juribuora/webcheckup
```

The former `/Users/juribuora/website-trust-security-mini-audit` location is a compatibility symlink to the canonical folder, so existing historical notes and integrations keep resolving during the transition. The GitHub repository slug remains `webcheckup-online`, matching the public domain.

## Changed

- Updated visible IT/EN/PL/RO landing-page titles, headers, footers, privacy pages, and form email subjects.
- Updated report templates, PDF metadata, public sample-report Markdown, PDFs, and preview images.
- Updated project documentation and operational command examples to the canonical path.
- Updated current `ai-agent-laptop` prompts, skills, scripts, agent-profile paths, and Agent UI configuration to use `/Users/juribuora/webcheckup`.

## Verified

- `python3 scripts/validate_business_repo.py` passed.
- Python scripts compile and `landing-page/intake.js` passes syntax validation.
- Local browser checks confirmed the WebCheckup title, header, footer, English page, and privacy page render correctly.
- The four regenerated public sample-report covers were rendered and visually checked.

## Next

Commit and push the WebCheckup brand assets to deploy them through the existing GitHub Pages workflow. The retained compatibility symlink is local only and is not part of the Git repository.
