"""Wywołanie narzędzi serwera MCP odoo z linii poleceń (gdy narzędzia nie są wczytane w sesji).

Użycie (z katalogu głównego projektu):
    mcp-odoo/.venv/bin/python mcp-odoo/mcp_call.py calls.json

calls.json — lista wywołań: [{"label": "...", "tool": "search_records", "args": {...}}, ...]
Wszystkie wywołania idą przez jedno połączenie z serwerem. Nie wypisuje sekretów.
"""

import asyncio
import json
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

RUN = Path(__file__).resolve().parent / "run.sh"


async def main(calls):
    params = StdioServerParameters(command=str(RUN), args=[])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            for call in calls:
                result = await session.call_tool(call["tool"], call.get("args", {}))
                text = "\n".join(c.text for c in result.content if hasattr(c, "text"))
                status = "FAIL" if result.is_error else "OK"
                print(f"===== [{status}] {call.get('label', call['tool'])}\n{text}\n")


if __name__ == "__main__":
    asyncio.run(main(json.loads(Path(sys.argv[1]).read_text())))
