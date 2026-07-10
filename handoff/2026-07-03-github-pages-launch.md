# GitHub Pages Launch Handoff

## Main target

Publish the landing page to GitHub Pages under Juri's GitHub account and connect it cleanly to `www.webcheckup.online` without exposing private client or operations files.

## What was done

- created a public-safe git setup using a whitelist `.gitignore`
- initialized git in `/Users/juribuora/website-trust-security-mini-audit`
- created the public GitHub repo `JuriBuora/webcheckup-online`
- pushed the landing page, Pages workflow, and deploy guide
- enabled GitHub Pages for the repo with build type `workflow`
- set the custom domain in GitHub Pages to `www.webcheckup.online`
- removed the unused `landing-page/CNAME` file after confirming GitHub ignores it for workflow-based Pages
- updated `DEPLOY_GITHUB_PAGES.md` to match the real GitHub Pages behavior

## Files changed

- `/Users/juribuora/website-trust-security-mini-audit/.gitignore`
- `/Users/juribuora/website-trust-security-mini-audit/.github/workflows/deploy-pages.yml`
- `/Users/juribuora/website-trust-security-mini-audit/DEPLOY_GITHUB_PAGES.md`
- `/Users/juribuora/website-trust-security-mini-audit/landing-page/index.html`
- `/Users/juribuora/website-trust-security-mini-audit/landing-page/intake.js`
- `/Users/juribuora/website-trust-security-mini-audit/landing-page/styles.css`
- `/Users/juribuora/website-trust-security-mini-audit/landing-page/.nojekyll`
- `/Users/juribuora/website-trust-security-mini-audit/landing-page/assets/public-sample-report.pdf`
- `/Users/juribuora/website-trust-security-mini-audit/landing-page/assets/sample-report-page.png`

## GitHub state

- repo: `https://github.com/JuriBuora/webcheckup-online`
- default Pages URL is serving correctly: `https://juribuora.github.io/webcheckup-online/`
- Pages custom domain is configured to: `www.webcheckup.online`
- latest successful workflow runs:
  - `28668319873`
  - `28668452772`

## Commands and checks used

- `git init -b main`
- `gh repo create JuriBuora/webcheckup-online --public --source=. --remote=origin --push`
- `gh api -X POST repos/JuriBuora/webcheckup-online/pages -f build_type=workflow`
- `gh api -X PUT repos/JuriBuora/webcheckup-online/pages -f cname=www.webcheckup.online -f build_type=workflow`
- `gh run watch ... --exit-status`
- `curl -I https://juribuora.github.io/webcheckup-online/`
- `gh api -i repos/JuriBuora/webcheckup-online/pages/health`
- `dig +short www.webcheckup.online CNAME`

## Current state

GitHub is ready.

The only blocker for the custom domain is DNS at Namecheap.

Current DNS check shows:

- `www.webcheckup.online` currently points to `parkingpage.namecheap.com`
- apex `webcheckup.online` currently resolves to `192.64.119.58`
- GitHub Pages health check reports the `www` CNAME is not pointing to `juribuora.github.io`
- HTTPS is not yet enforceable because the DNS is still on Namecheap parking

## Next steps

In Namecheap:

1. Change `www` to a `CNAME` pointing to `juribuora.github.io`
2. Decide what to do with the apex `webcheckup.online`
3. Recommended: redirect apex to `https://www.webcheckup.online`
4. Wait for DNS propagation
5. Re-check Pages health
6. Enable HTTPS once GitHub issues the certificate

## What to double-check

- form submissions still arrive after the public domain is live
- the sample PDF opens from the public domain
- no mixed-content or path issues appear after switching from the GitHub URL to the custom domain
- apex redirect behavior from Namecheap

## What not to do

- do not push `clients/`, `operations/`, `handoff/`, or other local private folders into the public repo
- do not rely on a `CNAME` file for this workflow-based Pages setup
- do not enable HTTPS on GitHub Pages until the custom domain DNS is correct and the certificate exists
