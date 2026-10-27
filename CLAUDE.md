# Projekt: laboratoria Odoo (ERP, semestr 9)

Folder służy do wykonywania zadań laboratoryjnych w Odoo przez serwer MCP (`odoo`)
oraz do dokumentowania wyników.

## Zasady ogólne

- Odpowiadaj po polsku.
- Na początku pracy przeczytaj `STATUS.md` oraz materiały w `materialy/` dotyczące aktualnego zadania.
- Po każdym istotnym etapie aktualizuj `STATUS.md`: zapisuj konkrety potrzebne do wznowienia pracy
  w nowej sesji (co zrobiono, ID rekordów, numery dokumentów, co zostało, kolejny krok).
- Zadania laboratoryjne wykonuj dopiero po otrzymaniu konkretnego polecenia.

## Praca z Odoo

- Przed operacją sprawdź rzeczywisty stan w Odoo, a po operacji sprawdź jej wynik.
- Przed utworzeniem rekordu sprawdź, czy już nie istnieje (wyszukaj po nazwie/kodzie/kluczowych polach).
- Nie uznawaj operacji za wykonaną bez potwierdzenia z systemu (odczyt rekordu po zapisie).
- Przed każdym zapisem w Odoo (create, write, unlink, wywołanie metody biznesowej, np.
  `action_confirm`, `button_validate`, `action_post`) pokaż, co dokładnie zostanie zmienione
  (model, ID, pola: wartość przed → po) i wykonaj to dopiero po mojej zgodzie,
  chyba że polecenie wprost na to pozwala.
- Dokumentuj istotne ID rekordów, numery dokumentów oraz wartości przed operacją i po niej.

## Rzetelność

- Rozróżniaj wyraźnie: **propozycje** (Twoje), **uzgodnienia prowadzącego** (z materiałów lub ode mnie)
  i **wyniki faktycznie wykonanych prób** (potwierdzone odczytem z Odoo).
- Nie wymyślaj brakujących zasad biznesowych, potwierdzeń ani wyników. Jeśli czegoś brakuje — zapytaj
  albo zapisz jako otwarte pytanie w `STATUS.md`.

## Sekrety

- Nie czytaj pliku `.env` (blokuje to też `.claude/settings.json`). Serwer MCP wczytuje go sam.
- Nie zapisuj sekretów (haseł, kluczy API) w dokumentacji i nie wyświetlaj ich w odpowiedziach.
- Do sprawdzenia konfiguracji używaj `mcp-odoo/check_connection.py`, który nie wypisuje sekretów.

## Struktura

- `STATUS.md` — stan prac, sprawdzenia, blokady, kolejny krok.
- `materialy/` — polecenia labów, SIWZ, ustalenia z prowadzącym.
- `mcp-odoo/` — uruchamianie serwera MCP (`run.sh`), venv, skrypt sprawdzający połączenie.
- `.mcp.json` — rejestracja serwera MCP `odoo` dla Claude Code (zakres projektu).
