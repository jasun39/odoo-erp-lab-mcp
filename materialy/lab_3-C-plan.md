# Strumień C (MAG-P05, P06, P07) — plan prób (PROPOZYCJA, niezatwierdzona)

Status: **propozycja Claude**, 2026-10-26. Nie jest uzgodnieniem prowadzącego ani wynikiem próby.
Zakres na teraz (polecenie użytkownika 2026-10-26): **tylko MAG-P05**. P06 i P07 — do przygotowania później.

## MAG-P05 (MAG-013, MAG-014, MAG-018)

Dane z polecenia: A: fizycznie 10 dopuszczonych, zarezerwowane 6. B: zamówienie 10 / realizacja 6. C: źródło 5 / żądane 6.

### Fakty z odczytu (2026-10-26)

- Typ „Zlecenia dostawy” (35): rezerwacja przy potwierdzeniu (`at_confirm`), zaległości (backorder) = **pytaj** (okno Odoo).
  Przy częściowej realizacji użyję `button_validate` z kontekstem `skip_backorder` = utworzenie zaległości (jak „Utwórz zaległość” w oknie).
- Brak partnera-klienta testowego; jedyny klient: AGH (17) — nie używam danych prawdziwego partnera.
- Brak produktów i partii z „P05” w nazwie.

### Proponowane zasady (do uzgodnienia)

- Wolny zapas = fizyczny w Zapasach (z podlokalizacjami) − zarezerwowany; kwarantanna poza zakresem (wynik P03-NEG-1: pole
  `free_qty` produktu liczy kwarantannę — w odczytach podaję stany wg lokalizacji).
- Zamówienie B przez **zamówienie sprzedaży** (powiązanie wydania z zamówieniem — MAG-014); A i C przez same wydania magazynowe.
- Pozostałe 4 szt. w B = **zaległość (backorder)** powiązana z tym samym zamówieniem.

### Zapisy w Odoo (do zgody)

| # | Operacja | Model | Dane / oczekiwanie |
|---|---|---|---|
| K1 | create ×3 | product.product | `Z3-TEST P05-A`, `Z3-TEST P05-B`, `Z3-TEST P05-C`: partie, daty jak Danusia, Goods, szt. |
| K2 | create | res.partner | `Klient testowy Z3` (firma) |
| 5.0 | 3 przyjęcia + validate | stock.picking (typ 34) | P05-A `P05A-1` 10 → Zapasy; P05-B `P05B-1` 6 → Zapasy; P05-C `P05C-1` 5 → Zapasy |
| 5.1 | wydanie A1 6 szt. + assign; odczyt | stock.picking (typ 35) | **POS:** fizycznie 10, zarezerwowane 6, wolne 4; dokument rezerwujący A1 |
| 5.2 | wydanie A2 6 szt. + assign; odczyt | stock.picking (typ 35) | **POS:** A2 dostaje tylko 4 (częściowo dostępne), A1 nadal 6 |
| 5.2N | A2: ręczne podniesienie linii do 6 szt. + validate | stock.move.line | **NEG-1:** czy da się wydać sztuki zarezerwowane dla A1; odczyt A1 i stanu po |
| 5.3 | zamówienie sprzedaży 10 szt. P05-B (Klient testowy Z3, cena 0) + confirm | sale.order | powstaje wydanie, rezerwacja 6 z 10 |
| 5.4 | realizacja 6 z partią P05B-1 + validate z utworzeniem zaległości | stock.picking | **POS:** wydano 6 (partia P05B-1), zaległość 4 powiązana z zamówieniem; odczyt `qty_delivered` = 6 |
| 5.5 | wydanie C 6 szt. + assign; linia 6 szt. partii P05C-1 + validate | stock.picking (typ 35) | **NEG-2:** rozchód 6 ze stanu 5 — odczyt ilości wydanej, otwartej i stanu końcowego (czy powstaje stan ujemny) |
| 5.X | sprzątanie (po zapisaniu dowodów) | stock.picking | action_cancel otwartych wydań A1/A2 i zaległości B, **jeśli** zostaną otwarte — osobno do decyzji po wyniku |

Przed każdym krokiem i po nim: odczyt stanów wg produkt/partia/lokalizacja i rezerwacji; wyniki z ID w `lab_3-C-wyniki.md`.

## MAG-P06, MAG-P07 — do przygotowania

- P06: istniejący zwrot `IN/00008` trafił do Zapasów typem „Przyjęcia”, a typ „Zwroty klientów” (45) kieruje do Kwarantanny — punkt wyjścia.
- P07: inwentaryzacja 8 → 7 i bilans serii operacji — do zaplanowania.
- P07: wykorzystać stan −1 P05C-1 w Zapasach (z MAG-P05-C NEG-2) jako rozbieżność do spisu i zatwierdzonej korekty —
  decyzja użytkownika 2026-10-26.
