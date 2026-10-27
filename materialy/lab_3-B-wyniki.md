# Strumień B (MAG-P02, P03, P08) — wyniki prób (F2)

Wykonano 2026-10-26 od ok. 16:07 (Europe/Warsaw; daty poniżej w UTC) przez MCP (`mcp-server-odoo` 0.9.0, JSON-2,
użytkownik id 7). Zgoda użytkownika na plan `lab_3-B-plan.md`: 2026-10-26. Decyzja jakościowa Z5, kody etykiet
i warunki przechowywania — **symulowane / fikcyjne dane ćwiczenia**.

## Produkty testowe

| ID | Produkt |
|---|---|
| 8 | Z3-TEST P02-FEFO |
| 9 | Z3-TEST P02-GR |
| 10 | Z3-TEST P03-Q |

## MAG-P02 (MAG-005, MAG-006)

### Rekordy

| Krok | Model | ID | Numer / nazwa | Stan |
|---|---|---|---|---|
| 2.1 | stock.picking | 25 | IN/00015 — F-A (lot 9) 6, F-B (lot 10) 8 → Zapasy | done 15:07:55 |
| 2.2 | stock.picking | 26 | IN/00016 — F-X (lot 11) 4 → Kwarantanna | done 15:07:58 |
| 2.3 | stock.picking | 27 | OUT/00002 — wydanie 8 | cancel (2.7) |
| 2.4 | stock.picking | 28 | IN/00017 — G-PRZED (12), G-NA (13), G-PO (14), G-BRAK (15) po 1 → Zapasy | done 15:09:51 |
| 2.5 | stock.lot | 15 | G-BRAK — wyczyszczone wszystkie daty | — |
| 2.6 | stock.picking | 29 | OUT/00003 — wydanie 3 | cancel (2.7) |

### Daty partii (UTC; usunięcie = ważność − 30 dni, alert = ważność − 45 dni)

| Partia | Usunięcie | Ważność | Uwagi |
|---|---|---|---|
| F-A | 2026-12-01 11:00 | 2026-12-31 11:00 | dopuszczona (Zapasy) |
| F-B | 2027-01-15 11:00 | 2027-02-14 11:00 | dopuszczona (Zapasy) |
| F-X | 2026-11-15 11:00 | 2026-12-15 11:00 | najwcześniejsza, **niedopuszczona** (Kwarantanna) |
| G-PRZED | 2026-11-30 11:00 | 2026-12-30 11:00 | przed granicą |
| G-NA | 2026-10-25 23:00 (= 26.10 00:00 Warszawa) | 2026-11-24 23:00 | na granicy (dziś) |
| G-PO | 2026-10-24 22:00 (= 25.10 00:00 Warszawa) | 2026-11-23 22:00 | po granicy |
| G-BRAK | — | — | daty usunięte ręcznie (2.5) |

### MAG-P02-POS — wynik: zgodny z oczekiwaniem

Wydanie OUT/00002 (8 szt.) po action_assign: **F-A 6 + F-B 2** z Zapasów; F-X (najwcześniejsza data, kwarantanna) nieużyta.
FEFO z kategorii `Goods` zadziałało mimo FIFO ustawionego na lokalizacjach Zapasy/Półka 1.

### MAG-P02-NEG

- **NEG-1 (kontrola przy przyjęciu):** walidacja IN/00017 zwróciła okno Odoo „Potwierdzenie” (`expiry.picking.confirmation`)
  — przyjmowane partie po dacie usunięcia (wskazana G-NA; dotyczy G-NA i G-PO). Przyjęcie zatrzymane do potwierdzenia.
  Potwierdzone na polecenie użytkownika (2026-10-26) wywołaniem `button_validate` z kontekstem `skip_expired`
  (to samo co przycisk w oknie) — jako dane testowe. **Wynik: system ostrzega na granicy (K+).**
- **NEG-2 (wydanie po granicy / na granicy):** wydanie OUT/00003 (3 szt.) zarezerwowało **tylko G-PRZED i G-BRAK**
  (ruch `partially_available`, 2 z 3). **G-NA i G-PO pominięte** mimo najwcześniejszych dat — FEFO nie uznał ich
  za dopuszczone. **Wynik: K+.** Granica w Odoo = moment daty usunięcia (G-NA, 26.10 00:00 Warszawa, już niedostępna).
- **NEG-3 (brak daty):** partia **G-BRAK bez dat została zarezerwowana** do wydania. Brak daty jest traktowany jak dopuszczenie.
  **Wynik: K− (luka)** — do uzgodnienia reguła dla partii bez daty (właściciel: Z3 / Z5).
- Nie badano: ręcznej zmiany linii wydania na G-PO (czy da się wydać partię po granicy ręcznie).
- Obserwacja MAG-006: `use_date` („najlepiej spożyć przed”) = ważność − 150 dni wypada **przed** datą alertu i usunięcia
  (np. F-A: 2026-08-03, czyli w przeszłości). Kolejność dat z parametrów produktu jest niejednoznaczna — do uzgodnienia.
- Rezerwacje po anulowaniu wydań (2.7): 0 na wszystkich partiach P02.

## MAG-P03 (MAG-004, MAG-007, MAG-017)

### Rekordy

| Krok | Model | ID | Numer / nazwa | Stan |
|---|---|---|---|---|
| 3.1 | quality.alert | 1 | „Wycofanie DAN-P01-A — decyzja SYMULOWANA (do potwierdzenia przez Z5)”, lot 3, zespół 1, odp. id 7 | New |
| 3.3 | stock.picking | 30 | INT/00010 — DAN-P01-A 1: Półka 1 → Kwarantanna | done 15:11:14 |
| 3.3 | stock.picking | 31 | INT/00011 — DAN-P01-A 2: Zaplecze → Kwarantanna | done 15:11:17 |
| 3.5 | stock.picking | 32 | IN/00018 — P03-Q `Q-1` (lot 16) 3 → Kwarantanna | done 15:11:50 |
| 3.7/3.8 | stock.picking | 33 | OUT/00004 — wydanie 1 P03-Q, linia ręczna z Kwarantanny | **done 15:11:59** |
| 3.8x | stock.picking | 34 | RET00001 — zwrot 1 Q-1 Customers → Kwarantanna (przywrócenie) | done 15:12:24 |
| K4 | product.product / mrp.bom | 11 / 1 | Z3-TEST zestaw P03, BoM 1 × P03-Q | — |
| 3.9 | mrp.production | 2 | MO/00002 — 1 zestaw | cancel |

### MAG-P03-POS — wynik: zgodny z oczekiwaniem

- Decyzja jakościowa: **symulowana** (alert 1) — brak decyzji Z5.
- Cały zapas DAN-P01-A przed: Półka 1: 1, Zaplecze: 2 (suma 3, inne lokalizacje: 0).
- Po dwóch przesunięciach: **Kwarantanna: 3**, Półka 1 i Zaplecze: 0. Dobra partia **DAN-P01-B: Zaplecze 2 — bez zmian**.
- Identyfikowalność DAN-P01-A (wstecz): dostawa IN/00009 od Dostawca testowy Z3 (14:50:11) → INT/00005 (Przyjęcie → Półka 1: 1,
  Zaplecze: 2) → INT/00010, INT/00011 (→ Kwarantanna). Naprzód: **brak sprzedaży i zużycia do zestawów** tej partii
  (0 linii sprzedaży, 0 zleceń produkcji) — nie da się wykazać ścieżki naprzód bez danych Z1/Z4.
- Ścieżka naprzód wykazana na partii 0000002: IN/00007 → OUT/00001 (S00002, AGH) → zwrot IN/00008 (sale_id S00002).
  Klient AGH jest jawnym partnerem zamówienia; klienta anonimowego nie identyfikowano.

### MAG-P03-NEG (produkt P03-Q, zapas wyłącznie w Kwarantannie: Q-1 3 szt.)

- **NEG-1 dostępność do sprzedaży — K− (luka):** `qty_available` = `free_qty` = `virtual_available` = **3**. Kwarantanna (pod widokiem
  magazynu WH/Input) wlicza się do dostępności produktu. To samo dla Trufle (11 = 6 + 3 + 2 w kwarantannie).
- **NEG-2 rezerwacja — K+:** wydanie OUT/00004 (źródło Zapasy) po action_assign: stan `confirmed`, **0 zarezerwowanych**.
- **NEG-3 ręczne wydanie — K− (luka krytyczna):** ręczna linia ruchu z Kwarantanny (Q-1, 1 szt.) na OUT/00004 —
  **walidacja przyjęta**, 1 szt. trafiła do Customers. Odoo nie blokuje ręcznego wydania zapasu kwarantanny.
  Stan przywrócony zwrotem RET00001 (Kwarantanna znów 3).
- **NEG-4 zestaw — K+ z zastrzeżeniem:** MO/00002 po action_confirm/action_assign: komponent P03-Q `confirmed`, **niezarezerwowany**
  (źródło Zapasy). Jednocześnie pole `components_availability` pokazuje **„Dostępny”** — informacja dla planisty myląca
  (wynika z dostępności liczonej z kwarantanną). Ręcznego zużycia z kwarantanny w MO nie badano.
- Kanały: sprzedaż = wydanie (typ 35); kasa PoS — **niezainstalowana**, nie badano. Role: wszystkie próby jako id 7 (administrator) —
  nie sprawdzano, czy zwykły użytkownik magazynu może wykonać NEG-3.

## MAG-P08 (MAG-016, MAG-019)

Kody `Z3-TRU-001` / `Z3-TRU-010` i warunki przechowywania — **dane fikcyjne ćwiczenia**. „Skan” = wyszukanie po kodzie przez API
(`product.product.barcode`, `stock.lot.name`); **nie** test fizycznego skanera ani aplikacji Barcode; nie powtórzono z Z1.

### Rekordy

| Krok | Model | ID | Zmiana | Przed → po |
|---|---|---|---|---|
| 8.3 | product.template | 6 (Trufle) | barcode | puste → `Z3-TRU-001` |
| 8.5 | product.template | 6 (Trufle) | description | puste → „Warunki przechowywania (dane ćwiczenia…): 15–18 °C, wilgotność ≤ 70 %, z dala od światła” |
| 8.6 | quality.alert | 2 | „Naruszenie warunków: Trufle TRU-P04-B, Półka 1 — 24 °C (symulacja)”, lot 7, zespół 1, odp. id 7 | New |

### MAG-P08-POS — wynik: zgodny z oczekiwaniem (w zakresie symulacji)

- Etykieta próbki: produkt `Z3-TRU-001`, partia `TRU-P04-B`, jm szt.; kartoteka Trufle: jm Units, śledzenie partią, partie TRU-P04-B (7), TRU-P04-BQ (8).
- Po korekcie kartoteki: skan `Z3-TRU-001` → **Trufle (6)**; skan partii `TRU-P04-B` → partia 7, produkt **Trufle**. Jednoznacznie.

### MAG-P08-NEG

- **NEG-1 (konflikt kodu):** przed korektą skan `Z3-TRU-001` → **brak produktu** (kod nieprzypisany nigdzie) — rozbieżność wykryta,
  nie zignorowana. Kod obcy `Z3-TRU-010` po korekcie → brak produktu. **K+.**
- **NEG-2 (naruszenie warunku):** alert 2 obejmuje **tylko partię TRU-P04-B** i wskazuje lokalizację Półka 1 (6 szt.) w opisie;
  partia TRU-P04-BQ (Kwarantanna 2) i zapas TRU-P04-B na Zapleczu (3) nie mają oceny. Przekazanie do jakości = alert w zespole
  „Main Quality Team”, etap New — **brak potwierdzenia Z5**. **K+ z ograniczeniem:** lokalizacja jest tylko w opisie (alert nie ma
  pola lokalizacji), alert nie blokuje zapasu.
- Ograniczenie MAG-019: brak w Odoo osobnego mechanizmu warunków lokalizacji (kategoria przechowywania nieużyta) — warunki zapisane
  jako opis produktu.

## Podsumowanie strumienia B

| Proces | POS | NEG |
|---|---|---|
| P02 | K+ (6 F-A + 2 F-B) | NEG-1 K+ (ostrzeżenie przy przyjęciu), NEG-2 K+ (partie po granicy pominięte), **NEG-3 K− (brak daty = dopuszczona)** |
| P03 | K+ (3 szt. w kwarantannie, ślad wstecz; naprzód brak danych dla tej partii) | **NEG-1 K− (dostępność z kwarantanną)**, NEG-2 K+, **NEG-3 K− krytyczna (ręczne wydanie z kwarantanny)**, NEG-4 K+ z zastrzeżeniem |
| P08 | K+ (symulacja) | NEG-1 K+, NEG-2 K+ z ograniczeniem |
