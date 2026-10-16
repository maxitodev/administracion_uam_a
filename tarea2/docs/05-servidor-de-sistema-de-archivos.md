# 5. El servidor de sistema de archivos

[← Volver al README](../README.md#parte-2-mcp-investigación)

## No es parte del protocolo

MCP define cómo se habla (mensajes, primitivas y transportes), pero no qué herramientas existen. El servidor de sistema de archivos es uno de los **servidores de referencia** que mantiene el propio proyecto en el repositorio `modelcontextprotocol/servers`: un ejemplo de cómo implementar el protocolo, escrito en TypeScript y publicado en npm como `@modelcontextprotocol/server-filesystem` (Model Context Protocol, 2026d). Cualquiera podría escribir otro servidor de archivos con otras reglas, como hice yo con [mi servidor propio](../README.md#5-opcional-servidor-propio).

La versión que instalé es la **1.0.0**, publicada el 11 de octubre de 2026 (Model Context Protocol, 2026g). Según su registro de cambios, es la primera con versionado semántico y la última de la generación anterior del protocolo: está hecha con el SDK 1.x de TypeScript y por eso negocia la revisión 2025-11-25 (ver [punto 4](04-arquitectura.md#ciclo-de-vida-de-2025-11-25-a-2026-07-28)).

## Qué herramientas expone

`tools/list` devolvió 14 herramientas. El README documenta 13; la decimocuarta, `read_file`, es un alias obsoleto de `read_text_file` que el código sigue registrando.

| Herramienta | Qué hace | ¿Modifica? |
|---|---|---|
| `read_text_file` | Lee un archivo como texto; con `head` o `tail` lee sólo el principio o el final. | No |
| `read_media_file` | Lee una imagen o un audio y lo devuelve en base64 con su tipo MIME. | No |
| `read_multiple_files` | Lee varios archivos de una vez; si uno falla, sigue con los demás. | No |
| `list_directory` | Lista una carpeta con los prefijos `[FILE]` y `[DIR]`. | No |
| `list_directory_with_sizes` | Lo mismo, con tamaños. | No |
| `directory_tree` | Devuelve el árbol completo de una carpeta en JSON. | No |
| `search_files` | Busca por nombre con patrones *glob* (`*.md`, `**/*.md`) dentro de una carpeta. | No |
| `get_file_info` | Da tamaño, fechas y permisos de un archivo o carpeta. | No |
| `list_allowed_directories` | Dice qué carpetas tiene permitidas. | No |
| `create_directory` | Crea una carpeta y las intermedias; si ya existe, no falla. | Sí |
| `write_file` | Crea un archivo o **sobrescribe** uno existente sin avisar. | Sí, destructiva |
| `edit_file` | Reemplaza líneas exactas y devuelve el *diff*; acepta `dryRun` para previsualizar. | Sí, destructiva |
| `move_file` | Mueve o renombra; falla si el destino ya existe. | Sí, destructiva |

Cada herramienta trae anotaciones: las de lectura declaran `readOnlyHint: true` y `write_file`, `edit_file` y `move_file` declaran `destructiveHint: true`. El host puede usarlas para decidir cuándo pedir confirmación, aunque la especificación aclara que son sugerencias y no deben tomarse como garantía. Claude Desktop las usa para agrupar: en los permisos del conector muestra 10 herramientas *de solo lectura* y 4 *de escritura/eliminación* (`write_file`, `edit_file`, `create_directory` y `move_file`), y todas empiezan en «Requiere aprobación». La búsqueda es **por nombre**: no hay una herramienta para buscar dentro del contenido. Para encontrar en qué archivo aparece una palabra, el modelo lista o busca los archivos y después los lee.

## Cómo lo limitan los directorios permitidos

Al lanzarlo se le pasan una o varias carpetas como argumentos. En mi configuración es una sola, creada para esta tarea:

```text
npx -y @modelcontextprotocol/server-filesystem@1.0.0 C:\Users\maxsa\Documents\UAM-A\administracion_uam_a\tarea2\sandbox
```

Si el cliente ofrece *Roots*, la lista que manda el cliente **reemplaza** por completo a los argumentos (Model Context Protocol, 2026d). Si no la ofrece, se usan los argumentos. Lo comprobé con la misma configuración en dos clientes de la misma aplicación:

| Cliente | ¿Ofrece Roots? | Carpeta que quedó permitida |
|---|---|---|
| Chat de Claude Desktop | No. El registro dice *Client does not support MCP Roots, using allowed directories set from server args*. | `tarea2\sandbox`, la del argumento |
| Pestaña Code de Claude Desktop, abierta en el repositorio | Sí. El registro dice *Updated allowed directories from MCP roots: 1 valid directories*. | `C:\Users\maxsa\Documents\UAM-A\administracion_uam_a`, es decir, **todo el repositorio** según `list_allowed_directories` |

O sea, el argumento de la configuración no es un límite fijo: si el cliente manda raíces, mandan las del cliente. Por eso la demostración se hace en el chat. Si el servidor se usara desde un agente de programación, ese agente debe abrirse en la carpeta que se le quiere dar, no en la raíz del proyecto ni en la carpeta de usuario.

En cada operación, el servidor convierte la ruta pedida en absoluta, la normaliza (resuelve los `..`) y sigue los enlaces simbólicos con `realpath` hasta el archivo real. Si el resultado no está dentro de una carpeta permitida, rechaza la operación antes de tocar el disco. Lo revisé en el código del paquete instalado (`dist/lib.js`) y lo probé:

```text
read_text_file  C:\…\tarea2\sandbox\..\README.md
→ Access denied - path outside allowed directories: C:\…\tarea2\README.md not in C:\…\tarea2\sandbox

list_directory  C:\…\tarea2\sandbox\..
→ Access denied - path outside allowed directories: C:\…\tarea2 not in C:\…\tarea2\sandbox
```

Hay dos defensas más en el código. Los archivos nuevos se crean con la bandera `wx`, que falla si ya existe algo con ese nombre, para no escribir a través de un enlace simbólico plantado. Y al editar se abre el archivo con `O_NOFOLLOW`, aunque un comentario del propio código aclara que esa bandera sólo existe en sistemas POSIX: en Windows no aplica.

Este límite lo aplica **el servidor**, no el sistema operativo. El proceso de Node corre con todos mis permisos de usuario; si alguien me pasara un servidor modificado, o si el servidor tuviera un error, el límite desaparecería. La guía de seguridad de MCP llama a estas listas de directorios límites «cooperativos» y recomienda sumarles un *sandbox* o acceso de sólo lectura (Model Context Protocol, s. f.-b).

## Qué pasaría sin ese límite

Si se lanzara con `C:\` o con mi carpeta de usuario completa, que es lo que el enunciado prohíbe, el modelo podría:

- **Leer secretos.** En mi carpeta de usuario están `.ssh/`, `.aws/`, `.docker/` y `.gemini/`, que es donde esas herramientas guardan llaves y credenciales, además de los `.env` de otros proyectos. Lo que el modelo lee viaja al servidor del proveedor como parte de la conversación.
- **Modificar o borrar cualquier cosa.** `write_file` sobrescribe sin avisar y `move_file` puede sacar archivos de su lugar. Un error del modelo o una instrucción escondida en un archivo (ver [punto 6](06-seguridad.md)) podría dañar trabajo que no tiene nada que ver con la tarea.
- **Juntar las tres piezas del peor caso.** Datos privados, contenido no confiable y la capacidad de mandar información fuera: lo que Willison (2025) llama la «trifecta letal».

Con la carpeta `tarea2/sandbox/` el daño máximo queda en cuatro archivos de ejemplo que, además, están en Git: cualquier cambio se ve con `git diff` y se deshace con `git restore`.

## Referencias

Model Context Protocol. (2026d). *Filesystem MCP Server* [Archivo README]. GitHub. Recuperado el 15 de octubre de 2026, de https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem

Model Context Protocol. (2026g, 11 de octubre). *@modelcontextprotocol/server-filesystem* (Versión 1.0.0) [Software]. npm. https://www.npmjs.com/package/@modelcontextprotocol/server-filesystem

Model Context Protocol. (s. f.-b). *Local server security*. Recuperado el 15 de octubre de 2026, de https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/local-server-security

Willison, S. (2025, 16 de junio). *The lethal trifecta for AI agents: Private data, untrusted content, and external communication*. Simon Willison's Weblog. https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/
