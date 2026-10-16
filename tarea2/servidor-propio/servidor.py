"""Servidor MCP «entregas-apsw»: revisa las entregas de este repositorio.

Expone tres herramientas de sólo lectura y un recurso:

- revisar_entrega(tarea): compara la carpeta de una tarea con la estructura
  que pide el enunciado y dice qué falta.
- buscar_credenciales(subcarpeta): busca cosas con forma de llave, token o
  contraseña antes de hacer push.
- dias_para_entrega(fecha_limite, fecha_entrega): cuánto falta o, si ya pasó,
  cuántos días de retraso y qué descuento aplica.
- recurso apsw://reglas-entrega: las reglas de entrega del curso.

Se ejecuta por stdio; el cliente (Claude Desktop) lo lanza como subproceso:

    python servidor.py <raíz del repositorio>

Igual que el servidor de sistema de archivos, sólo trabaja dentro de la
carpeta que recibe como argumento: cualquier ruta que resuelva fuera de ella
se rechaza.
"""

from __future__ import annotations

import re
import sys
from datetime import datetime
from pathlib import Path

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from mcp.types import ToolAnnotations

if len(sys.argv) != 2:
    # stdout es el canal de JSON-RPC: los mensajes para humanos van a stderr.
    print("uso: python servidor.py <raíz del repositorio>", file=sys.stderr)
    sys.exit(2)

RAIZ = Path(sys.argv[1]).resolve(strict=True)

# Lo que pide cada enunciado. La clave es la carpeta y el valor, lo que debe
# contener. "*.md" quiere decir «al menos un archivo con esa extensión».
ESTRUCTURA = {
    "tarea1": {
        "README.md": "documento de entrega",
        "img/*.png": "capturas",
        "postgres/compose.yaml": "stack de PostgreSQL",
        "mysql/compose.yaml": "stack de MySQL",
    },
    "tarea2": {
        "README.md": "documento principal",
        "docs/*.md": "la investigación, en archivos .md",
        "config/*.json": "la configuración de MCP, sin credenciales",
        "img/*.png": "capturas de la instalación y de MCP",
        "presentacion/*": "las diapositivas de la exposición",
        "servidor-propio/servidor.py": "opcional: servidor MCP propio",
    },
}

# Formas típicas de una credencial. No es un escáner completo: sirve para
# detectar el descuido de subir un token pegado en un archivo de configuración.
PATRONES = {
    "token de GitHub": re.compile(r"\b(ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{36}\b|\bgithub_pat_[A-Za-z0-9_]{60,}"),
    "llave de Anthropic": re.compile(r"\bsk-ant-[A-Za-z0-9_\-]{20,}"),
    "llave de OpenAI": re.compile(r"\bsk-(proj-)?[A-Za-z0-9]{20,}"),
    "llave de Google": re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b"),
    "llave de AWS": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "llave privada": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    # Una variable de configuración (PASSWORD=…, "api_key": "…") con un valor de 8 o más caracteres.
    "token o contraseña asignados": re.compile(
        r"(?i)(password|passwd|secret|api[_-]?key|token)['\"]?\s*[:=]\s*['\"]?[\w\-./+!@$%^&*]{8,}"
    ),
}
OMITIR = {".git", ".venv", "node_modules", "__pycache__", "build", ".dart_tool", ".gradle"}
TEXTO = {".md", ".txt", ".json", ".yaml", ".yml", ".toml", ".env", ".example", ".py", ".js", ".ts",
         ".sh", ".sql", ".kt", ".kts", ".dart", ".xml", ".properties", ".gitignore", ""}

REGLAS = """\
Reglas de entrega de la UEA Administración de Proyectos de Software (1151055):
- Todo se entrega en GitHub; en la plataforma del curso sólo se registra la liga.
- La documentación va en Markdown (README.md); no se aceptan Word ni PDF.
- El historial es evidencia: trabajo incremental, no una sola confirmación al final.
- Ninguna credencial, llave ni token en el repositorio.
- El uso de inteligencia artificial se declara en el README; lo no declarado se anula.
- Entrega tardía: 10 % menos por día, con demora máxima de diez días.
"""

mcp = MCPServer(
    name="entregas-apsw",
    instructions=(
        "Herramientas para revisar las tareas del repositorio de la UEA 1151055. "
        "Todas son de sólo lectura y trabajan dentro de la raíz del repositorio."
    ),
    version="1.0.0",
)

SOLO_LECTURA = ToolAnnotations(read_only_hint=True, destructive_hint=False, open_world_hint=False)


def dentro_de_raiz(relativa: str) -> Path:
    """Resuelve una ruta relativa a la raíz y rechaza la que se salga de ella."""
    ruta = (RAIZ / relativa).resolve()
    if ruta != RAIZ and RAIZ not in ruta.parents:
        # ToolError llega al modelo como resultado con isError: lo lee y se lo explica al usuario.
        raise ToolError(f"Acceso denegado: «{relativa}» queda fuera de {RAIZ}")
    return ruta


@mcp.tool(annotations=SOLO_LECTURA)
def revisar_entrega(tarea: str) -> str:
    """Revisa que la carpeta de una tarea (por ejemplo «tarea2») tenga lo que pide el enunciado.

    Devuelve cada requisito marcado como presente o faltante y cuántos archivos lo cumplen.
    """
    tarea = tarea.strip().lower().replace(" ", "")
    if tarea not in ESTRUCTURA:
        return f"No conozco «{tarea}». Tareas registradas: {', '.join(ESTRUCTURA)}."
    carpeta = dentro_de_raiz(tarea)
    if not carpeta.is_dir():
        return f"La carpeta {tarea}/ todavía no existe."

    lineas, faltan = [f"Revisión de {tarea}/:"], 0
    for patron, que_es in ESTRUCTURA[tarea].items():
        encontrados = [p for p in carpeta.glob(patron) if p.is_file()]
        if encontrados:
            lineas.append(f"  [ok] {patron} ({len(encontrados)}): {que_es}")
        else:
            faltan += 1
            lineas.append(f"  [falta] {patron}: {que_es}")
    lineas.append("Completa." if faltan == 0 else f"Faltan {faltan} requisito(s).")
    return "\n".join(lineas)


@mcp.tool(annotations=SOLO_LECTURA)
def buscar_credenciales(subcarpeta: str = ".") -> str:
    """Busca en los archivos de texto del repositorio cosas con forma de token, llave o contraseña.

    Sirve para revisar antes de hacer push. `subcarpeta` es relativa a la raíz del repositorio.
    Muestra sólo el principio de cada coincidencia, nunca el valor completo.
    """
    base = dentro_de_raiz(subcarpeta)
    hallazgos, revisados = [], 0
    for archivo in sorted(base.rglob("*")):
        if not archivo.is_file() or OMITIR.intersection(archivo.relative_to(RAIZ).parts):
            continue
        if archivo.suffix.lower() not in TEXTO or archivo.stat().st_size > 1_000_000:
            continue
        revisados += 1
        texto = archivo.read_text(encoding="utf-8", errors="ignore")
        for numero, linea in enumerate(texto.splitlines(), start=1):
            for tipo, patron in PATRONES.items():
                if m := patron.search(linea):
                    muestra = m.group(0)[:8] + "…"
                    hallazgos.append(f"  {archivo.relative_to(RAIZ).as_posix()}:{numero}  {tipo}  ({muestra})")
    if not hallazgos:
        return f"Sin coincidencias en {revisados} archivos de texto bajo {subcarpeta}."
    return f"{len(hallazgos)} posible(s) credencial(es) en {revisados} archivos:\n" + "\n".join(hallazgos)


@mcp.tool(annotations=SOLO_LECTURA)
def dias_para_entrega(fecha_limite: str, fecha_entrega: str = "") -> str:
    """Calcula cuánto falta para la fecha límite o, si ya pasó, el retraso y su descuento.

    Las fechas van como «AAAA-MM-DD HH:MM»; si falta la hora de la fecha límite se toma 23:59.
    Si `fecha_entrega` va vacía se usa la hora actual. El curso descuenta 10 % por día de
    retraso (cada día iniciado cuenta) y no acepta más de diez días.
    """

    def leer(texto: str, hora_por_omision: str) -> datetime:
        texto = texto.strip()
        if len(texto) == 10:
            texto += " " + hora_por_omision
        return datetime.strptime(texto, "%Y-%m-%d %H:%M")

    limite = leer(fecha_limite, "23:59")
    entrega = leer(fecha_entrega, "00:00") if fecha_entrega.strip() else datetime.now().replace(second=0, microsecond=0)
    diferencia = limite - entrega
    if diferencia.total_seconds() >= 0:
        horas = int(diferencia.total_seconds() // 3600)
        return f"A tiempo: faltan {horas // 24} día(s) y {horas % 24} hora(s) para {limite:%Y-%m-%d %H:%M}."

    retraso = entrega - limite
    dias = retraso.days + (1 if retraso.seconds or retraso.microseconds else 0)
    if dias > 10:
        return f"Tarde por {dias} días: pasa la demora máxima de diez días y ya no se acepta."
    return f"Tarde por {dias} día(s): la calificación se reduce {dias * 10} %."


@mcp.resource("apsw://reglas-entrega", name="reglas-entrega", mime_type="text/plain")
def reglas_entrega() -> str:
    """Las reglas de entrega del curso, para que el modelo las consulte."""
    return REGLAS


if __name__ == "__main__":
    mcp.run("stdio")
