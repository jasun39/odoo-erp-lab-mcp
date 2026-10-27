# MAG-P01 — plan prób (PROPOZYCJA, niezatwierdzona)

Status: **propozycja Claude**, 2026-10-26. Nie jest uzgodnieniem prowadzącego ani wynikiem próby.
Decyzje użytkownika (2026-10-26): zaczynamy od strumienia A (P01/P04); „zaplecze” = lokalizacja
`WH/Input/Zapasy/Zaplecze` (id 41); uzgodnień z prowadzącym brak → poniższe zasady to propozycje.

## Propozycje zasad (do uzgodnienia z prowadzącym / Z1, Z2, Z4)

| Kanał | Proponowane źródło | Uzasadnienie |
|---|---|---|
| Przyjęcie (Z2) | nowa lokalizacja `WH/Input/Przyjęcie` (poza Zapasy) | towar przed rozłożeniem nie jest dostępny |
| Sprzedaż / wydanie (Z1) | `WH/Input/Zapasy` z podlokalizacjami (Półka 1, Zaplecze) | domyślne źródło typu „Zlecenia dostawy” (35) — bez zmian |
| Produkcja / zestawy (Z4) | `WH/Input/Zapasy` | domyślne źródło typu „Produkcja” (44) — bez zmian |
| Kwarantanna | `WH/Input/Kwarantanna` (42) poza Zapasy | nie wchodzi w żadne domyślne źródło |

Globalnych ustawień typów operacji **nie zmieniamy** (dotyczą innych zespołów) — w próbach lokalizacje
podajemy jawnie na dokumentach.

## Zapisy w Odoo (do zgody)

| # | Operacja | Model | Dane |
|---|---|---|---|
| Z1 | create | stock.location | `Przyjęcie`, rodzic WH/Input (33), usage internal |
| Z2 | create (jeśli brak) | res.partner | `Dostawca testowy Z3`, firma |
| Z3 | create + validate | stock.picking (typ 34) | Dostawca testowy Z3 → Przyjęcie; Danusia: partia `DAN-P01-A` 3 szt., partia `DAN-P01-B` 2 szt.; daty z produktu; `ref` partii = nr partii dostawcy |
| Z4 | create + validate | stock.picking (typ 40) | Przyjęcie → Półka 1: DAN-P01-A 1; Przyjęcie → Zaplecze: DAN-P01-A 2; DAN-P01-B 2 → Zaplecze |
| Z5 | create + validate (próba NEG-1) | stock.picking (typ 34) | Danusia 1 szt. **bez partii** — oczekiwana blokada walidacji |
| Z6 | create + validate (próba NEG-2) | stock.picking (typ 34) | Danusia 1 szt., partia `DAN-P01-NODATE`, **bez daty ważności** — rejestrujemy zachowanie |

Odczyty (bez zgody): stany wg produkt/partia/lokalizacja przed i po (rozwinięcie 3 = 1 + 2).
NEG-3 (tylko odczyt, istniejące dane): KAKAO ma śledzenie partiami, a 20 kg stanu bez partii.

## Wymagania techniczne

Walidacja dokumentów to metoda biznesowa (`button_validate`) → w `.env`:
`ODOO_YOLO=true` i `ODOO_MCP_ENABLE_METHOD_CALLS=true`, potem nowa sesja Claude Code.
