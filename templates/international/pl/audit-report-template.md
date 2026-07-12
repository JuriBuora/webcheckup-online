# WebCheckup

## Bezpieczeństwo, Zaufanie i Widoczność

**Klient:** {{BUSINESS}}  
**Analizowana strona:** {{URL}}  
**Data:** {{DATA}}  
**Rodzaj kontroli:** Analiza zewnętrzna i nieinwazyjna  
**Przygotował:** Juri Buora

---

## 1. Podsumowanie w prostych słowach

{{RIEPILOGO}}

W skrócie: obejrzałem stronę z zewnątrz, tak jak zrobiłby to klient albo wyszukiwarka. Poniżej znajdziesz, co działa dobrze, co warto poprawić i w jakiej kolejności - bez zbędnego żargonu i bez obietnic "pełnego bezpieczeństwa" czy zgodności prawnej.

---

<!-- pagebreak -->

## 2. Tabela priorytetów

| Problem | Wpływ | Priorytet | Kto to naprawia |
| --- | --- | --- | --- |
| {{PROBLEMA_1}} | {{IMPATTO_1}} | Wysoki | {{CHI_1}} |
| {{PROBLEMA_2}} | {{IMPATTO_2}} | Średni | {{CHI_2}} |
| {{PROBLEMA_3}} | {{IMPATTO_3}} | Niski | {{CHI_3}} |

Legenda priorytetów:

- **Wysoki:** warto zająć się szybko, bo może obniżyć zaufanie, liczbę kontaktów lub działanie strony.
- **Średni:** przydatne i konkretne, ale nie pilne.
- **Niski:** poprawa zalecana, gdy będzie czas.

---

## 3. Szczegóły ustaleń

Wypełnij jedną sekcję dla każdego istotnego problemu wykrytego na podstawie checklisty. Powiel poniższy blok dla każdego ustalenia.

{{FINDINGS}}

### {{TITOLO_FINDING}}

**Obszar:** {{AREA}} · **Priorytet:** {{PRIORITA}}

#### Co zauważyłem

{{COSA_VISTO}}

#### Dlaczego to ważne dla biznesu

{{PERCHE_CONTA}}

#### Co zrobić (praktyczne kroki)

{{COSA_FARE}}

**Kto może to naprawić:** {{CHI_SISTEMA}}

---

### Zrzuty ekranu (jeśli dostępne)

#### Desktop

![Zrzut ekranu strony głównej - desktop](../screenshots/homepage-desktop-viewport.png)

<!-- pagebreak -->

#### Mobile

![Zrzut ekranu strony głównej - mobile](../screenshots/homepage-mobile-viewport.png)

<!-- pagebreak -->

---

## 4. Szybkie poprawki - 3 rzeczy do naprawienia w tym tygodniu

Małe, ale widoczne działania, które właściciel lub webmaster mogą wykonać bez przebudowy strony:

1. {{QUICK_WIN_1}}
2. {{QUICK_WIN_2}}
3. {{QUICK_WIN_3}}

---

## 5. Gotowa wiadomość dla webmastera

Możesz skopiować i wysłać ten tekst osobie zarządzającej stroną:

> Cześć, zrobiliśmy zewnętrzny check-up strony i pojawiło się kilka punktów do sprawdzenia. Główne priorytety to: {{PUNTI_WEBMASTER}}. Możesz sprawdzić wykonalność, czas i koszt ich naprawy?

---

<!-- pagebreak -->

## 6. Załącznik z dowodami technicznymi

| Dowód | Wynik | Plik źródłowy |
| --- | --- | --- |
| HTTPS strony głównej | {{EV_HTTPS}} | `homepage-headers.txt` |
| Przekierowanie HTTP | {{EV_REDIRECT}} | `http-redirect-headers.txt` |
| Certyfikat TLS | {{EV_TLS}} | `tls-certificate.txt` |
| Nagłówki hardening | {{EV_HEADERS}} | `homepage-headers.txt` |
| Lighthouse mobile | {{EV_LH_MOBILE}} | `lighthouse-mobile.json` |
| Lighthouse desktop | {{EV_LH_DESKTOP}} | `lighthouse-desktop.json` |
| Główne linki | {{EV_LINKS}} | `link-check-main.txt` |
| Widoczna prywatność/cookies | {{EV_PRIVACY}} | `privacy-policy.html`, `cookie-policy.html` |

---

## 7. Zastrzeżenie

Ważna informacja: ten check-up to zewnętrzna, nieinwazyjna analiza strony internetowej. Nie obejmuje testów penetracyjnych, agresywnego skanowania, dostępu do obszarów prywatnych, testów logowania, exploitów ani pełnej weryfikacji prawnej. Uwagi dotyczące prywatności/cookies nie stanowią porady prawnej, a jedynie wskazują widoczne elementy, które można zweryfikować z własnym konsultantem lub dostawcą strony.
