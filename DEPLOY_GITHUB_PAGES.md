# Deploy To GitHub Pages

This project is ready to publish the landing page from GitHub Pages using:

- GitHub account: `JuriBuora`
- Pages host target: `JuriBuora.github.io`
- public domain: `www.webcheckup.online`

## Repo setup

Files already added:

- `.github/workflows/deploy-pages.yml`
- `landing-page/.nojekyll`

The workflow deploys the contents of `landing-page/` to GitHub Pages on every push to `main`.

Important:

- this repo publishes through a GitHub Actions workflow
- with GitHub Actions publishing, the custom domain is set in GitHub Pages settings or via the Pages API
- a `CNAME` file is not required for this workflow-based setup and is ignored by GitHub Pages

## GitHub steps

1. Create a new GitHub repository under the `JuriBuora` account.
2. Push this project to the `main` branch of that repository.
3. Create or enable the Pages site with build type `workflow`.
4. Let the workflow run once.

After the first successful run, GitHub Pages should publish a default Pages URL under the `github.io` host for the repository.

## Namecheap DNS for `www.webcheckup.online`

Recommended setup if `www` is the canonical live domain:

### Required record

- `CNAME`
  - host: `www`
  - value / target: `JuriBuora.github.io`
  - TTL: automatic/default

### Recommended root-domain behavior

For the bare domain `webcheckup.online`, choose one of these:

1. Simpler: redirect `@` to `https://www.webcheckup.online`
2. Direct GitHub Pages support for apex:
   - use the GitHub Pages apex A records instead of only a redirect

If you want the site to live only on `www`, the redirect option is cleaner.

## GitHub custom domain

In the GitHub Pages settings for the repository:

1. set the custom domain to `www.webcheckup.online`
2. save
3. wait for DNS check to pass
4. then enable `Enforce HTTPS`

## Important note

The site is currently a static landing page. There is no backend deployment step required.

The intake funnel already points at the production FormSubmit token:

- normal POST: `https://formsubmit.co/e8ec857b0d8bfe719a8a391d716536b2`
- AJAX POST: `https://formsubmit.co/ajax/e8ec857b0d8bfe719a8a391d716536b2`

## After deploy

Smoke-test these on the public URL:

1. homepage loads
2. all language routes (`/en/`, `/pl/`, `/ro/`) and their privacy pages load
3. sample PDF opens
4. `robots.txt` and `sitemap.xml` load
5. form moves through all 3 steps, requires both acknowledgements, and renders typed HTML as text
6. one real submission succeeds only when the mailbox owner expects it
7. HTTPS is active on `https://www.webcheckup.online` and HTTP redirects there

## Header limitation on GitHub Pages

The deployed pages include a restrictive CSP and referrer-policy meta tag. GitHub Pages itself cannot set response headers such as HSTS, `X-Content-Type-Options`, `Permissions-Policy`, or clickjacking protection. Put the site behind a CDN/proxy that supports header rules, or move it to a host that does, before treating those protections as deployed.
