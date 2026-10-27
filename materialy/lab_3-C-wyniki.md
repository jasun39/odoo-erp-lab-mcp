# Strumień C — MAG-P05 — wyniki prób (F2)

Wykonano 2026-10-26 ok. 16:18–16:20 (Europe/Warsaw; daty poniżej w UTC) przez MCP (`mcp-server-odoo` 0.9.0, JSON-2,
użytkownik id 7, administrator). Zgoda użytkownika na K1–K2, 5.0–5.5: 2026-10-26. Plan: `lab_3-C-plan.md`.
Zasady (wolny zapas, zaległość w B) = **propozycja**, nieuzgodniona z prowadzącym/Z1.

## Rekordy

| Krok | Model | ID | Numer / nazwa | Stan |
|---|---|---|---|---|
| K1 | product.product | 12 / 13 / 14 | Z3-TEST P05-A / P05-B / P05-C (partie, Goods, szt.) | — |
| K2 | res.partner | 19 | Klient testowy Z3 | — |
| 5.0 | stock.picking | 35 / 36 / 37 | IN/00019 (P05A-1 10), IN/00020 (P05B-1 6), IN/00021 (P05C-1 5) → Zapasy | done |
| 5.1 | stock.picking | 38 | OUT/00005 — A1, 6 szt. P05-A | **partially_available (4 z 6)** po 5.2N |
| 5.2 | stock.picking | 39 | OUT/00006 — A2, 6 szt. P05-A | done 15:18:37 (NEG-1) |
| 5.3 | sale.order | 3 | S00003 — Klient testowy Z3, 10 szt. P05-B, cena 0, magazyn „Przyjęcia” | sale |
| 5.4 | stock.picking | 40 | OUT/00007 (S00003) — 6 szt. P05B-1 | done |
| 5.4 | stock.picking | 41 | OUT/00008 (S00003, zaległość do OUT/00007) — 4 szt. | **confirmed (otwarta)** |
| 5.5 | stock.picking | 42 | OUT/00009 — 6 szt. P05-C ze stanu 5 | done 15:19:34 (NEG-2) |

## Wariant A (MAG-013) — POS zgodny, NEG-1 luka

- 5.1: P05A-1 w Zapasach: **fizycznie 10, zarezerwowane 6**, `free_qty` **4**, `outgoing_qty` 6; dokument rezerwujący **OUT/00005** (linia 67).
- 5.2: nowa potrzeba OUT/00006 (6 szt.) dostała **tylko 4** (`partially_available`); A1 bez zmian (6). Zarezerwowane razem 10 = fizycznie 10.
  **POS: K+** — jedna sztuka nie jest liczona jako dostępna dla dwóch potrzeb.
- **NEG-1 (5.2N) — K− (luka):** ręczne podniesienie linii OUT/00006 do 6 szt. → przed walidacją `reserved_quantity` kwantu **12 przy 10 fizycznie**;
  walidacja **przyjęta** (OUT/00006 done, 6 szt.). Rezerwacja A1 (OUT/00005) **po cichu zmniejszona z 6 do 4** (`partially_available`),
  bez komunikatu. Po: Zapasy 4 (zarezerwowane 4 dla A1), Customers 6. Zarezerwowany zapas innego dokumentu został użyty.

## Wariant B (MAG-014) — POS zgodny

- S00003 (10 szt.) po potwierdzeniu: wydanie OUT/00007, rezerwacja **6 z 10** (stan 6).
- Walidacja z utworzeniem zaległości (kontekst `skip_backorder` = „Utwórz zaległość”): **OUT/00007 done — 6 szt. partii P05B-1**;
  **OUT/00008 — zaległość 4 szt.**, `backorder_id` = OUT/00007, `sale_id` = S00003, stan `confirmed` (czeka na dostępność).
- Linia zamówienia: zamówiono 10, **wydano 6**, do wydania 4. Powiązanie wydania i partii z zamówieniem zachowane.
- Ograniczenie: obsługa pozostałych 4 = otwarta zaległość; decyzja handlowa (czekać / anulować / zakup) — Z1, poza próbą.

## Wariant C (MAG-018) — NEG-2 luka

- Przed: P05C-1 w Zapasach **5**. Wydanie OUT/00009 na 6: rezerwacja 5 (`partially_available`).
- Linia ręcznie podniesiona do 6 szt. → walidacja **przyjęta bez blokady i bez zaległości**: wydano **6**, otwarte **0**.
- Stan końcowy: **Zapasy −1** (P05C-1), Customers 6; `qty_available` = `free_qty` = **−1**.
  **K− (luka):** rozchód ponad dostępny zapas potwierdzony; brakująca ilość stała się stanem ujemnym (widocznym w kwancie,
  ale niezablokowanym).

## Uwagi

- Wszystkie próby jako administrator (id 7); nie sprawdzano uprawnień zwykłego użytkownika magazynu.
- NEG-1 i NEG-2 to ten sam mechanizm: Odoo pozwala ręcznie wpisać ilość wydaną większą niż zarezerwowana/dostępna.

## Podsumowanie

| Wariant | Wynik |
|---|---|
| A POS (MAG-013) | K+ — 10 / 6 / 4, nowa potrzeba dostaje 4 |
| A NEG-1 | **K−** — użycie cudzej rezerwacji, A1 obniżone 6 → 4 bez komunikatu |
| B POS (MAG-014) | K+ — 6 z partią, zaległość 4 przy S00003 |
| C NEG-2 (MAG-018) | **K−** — wydano 6 ze stanu 5, stan −1 |

## Decyzja po wynikach (5.X)

2026-10-26, użytkownik: OUT/00005, OUT/00008 i stan −1 P05C-1 (Zapasy) pozostają bez zmian jako dowody.
Stan −1 zostanie użyty w MAG-P07 (spis i zatwierdzona korekta inwentaryzacyjna).

---

# MAG-P06 i MAG-P07 — wyniki prób (F2)

Wykonano 2026-10-26 ok. 17:34–17:37 (Europe/Warsaw; daty w UTC) przez MCP, użytkownik id 7. **Polecenie użytkownika
(2026-10-26): Claude sam podejmuje decyzje** — poniższe zasady i dane to **decyzje Claude**, nie uzgodnienia prowadzącego.

## Decyzje Claude

- Osobny produkt `Z3-TEST P06-DAN` (15) — czyste dane „źródło 10 na półce” (Danusia ma inne stany); dwie partie (P06-A wcześniejsza data, P06-B),
  żeby sprawdzić, czy zwrot dotyczy właściwej partii.
- Seria P06 jest jednocześnie „odrębną serią przyjęć, wydań, zwrotów i transferów” dla bilansu P07; **otwarcie = 0** (produkt nowy).
- Zwrot: typ „Zwroty klientów” (45, Customers → Kwarantanna), już przypisany jako typ zwrotu dla „Zlecenia dostawy” (35) — bez zmian globalnych.
  Odoo 20 nie ma kreatora `stock.return.picking`; zwrot utworzony przez API z powiązaniami Odoo: `return_id` (wydanie), `origin_returned_move_id`,
  `sale_line_id`, `to_refund`, powód zwrotu id 2 „Item arrived damaged or defective”. Partia zwrotu **pobrana z linii pierwotnego wydania**.
- Dopuszczenie zwrotu do ponownej sprzedaży: tylko po odrębnej decyzji jakości (Z5) — alert jakości, bez zwalniania.
- Spis P07: rozbieżność −1 na P06-B / Półka 1, przyczyna **symulowana** („uszkodzona, zutylizowana bez rejestracji”). Liczenie (ilość policzona)
  i zatwierdzenie (apply) jako osobne kroki; obie role — id 7 (jedyny dostępny użytkownik).
- Stan −1 P05C-1 (z P05-C NEG-2) skorygowany spisem 0 (+1) z przyczyną — decyzja użytkownika z 2026-10-26.
- Kontrolowana niezgodność P07: **ponowienie dokumentu dostawy** (duplikat 1 szt. P06-A z tym samym źródłem), wykrycie bilansem, odwrócenie zwrotem
  do dostawcy (bez usuwania historii).

## Rekordy

| Krok | Model | ID | Numer / nazwa | Stan |
|---|---|---|---|---|
| 6.0 | product.product | 15 | Z3-TEST P06-DAN; partie P06-A (20, usunięcie 2027-01-01), P06-B (21, 2027-03-01) | — |
| 6.0 | stock.picking | 43 | IN/00022 — P06-A 4, P06-B 6 → Zaplecze (Dostawca testowy Z3) | done 16:34:01 |
| 6.0 | stock.picking | 44 | INT/00012 — 10 szt. Zaplecze → Półka 1 | done 16:34:05 |
| 6.1 | sale.order | 4 | S00004 — Klient testowy Z3, 3 szt. | sale |
| 6.1 | stock.picking | 45 | OUT/00010 (S00004) — P06-A 3 z Półki 1 (FEFO) | done 16:34:08 |
| 6.2 | stock.picking | 46 | **RET00002** — zwrot 1 P06-A Customers → Kwarantanna, return_id OUT/00010 | done 16:34:39 |
| 6.3 | quality.alert | 3 | „Kontrola zwrotu RET — … P06-A 1 szt.”, picking RET00002, zespół 1 | New |
| 6.4 | stock.picking | 47 | OUT/00011 — próbne wydanie 8 | cancel |
| 7.1 | stock.quant | 68 | P06-B / Półka 1: spis 5 (system 6) → korekta −1 (ruch 83) | zastosowana 16:35:19 |
| 7.2b | stock.quant | 59 | P05C-1 / Zapasy: spis 0 (system −1) → korekta +1 (ruch 84) | zastosowana 16:35:23 |
| 7.4 | stock.picking | 48 | **IN/00023 — kontrolowany duplikat** 1 szt. P06-A (to samo źródło co IN/00022) | done 16:36:15 |
| 7.4 | stock.picking | 49 | OUT/00012 — odwrócenie duplikatu, Zaplecze → Vendors, return_id IN/00023 | done 16:36:22 |

## MAG-P06 (MAG-015)

- **POS — K+:** po sprzedaży 3 i zwrocie 1: **Półka 1: 7** (P06-A 1 + P06-B 6), **Kwarantanna: 1** (P06-A), **fizycznie 8**.
  Zwrot powiązany: OUT/00010 → RET00002 (`return_ids`), ruch z `origin_returned_move_id`, linia S00004: zamówiono 3, **wydano 2** (zwrot zmniejszył ilość wydaną).
- Przekazanie: alert jakości 3 (Z5) — **dopuszczenie wymaga odrębnej decyzji**; rozliczenie (korekta faktury) — FIN-P02, **nie wykonano** (poza Z3), ruch ma `to_refund`.
- **NEG-1 (zwrot dostępny dla kasy/sprzedaży?):** próbne wydanie 8 zarezerwowało **7** (P06-A 1 + P06-B 6 z Półki), zwrot w kwarantannie pominięty — **K+**.
  Ale `qty_available` = `free_qty` = **8** (liczy kwarantannę) — **K−** w informacji o dostępności (ta sama luka co P03-NEG-1). PoS niezainstalowany — kasy nie badano.
- **NEG-2 (właściwa partia):** zwrot ma partię **P06-A** = partia z wydania; P06-B nietknięta — **K+**.

## MAG-P07 (MAG-012, MAG-020)

- **Spis (POS) — K+:** P06-DAN system 8 → spis na Półce 1 / P06-B: 5 zamiast 6 → **różnica −1** (`inventory_diff_quantity` −1, liczący id 7).
  Po zatwierdzeniu: ruch 83 do „Inventory adjustment” z opisem przyczyny i zatwierdzającego, `create_uid` = id 7; stan 7.
- **Korekta stanu ujemnego P05-C:** −1 → 0 (ruch 84 z przyczyną wskazującą OUT/00009). `qty_available` P05-C = 0.
- **Bilans serii (otwarcie 0 + przyjęcia − wydania ± zwroty ± korekty, wg partii i lokalizacji) — K+:**

| Partia | Lokalizacja | Przyjęcia | Transfery | Wydania | Zwroty od klienta | Zwroty do dostawcy | Korekty | Wynik | Stan Odoo |
|---|---|---|---|---|---|---|---|---|---|
| P06-A | Kwarantanna | 0 | 0 | 0 | +1 | 0 | 0 | 1 | 1 |
| P06-A | Półka 1 | 0 | +4 | −3 | 0 | 0 | 0 | 1 | 1 |
| P06-A | Zaplecze | +5 | −4 | 0 | 0 | −1 | 0 | 0 | 0 |
| P06-B | Półka 1 | 0 | +6 | 0 | 0 | 0 | −1 | 5 | 5 |
| P06-B | Zaplecze | +6 | −6 | 0 | 0 | 0 | 0 | 0 | 0 |
| **Razem firma** | | **+11** | **0** | **−3** | **+1** | **−1** | **−1** | **7** | **7** |

  (stan końcowy, po duplikacie i jego odwróceniu). **Transfer wewnętrzny nie zmienia sumy firmy** (transfery razem 0). Kwarantanna ujęta.
- **NEG (kontrolowana niezgodność) — K+:** duplikat IN/00023 podniósł przyjęcia do **11 vs 10** z dokumentu dostawy; wykryty w bilansie i wskazany
  jako dokument źródłowy (dwa przyjęcia z tym samym źródłem: IN/00022, IN/00023). Odwrócony OUT/00012 — historia zachowana, bez usuwania.
- **Ważne ograniczenie:** bilans liczony z ruchów Odoo zawsze zgadza się ze stanami Odoo (to te same dane). Duplikat wykrywa dopiero porównanie
  z **dokumentem zewnętrznym** (tu: dostawa = 10 szt.). **Odoo nie ostrzegło** przy przyjęciu duplikatu z tym samym źródłem i dostawcą.
