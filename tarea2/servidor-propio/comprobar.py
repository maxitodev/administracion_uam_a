"""Cliente MCP mínimo para comprobar los dos servidores sin abrir Claude Desktop.

Hace lo mismo que el cliente real: lanza el servidor como subproceso, negocia
la versión del protocolo, pide el catálogo de herramientas (tools/list) y
llama algunas (tools/call). Así se ve que el servidor funciona antes de
conectarlo al cliente.

    python comprobar.py archivos <carpeta autorizada>
    python comprobar.py propio <raíz del repositorio>
"""

from __future__ import annotations

import asyncio
import shutil
import sys
from pathlib import Path

from mcp import Client, StdioServerParameters

AQUI = Path(__file__).resolve().parent


def mostrar(titulo: str, resultado) -> None:
    texto = "\n".join(c.text for c in resultado.content if getattr(c, "text", None))
    estado = "ERROR" if resultado.is_error else "ok"
    print(f"\n>>> {titulo} [{estado}]")
    print(texto)


async def probar(parametros: StdioServerParameters, llamadas: list[tuple[str, str, dict]]) -> None:
    async with Client(parametros) as cliente:
        info = cliente.server_info
        print(f"Servidor: {info.name} {info.version} · protocolo {cliente.protocol_version}")
        herramientas = (await cliente.list_tools()).tools
        print(f"\ntools/list devolvió {len(herramientas)} herramientas:")
        for h in herramientas:
            solo_lectura = h.annotations and h.annotations.read_only_hint
            marca = " (sólo lectura)" if solo_lectura else ""
            primera = (h.description or "").strip().splitlines()[0]
            print(f"  - {h.name}{marca}: {primera}")
        for titulo, nombre, argumentos in llamadas:
            mostrar(titulo, await cliente.call_tool(nombre, argumentos))


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")  # la consola de Windows no es UTF-8 por omisión
    if len(sys.argv) != 3 or sys.argv[1] not in {"archivos", "propio"}:
        sys.exit(__doc__)
    modo, carpeta = sys.argv[1], str(Path(sys.argv[2]).resolve())

    if modo == "archivos":
        # El mismo comando que pone config/claude_desktop_config.json.
        parametros = StdioServerParameters(
            command=shutil.which("npx") or "npx",
            args=["-y", "@modelcontextprotocol/server-filesystem@1.0.0", carpeta],
        )
        afuera = str(Path(carpeta).parent / "README.md")
        llamadas = [
            ("list_allowed_directories", "list_allowed_directories", {}),
            ("list_directory", "list_directory", {"path": carpeta}),
            ("leer un archivo fuera de la carpeta", "read_text_file", {"path": afuera}),
            ("salir con ../", "list_directory", {"path": str(Path(carpeta) / "..")}),
        ]
    else:
        parametros = StdioServerParameters(
            command=sys.executable,
            args=[str(AQUI / "servidor.py"), carpeta],
        )
        llamadas = [
            ("revisar_entrega", "revisar_entrega", {"tarea": "tarea2"}),
            ("buscar_credenciales", "buscar_credenciales", {"subcarpeta": "."}),
            ("dias_para_entrega", "dias_para_entrega",
             {"fecha_limite": "2026-10-17 23:59", "fecha_entrega": "2026-10-19 10:00"}),
            ("salir de la raíz", "buscar_credenciales", {"subcarpeta": ".."}),
        ]
    asyncio.run(probar(parametros, llamadas))


if __name__ == "__main__":
    main()
