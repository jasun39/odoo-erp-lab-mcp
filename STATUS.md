# STATUS

_Ostatnia aktualizacja: 2026-10-26_

## Środowisko (sprawdzone 2026-10-26)

- macOS 26.4 (arm64).
- Python 3.10.13 (Homebrew) — użyty do venv `mcp-odoo/.venv`; systemowy Python 3.9.6 za stary dla MCP.
- `mcp-server-odoo` 0.9.0 zainstalowany w `mcp-odoo/.venv`; `mcp-odoo/run.sh --version` działa.
- Brak w PATH: `claude` CLI, uv, Node (Node i uv niepotrzebne).
- `.mcp.json` i `.claude/settings.json` — poprawny JSON.

## Odoo

- Adres instancji: `https://edu-agh-wawel-lab-2026-g1-z3.odoo.com` (Odoo Online, subdomena odoo.com).
- Wersja (sprawdzone 2026-10-26, publiczne endpointy): **20.0+e** (Enterprise), XML-RPC `common.version` odpowiada.
- Lista baz (`db.list`): **wyłączona** (Fault). Baza: `edu-agh-wawel-lab-2026-g1-z3` (potwierdzone JSON-2).
- Użytkownik API: `res.users` id **7**, login `mjuchacz@student.agh.edu.pl`, lang `pl_PL`, tz `Europe/Warsaw`.
- JSON-2 (`/json/2`, klucz API): **działa** (`context_get` → uid 7).
- XML-RPC `authenticate`: **odmowa** — login w `.env` (`...@student.agh.edu.com`) różni się od
  loginu w Odoo (`...@student.agh.edu.pl`). Serwer MCP używa JSON-2, więc nie blokuje to pracy.
- Serwer MCP (`check_mcp.py`, stdio przez `run.sh`, 2026-10-26): start OK, „connected over JSON-2”,
  16 narzędzi, odczyt `search_records` na `res.users` OK. Tryb `ODOO_YOLO=read`.
  Narzędzia zapisu są widoczne na liście także w trybie `read` — blokada zapisu w tym trybie
  **niesprawdzona** (nie testowano, by nie robić zmian).
- Rejestracja w Claude Code (`.mcp.json`) — zatwierdzenie serwera w nowej sesji i `/mcp`: **niesprawdzone**.

## Blokady / do zrobienia przez użytkownika

- 2026-10-26: klucz API był wpisany do `.env.example` (widoczny w kontekście Claude) — unieważnić
  w Odoo, wygenerować nowy, wpisać tylko do `.env`; wyczyścić `.env.example`. Stan: niepotwierdzony.
- `ODOO_USER` w `.env` jest teraz puste (2026-10-26): JSON-2 i serwer MCP działają bez niego
  (sprawdzone); potrzebne tylko do XML-RPC — wtedy wpisać `mjuchacz@student.agh.edu.pl`.

## Kolejny krok

1. Wykonać punkty z „Blokady”, ponownie `check_connection.py` (oczekiwane: authenticate OK).
2. Nowa sesja Claude Code w tym folderze → zatwierdzić serwer `odoo` → `/mcp`.
3. Na czas zadań z zapisami: `ODOO_YOLO=true` (i ewentualnie `ODOO_MCP_ENABLE_METHOD_CALLS=true`).

## Laboratoria

### Lab 3 — Z3 Magazyn (MAG-P01…P08, CRIM-Z3) — rozpoczęte 2026-10-26

- Polecenie: `materialy/lab_3.pdf`, tekst `materialy/lab_3.txt`.
- Stan Odoo przed pracą (odczyt MCP): `materialy/lab_3-stan-poczatkowy.md`.
- Narzędzia MCP nie były wczytane w sesji, w której powstał `.mcp.json` — odczyty przez
  `mcp-odoo/mcp_call.py` (ten sam serwer MCP przez stdio). W nowej sesji powinny być dostępne natywnie.
- Decyzje użytkownika: strumień A (P01, potem P04); „zaplecze” = lokalizacja Zaplecze (41);
  uzgodnień z prowadzącym brak → zasady w planach to propozycje.
- **MAG-P01 wykonane 2026-10-26** (zgoda na Z1–Z6) — wyniki: `materialy/lab_3-P01-wyniki.md`.
  Rekordy: lokalizacja Przyjęcie 45, partner 18, IN/00009 (14), INT/00005 (15), IN/00010 (16, otwarty NEG-1),
  IN/00011 (17), partie DAN-P01-A 3 / DAN-P01-B 4 / DAN-P01-NODATE 5.
  POS zgodny (A = Półka 1: 1 + Zaplecze: 2); NEG-1 zablokowany; NEG-2 przyjęty z datami domyślnymi (luka);
  NEG-3 KAKAO 20 kg bez partii.
- IN/00010 (16) zostaje otwarty jako dowód NEG-1 — decyzja użytkownika 2026-10-26.
- **MAG-P04 wykonane 2026-10-26** (zgoda na K1–K2, A, B, C, C1x; osoba reagująca id 7) —
  wyniki: `materialy/lab_3-P04-wyniki.md`. Produkty 5 Tiki-Taki / 6 Trufle / 7 Z3-TEST P04-C; trasa 16, reguła 28;
  OP/00001 (1), OP/00002 (2), OP/00003 (3); dokumenty IN/00012–14, INT/00007, INT/00008, INT/00009 (cancel); RFQ P00002 (draft).
  A: 4/4 suma 8 ✓. B: 6/3, ponowienie bez duplikatu ✓. C: RFQ do Z2 ✓, **luka: fikcyjny transfer z pustego zaplecza**.
- OP/00002 (2) zostaje bez zmian jako dowód luki NEG-3 — decyzja użytkownika 2026-10-26.
  **Uwaga:** nie uruchamiać jego uzupełnienia — utworzy ponownie fikcyjny transfer z pustego Zaplecza.
- RFQ P00002 — przekazać Z2 (poza systemem; brak potwierdzenia).
- Strumień A zakończony (P01, P04).
- **Strumień B (P02, P03, P08) wykonany 2026-10-26** (zgoda na plan `materialy/lab_3-B-plan.md`; decyzja Z5,
  kody i warunki symulowane) — wyniki: `materialy/lab_3-B-wyniki.md`.
  Produkty 8 P02-FEFO, 9 P02-GR, 10 P03-Q, 11 zestaw P03 (BoM 1); alerty jakości 1 (wycofanie DAN-P01-A), 2 (naruszenie Trufle);
  dokumenty IN/00015–18, OUT/00002–03 (cancel), OUT/00004 (done — NEG-3), RET00001, INT/00010–11, MO/00002 (cancel);
  Trufle barcode `Z3-TRU-001`. DAN-P01-A: 3 szt. w Kwarantannie (zmienia stan z P01).
  Luki: brak daty = dopuszczona (P02-NEG-3); dostępność liczy kwarantannę (P03-NEG-1);
  **ręczne wydanie z kwarantanny możliwe (P03-NEG-3, krytyczna)**.
  Potwierdzenie ostrzeżenia o przeterminowanych partiach w IN/00017 — na polecenie użytkownika.
- **Strumień C — MAG-P05 wykonany 2026-10-26** (zgoda K1–K2, 5.0–5.5) — wyniki `materialy/lab_3-C-wyniki.md`.
  Produkty 12/13/14 (P05-A/B/C), klient 19; S00003; OUT/00005 (A1, 4 z 6 — otwarte), OUT/00006, OUT/00007,
  OUT/00008 (zaległość 4 — otwarta), OUT/00009. A POS ✓, B POS ✓; luki: użycie cudzej rezerwacji (A NEG-1),
  **stan ujemny P05C-1 −1 w Zapasach** (C NEG-2).
- 5.X — decyzja użytkownika 2026-10-26: OUT/00005 (A1, 4 z 6), OUT/00008 (zaległość 4) i stan −1 P05C-1 w Zapasach
  **zostają bez zmian jako dowody**. Stan −1 → do wykorzystania w **MAG-P07** (spis i zatwierdzona korekta).
- **MAG-P06 i MAG-P07 wykonane 2026-10-26** — polecenie użytkownika: Claude sam podejmuje decyzje (opisane w wynikach
  jako decyzje Claude). Wyniki: `materialy/lab_3-C-wyniki.md` (część P06/P07). Produkt 15 Z3-TEST P06-DAN (partie 20/21),
  S00004, OUT/00010, RET00002, alert 3, OUT/00011 (cancel), korekty spisu (ruchy 83, 84), duplikat IN/00023 + odwrócenie OUT/00012.
  P06 POS ✓ (7/1/8); P07 POS ✓ (−1 z przyczyną, bilans 7 = Odoo), duplikat wykryty i odwrócony. Stan −1 P05-C skorygowany do 0.
- **Podsumowanie dla zespołu:** `materialy/lab_3-podsumowanie-zespol.md` (wszystkie strumienie, luki L1–L8, otwarte dowody).
- Kolejny krok: CRIM-Z3; uzgodnienia z prowadzącym i partnerami; próby L1/L3/L4 na koncie zwykłego użytkownika.
- `.env`: ODOO_YOLO=true, ODOO_MCP_ENABLE_METHOD_CALLS=true (potwierdzone logiem serwera).
- Otwarte pytania (do użytkownika / prowadzącego):
  1. ~~Strumień~~ — ustalone: A.
  2. Uzgodnienia z polecenia („Uzgodnić…”): źródła sprzedaży/wydania/produkcji, znaczenie dat
     alertu/usunięcia/ważności i strefa, lokalizacja kontroli zwrotów — brak w materiałach.
  3. Czy „zaplecze” = lokalizacja `Zaplecze` (41, pusta), czy `Zapasy` (34, tam jest towar).
  4. Do zapisów potrzebne `ODOO_YOLO=true` w `.env` (teraz `read`).
