<!-- DA RIVEDERE DA JURI PRIMA DELLA PUBBLICAZIONE -->

# Check-up Sito Web - Esempio Report Pubblico

## Sicurezza, Fiducia e Visibilità

**Cliente:** Attività di esempio  
**Sito analizzato:** https://www.esempio-attivita.it/  
**Data:** 10/07/2026  
**Tipo di controllo:** Analisi esterna e non invasiva  
**Preparato da:** Juri

---

## 1. Riepilogo in parole semplici

Questo esempio pubblico serve a mostrare il formato del check-up: un report breve, concreto e leggibile anche da chi non gestisce il sito ogni giorno. In questo caso il sito comunica l'attività in modo abbastanza chiaro, ma perde qualcosa su mobile e nella chiarezza del percorso contatto; inoltre presenta alcuni margini tecnici semplici da far verificare al webmaster.

In sintesi: l'obiettivo non è dimostrare che un sito sia "sicuro" o "conforme", ma indicare in ordine pratico cosa conviene sistemare prima per non perdere fiducia, leggibilità e richieste.

---

## 2. Tabella priorità

| Problema | Impatto | Priorità | Chi lo sistema |
| --- | --- | --- | --- |
| Testi secondari poco leggibili da mobile | Alcuni utenti leggono con fatica descrizioni e dettagli utili su smartphone | Alta | Webmaster / frontend |
| CTA principale poco chiara | Parte delle visite non capisce subito come contattare o chiedere un preventivo | Media | Titolare / webmaster |
| Header browser di base mancanti | La configurazione tecnica trasmette meno affidabilita del necessario | Bassa | Webmaster / hosting |

---

## 3. Finding principali

### Finding 1 - Testi secondari poco leggibili da mobile

**Cosa ho visto**  
La homepage resta utilizzabile da telefono, ma alcune descrizioni e testi secondari hanno contrasto debole e corpo piccolo rispetto allo sfondo.

**Perché conta**  
Una parte dei visitatori arriva da smartphone e decide in pochi secondi se continuare o uscire: se i testi fanno fatica a leggersi, cala la chiarezza dell'offerta.

**Cosa fare**  
Far aumentare contrasto, dimensione e spaziatura dei testi secondari nelle sezioni informative più importanti, poi ricontrollare la homepage su uno smartphone reale.

**Chi lo sistema**  
Webmaster / frontend

### Finding 2 - CTA principale poco chiara

**Cosa ho visto**  
Il sito presenta bene l'attività, ma la prossima azione utile non emerge subito: il visitatore deve capire da solo se chiamare, scrivere o chiedere un preventivo.

**Perché conta**  
Quando la CTA non è esplicita, una parte delle visite resta passiva e non si trasforma in contatto.

**Cosa fare**  
Sostituire la CTA generica con un invito più preciso e ripeterlo nei punti chiave della pagina, lasciando telefono e modulo facili da trovare.

**Chi lo sistema**  
Titolare per il messaggio, webmaster per posizione e stile

### Finding 3 - Header browser di base mancanti

**Cosa ho visto**  
Dal controllo esterno non risultano presenti alcuni header comuni di hardening browser come `X-Content-Type-Options` e `Referrer-Policy`.

**Perché conta**  
Non è un segnale di emergenza, ma indica una configurazione tecnica migliorabile su un sito che deve trasmettere affidabilita.

**Cosa fare**  
Far verificare a webmaster o hosting i principali header di base lato server o CDN, senza modificare il resto del sito.

**Chi lo sistema**  
Webmaster / hosting

### Finding 4 - Title e descrizione SEO troppo generici

**Cosa ho visto**  
La homepage usa un title presente ma poco specifico rispetto a servizio e localita, e la meta description non aiuta abbastanza il click dai risultati di ricerca.

**Perché conta**  
Un sito chiaro anche su Google parte meglio: aiuta sia la visibilita sia la percezione del servizio prima ancora dell'apertura della pagina.

**Cosa fare**  
Riscrivere title e meta description della homepage con attivita, area geografica e beneficio principale, mantenendo un tono semplice.

**Chi lo sistema**  
Titolare per il testo, webmaster per l'aggiornamento

---

## 4. Quick wins

1. Aumentare contrasto e leggibilita dei testi secondari nella homepage mobile.
2. Rendere piu esplicito il pulsante principale di contatto o preventivo.
3. Far controllare al webmaster i principali header browser di base.

---

## 5. Appendice tecnica essenziale

| Evidenza | Risultato sintetico | Chi agisce |
| --- | --- | --- |
| Homepage mobile | Navigabile, ma leggibilita migliorabile nei testi secondari | Webmaster |
| Percorso contatto | Presente, ma CTA da rendere piu chiara | Titolare / webmaster |
| HTTPS | Attivo, senza avvisi evidenti | Nessuna urgenza |
| Header browser | Mancano alcuni header di base | Webmaster / hosting |
| SEO homepage | Title e description da rendere piu specifici | Titolare / webmaster |

---

## 6. Nota finale

Questo report e anonimizzato e non descrive un'azienda reale. Serve solo a mostrare il formato del deliverable e il livello di chiarezza che il cliente riceve.
