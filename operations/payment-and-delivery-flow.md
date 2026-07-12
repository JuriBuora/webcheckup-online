# Payment And Delivery Flow

Use this as the default operator flow for every paid audit.

## Goal

Make payment, delivery, and follow-up consistent enough that one operator does not improvise every time.

## Default flow

### 1. Lead replies

Record in `clients/<cliente>/notes.md`:

- status
- contact
- website
- agreed price

### 2. Confirm scope

Send a short message that confirms:

- this is an external and non-invasive check-up
- price is `€49`
- delivery target is within `2 giorni lavorativi` after payment confirmation

### 3. Confirm payment

Before starting the full paid report, update:

- `Pagamento: confermato`
- payment date
- promised delivery date

If payment is not confirmed, do not start the paid audit.

### 4. Create the working package

Check the lead's language first (the `Fonte` field in the FormSubmit notification tells you: `landing-page` = Italian, `landing-page-en/pl/ro` = English/Polish/Romanian). Run:

```bash
cd /Users/juribuora/webcheckup
python3 scripts/create_client_folder.py "Nome Attivita" \
  --website "https://www.esempio.it" \
  --contact-email "email@example.com" \
  --language it
```

Use `--language en|pl|ro` for non-Italian leads - it pulls the matching template set from `templates/international/<lang>/` and translates the webmaster message too. Remember to also pass `--lang <lang>` to `scripts/generate_report_pdf.py` later so the PDF cover, labels and footer come out in the same language.

### 5. Do the audit

Use:

- `checklists/website-audit-checklist.md`
- `checklists/report-ready-qa-checklist.md`
- `operations/too-few-findings-policy.md`

### 6. Generate and check the PDF

The PDF is not deliverable until:

- report markdown is complete
- PDF generates successfully
- PDF is visually checked
- delivery message and phone summary are updated

### 7. Log the delivery

Add a row to `operations/delivery-log.csv` with:

- date
- client
- domain
- amount
- payment status
- delivery status
- proof requested

### 8. Send the package

Default package:

- PDF report
- short summary
- webmaster-forward message

### 9. Ask for proof

After delivery, use:

- `templates/testimonial-request.md`

Only ask after the client has had time to read the report.

## Operator rules

- no paid work starts before payment confirmation
- no report goes out without delivery logging
- no weak report goes out just to avoid an awkward conversation
- no advanced-security upsell unless the scope clearly justifies it

## Pagamento e ricevuta [DECISIONE-JURI]

Default consigliato da confermare:

- metodo semplice: bonifico oppure link PayPal
- il pagamento deve risultare confermato prima di iniziare il Mini-Audit a pagamento
- la consegna resta entro 2 giorni lavorativi dopo conferma pagamento
- usare una ricevuta semplice coerente con il metodo reale di incasso

Non trattare questa sezione come decisione finale finché Juri non conferma:

- metodo definitivo
- eventuale fattura o ricevuta fiscale
- testo esatto da usare nei messaggi cliente
