# Verificare Site Web

## Securitate, Incredere si Vizibilitate

**Client:** {{BUSINESS}}  
**Site analizat:** {{URL}}  
**Data:** {{DATA}}  
**Tip de verificare:** Analiza externa si neinvaziva  
**Pregatit de:** Juri Buora

---

## 1. Rezumat in cuvinte simple

{{RIEPILOGO}}

Pe scurt: am privit site-ul din exterior, asa cum ar face-o un client sau un motor de cautare. Mai jos gasesti ce functioneaza, ce merita imbunatatit si in ce ordine - fara tehnicisme inutile si fara promisiuni de "securitate totala" sau conformitate legala.

---

<!-- pagebreak -->

## 2. Tabel de prioritati

| Problema | Impact | Prioritate | Cine o rezolva |
| --- | --- | --- | --- |
| {{PROBLEMA_1}} | {{IMPATTO_1}} | Ridicata | {{CHI_1}} |
| {{PROBLEMA_2}} | {{IMPATTO_2}} | Medie | {{CHI_2}} |
| {{PROBLEMA_3}} | {{IMPATTO_3}} | Scazuta | {{CHI_3}} |

Legenda prioritatilor:

- **Ridicata:** merita abordata curand, pentru ca poate reduce increderea, contactele sau functionarea de baza.
- **Medie:** utila si concreta, dar nu urgenta.
- **Scazuta:** imbunatatire recomandata cand exista timp.

---

## 3. Detaliile constatarilor

Completeaza o sectiune pentru fiecare problema relevanta identificata prin checklist. Dubleaza blocul de mai jos pentru fiecare constatare.

{{FINDINGS}}

### {{TITOLO_FINDING}}

**Zona:** {{AREA}} · **Prioritate:** {{PRIORITA}}

#### Ce am observat

{{COSA_VISTO}}

#### De ce conteaza pentru afacere

{{PERCHE_CONTA}}

#### Ce este de facut (pasi practici)

{{COSA_FARE}}

**Cine poate rezolva:** {{CHI_SISTEMA}}

---

### Capturi de ecran (daca sunt disponibile)

#### Desktop

![Captura de ecran pagina principala - desktop](../screenshots/homepage-desktop-viewport.png)

<!-- pagebreak -->

#### Mobil

![Captura de ecran pagina principala - mobil](../screenshots/homepage-mobile-viewport.png)

<!-- pagebreak -->

---

## 4. Actiuni rapide - 3 lucruri de reparat saptamana aceasta

Actiuni mici dar vizibile pe care proprietarul sau webmasterul le pot face fara sa refaca site-ul:

1. {{QUICK_WIN_1}}
2. {{QUICK_WIN_2}}
3. {{QUICK_WIN_3}}

---

## 5. Mesaj gata de trimis catre webmaster

Poti copia si trimite acest text persoanei care administreaza site-ul:

> Buna, am facut o verificare externa a site-ului si au aparut cateva puncte de verificat. Prioritatile principale sunt: {{PUNTI_WEBMASTER}}. Poti verifica fezabilitatea, timpul si costul pentru a le rezolva?

---

<!-- pagebreak -->

## 6. Anexa cu dovezi tehnice

| Dovada | Rezultat | Fisier sursa |
| --- | --- | --- |
| HTTPS pagina principala | {{EV_HTTPS}} | `homepage-headers.txt` |
| Redirect HTTP | {{EV_REDIRECT}} | `http-redirect-headers.txt` |
| Certificat TLS | {{EV_TLS}} | `tls-certificate.txt` |
| Headere de hardening | {{EV_HEADERS}} | `homepage-headers.txt` |
| Lighthouse mobil | {{EV_LH_MOBILE}} | `lighthouse-mobile.json` |
| Lighthouse desktop | {{EV_LH_DESKTOP}} | `lighthouse-desktop.json` |
| Linkuri principale | {{EV_LINKS}} | `link-check-main.txt` |
| Confidentialitate/cookies vizibile | {{EV_PRIVACY}} | `privacy-policy.html`, `cookie-policy.html` |

---

## 7. Declaratie de limitare a responsabilitatii

Nota importanta: aceasta verificare este o analiza externa si neinvaziva a site-ului web. Nu include teste de penetrare, scanari agresive, acces la zone private, teste de login, exploatari sau o verificare legala completa. Observatiile despre confidentialitate/cookies nu constituie consultanta juridica, ci indica elemente vizibile care pot fi verificate cu propriul consultant sau furnizor de site.
