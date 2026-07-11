# Handoff - Security and Trust Mini-Audit (2026-07-10)

## Target

Review the `website-trust-security-mini-audit` repository and the public deployment for security, trust, reliability, and maintainability issues. This was a read-only audit of product code/configuration; no production submission was sent and no fix was deployed.

## Overall verdict

The local repository is organized, internally consistent, and keeps real client data out of Git. The public service is **not currently production-ready**, mainly because the custom domain has invalid HTTPS and production is 21 commits behind the local `main` branch.

## Findings

### P0 - Custom-domain HTTPS is invalid

- `https://www.webcheckup.online/` presents a certificate for `*.github.io`, not `www.webcheckup.online`.
- Standards-compliant clients reject the connection with a hostname mismatch.
- GitHub Pages reports `cname: www.webcheckup.online` but `https_enforced: false`.
- `http://www.webcheckup.online/` serves content directly instead of redirecting to HTTPS.

Recommended fix: repair/verify the GitHub Pages custom-domain configuration, wait for GitHub to provision the correct certificate, then enable **Enforce HTTPS**. Re-test without `curl -k` before any outreach sends traffic to the site.

### P1 - Production is stale and multilingual routes are broken

- Local `main` is 21 commits ahead of `origin/main`.
- The last successful Pages deployment was 2026-07-03.
- Live `/en/`, `/pl/`, and `/ro/` return 404 even though those pages exist locally.
- The live page still loads `intake.js?v=3`; local code uses `v=4`.

Recommended fix: review and push the 21 local commits, confirm the Pages workflow succeeds, and smoke-test all four languages and their PDFs.

### P1 - DOM injection in the intake summary

- `landing-page/intake.js:121-126` inserts visitor-controlled form values with `innerHTML`.
- A crafted name, URL, or goal can inject markup/scripts into the visitor's page before submission.

Recommended fix: build the summary with DOM nodes and `textContent` (or apply strict escaping); do not interpolate form values into HTML.

### P1 - Missing privacy/data-processing disclosure for the lead form

- The form collects name, email, optional phone/WhatsApp, website, business context, and free-text notes.
- Data is sent to third-party FormSubmit, but the page does not link to a privacy notice or disclose that processor/retention path.
- The checkbox only authorizes a public, non-invasive website review; it is not a privacy acknowledgement.

Recommended fix: add an appropriate privacy notice and a clearly linked disclosure beside the form, reviewed for the actual business setup and FormSubmit usage. This is a legal/operational item to verify with a qualified adviser, not a claim that the site is or is not GDPR-compliant.

### P2 - Consent evidence is not submitted

- The required checkbox in all four language pages has an `id` but no `name` or `value`, so it is omitted from `FormData` and the fallback POST.

Recommended fix: add a stable `name` and explicit value in every language page, and include it in tests.

### P2 - Success state can be spoofed

- Any visitor can append a query containing `sent=1` and the page hides the form and claims the request was received.
- The code uses substring matching, so unrelated query values containing that text also trigger success.

Recommended fix: show success only immediately after a confirmed AJAX response, or use a session-scoped marker; if the fallback redirect must be supported, parse the query exactly and document that it is only a display hint.

### P2 - Missing browser hardening headers

- The live homepage lacks HSTS, CSP, `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy`, and clickjacking protection.
- GitHub Pages offers limited custom-header control, so a fronting platform/CDN may be needed for a proper policy.

Recommended fix: after HTTPS is repaired, choose hosting/fronting that can set headers; start with a tested CSP compatible with FormSubmit, HSTS, `nosniff`, a conservative referrer policy, permissions policy, and `frame-ancestors`.

### P2 - SEO discovery files are absent

- Live `/robots.txt` and `/sitemap.xml` return 404.

Recommended fix: add both files and include all four canonical language URLs in the sitemap.

### P3 - Workflow actions are tag-pinned, not commit-SHA-pinned

- The Pages workflow uses version tags for GitHub Actions.

Recommended fix: pin third-party action revisions to full commit SHAs and use Dependabot/Renovate or a documented update process.

### P3 - Business decisions remain unresolved

- Payment method and receipt/invoice handling remain marked `[DECISIONE-JURI]`.
- PLN/RON pricing and the €99-149 second tier are also not final.

Recommended fix: settle payment/receipt handling before taking paid orders; resolve localized pricing before targeted Polish/Romanian promotion.

### P3 - Local Git object housekeeping

- `git fsck --full --no-reflogs` reports one dangling blob.
- `git count-objects` reports 120 temporary garbage objects (~1.27 MiB).

Recommended fix: only after confirming no recovery work is needed, run normal Git maintenance (`git gc`) during a quiet session. This is housekeeping, not a security incident.

## Positive checks

- Working tree was clean at audit start.
- `python3 scripts/validate_business_repo.py` passed all checks.
- Python scripts compile; `landing-page/intake.js` passes `node --check`.
- No obvious credentials/private keys were found in tracked source.
- Real clients, outbox, prospects, delivery log, logs, temp output, and generated runtime data are ignored by Git.
- Git history did not reveal tracked client/outbox/prospect paths in the targeted check.
- No duplicate HTML IDs or broken local asset/anchor references were found across IT/EN/PL/RO pages.
- Python subprocess usage is argument-array based; no `shell=True`, `eval`, or `exec` pattern was found.
- GitHub Actions permissions are limited to the permissions needed for Pages deployment.

## Checks run

- Repository guidance, README, runbook, prior service audit, and handoff reviewed.
- `python3 scripts/validate_business_repo.py`
- `python3 -m compileall -q scripts`
- `node --check landing-page/intake.js`
- `git diff --check`, targeted secret/history scans, local-link and duplicate-ID checks
- DNS, TLS certificate, HTTP/HTTPS behavior, live route/status, response-header, GitHub Pages API, and Actions-run checks

## Recommended order

1. Repair custom-domain certificate and enforce HTTPS.
2. Review/push the 21 commits and verify the multilingual deployment.
3. Replace unsafe `innerHTML`, fix consent submission, and harden the success state.
4. Add the privacy/data-processing disclosure.
5. Add security headers (or move/front hosting), sitemap, and robots file.
6. Pin Actions by SHA, settle business decisions, and do Git housekeeping.

## What not to do

- Do not claim the privacy item is a full GDPR determination.
- Do not test the production form with a real submission unless the mailbox owner expects the message.
- Do not run destructive Git cleanup before confirming no dangling object is needed.
