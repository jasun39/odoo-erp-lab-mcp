#!/bin/sh
# Uruchamia mcp-server-odoo z katalogu głównego projektu, żeby serwer
# znalazł plik .env (szuka go w bieżącym katalogu), niezależnie od tego,
# z jakiego katalogu Claude Code startuje proces.
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR/.."
exec "$DIR/.venv/bin/mcp-server-odoo" "$@"
