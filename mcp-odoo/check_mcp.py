"""Test serwera MCP tak, jak uruchamia go Claude Code (stdio przez run.sh) — tylko odczyt.

Użycie (z katalogu głównego projektu):
    mcp-odoo/.venv/bin/python mcp-odoo/check_mcp.py

Startuje serwer, wypisuje listę narzędzi i odczytuje własnego użytkownika
(res.users, pola name/login) narzędziem do wyszukiwania. Nie wypisuje sekretów.
"""

import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

RUN = Path(__file__).resolve().parent / "run.sh"


async def main():
    params = StdioServerParameters(command=str(RUN), args=[])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            info = await session.initialize()
            print(f"[OK]   serwer: {info.server_info.name} {info.server_info.version}")
            tools = (await session.list_tools()).tools
            print(f"[OK]   narzędzia ({len(tools)}): {', '.join(t.name for t in tools)}")

            search = next((t for t in tools if t.name == "search_records"), None)
            if not search:
                sys.exit("[FAIL] brak narzędzia search_records")
            result = await session.call_tool(
                "search_records",
                {"model": "res.users", "domain": [["share", "=", False]],
                 "fields": ["name", "login"], "limit": 20},
            )
            text = "\n".join(c.text for c in result.content if hasattr(c, "text"))
            status = "FAIL" if result.is_error else "OK"
            print(f"[{status}] search_records res.users:\n{text[:2000]}")


if __name__ == "__main__":
    asyncio.run(main())
