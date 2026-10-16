# 7. Casos de uso

[← Volver al README](../README.md#parte-2-mcp-investigación)

## Primero, los nombres

Conviene separar tres cosas que se mezclan seguido:

- **Una familia de modelos** es el LLM que genera el texto: Claude (Anthropic), GPT (OpenAI), Gemini (Google), Llama (Meta) o Qwen (el equipo Qwen de Alibaba Cloud), que publica modelos de pesos abiertos como Qwen3 (Yang et al., 2025). Un modelo no habla MCP por sí solo: recibe texto y devuelve texto.
- **Un host** es la aplicación que usa el modelo y habla MCP con los servidores: un chat de escritorio, un editor o una terminal. Algunos hosts dejan elegir entre modelos de varias familias.
- **Un servidor MCP** es el programa que da las herramientas, como el de sistema de archivos.

Por eso «Qwen» no es una herramienta que use MCP, sino un modelo que se puede usar dentro de un host que sí lo hace. En cambio, Google Antigravity sí es un entorno de desarrollo: es el host.

## Herramientas actuales que usan MCP

| Herramienta (empresa) | Qué es | Cómo se le agrega un servidor MCP |
|---|---|---|
| **Claude Desktop** (Anthropic) | Aplicación de chat para Windows y macOS. Es el host que usé en esta tarea. | `claude_desktop_config.json`, en la clave `mcpServers`, o con extensiones `.mcpb` (Model Context Protocol, s. f.-a). |
| **Claude Code** (Anthropic) | Agente de programación para la terminal, los editores y la aplicación de escritorio. | `claude mcp add <nombre> -- <comando>`, o un archivo `.mcp.json` en la raíz del proyecto que se comparte con el equipo (Anthropic, s. f.-a). |
| **Visual Studio Code con GitHub Copilot** (Microsoft y GitHub) | Editor con agentes en el chat. | `.mcp.json` en la raíz del proyecto; antes se usaba `.vscode/mcp.json`, con la clave `servers` (Microsoft, 2026). |
| **Cursor** (Anysphere) | Editor con IA, derivado de VS Code. | `.cursor/mcp.json` en el proyecto o `~/.cursor/mcp.json` para todos (Anysphere, s. f.). |
| **Google Antigravity** (Google) | Entorno de desarrollo centrado en agentes. | Desde su MCP Store o en `mcp_config.json`, con la clave `mcpServers` (Google, s. f.). |
| **Zed** (Zed Industries) | Editor de código. | En su configuración, bajo `context_servers`, o con extensiones (Zed Industries, s. f.). |
| **Codex CLI** (OpenAI) | Agente de programación para la terminal. | `codex mcp add`, o tablas `[mcp_servers.<nombre>]` en `~/.codex/config.toml` (OpenAI, s. f.-b). |

En casi todas, la configuración tiene la misma forma: un nombre, un comando y sus argumentos. El servidor que instalé para Claude Desktop se puede copiar casi sin cambios a Cursor o a Antigravity, porque los tres usan `mcpServers`. Eso es lo que significa que un servidor se escriba una vez y lo use cualquier host ([punto 3](03-mcp-frente-a-una-api.md#tabla-comparativa)).

## Cómo editan un repositorio completo sin subir archivos a mano

Antes había que copiar cada archivo al chat. Las herramientas de programación de la tabla trabajan de otra forma:

1. **El host corre en mi máquina** y yo le indico la carpeta del proyecto, que pasa a ser su raíz de trabajo.
2. **El modelo pide lo que necesita.** No recibe el repositorio entero: pide listar carpetas, buscar archivos por nombre o por texto y leer sólo los que le interesan. El host ejecuta cada petición y le devuelve el resultado.
3. **Los cambios llegan como ediciones**, no como archivos completos: «reemplaza estas líneas por estas otras», igual que `edit_file`. El host las aplica y me muestra el *diff* para que lo apruebe.
4. **Puede comprobar su trabajo** si el host le da una herramienta para ejecutar comandos: correr las pruebas, leer el error y corregir.
5. **Git es la red de seguridad.** Todo cambio queda en el árbol de trabajo, se revisa con `git diff` y se confirma o se descarta.

En los agentes de programación, leer y editar archivos suelen ser herramientas que ya trae el host. MCP agrega lo que está fuera del repositorio: el servidor de GitHub para abrir *issues* y *pull requests*, uno de base de datos para consultar el esquema real o uno de documentación para leer la versión actual de una biblioteca. Como todos hablan el mismo protocolo, el mismo agente puede leer el código, consultar la base y abrir el *pull request* sin que yo copie nada.

## Referencias

Anthropic. (s. f.-a). *Connect Claude Code to tools via MCP*. Claude Code Docs. Recuperado el 15 de octubre de 2026, de https://code.claude.com/docs/en/mcp

Anysphere. (s. f.). *Model Context Protocol (MCP)*. Cursor Docs. Recuperado el 15 de octubre de 2026, de https://cursor.com/docs/context/mcp

Google. (s. f.). *Model Context Protocol (MCP)*. Google Antigravity Docs. Recuperado el 15 de octubre de 2026, de https://antigravity.google/docs/mcp

Microsoft. (2026, 14 de octubre). *Add and manage MCP servers in VS Code*. Visual Studio Code Docs. https://code.visualstudio.com/docs/copilot/customization/mcp-servers

Model Context Protocol. (s. f.-a). *Connect to local MCP servers*. Recuperado el 15 de octubre de 2026, de https://modelcontextprotocol.io/docs/develop/connect-local-servers

OpenAI. (s. f.-b). *Model Context Protocol – Codex*. OpenAI Developers. Recuperado el 15 de octubre de 2026, de https://developers.openai.com/codex/mcp

Yang, A., Li, A., Yang, B., Zhang, B., Hui, B., Zheng, B., Yu, B., Gao, C., Huang, C., Lv, C., Zheng, C., Liu, D., Zhou, F., Huang, F., Hu, F., Ge, H., Wei, H., Lin, H., Tang, J., … Qiu, Z. (2025). *Qwen3 technical report* [Preprint]. arXiv. https://doi.org/10.48550/arXiv.2505.09388

Zed Industries. (s. f.). *Model Context Protocol*. Zed Docs. Recuperado el 15 de octubre de 2026, de https://zed.dev/docs/ai/mcp
