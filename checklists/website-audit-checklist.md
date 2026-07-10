# Checklist Audit Sito Web — Rubrica ripetibile

Usa questa checklist per ogni report. Ogni area ha criteri oggettivi: stesso sito, stesso operatore → stesso verdetto.

**Verdetto per area:** `OK` / `Migliorabile` / `Problema`

## Dati cliente

- [ ] Nome attività:
- [ ] URL sito:
- [ ] Data audit:
- [ ] Settore:
- [ ] Obiettivo principale del sito: chiamate / prenotazioni / richieste / vendita / visite in sede

## Regole operative

- [ ] Analisi solo esterna e non invasiva
- [ ] Nessun test su login o aree riservate
- [ ] Nessun exploit, brute force, fuzzing o scansione aggressiva
- [ ] Nessuna promessa di sicurezza completa o conformità GDPR

---

## 1. Prima impressione e fiducia

### Cosa guardare

- Homepage desktop: cosa offre l'attività, dove si trova, foto reali, contatti visibili, prove sociali, testi aggiornati
- Screenshot: homepage desktop

### Come giudicare — OK / Migliorabile / Problema

| Verdetto | Criterio oggettivo |
| --- | --- |
| **OK** | In 10 secondi si capisce attività + zona; contatto principale visibile senza scroll; nessun errore evidente o pagina vuota |
| **Migliorabile** | Attività comprensibile ma contatti, foto o prove sociali richiedono scroll/cerca; testi datati o generici ma non fuorvianti |
| **Problema** | Non si capisce cosa fa l'attività; contatti assenti o nascosti; errori visibili, pagine incomplete, immagini rotte in evidenza |

**Verdetto area:** [ ] OK / [ ] Migliorabile / [ ] Problema

### Impatto business

Se la prima impressione è debole, i visitatori abbandonano prima di chiamare o richiedere un preventivo.

### Chi sistema

Titolare (testi/foto) · Webmaster (layout/homepage) · Fotografo/copywriter se esterno

---

## 2. Mobile usability

### Cosa guardare

- Homepage su smartphone (viewport stretto o dispositivo reale): menu, testi, pulsanti, form, telefono/WhatsApp cliccabili
- Screenshot: homepage mobile

### Come giudicare — OK / Migliorabile / Problema

| Verdetto | Criterio oggettivo |
| --- | --- |
| **OK** | Testi leggibili senza zoom; menu funziona; pulsanti ≥ 44 px e non sovrapposti; telefono/email cliccabili |
| **Migliorabile** | Usabile ma testi piccoli, menu macchinoso o CTA richiede scroll eccessivo |
| **Problema** | Testo illeggibile o tagliato; menu non apre; pulsanti non cliccabili; layout desktop forzato su mobile |

**Verdetto area:** [ ] OK / [ ] Migliorabile / [ ] Problema

### Impatto business

La maggior parte dei visitatori arriva da smartphone; un sito difficile da usare riduce chiamate e richieste.

### Chi sistema

Webmaster / frontend · Hosting (solo se tema non responsive)

---

## 3. Velocità del sito

### Cosa guardare

- Google PageSpeed Insights: punteggio mobile e desktop, Largest Contentful Paint, immagini pesanti
- Salvare esportazione in `raw-results/`

### Come giudicare — OK / Migliorabile / Problema

| Verdetto | Criterio oggettivo |
| --- | --- |
| **OK** | Mobile PSI ≥ 50 oppure caricamento percepito < 4 s; nessun blocco evidente prima del contenuto |
| **Migliorabile** | Mobile PSI 30–49 oppure ritardo visibile su immagini hero; desktop accettabile |
| **Problema** | Mobile PSI < 30, pagina bianca > 5 s, o sito chiaramente bloccato dal caricamento su 4G |

**Verdetto area:** [ ] OK / [ ] Migliorabile / [ ] Problema

### Impatto business

Un sito lento fa uscire il cliente prima che trovi il telefono o il form.

### Chi sistema

Webmaster (immagini, plugin) · Hosting/CDN (cache, server)

---

## 4. HTTPS / SSL / TLS

### Cosa guardare

- Barra indirizzi: HTTPS attivo, avvisi browser
- `http://` reindirizza a `https://`
- Qualys SSL Labs (sintesi) salvata in `raw-results/`

### Come giudicare — OK / Migliorabile / Problema

| Verdetto | Criterio oggettivo |
| --- | --- |
| **OK** | HTTPS su homepage; certificato valido; nessun avviso browser; redirect HTTP→HTTPS presente |
| **Migliorabile** | HTTPS attivo ma certificato in scadenza < 30 giorni, mixed content su risorse secondarie, o redirect parziale |
| **Problema** | Solo HTTP, certificato scaduto/invalido, o avviso "Non sicuro" visibile all'utente |

**Verdetto area:** [ ] OK / [ ] Migliorabile / [ ] Problema

### Impatto business

Avvisi di sicurezza nel browser riducono la fiducia e spingono i clienti a non compilare form o chiamare.

### Chi sistema

Hosting · Webmaster (mixed content) · Titolare (rinnovo dominio/certificato)

---

## 5. Header di hardening browser

### Cosa guardare

- Mozilla HTTP Observatory sul dominio principale
- Header presenti: `Strict-Transport-Security`, `X-Content-Type-Options`, `Referrer-Policy`, `Content-Security-Policy` (almeno in forma base)
- Salvare risultato in `raw-results/`

### Come giudicare — OK / Migliorabile / Problema

| Verdetto | Criterio oggettivo |
| --- | --- |
| **OK** | Observatory ≥ B oppure ≥ 3 header di hardening presenti senza errori gravi |
| **Migliorabile** | Observatory C/D o 1–2 header mancanti su configurazione altrimenti sana |
| **Problema** | Observatory F o nessun header di hardening; configurazione palesemente assente |

**Verdetto area:** [ ] OK / [ ] Migliorabile / [ ] Problema

### Impatto business

Non blocca le vendite da solo, ma segnala maturità tecnica — utile per attività che vendono fiducia (studi, artigiani premium).

### Chi sistema

Webmaster · Hosting / CDN (configurazione server)

---

## 6. SEO base

### Cosa guardare

- Title e meta description della homepage (view-source o inspector)
- H1 unico e coerente con l'attività
- Indirizzo/località nei testi; alt text su immagini principali

### Come giudicare — OK / Migliorabile / Problema

| Verdetto | Criterio oggettivo |
| --- | --- |
| **OK** | Title descrittivo (attività + zona/servizio); meta description presente; H1 chiaro; località citata |
| **Migliorabile** | Title generico ("Home") o meta description vuota/copiata; H1 presente ma vago |
| **Problema** | Title/H1 assenti o identici su tutte le pagine; nessuna indicazione geografica per attività locale |

**Verdetto area:** [ ] OK / [ ] Migliorabile / [ ] Problema

### Impatto business

SEO base debole rende il sito meno visibile su Google e meno chiaro quando qualcuno lo trova.

### Chi sistema

Titolare (testi) · Webmaster / SEO leggero

---

## 7. Link rotti

### Cosa guardare

- Menu principale, footer, link contatti, social, CTA principali
- Verifica manuale o `link-check` in `raw-results/` — senza inviare form

### Come giudicare — OK / Migliorabile / Problema

| Verdetto | Criterio oggettivo |
| --- | --- |
| **OK** | Tutti i link del menu e footer funzionano (HTTP 200 o redirect corretto) |
| **Migliorabile** | 1 link secondario rotto (es. social vecchio) ma percorso contatto principale OK |
| **Problema** | ≥ 2 link rotti su percorsi importanti, o CTA/contatto principale non funziona |

**Verdetto area:** [ ] OK / [ ] Migliorabile / [ ] Problema

### Impatto business

Un link rotto sul pulsante "Contatti" o "Prenota" fa perdere la richiesta nel momento di massima intenzione.

### Chi sistema

Webmaster · Titolare (URL social aggiornati)

---

## 8. Privacy / cookie (osservazioni visibili)

### Cosa guardare

- Banner cookie se presenti tracker evidenti
- Link privacy policy e cookie policy nel footer
- Solo osservazioni visibili — **non** consulenza legale

### Come giudicare — OK / Migliorabile / Problema

| Verdetto | Criterio oggettivo |
| --- | --- |
| **OK** | Banner presente se serve; link privacy e cookie raggiungibili; testi leggibili |
| **Migliorabile** | Banner assente ma pochi tracker, oppure policy presente ma difficile da trovare |
| **Problema** | Tracker evidenti (Analytics, Pixel) senza banner; link policy assenti o pagine vuote |

**Verdetto area:** [ ] OK / [ ] Migliorabile / [ ] Problema

### Impatto business

Elementi privacy poco chiari possono ridurre la fiducia; segnalare come "da verificare con consulente/fornitore".

### Chi sistema

Titolare · Webmaster · Consulente privacy/fornitore cookie (per modifiche formali)

---

## 9. Percorso contatto e conversione

### Cosa guardare

- CTA principale in homepage: chiara e visibile?
- Telefono/email/WhatsApp/form: pochi passaggi per contattare
- Orari, mappa, indirizzo se rilevanti per il settore

### Come giudicare — OK / Migliorabile / Problema

| Verdetto | Criterio oggettivo |
| --- | --- |
| **OK** | CTA evidente above-the-fold; contatto in ≤ 2 tap/click; form semplice (≤ 5 campi) |
| **Migliorabile** | Contatto presente ma CTA generica ("Scopri di più") o richiede navigazione extra |
| **Problema** | Nessuna CTA chiara; contatto solo in footer piccolo; form lungo o confuso |

**Verdetto area:** [ ] OK / [ ] Migliorabile / [ ] Problema

### Impatto business

Ogni passaggio in più tra visitatore e contatto riduce le richieste che diventano clienti.

### Chi sistema

Titolare (messaggio CTA) · Webmaster (posizionamento form/bottoni)

---

## 10. Sintesi priorità (compilare dopo le 9 aree)

- [ ] Ogni area con verdetto **Problema** → priorità **Alta** nel report
- [ ] Ogni area **Migliorabile** con impatto contatti/mobile → **Media**
- [ ] Resto → **Bassa** salvo contesto settore
- [ ] 2–3 punti positivi reali inclusi nel report
- [ ] Disclaimer finale presente

## Output finale

- [ ] Screenshot in `screenshots/`
- [ ] Risultati strumenti in `raw-results/`
- [ ] Report Markdown in `report/`
- [ ] `checklists/report-ready-qa-checklist.md` completata
- [ ] PDF con `scripts/generate_report_pdf.py`
- [ ] PDF controllato visivamente
- [ ] Messaggio consegna preparato
- [ ] Consegna registrata in `operations/delivery-log.csv`
