# WebCheckup

Progetto per vendere un servizio semplice e pratico di check-up sito web per piccole attività italiane.

Il brand è **WebCheckup**. Il posizionamento principale è:

> WebCheckup — Sicurezza, Fiducia e Visibilità

L'obiettivo è validare velocemente un'offerta da €49 senza costruire un SaaS o un processo troppo complesso.

## Offerta

Per €49 il cliente riceve un report PDF semplice con:

- problemi visibili sul sito
- priorità chiare
- impatto sul business
- raccomandazioni pratiche
- indicazione di chi può sistemare ogni punto

Il servizio è un'analisi esterna e non invasiva. Non è un penetration test.

## Cosa controllare

- Prima impressione e fiducia
- Usabilità mobile
- Velocità del sito
- HTTPS / SSL / TLS
- Header di hardening browser
- SEO base
- Link rotti
- Privacy / cookie visibili
- Contatti e percorso di conversione
- Piano di priorità
- Appendice evidenze tecniche

## File principali

- `landing-page/index.html`: pagina statica in italiano per vendere il check-up
- `landing-page/styles.css`: stile della landing page
- `landing-page/intake.js`: logica del funnel multi-step e invio richiesta
- `DEPLOY_GITHUB_PAGES.md`: guida pratica per pubblicare su GitHub Pages con `www.webcheckup.online`
- `offer/mini-audit-one-page.md`: definizione pratica dell'offerta, inclusioni, esclusioni, turnaround, pagamento e revisione
- `templates/audit-report-template.md`: template report pronto per essere esportato in PDF
- `templates/summary-cliente-phone-template.md`: sintesi breve da inviare o leggere da telefono
- `templates/delivery-message-template.md`: messaggio breve di consegna del report
- `templates/testimonial-request.md`: richiesta breve di testimonianza dopo la consegna
- `templates/outreach-message.md`: primo messaggio commerciale
- `templates/follow-up-message.md`: messaggio di follow-up
- `checklists/website-audit-checklist.md`: checklist operativa per eseguire audit coerenti
- `checklists/report-ready-qa-checklist.md`: checklist finale per decidere se il report è davvero pronto
- `scripts/create_client_folder.py`: script per creare cartelle cliente ordinate
- `scripts/generate_report_pdf.py`: generatore PDF riutilizzabile con metadata, page break, tabelle, immagini e appendice evidenze
- `operations/`: note prospect, bozze email e log operativi creati dal local agent
- `proof/`: sample report pubblico e case study anonimo

## Quick Start Operatore

Se vuoi gestire un cliente senza perderti, segui solo questo ordine:

1. leggi `operations/one-client-runbook.md`
2. tieni aperti anche:
   - `offer/mini-audit-one-page.md`
   - `checklists/report-ready-qa-checklist.md`
   - `operations/payment-and-delivery-flow.md`
   - `operations/too-few-findings-policy.md`
3. se il lead risponde, crea il pacchetto cliente (aggiungi `--language en|pl|ro` se il lead non è italiano - vedi sotto):

```bash
cd /Users/juribuora/webcheckup
python3 scripts/create_client_folder.py "Nome Attivita" \
  --website "https://www.esempio.it" \
  --contact-email "email@example.com"
```

4. aggiorna `notes.md`
5. salva screenshot e risultati in `screenshots/` e `raw-results/`
6. compila `report/report-completo.md`
7. passa la checklist `checklists/report-ready-qa-checklist.md`
8. genera il PDF
9. aggiorna `report/summary-cliente-phone.md`, `report/messaggio-consegna.md` e `report/messaggio-webmaster.md`
10. registra la consegna in `operations/delivery-log.csv`
11. chiudi con `handoff.md`

Il comando sopra non crea solo cartelle: prepara anche i file base per report, consegna e handoff.
In piu copia anche una checklist locale `report/checklist-prima-consegna.md` per il gate finale prima del PDF.

## Productization Defaults

Per evitare ambiguità, il repo adesso assume questi default:

- prezzo mini-audit: `€49`
- consegna standard: entro `2 giorni lavorativi` dopo conferma pagamento
- pagamento: prima del report completo
- revisione inclusa: `1` giro chiarimenti entro `7 giorni`
- se emergono troppo pochi finding utili, non si forza la vendita del report

I dettagli operativi sono in:

- `offer/mini-audit-one-page.md`
- `operations/payment-and-delivery-flow.md`
- `operations/too-few-findings-policy.md`

## Repo checks

Per un controllo rapido della coerenza del repo e dello scaffold cliente:

```bash
cd /Users/juribuora/webcheckup
python3 scripts/validate_business_repo.py
```

Il check verifica i file chiave, alcuni testi di allineamento e fa uno smoke test di `scripts/create_client_folder.py` in una cartella temporanea.

## Local Agent

Il local agent generale vive qui:

```text
/Users/juribuora/ai-agent-laptop/scripts/local-agent
```

Wrapper specifico per questo progetto:

```bash
/Users/juribuora/ai-agent-laptop/scripts/website-audit-agent "trova prossime azioni per il servizio"
```

Helper per ricerca prospect + bozza outreach:

```bash
/Users/juribuora/ai-agent-laptop/scripts/draft-website-audit-outreach.sh "Nome Attività" "https://example.com" "email@example.com"
```

Le email create dal local agent finiscono in:

```text
operations/outbox
```

Non vengono inviate automaticamente. Devono essere revisionate e approvate da Juri.

## Workflow consigliato

1. Trova 10 piccole attività locali con sito web migliorabile.
2. Manda il messaggio in `templates/outreach-message.md`.
3. Se rispondono, fai una mini-analisi gratuita di 2-3 punti.
4. Se accettano, crea una cartella cliente:

```bash
python3 scripts/create_client_folder.py "Nome Cliente" \
  --website "https://www.esempio.it" \
  --contact-email "email@example.com"
```

5. Raccogli screenshot e risultati non invasivi.
6. Compila `clients/nome-cliente/report/report-completo.md`.
7. Esporta il report in PDF con lo script del progetto (aggiungi `--lang en|pl|ro` se il cliente non è italiano, cosi titolo, intestazioni e piè di pagina escono nella lingua giusta):

```bash
/Users/juribuora/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  scripts/generate_report_pdf.py clients/nome-cliente/report/report-completo.md \
  --output clients/nome-cliente/report/report-completo.pdf \
  --title "Check-up Sito Web - Nome Cliente"
```

8. Controlla visivamente il PDF prima di inviarlo.
9. Aggiorna la sintesi telefono e i messaggi di consegna.
10. Proponi un piccolo upsell solo se emerge un bisogno concreto.

## Proof Assets

Per mostrare il servizio senza improvvisare ogni volta:

- `proof/public-sample-report.md`
- `proof/public-sample-report.pdf`
- `proof/case-study-local-business-checkup.md`

## Intake Funnel

La landing page non usa più `mailto:` come CTA principale.

Ora il flusso è:

- CTA principali -> sezione `#contatto`
- form guidato in 3 step
- invio verso `FormSubmit`
- fallback al submit classico se la chiamata AJAX fallisce

Nota operativa importante:

- alla prima richiesta reale, `FormSubmit` invierà una mail di conferma all'indirizzo destinatario
- dopo la conferma iniziale, conviene sostituire l'email nuda nell'`action` con la stringa invisibile/obfuscated fornita da `FormSubmit`

Stato attuale:

- la landing page usa già la stringa endpoint obfuscated di produzione per `FormSubmit`

## Lingue disponibili (IT, EN, PL, RO)

Il servizio ora si vende in 4 lingue: italiano (default), inglese, polacco e rumeno. L'idea è consegnare al cliente la lingua giusta in base a dove/come è arrivato, non tradurre a caso.

**Sito:**

- `landing-page/index.html` (italiano, alla radice)
- `landing-page/en/index.html`, `landing-page/pl/index.html`, `landing-page/ro/index.html`
- ogni pagina ha un piccolo cambio-lingua IT/EN/PL/RO in alto e i tag `hreflang` per i motori di ricerca
- `landing-page/intake.js` è condiviso da tutte e 4 le pagine: legge la lingua da `<html lang="...">` e mostra i testi del form (stato invio, riepilogo) nella lingua giusta, ma i nomi interni dei campi restano identici in italiano così l'email di notifica arriva sempre con le stesse colonne
- ogni form ha un campo nascosto `Fonte` diverso per lingua (`landing-page-en`, `landing-page-pl`, `landing-page-ro`) - **usa questo valore nell'email di notifica per sapere subito in che lingua rispondere e in che lingua creare il pacchetto cliente**

**Materiali outreach (bozze, non ancora da inviare senza verifica):**

- `templates/international/{en,pl,ro}/outreach-message.md` e `follow-up-message.md`
- leggi `templates/international/README.md` prima di usarli: le regole sull'email commerciale a freddo non sono identiche in tutti i paesi (i paesi nordici in particolare sono più restrittivi), quindi sono bozze pronte per revisione, non email pronte per l'invio

**Report cliente vero e proprio:**

- `templates/international/{en,pl,ro}/audit-report-template.md`, `delivery-message-template.md`, `summary-cliente-phone-template.md`, `testimonial-request.md` - stessa struttura e stessi placeholder `{{...}}` dell'italiano, solo tradotti
- `scripts/create_client_folder.py --language en|pl|ro` sceglie automaticamente il set di template giusto e traduce anche il messaggio pronto per il webmaster; `notes.md` e `handoff.md` restano sempre in italiano (sono per uso interno di Juri) ma registrano la lingua del cliente
- `scripts/generate_report_pdf.py --lang en|pl|ro` traduce copertina, etichette e piè di pagina del PDF; il PDF incorpora il font Liberation Sans (in `scripts/fonts/`) cosi caratteri come ń ś ć ł polacchi o ă â î ș ț rumeni non escono come quadratini
- `proof/international/{en,pl,ro}/public-sample-report.md` + `.pdf`: stesso esempio anonimizzato dell'italiano, tradotto, collegato dalla rispettiva pagina lingua (`landing-page/assets/public-sample-report-en.pdf` ecc.)

**Prezzo:** resta `€49` in tutte le lingue per ora, non convertito in PLN/RON. `[DECISIONE-JURI]`: valutare se e quando localizzare il prezzo per i mercati non-euro.

## GitHub Pages

Il progetto è stato predisposto per GitHub Pages con dominio:

- `www.webcheckup.online`

File chiave:

- `.github/workflows/deploy-pages.yml`
- `landing-page/CNAME`
- `landing-page/.nojekyll`
- `DEPLOY_GITHUB_PAGES.md`

## Strumenti consigliati

- Google PageSpeed Insights
- Mozilla HTTP Observatory
- Qualys SSL Labs
- Wappalyzer
- DevTools del browser in modalità mobile
- Controlli SEO manuali
- Revisione manuale cookie/privacy
- Controllo manuale dei link principali

## Da evitare

- scansioni aggressive
- exploit
- test su login
- brute force
- fuzzing di directory
- sqlmap
- Nessus
- Burp Suite in modalità intrusiva

## Disclaimer da includere nei report

> Nota importante: questo check-up è un'analisi esterna e non invasiva del sito web. Non include penetration test, scansioni aggressive, accesso ad aree riservate, test su login, exploit o verifiche legali complete. Le osservazioni su privacy/cookie non costituiscono consulenza legale, ma indicano elementi visibili che possono essere verificati con il proprio consulente o fornitore web.
