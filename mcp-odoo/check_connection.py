"""Sprawdzenie połączenia z Odoo — wyłącznie odczyt, bez wypisywania sekretów.

Użycie (z katalogu głównego projektu):
    mcp-odoo/.venv/bin/python mcp-odoo/check_connection.py            # z .env
    mcp-odoo/.venv/bin/python mcp-odoo/check_connection.py --url URL  # tylko publiczne endpointy

Kroki:
 1. wersja serwera (publiczne: /web/webclient/version_info, XML-RPC common.version),
 2. lista baz (publiczna, jeśli nie jest wyłączona),
 3. logowanie (XML-RPC authenticate) i odczyt własnego użytkownika,
 4. dla Odoo 19+: test JSON-2 (res.users/context_get) — wystarczy klucz API.
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
import xmlrpc.client
from pathlib import Path

from dotenv import load_dotenv

TIMEOUT = 15


def post_json(url, payload, headers=None):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        url, data=data, headers={"Content-Type": "application/json", **(headers or {})}
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return resp.status, json.loads(resp.read().decode() or "null")


def step(name, fn):
    try:
        result = fn()
        print(f"[OK]   {name}: {result}")
        return result
    except Exception as exc:  # raport, nie przerywamy pozostałych kroków
        msg = str(exc).splitlines()[0][:200]
        print(f"[FAIL] {name}: {type(exc).__name__}: {msg}")
        return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="tylko publiczne sprawdzenia dla podanego adresu")
    args = parser.parse_args()

    if args.url:
        url, db, user, secret = args.url.rstrip("/"), None, None, None
    else:
        env = Path(__file__).resolve().parent.parent / ".env"
        if not env.exists():
            sys.exit("Brak pliku .env — utwórz go: cp .env.example .env")
        load_dotenv(env)
        url = (os.getenv("ODOO_URL") or "").rstrip("/")
        db = os.getenv("ODOO_DB") or None
        user = os.getenv("ODOO_USER") or None
        secret = os.getenv("ODOO_API_KEY") or os.getenv("ODOO_PASSWORD") or None
        if not url:
            sys.exit("ODOO_URL nie jest ustawione w .env")
        print(f"ODOO_URL={url}  ODOO_DB={db or '(puste)'}  ODOO_USER={user or '(puste)'}  "
              f"sekret={'ustawiony' if secret else 'BRAK'}")

    if not url.startswith(("http://", "https://")):
        sys.exit(f"Nieprawidłowy adres: {url!r} — podaj pełny adres, np. https://firma.odoo.com")

    common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common", allow_none=True)

    step("version_info (JSON)",
         lambda: post_json(f"{url}/web/webclient/version_info",
                           {"jsonrpc": "2.0", "method": "call", "params": {}})[1].get("result"))
    version = step("common.version (XML-RPC)", common.version)
    try:
        dbs = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/db").list()
        print(f"[OK]   lista baz (db.list): {dbs}")
    except xmlrpc.client.Fault:
        dbs = None
        print("[INFO] lista baz (db.list): wyłączona na serwerze — ODOO_DB trzeba podać ręcznie")

    if args.url:
        return
    if not db and isinstance(dbs, list) and len(dbs) == 1:
        db = dbs[0]
        print(f"       ODOO_DB puste — używam jedynej bazy z listy: {db}")

    # JSON-2 (Odoo 19+): wystarczy klucz API, login nie jest potrzebny.
    api_key = os.getenv("ODOO_API_KEY")
    major = (version or {}).get("server_version_info", [0])[0]
    if isinstance(major, int) and major >= 19:
        if api_key:
            headers = {"Authorization": f"bearer {api_key}"}
            if db:
                headers["X-Odoo-Database"] = db
            step("JSON-2 res.users/context_get",
                 lambda: post_json(f"{url}/json/2/res.users/context_get", {}, headers)[1])
        else:
            print("[SKIP] JSON-2: brak ODOO_API_KEY w .env")

    # XML-RPC: wymaga bazy, loginu i sekretu.
    missing = [n for n, v in (("ODOO_DB", db), ("ODOO_USER", user), ("sekret", secret)) if not v]
    if missing:
        print(f"[SKIP] logowanie XML-RPC: brak {', '.join(missing)} w .env")
        return

    def login():
        uid = common.authenticate(db, user, secret, {})
        if not uid:
            raise RuntimeError("odmowa logowania (uid=False) — sprawdź ODOO_USER")
        return uid

    uid = step("authenticate (XML-RPC)", login)
    if uid:
        models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object", allow_none=True)
        step("odczyt własnego użytkownika",
             lambda: models.execute_kw(db, uid, secret, "res.users", "read", [[uid]],
                                       {"fields": ["name", "login", "lang", "company_id"]}))

if __name__ == "__main__":
    main()
