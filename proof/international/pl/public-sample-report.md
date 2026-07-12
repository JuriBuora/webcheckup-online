<!-- DA RIVEDERE DA JURI PRIMA DELLA PUBBLICAZIONE -->

# WebCheckup - Przykładowy Raport Publiczny

## Bezpieczeństwo, Zaufanie i Widoczność

**Klient:** Firma przykładowa  
**Analizowana strona:** https://www.firma-przykladowa.pl/  
**Data:** 10/07/2026  
**Rodzaj kontroli:** Analiza zewnętrzna i nieinwazyjna  
**Przygotował:** Juri

---

## 1. Podsumowanie w prostych słowach

Ten publiczny przykład ma pokazać format check-upu: krótki, konkretny raport, czytelny nawet dla kogoś, kto nie zajmuje się stroną na co dzień. W tym przypadku strona komunikuje działalność dość jasno, ale traci coś na urządzeniach mobilnych i w jasności ścieżki kontaktu; ma też kilka prostych punktów technicznych do sprawdzenia przez webmastera.

W skrócie: celem nie jest udowodnienie, że strona jest "bezpieczna" czy "zgodna z przepisami", lecz wskazanie w praktycznej kolejności, co warto naprawić najpierw, by nie tracić zaufania, czytelności i zapytań.

---

## 2. Tabela priorytetów

| Problem | Wpływ | Priorytet | Kto to naprawia |
| --- | --- | --- | --- |
| Teksty drugorzędne słabo czytelne na mobile | Część użytkowników z trudem czyta opisy i przydatne szczegóły na smartfonie | Wysoki | Webmaster / frontend |
| Główne CTA niejasne | Część odwiedzających nie rozumie od razu, jak się skontaktować lub poprosić o wycenę | Średni | Właściciel / webmaster |
| Brak podstawowych nagłówków przeglądarki | Konfiguracja techniczna przekazuje mniej wiarygodności niż powinna | Niski | Webmaster / hosting |

---

## 3. Główne ustalenia

### Ustalenie 1 - Teksty drugorzędne słabo czytelne na mobile

**Co zauważyłem**  
Strona główna pozostaje użyteczna na telefonie, ale niektóre opisy i teksty drugorzędne mają słaby kontrast i mały rozmiar czcionki względem tła.

**Dlaczego to ważne**  
Część odwiedzających wchodzi ze smartfona i w ciągu kilku sekund decyduje, czy zostać, czy wyjść: jeśli tekst trudno się czyta, spada jasność oferty.

**Co zrobić**  
Zwiększyć kontrast, rozmiar i odstępy tekstów drugorzędnych w najważniejszych sekcjach informacyjnych, a następnie ponownie sprawdzić stronę główną na prawdziwym smartfonie.

**Kto to naprawia**  
Webmaster / frontend

### Ustalenie 2 - Główne CTA niejasne

**Co zauważyłem**  
Strona dobrze prezentuje działalność, ale kolejny użyteczny krok nie wybrzmiewa od razu: odwiedzający musi sam zorientować się, czy zadzwonić, napisać, czy poprosić o wycenę.

**Dlaczego to ważne**  
Gdy CTA nie jest jednoznaczne, część wizyt pozostaje bierna i nie zamienia się w kontakt.

**Co zrobić**  
Zastąpić ogólne CTA bardziej precyzyjnym zaproszeniem i powtórzyć je w kluczowych miejscach strony, zostawiając telefon i formularz łatwe do znalezienia.

**Kto to naprawia**  
Właściciel odpowiada za treść, webmaster za pozycję i styl

### Ustalenie 3 - Brak podstawowych nagłówków przeglądarki

**Co zauważyłem**  
Kontrola zewnętrzna pokazuje brak niektórych typowych nagłówków hardeningowych przeglądarki, takich jak `X-Content-Type-Options` i `Referrer-Policy`.

**Dlaczego to ważne**  
To nie jest sygnał alarmowy, ale wskazuje na konfigurację techniczną możliwą do poprawy na stronie, która ma przekazywać wiarygodność.

**Co zrobić**  
Poprosić webmastera lub dostawcę hostingu o sprawdzenie głównych podstawowych nagłówków po stronie serwera lub CDN, bez zmieniania niczego innego na stronie.

**Kto to naprawia**  
Webmaster / hosting

### Ustalenie 4 - Zbyt ogólny title i opis SEO

**Co zauważyłem**  
Strona główna ma title, ale jest on mało konkretny w odniesieniu do usługi i lokalizacji, a meta description niewystarczająco zachęca do kliknięcia w wynikach wyszukiwania.

**Dlaczego to ważne**  
Strona jasna również dla Google zaczyna lepiej: pomaga to zarówno widoczności, jak i odbiorowi usługi jeszcze przed otwarciem strony.

**Co zrobić**  
Przepisać title i meta description strony głównej, uwzględniając działalność, obszar geograficzny i główną korzyść, zachowując prosty ton.

**Kto to naprawia**  
Właściciel odpowiada za tekst, webmaster za aktualizację

---

## 4. Szybkie poprawki

1. Zwiększyć kontrast i czytelność tekstów drugorzędnych na mobilnej stronie głównej.
2. Uczynić główny przycisk kontaktu lub wyceny bardziej jednoznacznym.
3. Poprosić webmastera o sprawdzenie głównych podstawowych nagłówków przeglądarki.

---

## 5. Najważniejszy załącznik techniczny

| Dowód | Wynik w skrócie | Kto działa |
| --- | --- | --- |
| Strona główna mobile | Użyteczna, ale czytelność tekstów drugorzędnych do poprawy | Webmaster |
| Ścieżka kontaktu | Obecna, ale CTA wymaga większej jasności | Właściciel / webmaster |
| HTTPS | Aktywne, bez widocznych ostrzeżeń | Brak pilności |
| Nagłówki przeglądarki | Brakuje niektórych podstawowych nagłówków | Webmaster / hosting |
| SEO strony głównej | Title i description do doprecyzowania | Właściciel / webmaster |

---

## 6. Uwaga końcowa

Ten raport jest zanonimizowany i nie opisuje prawdziwej firmy. Służy wyłącznie pokazaniu formatu dostarczanego materiału i poziomu jasności, jaki otrzymuje klient.
