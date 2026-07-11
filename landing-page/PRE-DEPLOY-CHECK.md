# Pre-Deploy Check

- [ ] La preview locale della pagina restituisce `200`
- [ ] La hero mostra prezzo e consegna coerenti con l'offerta (`€49`, `2 giorni lavorativi`)
- [ ] Tutti i link principali e i `href` sono stati controllati a vista
- [ ] Nessun file `.bak` viene incluso nel commit o nel deploy
- [ ] Nessun segreto o chiave sensibile e esposto in `landing-page/intake.js`
- [ ] Il form mantiene validazione e stato di successo
- [ ] Il riepilogo del form mostra il testo inserito come testo, senza renderizzare HTML
- [ ] Entrambe le conferme (sito pubblico e informativa privacy) sono richieste e ricevute nell'email del form
- [ ] Le pagine privacy IT/EN/PL/RO, `robots.txt` e `sitemap.xml` restituiscono `200`
- [ ] Il CSP meta lascia funzionare il form AJAX e il fallback FormSubmit
- [ ] Il layout mobile e leggibile e senza CTA rotte
- [ ] Il testo "Analisi esterna e non invasiva - non e un pen-test." e presente
- [ ] Prezzo, tempi e scope combaciano con `offer/mini-audit-one-page.md`

Deploy is a HUMAN step - see `DEPLOY_GITHUB_PAGES.md`.

## Hosting security headers

GitHub Pages does not provide repository-level response-header configuration. The pages include a restrictive CSP and referrer policy meta tag, but HSTS, `X-Content-Type-Options`, `Permissions-Policy`, and clickjacking protection must be configured by a CDN/proxy or a host that supports response headers. Do not claim those headers are active until a live header check confirms them.
