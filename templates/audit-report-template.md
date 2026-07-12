# WebCheckup

## Sicurezza, Fiducia e Visibilità

**Cliente:** {{BUSINESS}}  
**Sito analizzato:** {{URL}}  
**Data:** {{DATA}}  
**Tipo di controllo:** Analisi esterna e non invasiva  
**Preparato da:** Juri Buora

---

## 1. Riepilogo in parole semplici

{{RIEPILOGO}}

In sintesi: ho guardato il sito dall'esterno, come farebbe un cliente o un motore di ricerca. Qui sotto trovi cosa funziona, cosa conviene migliorare e in che ordine — senza tecnicismi inutili e senza promettere "sicurezza totale" o conformità legale.

---

<!-- pagebreak -->

## 2. Tabella priorità

| Problema | Impatto | Priorità | Chi lo sistema |
| --- | --- | --- | --- |
| {{PROBLEMA_1}} | {{IMPATTO_1}} | Alta | {{CHI_1}} |
| {{PROBLEMA_2}} | {{IMPATTO_2}} | Media | {{CHI_2}} |
| {{PROBLEMA_3}} | {{IMPATTO_3}} | Bassa | {{CHI_3}} |

Legenda priorità:

- **Alta:** conviene affrontare presto perché può ridurre fiducia, contatti o funzionamento.
- **Media:** utile e concreto, ma non urgente.
- **Bassa:** miglioramento consigliato quando c'è tempo.

---

## 3. Dettaglio dei finding

Compila una sezione per ogni problema rilevante emerso dalla checklist. Duplica il blocco sotto per ogni finding.

{{FINDINGS}}

### {{TITOLO_FINDING}}

**Area:** {{AREA}} · **Priorità:** {{PRIORITA}}

#### Cosa ho visto

{{COSA_VISTO}}

#### Perché conta per il business

{{PERCHE_CONTA}}

#### Cosa fare (passi pratici)

{{COSA_FARE}}

**Chi può sistemarlo:** {{CHI_SISTEMA}}

---

### Screenshot (se disponibili)

#### Desktop

![Screenshot homepage desktop](../screenshots/homepage-desktop-viewport.png)

<!-- pagebreak -->

#### Mobile

![Screenshot homepage mobile](../screenshots/homepage-mobile-viewport.png)

<!-- pagebreak -->

---

## 4. Quick wins — 3 cose sistemabili questa settimana

Azioni piccole ma visibili che il titolare o il webmaster possono fare senza rifare il sito:

1. {{QUICK_WIN_1}}
2. {{QUICK_WIN_2}}
3. {{QUICK_WIN_3}}

---

## 5. Messaggio pronto per il webmaster

Puoi copiare e inviare questo testo a chi gestisce il sito:

> Ciao, abbiamo fatto un check-up esterno del sito e sono emersi alcuni punti da verificare. Le priorità principali sono: {{PUNTI_WEBMASTER}}. Puoi controllare fattibilità, tempi e costo per sistemarli?

---

<!-- pagebreak -->

## 6. Appendice evidenze tecniche

| Evidenza | Risultato | File sorgente |
| --- | --- | --- |
| HTTPS homepage | {{EV_HTTPS}} | `homepage-headers.txt` |
| Redirect HTTP | {{EV_REDIRECT}} | `http-redirect-headers.txt` |
| Certificato TLS | {{EV_TLS}} | `tls-certificate.txt` |
| Header di hardening | {{EV_HEADERS}} | `homepage-headers.txt` |
| Lighthouse mobile | {{EV_LH_MOBILE}} | `lighthouse-mobile.json` |
| Lighthouse desktop | {{EV_LH_DESKTOP}} | `lighthouse-desktop.json` |
| Link principali | {{EV_LINKS}} | `link-check-main.txt` |
| Privacy/cookie visibili | {{EV_PRIVACY}} | `privacy-policy.html`, `cookie-policy.html` |

---

## 7. Disclaimer

Nota importante: questo check-up è un'analisi esterna e non invasiva del sito web. Non include penetration test, scansioni aggressive, accesso ad aree riservate, test su login, exploit o verifiche legali complete. Le osservazioni su privacy/cookie non costituiscono consulenza legale, ma indicano elementi visibili che possono essere verificati con il proprio consulente o fornitore web.
