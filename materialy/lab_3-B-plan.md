# Strumień B (MAG-P02, P03, P08) — plan prób (PROPOZYCJA, niezatwierdzona)

Status: **propozycja Claude**, 2026-10-26. Nie jest uzgodnieniem prowadzącego ani wynikiem próby.
Uzgodnień z prowadzącym/Z5 brak → wszystkie zasady, decyzje jakościowe i warunki poniżej to **propozycje/dane ćwiczenia**.

## Fakty z odczytu (2026-10-26)

- Strategia usuwania: kategoria `Goods` = **FEFO**; lokalizacje Zapasy/Półka 1 = FIFO. W Odoo strategia kategorii produktu
  ma pierwszeństwo przed lokalizacją — _do potwierdzenia próbą P02_.
- Daty partii liczone z daty ważności: usunięcie = ważność − 30 dni, alert = ważność − 45 dni (parametry produktów).
- **Dostępność produktu obejmuje kwarantannę:** Trufle `qty_available` = `free_qty` = 11 = półka 6 + zaplecze 3 + **kwarantanna 2**.
  _Obserwacja dla MAG-004 (dostępność do sprzedaży)._
- Brak BoM; MO/00001 (draft, „cuksy”) należy do innego zespołu — nie ruszamy. Brak point_of_sale.
- `quality.alert` ma pola: lot_ids, picking_id, product_id, team_id (Main Quality Team id 1), stage_id, user_id.
- Trufle nie ma kodu kreskowego w kartotece.

## Proponowane zasady (do uzgodnienia)

- **MAG-006:** daty przechowywane w UTC, prezentacja i granica w **Europe/Warsaw**. Data alertu = ostrzeżenie;
  data usunięcia = **granica wydania** (partia dopuszczona do wydania, gdy data usunięcia > teraz); data ważności = koniec przydatności.
- **MAG-005:** strategia FEFO z kategorii `Goods` (bez zmian globalnych).
- Niedopuszczenie partii = umieszczenie w `Kwarantanna` (42, poza Zapasy) + alert jakości.

## Produkty testowe (niezależne stany)

| # | Produkt | Cel |
|---|---|---|
| K1 | `Z3-TEST P02-FEFO` | P02 POS (A/B/X) |
| K2 | `Z3-TEST P02-GR` | P02 granica (przed / na / po / brak daty) |
| K3 | `Z3-TEST P03-Q` | P03 NEG: zapas wyłącznie w kwarantannie |
| K4 | `Z3-TEST zestaw P03` + BoM (1 × P03-Q) | P03 NEG: użycie do zestawu |

Wszystkie: partie, daty jak Danusia (180/150/30/45), Goods, szt. Dostawca: Dostawca testowy Z3 (18).

## MAG-P02 (MAG-005, MAG-006)

| # | Zapis | Dane / oczekiwanie |
|---|---|---|
| 2.1 | przyjęcie → Zapasy | P02-FEFO: `F-A` 6 szt. (usunięcie 2026-12-01), `F-B` 8 szt. (usunięcie 2027-01-15) |
| 2.2 | przyjęcie → Kwarantanna | P02-FEFO: `F-X` 4 szt. (usunięcie 2026-11-15 — **najwcześniejsza**, niedopuszczona) |
| 2.3 | wydanie (typ 35) 8 szt. + action_assign, odczyt | **POS:** zarezerwowane 6 F-A + 2 F-B; F-X nie użyta |
| 2.4 | przyjęcie → Zapasy | P02-GR po 1 szt.: `G-PRZED` (usunięcie 2026-11-30), `G-NA` (2026-10-26 00:00 Warszawa), `G-PO` (2026-10-25), `G-BRAK` |
| 2.5 | update stock.lot `G-BRAK` | wyczyszczenie dat (Odoo nadaje je domyślnie — wynik P01-NEG-2); jawnie jako przygotowanie danych |
| 2.6 | wydanie 3 szt. + action_assign, odczyt | **NEG:** które partie wybiera FEFO; oczekiwanie wymagania: G-PO i G-NA **nie** są dopuszczone, G-BRAK nieuznana |
| 2.7 | action_cancel wydań z 2.3 i 2.6 | po zapisaniu dowodu (rezerwacje nie blokują dalszych prób) |

## MAG-P03 (MAG-004, MAG-007, MAG-017)

Partia wskazana: **Danusia `DAN-P01-A`** (dziś Półka 1: 1 / Zaplecze 2 — zgodne z „DAN-X: półka 1/zaplecze 2”). Dobra partia: `DAN-P01-B`.

| # | Zapis | Dane / oczekiwanie |
|---|---|---|
| 3.1 | create quality.alert | „Wycofanie DAN-P01-A — decyzja **SYMULOWANA**, do potwierdzenia przez Z5”, lot_ids, zespół 1, etap New |
| 3.2 | odczyt | cały zapas DAN-P01-A we wszystkich lokalizacjach (oczek. 1 + 2) |
| 3.3 | 2 przesunięcia + validate | Półka 1 → Kwarantanna 1; Zaplecze → Kwarantanna 2; **POS:** 3 szt. w kwarantannie, DAN-P01-B bez zmian |
| 3.4 | odczyt (identyfikowalność) | DAN-P01-A: IN/00009 (Dostawca testowy Z3) → INT/00005 → przesunięcia 3.3; sprzedaż/zestawy tej partii: brak danych. Ścieżka naprzód pokazana dodatkowo na 0000002 (OUT/00001 → S00002 → zwrot IN/00008) |
| 3.5 | przyjęcie → Kwarantanna | P03-Q: `Q-1` 3 szt. (jedyny zapas produktu) |
| 3.6 | odczyt | **NEG-1 dostępność do sprzedaży:** qty_available/free_qty P03-Q (oczek. wymagania 0; prawdopodobnie 3) |
| 3.7 | wydanie 1 (typ 35) + action_assign | **NEG-2 rezerwacja:** oczek. brak rezerwacji |
| 3.8 | ręczna linia Kwarantanna/Q-1 + validate | **NEG-3 ręczne wydanie:** czy Odoo pozwala wydać z kwarantanny |
| 3.8x | zwrot 1 szt. do Kwarantanny (typ 45) | tylko jeśli 3.8 przejdzie — przywrócenie stanu |
| 3.9 | BoM + MO 1 szt. + action_confirm/assign | **NEG-4 zestaw:** oczek. komponent niezarezerwowany; potem action_cancel MO |

## MAG-P08 (MAG-016, MAG-019)

Produkt **Trufle (6)**, partia `TRU-P04-B`. Kody i warunki to **dane fikcyjne ćwiczenia**. „Skan” = wyszukanie po kodzie przez API
(nie jest to test fizycznego skanera ani aplikacji Barcode).

| # | Zapis | Dane / oczekiwanie |
|---|---|---|
| 8.1 | odczyt | kartoteka Trufle: brak kodu; etykieta próbki: produkt `Z3-TRU-001`, partia `TRU-P04-B` |
| 8.2 | odczyt | **NEG-1:** „skan” `Z3-TRU-001` → brak produktu (konflikt wykryty, nie pominięty) |
| 8.3 | update product.template Trufle | barcode = `Z3-TRU-001` (korekta kartoteki) |
| 8.4 | odczyt | **POS:** „skan” produktu → Trufle; „skan” partii `TRU-P04-B` → Trufle; kod obcy `Z3-TRU-010` → brak |
| 8.5 | update product.template Trufle | opis wewn.: „Warunki przechowywania (dane ćwiczenia): 15–18 °C, wilgotność ≤ 70 %, z dala od światła” |
| 8.6 | create quality.alert | „Naruszenie warunków: Trufle TRU-P04-B, Półka 1 — 24 °C (symulacja)”, lot_ids, zespół 1, etap New |
| 8.7 | odczyt | **NEG-2:** alert dotyczy tylko TRU-P04-B/Półka 1; partia TRU-P04-BQ i reszta zapasu bez oceny |

Przed każdym krokiem i po nim: odczyt stanów/dokumentów; wyniki z ID w `lab_3-B-wyniki.md`.
