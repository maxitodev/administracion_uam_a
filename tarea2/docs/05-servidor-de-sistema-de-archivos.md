# 5. El servidor de sistema de archivos

[← Volver al README](../README.md#parte-2-mcp-investigación)

El servidor de sistema de archivos no es parte del protocolo. Es uno de los **servidores de referencia** que mantiene el proyecto MCP para mostrar cómo implementarlo, y se publica en npm como `@modelcontextprotocol/server-filesystem` (Model Context Protocol, 2026a). Usé la versión 1.0.0, del 11 de octubre de 2026 (Model Context Protocol, 2026b).

## Qué herramientas expone

`tools/list` devolvió 14:

- **De lectura (10):** `read_text_file`, `read_media_file`, `read_multiple_files`, `read_file` (obsoleta), `list_directory`, `list_directory_with_sizes`, `directory_tree`, `search_files`, `get_file_info` y `list_allowed_directories`.
- **De escritura (4):** `write_file`, que crea un archivo o lo sobrescribe sin avisar; `edit_file`, que cambia líneas y devuelve el *diff*; `create_directory`; y `move_file`, que mueve o renombra.

Cada herramienta trae anotaciones (`readOnlyHint`, `destructiveHint`). Claude Desktop las usa para separarlas en esos dos grupos y, por omisión, pide aprobación para todas. `search_files` busca **por nombre** con patrones como `**/*.md`; para buscar por contenido, el modelo tiene que leer los archivos.

## Cómo lo limitan los directorios permitidos

La carpeta permitida se pasa como argumento al arrancar el servidor; en mi caso es `tarea2/sandbox/`. En cada operación, el servidor resuelve la ruta real, incluso con `..` o enlaces simbólicos, y si queda fuera la rechaza antes de tocar el disco:

```text
read_text_file  …\tarea2\sandbox\..\README.md
→ Access denied - path outside allowed directories: …\tarea2\README.md not in …\tarea2\sandbox
```

Si el cliente soporta *Roots*, sus raíces **reemplazan** al argumento (Model Context Protocol, 2026a). Lo comprobé con la misma configuración en dos partes de Claude Desktop:

| Cliente | ¿Manda Roots? | Carpeta permitida |
|---|---|---|
| Chat | No | `tarea2\sandbox` |
| Pestaña Code, abierta en el repositorio | Sí | Todo el repositorio |

Así que el argumento no siempre es el límite final. Además, el límite lo pone el código del servidor, no el sistema operativo: la guía de seguridad de MCP lo llama «cooperativo» (Model Context Protocol, s. f.).

## Qué pasaría sin ese límite

Si el servidor recibiera `C:\` o mi carpeta de usuario, el modelo podría leer llaves y credenciales (`.ssh`, `.aws`, archivos `.env`), y lo que lee viaja al servidor del proveedor. También podría sobrescribir o mover cualquier archivo por un error o por una instrucción escondida en un texto. Con `sandbox/` el daño máximo queda en cuatro archivos de ejemplo que además están en Git.

## Referencias

Model Context Protocol. (2026a). *Filesystem MCP Server* [Archivo README]. GitHub. Recuperado el 15 de octubre de 2026, de https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem

Model Context Protocol. (2026b, 11 de octubre). *@modelcontextprotocol/server-filesystem* (Versión 1.0.0) [Software]. npm. https://www.npmjs.com/package/@modelcontextprotocol/server-filesystem

Model Context Protocol. (s. f.). *Local server security*. Recuperado el 15 de octubre de 2026, de https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/local-server-security
