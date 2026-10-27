# Lab 3 (Z3 — Magazyn) — stan Odoo przed pracą

Odczyt przez MCP (`mcp-server-odoo`, JSON-2, tryb `ODOO_YOLO=read`), 2026-10-26 ok. 15:45 (Europe/Warsaw).
Wyłącznie **fakty odczytane z systemu**; interpretacje oznaczone jako _obserwacja_.

Polecenie: `materialy/lab_3.pdf` (tekst: `materialy/lab_3.txt`).

## Moduły zainstalowane

stock, stock_barcode, product_expiry, quality (Quality Base), mrp, purchase, purchase_stock,
sale_management, sale_stock, account. **Brak:** point_of_sale, quality_control, web_studio.

## Uprawnienia użytkownika (id 7)

Inventory / Administrator, Quality / Administrator, Sales, Purchase, Manufacturing, Accounting — Administrator.

## Magazyn i lokalizacje

| id | lokalizacja | typ | strategia usuwania | uwagi |
|---|---|---|---|---|
| — | magazyn id 4 „Przyjęcia”, kod `WH/Input` | — | — | przyjęcie 1 krok, wydanie 1 krok |
| 34 | WH/Input/Zapasy | internal | FIFO | lot_stock_id magazynu, kod kreskowy WH/INPUTSTOCK |
| 43 | WH/Input/Zapasy/Półka 1 | internal | FIFO | |
| 41 | WH/Input/Zapasy/Zaplecze | internal | — | pusta |
| 42 | WH/Input/Kwarantanna | internal | — | **poza** Zapasy |

Kategoria `Goods` (id 1): strategia **FEFO**. Strategia lokalizacji (FIFO na 34/43) ma pierwszeństwo
przed kategorią — _obserwacja, do sprawdzenia próbą w MAG-P02_.

## Typy operacji

| id | nazwa | kod | domyślnie z → do |
|---|---|---|---|
| 34 | Przyjęcia | incoming | Vendors → Zapasy |
| 40 | Przesunięcia wewnętrzne | internal | Zapasy → Zapasy |
| 35 | Zlecenia dostawy | outgoing | Zapasy → Customers |
| 44 | Produkcja | mrp_operation | Zapasy → Zapasy |
| 45 | Zwroty klientów (RET) | incoming | Customers → **Kwarantanna** |

## Produkty (śledzone partiami, z datami)

| id | produkt | jm | expiration / use / removal / alert (dni) |
|---|---|---|---|
| 4 | Danusia | Units | 180 / 150 / 30 / 45 |
| 1 | KAKAO | kg | 100 / 3 / 6 / 15 |

Brak w systemie: Tiki-Taki, Trufle (wymienione w poleceniu).

## Partie i stany (ilości > 0)

| partia | produkt | lokalizacja | ilość |
|---|---|---|---|
| 0000001 (id 1) | Danusia | Zapasy | 3 |
| 0000001 | Danusia | Półka 1 | 8 |
| 0000002 (id 2) | Danusia | Półka 1 | 13 |
| — (bez partii) | KAKAO | Zapasy | 5 |
| — (bez partii) | KAKAO | Półka 1 | 15 |

Daty partii 0000001 / 0000002 (UTC): use_date 2026-11-25, alert 2027-03-10, removal 2027-03-25, expiration 2027-04-24.
_Obserwacja:_ KAKAO ma śledzenie partiami, a stan bez partii (20 kg) — kandydat na MAG-P01-NEG.

## Dokumenty (13)

IN/00001–00008 (00004 draft, 00006 cancel), INT/00001–00004, OUT/00001 (S00002, 3 szt. Danusia 0000002).
Zwrot `WH/Input/IN/00008` (origin „Zwrot WH/Input/OUT/00001”, 1 szt. 0000002) przyjęty typem „Przyjęcia”
do **WH/Input/Zapasy**, nie do Kwarantanny — _obserwacja, istotna dla MAG-P06_.

## Brak

Reguły min/max (orderpoint): 0. Alerty i punkty kontroli jakości: 0. Dostawcy (supplier_rank>0): 0.
