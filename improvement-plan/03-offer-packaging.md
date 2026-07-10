# 03 — Offer & Packaging

**Goal:** turn the €49 mini-audit from "a project" into a clean, productized offer with clear terms, an objections FAQ, and a simple, honest upsell ladder — exactly the gaps named in `operations/service-audit-2026-07-03.md`.

**Work in:** `/Users/juribuora/website-trust-security-mini-audit`
**Read first:** `offer/mini-audit-one-page.md`, `operations/payment-and-delivery-flow.md`, `operations/too-few-findings-policy.md`, `operations/service-audit-2026-07-03.md`.
**Reminder:** no legal/GDPR guarantees, no promises you can't keep. Terms must be honest and simple. If a term needs a real business/legal decision (e.g., refund policy, invoicing/VAT), do NOT invent it — write a recommended default and mark it `[DECISIONE-JURI]` for the human to confirm.

---

## Task 1 — One-page offer sheet (single source of truth)

**Do:** Back up `offer/mini-audit-one-page.md` and rewrite it as the definitive one-pager with these labelled sections (Italian): Cosa include, Cosa NON include (external, non-invasive, non è un pen-test), Prezzo (€49), Tempi di consegna (`2 giorni lavorativi dopo conferma pagamento` — keep consistent with `payment-and-delivery-flow.md`), Revisioni (recommend: 1 revisione minore gratuita entro 7 giorni), Metodo di pagamento (`[DECISIONE-JURI]` — leave a placeholder with a recommended default like bonifico/PayPal), Ricevuta/fattura (`[DECISIONE-JURI]`), Casi limite (sito offline, nessun accesso, troppe poche criticità → rimando a `too-few-findings-policy.md`).

**Test:** `grep -cE 'Cosa include|Cosa NON include|Prezzo|Tempi di consegna|Revisioni|pagamento' offer/mini-audit-one-page.md` returns at least 6.
**Double-check:** delivery time and price match `payment-and-delivery-flow.md` and `README.md` (all say €49 and 2 giorni). If they disagree, fix so all three agree.
**If it fails:** restore `.bak`, redo.

## Task 2 — Objections FAQ

**Do:** Create `offer/faq-obiezioni.md` with 8–10 real objections and honest answers (Italian). Cover at least: "costa troppo / 49 è comunque una spesa", "il mio sito va bene così", "non ho tempo", "posso farlo da solo", "è sicuro / non toccate il sito?", "e la privacy/GDPR?" (answer: NON facciamo consulenza legale/GDPR, è un check-up tecnico-pratico), "cosa ottengo esattamente?", "e se non trovate niente?" (→ mini-analisi gratuita, no forzatura), "chi sistema i problemi?".

**Test:** `grep -c '^## ' offer/faq-obiezioni.md` returns at least 8.
**Double-check:** the GDPR/privacy answer makes NO legal guarantee. The "se non trovate niente" answer matches `too-few-findings-policy.md`.
**If it fails:** redo; keep answers short and honest.

## Task 3 — Simple, honest upsell ladder

**Do:** Create `offer/scala-servizi.md` describing 3 tiers, clearly and without overselling:
- **Tier 1 — Mini-Audit €49** (current core).
- **Tier 2 — Audit + Lista Interventi Prioritari** (recommend a price range `[DECISIONE-JURI]`, e.g. €99–149): the mini-audit plus a webmaster-ready change list and a short call.
- **Tier 3 — Sistemazione guidata / retainer** — mark clearly as **only when scope is authorized and justified** (per the service-audit warning: do not push advanced security by default). Describe when it's appropriate, not a hard price.
State the rule: never push Tier 3 as a default upsell; offer Tier 2 only after delivering Tier 1 value.

**Test:** file names all three tiers and the "non spingere Tier 3 di default" rule.
**Double-check:** consistent with `service-audit-2026-07-03.md` section 4 (service ladder). No promise to do deep security work casually.
**If it fails:** redo.

## Task 4 — Standardise the money/terms language across all client-facing files

**Do:** Grep the repo for price/time mentions and make them consistent with Task 1:
```bash
cd /Users/juribuora/website-trust-security-mini-audit
grep -rniE '49|giorni|revision|pagament' --include=*.md . | grep -vi improvement-plan
```
Fix any file that states a different price, delivery time, or revision policy than the one-pager. Back up each file before editing.

**Test:** re-run the grep; every price says €49, every delivery says 2 giorni lavorativi, revision policy matches.
**Double-check:** you did not change `improvement-plan/` files or invent new terms — only aligned to Task 1.
**If it fails:** restore the `.bak` of any file you broke; fix one file at a time.

## Task 5 — Draft the payment/invoice process for human decision

**Do:** In `operations/payment-and-delivery-flow.md`, add a clearly-marked section `## Pagamento e ricevuta [DECISIONE-JURI]` with a recommended simple default (e.g., bonifico or PayPal link, payment confirmed before starting the paid audit, simple receipt) — but do NOT assert it as final. The human confirms the real method.

**Test:** the `[DECISIONE-JURI]` section exists in the file.
**Double-check:** you did not claim to issue legal invoices/VAT documents unless the human confirmed it.
**If it fails:** redo, keep it a recommendation.

---

**When done:** update `PROGRESS.md`, commit each change. Anything tagged `[DECISIONE-JURI]` stays as a recommendation for the human — do not treat it as final.
