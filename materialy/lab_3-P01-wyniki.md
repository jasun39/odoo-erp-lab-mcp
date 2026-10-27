# MAG-P01 — wyniki prób (F2)

Wykonano 2026-10-26 ok. 15:48–15:52 (Europe/Warsaw; daty poniżej w UTC) przez MCP
(`mcp-server-odoo` 0.9.0, JSON-2, użytkownik id 7). Zgoda użytkownika na Z1–Z6: 2026-10-26.
Plan: `lab_3-P01-plan.md`. Zasady źródeł realizacji = **propozycja**, nieuzgodniona z prowadzącym.

## Utworzone rekordy

| Krok | Model | ID | Nazwa / numer | Stan |
|---|---|---|---|---|
| Z1 | stock.location | 45 | WH/Input/Przyjęcie (internal, rodzic WH/Input 33, poza Zapasy) | aktywna |
| Z2 | res.partner | 18 | Dostawca testowy Z3 (firma) | — |
| Z3 | stock.picking | 14 | WH/Input/IN/00009 (Vendors → Przyjęcie) | done 14:50:11 |
| Z3 | stock.lot | 3 | DAN-P01-A (Danusia) | 3 szt. |
| Z3 | stock.lot | 4 | DAN-P01-B (Danusia) | 2 szt. |
| Z4 | stock.picking | 15 | WH/Input/INT/00005 (Przyjęcie → Półka 1 / Zaplecze) | done 14:50:54 |
| Z5 | stock.picking | 16 | WH/Input/IN/00010 (NEG-1) | **assigned — otwarty** |
| Z6 | stock.picking | 17 | WH/Input/IN/00011 (NEG-2) | done 14:51:31 |
| Z6 | stock.lot | 5 | DAN-P01-NODATE (Danusia) | 1 szt. w Przyjęcie |

Uwaga: przed Z1 znaleziono zarchiwizowaną lokalizację `WH/Przyjęcia` (id 7) innego magazynu `WH` — bez zmian.
Pole `ref` (nr partii dostawcy) **nieuzupełnione** — brak rzeczywistego numeru w danych.

## MAG-P01-POS — wynik: zgodny z oczekiwaniem

- Dostawa IN/00009 od partnera „Dostawca testowy Z3” zachowała podział na 2 partie (3 + 2), daty partii
  (z kartoteki produktu): expiration 2027-04-24, removal 2027-03-25, alert 2027-03-10, use 2026-11-25.
- Stany Danusia wg partii (internal, aggregate_records): 0000001 = 11, 0000002 = 13, DAN-P01-A = 3,
  DAN-P01-B = 2, DAN-P01-NODATE = 1.
- Rozwinięcie DAN-P01-A = 3 → **Półka 1: 1 + Zaplecze: 2** (Przyjęcie: 0). Widać położenie każdej ilości.

| partia | lokalizacja | ilość przed | ilość po |
|---|---|---|---|
| DAN-P01-A | Półka 1 (43) | — | 1 |
| DAN-P01-A | Zaplecze (41) | — | 2 |
| DAN-P01-B | Zaplecze (41) | — | 2 |
| DAN-P01-NODATE | Przyjęcie (45) | — | 1 |
| 0000001 / 0000002 | bez zmian (3+8 / 13) | | |

## MAG-P01-NEG

- **NEG-1 (brak partii):** walidacja IN/00010 bez partii **zablokowana** przez Odoo komunikatem
  „Należy podać numer partii/numer seryjny produktu: Danusia”. Dokument pozostał `assigned` (otwarty,
  1 szt. oczekująca) — wymaga decyzji: anulować lub zostawić jako dowód.
- **NEG-2 (brak daty):** linia z partią DAN-P01-NODATE i wyczyszczoną datą ważności (`expiration_date=false`,
  potwierdzone odczytem przed walidacją) **została przyjęta** (IN/00011 done). Odoo **samo nadało** partii daty
  z kartoteki produktu (expiration 2027-04-24T14:51:31, removal/alert/use jak wyżej, liczone od chwili walidacji).
  Brak daty nie blokuje przyjęcia i nie jest widoczny po fakcie — data wygląda jak wprowadzona. **Luka do oceny/uzgodnienia
  (właściciel: do wskazania — Z3/Z2 kontrola dostawy).**
- **NEG-3 (istniejące dane, tylko odczyt):** KAKAO (śledzenie partiami) ma 20 kg **bez partii**
  (Zapasy 5, Półka 1 15) — anonimowa suma bez identyfikacji. Pochodzenie: wcześniejsze operacje zespołu, sprzed tej próby.
  Właściciel: do wskazania.

## Do zapisu w SIWZ (propozycja treści)

- MAG-001 → MAG-P01-POS: lokalizacje Przyjęcie (45), Półka 1 (43), Zaplecze (41), Kwarantanna (42, poza Zapasy);
  źródła realizacji — **propozycja** (`lab_3-P01-plan.md`), do uzgodnienia z Z1/Z4.
- MAG-002 → MAG-P01-POS: zestawienie wg produktu/partii/lokalizacji, 3 = 1 + 2.
- MAG-003 → POS + NEG-1 (blokada braku partii) + NEG-2 (brak daty nieblokowany, daty domyślne) + NEG-3.
