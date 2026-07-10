# Checklist QA Prima Della Consegna

Usa questa checklist come gate finale. Il report non si consegna finché ogni punto richiesto non è spuntato.

## Scope e onestà

- [ ] Il report dice chiaramente che l'analisi è esterna e non invasiva
- [ ] Non c'è nessuna promessa di sicurezza completa, conformità o garanzia legale
- [ ] I finding sono specifici per il sito, non testo generico riempitivo
- [ ] Se i finding erano deboli, è stata verificata `operations/too-few-findings-policy.md`
- [ ] Il report contiene abbastanza materiale utile da giustificare il lavoro a pagamento

## Qualità del report

- [ ] `report/report-completo.md` è completo e non contiene placeholder aperti
- [ ] `grep '{{' report/report-completo.md` non restituisce risultati
- [ ] La tabella priorità è compilata e coerente con i finding
- [ ] Ogni finding spiega cosa ho visto, perché conta e cosa fare
- [ ] Ogni finding indica chi di solito sistema il problema
- [ ] Sono presenti 2-3 punti positivi reali quando utili
- [ ] Il tono resta pratico, calmo e non allarmista
- [ ] È stata fatta una rilettura finale per ortografia e chiarezza

## Evidenze e soglia minima

- [ ] Screenshot e risultati strumenti citati nel report esistono davvero
- [ ] I file tecnici sono salvati in `raw-results/`
- [ ] Date, URL e nome dominio sono corretti in tutto il pacchetto
- [ ] È rispettata la soglia minima di `operations/too-few-findings-policy.md`

## Pacchetto consegna

- [ ] `report/report-completo.pdf` genera senza errori
- [ ] Il PDF è stato controllato visivamente
- [ ] La tabella priorità è leggibile anche nel PDF
- [ ] `report/summary-cliente-phone.md` è scritto e leggibile da telefono
- [ ] `report/messaggio-consegna.md` è pronto
- [ ] `report/messaggio-webmaster.md` è pronto

## Commerciale e log

- [ ] Stato pagamento registrato in `notes.md`
- [ ] Data di consegna registrata in `notes.md`
- [ ] Messaggio di consegna scritto prima dell'invio
- [ ] `handoff.md` aggiornato con stato e prossima azione
