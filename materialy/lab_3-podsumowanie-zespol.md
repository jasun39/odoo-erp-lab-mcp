# Lab 3 — Z3 Magazyn: podsumowanie dla zespołu

Stan na **2026-10-26** (ok. 17:40). Instancja: `edu-agh-wawel-lab-2026-g1-z3.odoo.com`, Odoo **20.0 Enterprise** (Odoo Online).
Wszystkie operacje wykonał Claude przez MCP (API JSON-2) z konta **mjuchacz@student.agh.edu.pl** (id 7, administrator).
Każdy wynik potwierdzono odczytem z Odoo po operacji.

## Jak czytać ten dokument

| Oznaczenie | Znaczenie |
|---|---|
| **K+** | system zachował się zgodnie z oczekiwaniem z polecenia (kryterium spełnione w tej próbie) |
| **K−** | luka — system zachował się wbrew oczekiwaniu |
| **propozycja** | zasada przyjęta przez nas, **nieuzgodniona z prowadzącym** — trzeba ją potwierdzić |
| **symulacja** | dane zmyślone na potrzeby ćwiczenia (decyzja Z5, kody etykiet, warunki, przyczyna różnicy) |

Uwaga: wyniki z polecenia są „oczekiwaniem do uzgodnienia”. Poniższe K+/K− to **wyniki naszych prób**, nie ostateczny odbiór.
Przed wpisaniem do SIWZ trzeba potwierdzić propozycje z prowadzącym i partnerami (Z1, Z2, Z4, Z5).

## Przegląd

| Strumień | Proces | ID SIWZ | Status | Najważniejszy wynik |
|---|---|---|---|---|
| A | MAG-P01 Lokalizacje, przyjęcie, partie | MAG-001, 002, 003 | ✅ wykonane | podział 3 = 1 + 2 widoczny; **brak daty przy przyjęciu nie blokuje** |
| A | MAG-P04 Pusta półka, transfer, uzupełnienie | MAG-008, 009, 010, 011 | ✅ wykonane | 0/8→4/4, 1/8→6/3 bez duplikatów; **reguła półki tworzy fikcyjny transfer przy 0/0** |
| B | MAG-P02 Daty, granica, FEFO | MAG-005, 006 | ✅ wykonane | 6A + 2B; partie po granicy pominięte; **partia bez daty dopuszczona** |
| B | MAG-P03 Wycofanie, kwarantanna, ślad | MAG-004, 007, 017 | ✅ wykonane | 3 szt. w kwarantannie; **ręczne wydanie z kwarantanny możliwe (krytyczne)** |
| B | MAG-P08 Etykiety, kody, warunki | MAG-016, 019 | ✅ wykonane (symulacja) | konflikt kodu wykryty; naruszenie zarejestrowane dla jednej partii |
| C | MAG-P05 Rezerwacje, wydanie częściowe | MAG-013, 014, 018 | ✅ wykonane | 10/6/4 i zaległość 4; **cudza rezerwacja do zabrania, stan ujemny możliwy** |
| C | MAG-P06 Zwrot do kontroli | MAG-015 | ✅ wykonane | półka 7 / kwarantanna 1 / fizycznie 8, ta sama partia |
| C | MAG-P07 Inwentaryzacja, bilans | MAG-012, 020 | ✅ wykonane | korekta −1 z przyczyną; bilans zgodny; duplikat wykryty i odwrócony |
| — | CRIM-Z3 Monitor półki | MAG-021…024 | ⏳ **nie rozpoczęte** | — |

## Najważniejsze luki (do zgłoszenia / decyzji)

| # | Luka | Gdzie wykazana | Waga |
|---|---|---|---|
| L1 | **Ręczne wydanie zapasu z kwarantanny jest możliwe** — Odoo zatwierdza wydanie z linią z Kwarantanny | P03-NEG-3 (OUT/00004) | **krytyczna** |
| L2 | **Dostępność produktu liczy kwarantannę** (`qty_available`/`free_qty`) — sprzedaż widzi niedopuszczony towar jako dostępny | P03-NEG-1, P06-NEG-1 | wysoka |
| L3 | **Ręczne podniesienie ilości na wydaniu** zabiera rezerwację innego dokumentu bez komunikatu | P05-A NEG-1 (OUT/00006 → OUT/00005) | wysoka |
| L4 | **Rozchód ponad stan** — wydano 6 ze stanu 5, powstał stan −1 | P05-C NEG-2 (OUT/00009) | wysoka |
| L5 | **Partia bez daty** jest traktowana jak dopuszczona (rezerwowana do wydania); przy przyjęciu Odoo samo wpisuje daty domyślne | P02-NEG-3, P01-NEG-2 | średnia |
| L6 | **Reguła uzupełnienia półki przy pustym zapleczu** tworzy przesunięcie „z niczego” | P04-C NEG-3 (INT/00009, anulowany) | średnia |
| L7 | **Brak ostrzeżenia przy zdublowanym przyjęciu** (to samo źródło i dostawca) — wykrywa je dopiero bilans z dokumentem dostawy | P07-NEG (IN/00023) | średnia |
| L8 | Zestaw (MO) pokazuje komponent jako „Dostępny”, choć leży tylko w kwarantannie (rezerwacji brak) | P03-NEG-4 | niska |

Wspólna przyczyna L1, L3, L4: **Odoo pozwala ręcznie wpisać ilość/lokalizację wydania**, a blokuje tylko automatyczna rezerwacja.
Wszystkie próby robiono jako **administrator** — nie sprawdzono, czy zwykły magazynier ma te same możliwości.

---

## Strumień A — struktura, zapasy, uzupełnienia

### MAG-P01 — Struktura lokalizacji, przyjęcie i widoczność produktu–partii

**Co zrobiliśmy**
- Utworzono lokalizację **WH/Input/Przyjęcie** (id 45, poza Zapasami) i partnera **Dostawca testowy Z3** (id 18).
- Przyjęto Danusię w dwóch partiach: **DAN-P01-A 3 szt.**, **DAN-P01-B 2 szt.** (IN/00009), rozłożono: A → Półka 1: 1, Zaplecze: 2; B → Zaplecze: 2 (INT/00005).
- Próby negatywne: przyjęcie bez partii (IN/00010) i z partią bez daty (IN/00011).

**Wyniki**
- POS **K+**: suma DAN-P01-A = 3 rozwija się na **Półka 1: 1 + Zaplecze: 2**.
- NEG-1 **K+**: przyjęcie bez partii zablokowane („Należy podać numer partii…”). IN/00010 zostawiony otwarty jako dowód.
- NEG-2 **K−**: brak daty nie blokuje — Odoo samo wpisało daty z kartoteki.
- NEG-3 (odczyt): KAKAO śledzone partiami, a 20 kg leży bez partii (dane sprzed naszych prób).

**Propozycje do uzgodnienia:** źródła kanałów — przyjęcie: Przyjęcie; sprzedaż/wydanie i produkcja: Zapasy (z podlokalizacjami); kwarantanna poza Zapasami.
Szczegóły: `lab_3-P01-plan.md`, `lab_3-P01-wyniki.md`.

### MAG-P04 — Pusta półka, transfer, próg uzupełnienia i brak w firmie

**Co zrobiliśmy**
- Produkty testowe: **Tiki-Taki** (5), **Trufle** (6), **Z3-TEST P04-C** (7). Trasa **„Z3: Uzupełnienie półki z zaplecza”** (16) z regułą Zaplecze → Półka 1.
- A: Tiki-Taki 0/8 → aktywność „Brak na półce” dla id 7 → transfer 4 (INT/00007).
- B: Trufle 1/8 (+2 w kwarantannie) → reguła min 2 / cel 6 (OP/00001) → transfer 5 (INT/00008), uruchomiona dwa razy.
- C: produkt 0/0 → reguła półki (OP/00002) oraz reguła zakupu na Zapasach (OP/00003) → zapytanie ofertowe **P00002** (szkic) dla Z2.

**Wyniki**
- A **K+**: Półka 4 / Zaplecze 4, suma 8; brak wykryty ze stanu, przed skargą klienta.
- B **K+**: potrzeba 5, ponowne uruchomienie nie zdublowało transferu; wynik 6/3; kwarantanna nieużyta.
- C: przekazanie do zakupów **K+** (P00002, niepotwierdzone — decyzja Z2); **K− (L6)**: reguła półki utworzyła fikcyjny transfer INT/00009 (anulowany).
  OP/00002 zostawiony jako dowód — **nie uruchamiać** go ponownie.

**Do uzgodnienia:** osoba reagująca na brak (przyjęto id 7); kupujący i cena w P00002 (puste / 0 zł). Szczegóły: `lab_3-P04-plan.md`, `lab_3-P04-wyniki.md`.

---

## Strumień B — daty, kwarantanna, wycofanie, etykiety

### MAG-P02 — Terminy, granica dopuszczenia i FEFO

**Co zrobiliśmy**
- Produkt **Z3-TEST P02-FEFO** (8): F-A 6 szt. (usunięcie 1.12), F-B 8 szt. (15.01), F-X 4 szt. w kwarantannie (15.11 — najwcześniejsza).
- Produkt **Z3-TEST P02-GR** (9): partie przed granicą / na granicy (dziś) / po granicy / bez daty. Wydania próbne anulowane po odczycie.

**Wyniki**
- POS **K+**: wydanie 8 → **6 F-A + 2 F-B**; F-X pominięta. FEFO z kategorii działa mimo FIFO na lokalizacjach.
- NEG-1 **K+**: przy przyjęciu partii po dacie usunięcia Odoo wyświetla ostrzeżenie (potwierdzone na polecenie — dane testowe).
- NEG-2 **K+**: partie na granicy i po granicy **nie zostały zarezerwowane**.
- NEG-3 **K− (L5)**: partia bez daty została zarezerwowana.

**Propozycje:** daty w UTC, prezentacja i granica w Europe/Warsaw; data usunięcia = granica wydania. Obserwacja: „najlepiej spożyć przed” wypada
przed datą usunięcia (parametry produktu) — do uzgodnienia znaczenia dat.

### MAG-P03 — Wycofanie, kwarantanna i identyfikowalność

**Co zrobiliśmy**
- Alert jakości 1: wycofanie **DAN-P01-A** — **decyzja symulowana**, do potwierdzenia przez Z5.
- Cały zapas partii (Półka 1: 1, Zaplecze: 2) przeniesiono do Kwarantanny dwoma transferami (INT/00010, INT/00011).
- Produkt **Z3-TEST P03-Q** (10) z zapasem **tylko w kwarantannie**: sprawdzono dostępność, rezerwację, ręczne wydanie i zestaw (BoM + MO/00002).

**Wyniki**
- POS **K+**: 3 szt. w kwarantannie, dobra partia DAN-P01-B bez zmian; ślad wstecz: IN/00009 → INT/00005 → INT/00010/11.
  Ślad naprzód: tej partii nie sprzedano ani nie zużyto — pokazany na partii 0000002 (OUT/00001 → S00002 → zwrot IN/00008).
- NEG: dostępność **K− (L2)**; rezerwacja **K+**; ręczne wydanie **K− krytyczna (L1)** — stan przywrócono zwrotem RET00001; zestaw **K+** z zastrzeżeniem (L8).

### MAG-P08 — Etykiety, kody i naruszenie warunków przechowywania (symulacja)

**Co zrobiliśmy**
- Trufle: kartoteka bez kodu → „skan” kodu z etykiety `Z3-TRU-001` → brak produktu → korekta kartoteki (barcode `Z3-TRU-001`) → skan poprawny.
- Opis produktu: warunki przechowywania 15–18 °C, ≤ 70 % (dane ćwiczenia). Alert jakości 2: naruszenie 24 °C, partia TRU-P04-B, Półka 1.

**Wyniki:** POS **K+**, NEG **K+** (konflikt wykryty; alert tylko dla jednej partii). Ograniczenia: „skan” = wyszukanie po kodzie przez API
(nie skaner ani aplikacja Barcode, bez Z1); lokalizacja naruszenia tylko w opisie alertu; brak osobnego mechanizmu warunków lokalizacji.

---

## Strumień C — rezerwacje, wydania, zwroty, bilans

### MAG-P05 — Rezerwacja, kompletacja częściowa i ochrona przed nadmiernym rozchodem

**Co zrobiliśmy**
- Produkty **Z3-TEST P05-A/B/C** (12/13/14), partner **Klient testowy Z3** (19).
- A: 10 szt., wydanie A1 rezerwuje 6 (OUT/00005), nowe wydanie A2 6 szt. (OUT/00006), potem ręczne podniesienie A2 do 6.
- B: zamówienie **S00003** na 10 przy stanie 6 → wydano 6 (OUT/00007), zaległość 4 (OUT/00008).
- C: wydanie 6 ze stanu 5 (OUT/00009).

**Wyniki**
- A POS **K+**: fizycznie 10, zarezerwowane 6, wolne 4; A2 dostał tylko 4. A NEG-1 **K− (L3)**: A2 wydał 6, A1 po cichu spadł z 6 do 4.
- B POS **K+**: wydano 6 z partią P05B-1, zaległość 4 przy tym samym zamówieniu (wydano 6 / do wydania 4).
- C NEG-2 **K− (L4)**: wydano 6, stan −1 (skorygowany potem w P07).
- Dowody zostawione otwarte: OUT/00005 (4 z 6), OUT/00008 (zaległość 4).

### MAG-P06 — Zwrot od klienta i przekazanie do kontroli

**Co zrobiliśmy** (decyzje Claude)
- Produkt **Z3-TEST P06-DAN** (15): 10 szt. (P06-A 4, P06-B 6) przyjęte na Zaplecze i przeniesione na Półkę 1.
- Sprzedaż **S00004** 3 szt. (OUT/00010, partia P06-A wg FEFO) i zwrot 1 szt. **RET00002** → Kwarantanna, powiązany z wydaniem i zamówieniem,
  powód „Item arrived damaged or defective”. Alert jakości 3 dla Z5.

**Wyniki**
- POS **K+**: **Półka 7, Kwarantanna 1, fizycznie 8**; w zamówieniu wydano 2 (zwrot odjęty).
- NEG **K+**: zwrot nie trafił do rezerwacji (próbne wydanie 8 dostało 7); zwrot ma tę samą partię co wydanie (P06-A).
- Dostępność produktu pokazuje 8 (**L2**). Rozliczenie (korekta faktury) — FIN-P02, poza naszym zakresem, niewykonane. PoS niezainstalowany.

### MAG-P07 — Inwentaryzacja, korekta i uzgodnienie bilansu

**Co zrobiliśmy** (decyzje Claude)
- Spis P06-DAN: system 8, spis 7 — na Półce 1 partia P06-B 5 zamiast 6; przyczyna symulowana (uszkodzenie bez rejestracji). Liczenie i zatwierdzenie jako osobne kroki.
- Korekta stanu −1 P05-C do 0 z przyczyną (OUT/00009).
- Bilans serii P06-DAN (otwarcie 0) wg partii i lokalizacji; kontrolowany duplikat dostawy **IN/00023** → wykrycie → odwrócenie **OUT/00012**.

**Wyniki**
- POS **K+**: korekta −1 ma autora (id 7) i powód w nazwie ruchu; bilans odtworzony: +11 przyjęć − 3 wydania + 1 zwrot − 1 zwrot do dostawcy − 1 korekta = **7**
  = stan Odoo; transfery wewnętrzne = 0 dla firmy; kwarantanna ujęta.
- NEG **K+**: duplikat widoczny w bilansie (11 vs 10 z dokumentu dostawy), wskazany dokument źródłowy, odwrócony bez usuwania historii.
  Odoo samo nie ostrzegło (**L7**).

---

## Dokumenty celowo pozostawione otwarte (dowody)

| Dokument | Proces | Dlaczego |
|---|---|---|
| IN/00010 | P01-NEG-1 | przyjęcie bez partii, zablokowane |
| OP/00002 | P04-C NEG-3 | reguła tworząca fikcyjny transfer — **nie uruchamiać** |
| P00002 (szkic RFQ) | P04-C | przekazanie braku do Z2 — decyzja Z2 |
| OUT/00005 | P05-A NEG-1 | rezerwacja obniżona 6 → 4 |
| OUT/00008 | P05-B | zaległość 4 do S00003 |
| alerty jakości 1, 2, 3 | P03, P08, P06 | czekają na Z5 |

## Dane testowe (żeby nie pomylić z danymi innych zespołów)

Produkty z prefiksem **„Z3-TEST”** oraz Tiki-Taki i Trufle zostały utworzone przez nas. Partnerzy: **Dostawca testowy Z3** (18) i **Klient testowy Z3** (19).
Wszystkie dokumenty mają w polu „Źródło” (origin) dopisek **„Lab3 MAG-Pxx”**. Danusia: nasze partie to DAN-P01-A/B/NODATE.
Zmienione dane wspólne: produkt **Trufle** — kod `Z3-TRU-001` i opis warunków; partia **DAN-P01-A** jest teraz w kwarantannie.

## Czego jeszcze brakuje

1. **Uzgodnienia z prowadzącym** dla wszystkich propozycji (źródła kanałów, znaczenie dat i granica, osoba reagująca, lokalizacja kontroli zwrotów).
2. **Potwierdzenia partnerów:** Z5 (decyzje jakościowe — alerty 1–3), Z2 (P00002, kontrola dostawy), Z1 (etykiety/skan, sprzedaż), Z4 (zestawy), FIN (korekta zwrotu).
3. **Próby na koncie zwykłego użytkownika magazynu** dla L1, L3, L4 (czy luka dotyczy tylko administratora).
4. **CRIM-Z3** (monitor półki i zagrożonych partii) — nierozpoczęte.
5. Wpisy do arkusza SIWZ (`Wawel_LAB_SIWZ_wymagania.xlsx`) — w plikach wyników są propozycje treści dla każdego ID.

## Jak sprawdzić w Odoo

- Stany wg partii i lokalizacji: **Magazyn → Raportowanie → Stan** (grupowanie: Produkt, Partia, Lokalizacja).
- Historia partii: **Magazyn → Produkty → Partie/Numery seryjne → [partia] → Identyfikowalność**.
- Ruchy: **Magazyn → Raportowanie → Historia ruchów** (filtr: Źródło zawiera „Lab3”).
- Alerty jakości: **Jakość → Alerty**. Reguły min/max: **Magazyn → Operacje → Uzupełnianie**.

## Pliki

| Plik | Zawartość |
|---|---|
| `materialy/lab_3.pdf`, `lab_3.txt` | polecenie |
| `materialy/lab_3-stan-poczatkowy.md` | stan Odoo przed naszymi pracami |
| `materialy/lab_3-P01-plan.md`, `lab_3-P01-wyniki.md` | MAG-P01 |
| `materialy/lab_3-P04-plan.md`, `lab_3-P04-wyniki.md` | MAG-P04 |
| `materialy/lab_3-B-plan.md`, `lab_3-B-wyniki.md` | MAG-P02, P03, P08 |
| `materialy/lab_3-C-plan.md`, `lab_3-C-wyniki.md` | MAG-P05, P06, P07 |
| `STATUS.md` | bieżący stan prac i kolejny krok |
