# MAG-P04 — wyniki prób (F2)

Wykonano 2026-10-26 ok. 15:56–16:01 (Europe/Warsaw; daty poniżej w UTC) przez MCP
(`mcp-server-odoo` 0.9.0, JSON-2, użytkownik id 7). Zgoda użytkownika na K1–K2, A0–A2, B0–B4, C1–C2, C1x: 2026-10-26.
Plan: `lab_3-P04-plan.md`. Zasady (trasa, reguły, osoba reagująca id 7) = **propozycja / decyzja użytkownika**,
nieuzgodnione z prowadzącym.

## Utworzone rekordy

| Krok | Model | ID | Nazwa / numer | Stan |
|---|---|---|---|---|
| K1 | product.product | 5 / 6 / 7 | Tiki-Taki / Trufle / Z3-TEST P04-C (partie, daty 180/150/30/45, Goods, szt.) | — |
| K2 | stock.route / stock.rule | 16 / 28 | „Z3: Uzupełnienie półki z zaplecza”: pull Zaplecze (41) → Półka 1 (43), typ 40, make_to_stock | aktywne |
| A0 | stock.picking | 19 | WH/Input/IN/00012 — Tiki-Taki `TIK-P04-A` (lot 6) 8 → Zaplecze | done 14:57:24 |
| A1 | mail.activity | 1 | To-Do „Brak na półce: Tiki-Taki (Półka 1 = 0, Zaplecze = 8)”, user id 7, termin 2026-10-31 | wykonana (msg 1870) |
| A2 | stock.picking | 20 | WH/Input/INT/00007 — TIK-P04-A 4: Zaplecze → Półka 1 | done 14:58:17 |
| B0 | stock.picking | 21 | WH/Input/IN/00013 — Trufle `TRU-P04-B` 1 → Półka 1, 8 → Zaplecze | done 14:58:51 |
| B0 | stock.picking | 22 | WH/Input/IN/00014 — Trufle `TRU-P04-BQ` 2 → Kwarantanna | done 14:58:54 |
| B1 | stock.warehouse.orderpoint | 1 | OP/00001 — Trufle, Półka 1, min 2 / max 6, manual, trasa 16 | — |
| B2 | stock.picking | 23 | WH/Input/INT/00008 (origin OP/00001) — 5 szt. Zaplecze → Półka 1 | done 14:59:19 |
| C1 | stock.warehouse.orderpoint | 2 | OP/00002 — Z3-TEST P04-C, Półka 1, min 2 / max 6, trasa 16 | aktywny |
| C1 | stock.picking | 24 | WH/Input/INT/00009 (origin OP/00002) — 6 szt. z pustego Zaplecza | **cancel (C1x)** |
| C2 | product.supplierinfo | 2 | Dostawca testowy Z3 → Z3-TEST P04-C, min 1, cena 0,00 | — |
| C2 | stock.warehouse.orderpoint | 3 | OP/00003 — Z3-TEST P04-C, Zapasy (34), min 2 / max 6, trasa Buy | — |
| C2 | purchase.order | 2 | **P00002** (origin OP/00003) — 6 szt., Dostawca testowy Z3 | **draft** (nie potwierdzono) |

## Wariant A (MAG-008, MAG-009) — wynik: zgodny z oczekiwaniem

- Przed: Tiki-Taki — Półka 1: brak stanu (0), Zaplecze: 8 (TIK-P04-A).
- Brak odczytany ze stanu (bez skargi klienta) → aktywność id 1 dla id 7 z opisem braku i reakcji.
- Transfer INT/00007: produkt, ilość 4, partia TIK-P04-A, źródło Zaplecze, cel Półka 1 — zapisane w linii ruchu (id 30).
- Po: **Półka 1: 4 / Zaplecze: 4, suma 8** (aggregate_records).
- Uwagi z wykonania: (1) pierwsza walidacja INT/00007 odrzucona „Należy podać numer partii…” — błąd skryptu
  (podano nazwę nowej partii zamiast istniejącej); poprawiono linię na lot_id 6 i zatwierdzono. Odrzucenie potwierdza
  dodatkowo, że transfer partii bez wskazania partii jest blokowany. (2) Aktywność oznaczono jako wykonaną ok. 25 s
  **przed** zatwierdzeniem transferu (kolejność w skrypcie) — ślad w chatterze nosi czas 14:57:52, transfer 14:58:17.

## Wariant B (MAG-010) — wynik: zgodny z oczekiwaniem

- Przed: Półka 1: 1, Zaplecze: 8 (TRU-P04-B), Kwarantanna: 2 (TRU-P04-BQ).
- OP/00001: qty_on_hand 1, qty_to_order **5** (= 6 − 1).
- action_replenish → **jeden** dokument INT/00008, 5 szt. Zaplecze → Półka 1; prognoza 6.
- **NEG-1 (ponowienie):** drugie action_replenish przy otwartym INT/00008 — **brak nowego dokumentu i ruchu**
  (nadal 1 ruch 5 szt.), qty_to_order 0. Potrzeba się nie mnoży.
- Zarezerwowana partia: TRU-P04-B z Zaplecza (nie z kwarantanny).
- Po walidacji: **Półka 1: 6 / Zaplecze: 3**, Kwarantanna: 2 bez zmian.
- **NEG-2 (kwarantanna):** kwarantanna nie była źródłem uzupełnienia. _Ograniczenie:_ nie badano przypadku, w którym
  wolny zapas istnieje **wyłącznie** w kwarantannie — tu reguła i tak bierze tylko z Zaplecza (41), więc wynik wynika
  z konfiguracji trasy, nie z osobnej blokady.

## Wariant C (MAG-011) — wynik: częściowo niezgodny

- Przed: Z3-TEST P04-C — brak stanów i dokumentów (0/0).
- **NEG-3 (pusty magazyn) — LUKA:** OP/00002 (Półka 1, trasa Zaplecze → Półka) po action_replenish **utworzył
  przesunięcie WH/Input/INT/00009 na 6 szt. z pustego Zaplecza** (stan `confirmed`, oczekuje na dostępność).
  To fikcyjny transfer, który polecenie wyklucza („0/0 nie daje transferu”). Dowód zapisany, dokument anulowany (C1x).
  _Ryzyko:_ OP/00002 nadal ma qty_to_order 6 — każde ponowne uruchomienie (lub harmonogram przy trigger auto)
  utworzy taki dokument ponownie. Decyzja użytkownika (2026-10-26): OP/00002 pozostaje bez zmian jako dowód luki.
- **Przekazanie do zakupów:** OP/00003 (Zapasy, Buy) → **szkic RFQ P00002**, 6 szt., Dostawca testowy Z3, origin OP/00003,
  planowana dostawa 2026-10-27. Nie powstał żaden transfer magazynowy. RFQ **nie potwierdzono** — decyzja należy do Z2.
- Braki: RFQ nie ma przypisanego kupującego (user_id puste) — odpowiedzialność Z2 niewskazana w systemie;
  cena dostawcy 0,00 (brak danych, nie wymyślano). Potwierdzenia partnera (Z2) — **brak**.

## Do zapisu w SIWZ (propozycja treści)

- MAG-008 → MAG-P04-A (INT/00007), B (INT/00008): ruchy z produktem, ilością, partią, źródłem i celem.
- MAG-009 → MAG-P04-A: aktywność id 1 dla osoby reagującej (id 7 — decyzja użytkownika, do potwierdzenia).
- MAG-010 → MAG-P04-B: OP/00001, POS 1/8 → 6/3, NEG-1 bez zwielokrotnienia; NEG-2 z ograniczeniem.
- MAG-011 → MAG-P04-C: RFQ P00002 (draft) dla Z2 — **K+ dla przekazania**, **K− dla NEG-3** (fikcyjny transfer INT/00009).
