# Esempi di finding riutilizzabili

Usa questi esempi come base di scrittura per mantenere i report coerenti. Adatta sempre il testo al sito reale: non copiare alla cieca.

## Struttura consigliata

- Problema osservato
- Impatto business in una riga
- Fix raccomandato
- Chi di solito lo sistema

### CTA principale poco chiara

**Problema**  
La homepage presenta il servizio, ma non accompagna bene il visitatore verso la prossima azione utile.

**Impatto business**  
Se il visitatore non capisce subito come contattare o prenotare, una parte delle visite non si trasforma in richieste.

**Fix raccomandato**  
Rendere il pulsante principale piu esplicito e ripeterlo nei punti chiave della pagina.

**Chi lo sistema**  
Titolare per il messaggio, webmaster per posizione e stile.

### Testi secondari poco leggibili da mobile

**Problema**  
Su smartphone alcuni testi hanno corpo piccolo o contrasto debole rispetto allo sfondo.

**Impatto business**  
Chi legge da telefono fa piu fatica a capire l'offerta e abbandona prima di contattare.

**Fix raccomandato**  
Aumentare contrasto, corpo del testo e spaziatura nei blocchi informativi secondari.

**Chi lo sistema**  
Webmaster o frontend.

### Immagini troppo pesanti nella hero

**Problema**  
L'immagine principale rallenta l'apertura della homepage, soprattutto su rete mobile.

**Impatto business**  
Un caricamento lento fa perdere attenzione proprio prima che compaiano contenuto e contatti.

**Fix raccomandato**  
Ridurre dimensioni e peso dell'immagine hero, attivare compressione e versioni responsive.

**Chi lo sistema**  
Webmaster, con eventuale supporto hosting/CDN.

### Redirect HTTP verso HTTPS incompleto

**Problema**  
Il sito usa HTTPS, ma non tutte le richieste in HTTP vengono reindirizzate in modo coerente.

**Impatto business**  
Percorsi incoerenti riducono fiducia e possono generare avvisi o link non uniformi.

**Fix raccomandato**  
Impostare redirect forzato da HTTP a HTTPS su tutto il dominio e ricontrollare le risorse miste.

**Chi lo sistema**  
Hosting o webmaster.

### Header browser di base mancanti

**Problema**  
Mancano alcuni header comuni di hardening come `X-Content-Type-Options` o `Referrer-Policy`.

**Impatto business**  
Non e un'emergenza da sola, ma segnala una configurazione tecnica migliorabile su un sito che deve trasmettere affidabilita.

**Fix raccomandato**  
Far verificare al webmaster o al provider i principali header di sicurezza lato server o CDN.

**Chi lo sistema**  
Webmaster, hosting o CDN.

### Title e meta description generici

**Problema**  
La homepage usa un title poco descrittivo o senza riferimento chiaro a servizio e localita.

**Impatto business**  
Il sito risulta meno chiaro nei risultati di ricerca e meno convincente quando viene trovato.

**Fix raccomandato**  
Riscrivere title e meta description con attivita, zona e beneficio principale.

**Chi lo sistema**  
Titolare per i contenuti, webmaster per l'implementazione.

### Privacy policy poco visibile

**Problema**  
Il link alla privacy o alla cookie policy e assente o difficile da trovare nel footer.

**Impatto business**  
Anche senza fare affermazioni legali, una policy poco visibile riduce fiducia e chiarezza percepita.

**Fix raccomandato**  
Aggiungere link visibili nel footer e verificare con il proprio consulente o fornitore che i testi siano aggiornati.

**Chi lo sistema**  
Titolare e webmaster, con eventuale consulente privacy.

### Link di contatto o social non funzionanti

**Problema**  
Uno o piu link importanti portano a errore o a profili non piu aggiornati.

**Impatto business**  
Quando un visitatore trova un link rotto sul percorso contatto, la richiesta spesso si perde del tutto.

**Fix raccomandato**  
Controllare menu, footer, telefono, email e social principali e sostituire i collegamenti non validi.

**Chi lo sistema**  
Webmaster, con conferma del titolare per i profili corretti.
