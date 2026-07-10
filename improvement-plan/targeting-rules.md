# Regole di targeting per batch outreach

Checklist pratica per scegliere i prospect prima di creare un batch. Usala prima di ogni sessione di ricerca.

## Chi includere (preferire)

- Piccole attività locali con sito web pubblico e email di contatto visibile
- Siti con problemi plausibili e visibili dall'esterno:
  - nessun HTTPS o avviso "non sicuro" nel browser
  - layout difficile da usare su telefono (menu, testi, bottoni)
  - pagine lente da caricare
  - informazioni di contatto poco chiare o difficili da trovare
  - immagine poco curata (foto vecchie, testi generici, poca fiducia)
- Attività il cui sito sembra non aggiornato da tempo (candidati utili per un check-up)
- Settori coerenti con le varianti template (ristoranti, artigiani, studi professionali generici)

## Chi escludere (sempre)

- Avvocati, banche, commercialisti, consulenti fiscali e organismi di revisione contabile
- Qualsiasi attività che corrisponde a `config/outreach-blocklist.txt`
- Catene grandi o gruppi con team marketing interno
- Siti senza email pubblica (non inventare indirizzi)
- Attività già contattate negli ultimi 30 giorni senza risposta (evita ripetizioni)

## Volume e consegna

- **Massimo 10–15 email al giorno** per proteggere la reputazione del mittente e la deliverability
- Un batch = un gruppo omogeneo (stesso settore o stesso tipo di problema)
- Le email partono **solo** tramite il gate di approvazione (`scripts/run-outreach-batch.sh` + approvazione su telefono). Nessun invio automatico senza revisione umana.

## Prima di approvare un batch

1. Controlla che ogni prospect abbia nome attività, URL e email corretti
2. Verifica che nessun nome o dominio ricada nelle categorie escluse
3. Conferma che il messaggio abbia `{{OSSERVAZIONE}}` compilata con un dettaglio reale del sito (non generica)
4. Tieni traccia del batch ID in `operations/` per eventuali follow-up
