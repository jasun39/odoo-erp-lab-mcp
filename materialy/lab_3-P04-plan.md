# MAG-P04 — plan prób (PROPOZYCJA, niezatwierdzona)

Status: **propozycja Claude**, 2026-10-26. Nie jest uzgodnieniem prowadzącego ani wynikiem próby.
Wymagania: MAG-008, MAG-009, MAG-010, MAG-011. Dane z polecenia: A: półka 0 / zaplecze 8, transfer 4.
B (niezależny): półka 1 / zaplecze 8, minimum 2, cel 6. C: 0/0.

## Stan wyjściowy (odczyt 2026-10-26)

- Brak trasy/reguły „Zaplecze → Półka 1”; brak reguł min/max; reguła zakupu `WH/Input: Zapasy (Buy)` (id 27, trasa Buy id 4) istnieje.
- Brak produktów Tiki-Taki i Trufle. Danusia i KAKAO mają już stany na półce — nie dają czystych stanów 0/8, 1/8, 0/0.
  Min/max działa na poziomie produktu i lokalizacji, nie partii → potrzebne **3 odrębne produkty**.

## Propozycje zasad (do uzgodnienia)

- Uzupełnienie półki: reguła pull `Zaplecze (41) → Półka 1 (43)`, typ „Przesunięcia wewnętrzne” (40), make_to_stock,
  w nowej trasie „Z3: Uzupełnienie półki z zaplecza”. Reguła min/max na Półka 1, wyzwalanie **ręczne**.
- Brak w firmie → reguła min/max na `Zapasy` (34) z trasą Buy → **szkic** zapytania ofertowego dla Z2 (nie potwierdzamy).
- Osoba reagująca na brak (MAG-009): **do wskazania** — w planie użytkownik id 7, jeśli nie wskażesz innej.
- Parametry dat nowych produktów skopiowane z Danusi (180/150/30/45 dni) — dane ćwiczeniowe, nie zasady producenta.

## Zapisy w Odoo (do zgody)

### Konfiguracja

| # | Operacja | Model | Dane |
|---|---|---|---|
| K1 | create ×3 | product.product | `Tiki-Taki` (A), `Trufle` (B), `Z3-TEST P04-C` (C): storable, partie, daty jak Danusia, kategoria Goods, szt. |
| K2 | create | stock.route + stock.rule | „Z3: Uzupełnienie półki z zaplecza”; reguła pull 41 → 43, typ 40, make_to_stock |

### Wariant A — transfer ręczny 0/8 → 4/4 (MAG-008, MAG-009)

| # | Operacja | Dane |
|---|---|---|
| A0 | przyjęcie (typ 34, Dostawca testowy Z3) + validate | Tiki-Taki partia `TIK-P04-A` 8 szt. → Zaplecze (41) |
| A1 | odczyt + create mail.activity | stan półka 0 / zaplecze 8 → aktywność „Brak na półce: Tiki-Taki” dla osoby reagującej (bez skargi klienta) |
| A2 | przesunięcie (typ 40) + validate | TIK-P04-A 4 szt. Zaplecze → Półka 1; oczekiwane 4/4, suma 8; aktywność oznaczona jako wykonana |

### Wariant B — reguła min 2 / cel 6, 1/8 → 6/3 (MAG-010)

| # | Operacja | Dane |
|---|---|---|
| B0 | przyjęcie + validate | Trufle `TRU-P04-B`: 1 → Półka 1, 8 → Zaplecze; osobna partia `TRU-P04-BQ` 2 → **Kwarantanna** (42) |
| B1 | create orderpoint | Trufle, Półka 1, min 2, max 6, trasa K2, trigger manual; odczyt `qty_to_order` (oczekiwane 5) |
| B2 | action_replenish | powstaje 1 przesunięcie 5 szt. z Zaplecza |
| B3 | action_replenish ponownie (NEG-1) | oczekiwane: brak drugiego przesunięcia, `qty_to_order` = 0 |
| B4 | validate przesunięcia | oczekiwane półka 6 / zaplecze 3; TRU-P04-BQ w kwarantannie bez zmian (NEG-2) |

### Wariant C — 0/0, przekazanie do zakupów (MAG-011)

| # | Operacja | Dane |
|---|---|---|
| C1 | create orderpoint + action_replenish (NEG-3) | Z3-TEST P04-C, Półka 1, min 2, max 6, trasa K2 — sprawdzamy, **czy powstaje fikcyjny transfer z pustego zaplecza** |
| C1x | anulowanie (tylko jeśli C1 utworzy transfer) | action_cancel tego transferu, po zapisaniu dowodu |
| C2 | create product.supplierinfo + orderpoint + action_replenish | dostawca Dostawca testowy Z3; orderpoint Zapasy (34), min 2, max 6, trasa Buy → **szkic RFQ** dla Z2 (bez potwierdzania) |

Przed każdym krokiem i po nim: odczyt stanów wg produkt/partia/lokalizacja i dokumentów; zapis ID w `lab_3-P04-wyniki.md`.
