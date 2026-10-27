# Laboratoria Odoo — Claude Code + MCP

Projekt do wykonywania zadań laboratoryjnych w Odoo przez Claude Code (CLI / VS Code / aplikacja
desktop) z serwerem MCP [`mcp-server-odoo`](https://github.com/ivnvxd/mcp-server-odoo) (MPL-2.0).

## Wymagania

| Narzędzie | Uwagi |
|---|---|
| Python ≥ 3.10 | wymagany przez `mcp-server-odoo` (np. macOS: systemowy 3.9 nie wystarcza — `brew install python@3.12`) |
| venv serwera MCP | `mcp-odoo/.venv` — tworzony lokalnie, poza gitem |
| `claude` CLI | opcjonalnie — do pracy w terminalu / `claude mcp list` |

## Instalacja (po sklonowaniu)

Utwórz venv z dowolnym Pythonem ≥ 3.10 (podmień `python3` na np. `python3.12`, jeśli domyślny jest starszy):

```bash
python3 -m venv mcp-odoo/.venv && mcp-odoo/.venv/bin/pip install mcp-server-odoo
```

Ścieżki w projekcie są względne: `.mcp.json` uruchamia `${CLAUDE_PROJECT_DIR:-.}/mcp-odoo/run.sh`
(Claude Code ustawia `CLAUDE_PROJECT_DIR` na katalog projektu), a `run.sh` przechodzi do katalogu projektu
i uruchamia serwer z `mcp-odoo/.venv`. Projekt działa więc z dowolnego miejsca na dysku.

## Konfiguracja

1. Utwórz plik z kluczem API na podstawie szablonu:

   ```bash
   cp .env.example .env
   ```

2. Uzupełnij `.env` w edytorze:
   `ODOO_URL`, `ODOO_DB`, `ODOO_USER`, `ODOO_API_KEY`.
3. Klucz API w Odoo: avatar w prawym górnym rogu → **Mój profil / Preferencje** →
   karta **Bezpieczeństwo konta** → **Nowy klucz API** → podaj opis (np. `claude-mcp-lab`) i czas
   ważności → potwierdź hasłem → skopiuj klucz (wyświetla się tylko raz) do `.env`.
   W Odoo 19 trzeba podać czas ważności klucza.
4. Tryb dostępu (`ODOO_YOLO` w `.env`): zacznij od `read`; na czas zadań z zapisami ustaw `true`.
   Metody biznesowe (np. `action_confirm`) wymagają dodatkowo `ODOO_MCP_ENABLE_METHOD_CALLS=true`.


## Sprawdzenie połączenia

1. Bez logowania (tylko publiczne endpointy):

   ```bash
   mcp-odoo/.venv/bin/python mcp-odoo/check_connection.py --url https://twoja-instancja.odoo.com
   ```

2. Z danymi z `.env` (tylko odczyt, sekrety nie są wypisywane):

   ```bash
   mcp-odoo/.venv/bin/python mcp-odoo/check_connection.py
   ```

3. Serwer MCP tak, jak uruchamia go Claude Code (stdio, tylko odczyt):

   ```bash
   mcp-odoo/.venv/bin/python mcp-odoo/check_mcp.py
   ```

4. Serwer MCP w Claude Code: przy pierwszym otwarciu projektu zatwierdź serwer `odoo` z `.mcp.json`,
   potem w sesji `/mcp` (status) albo w terminalu:

   ```bash
   claude mcp list
   ```

## Ograniczenia hostingu

- **Odoo Online**: zewnętrzne API (XML-RPC / JSON-2) jest dostępne tylko w planie **Custom**
  (oraz w okresie próbnym/edukacyjnym — do sprawdzenia). W planach One App Free i Standard
  połączenie przez MCP nie zadziała.
- Tryb standardowy serwera (bez `ODOO_YOLO`) wymaga modułu `mcp_server` w Odoo — na Odoo Online
  nie da się go zainstalować, dlatego używamy trybu `ODOO_YOLO` (uprawnienia = uprawnienia użytkownika
  Odoo, a zgody na zapisy egzekwuje `CLAUDE.md`).

## Struktura

```
CLAUDE.md               instrukcje dla Claude Code (wczytywane automatycznie)
STATUS.md               stan prac i kolejny krok
README.md               ten plik
.mcp.json               rejestracja serwera MCP "odoo"
.claude/settings.json   reguły uprawnień (blokada odczytu .env)
.env.example            szablon zmiennych (bez wartości)
materialy/              polecenia labów, SIWZ, ustalenia
mcp-odoo/run.sh         start serwera MCP z katalogu projektu
mcp-odoo/check_connection.py  test połączenia (tylko odczyt)
```
