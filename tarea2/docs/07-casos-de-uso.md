# 7. Casos de uso

[← Volver al README](../README.md#parte-2-mcp-investigación)

Primero, los nombres. Un **modelo** es el LLM que genera el texto: Claude, GPT, Gemini o Qwen, que es una familia de modelos del equipo Qwen de Alibaba Cloud (Yang et al., 2025). Un **host** es la aplicación que usa ese modelo y habla MCP con los servidores. Por eso Qwen no es una plataforma que use MCP, y Google Antigravity sí es un entorno de desarrollo: es un host.

## Herramientas que usan MCP

| Herramienta | Qué es | Dónde se configura un servidor |
|---|---|---|
| Claude Desktop (Anthropic) | Aplicación de chat; la usé en esta tarea | `claude_desktop_config.json` (Model Context Protocol, s. f.) |
| Claude Code (Anthropic) | Agente de programación para terminal y editores | `claude mcp add` o `.mcp.json` en el proyecto (Anthropic, s. f.) |
| VS Code con GitHub Copilot (Microsoft) | Editor con agentes en el chat | `.mcp.json` en el proyecto (Microsoft, 2026) |
| Cursor (Anysphere) | Editor con IA, derivado de VS Code | `.cursor/mcp.json` (Anysphere, s. f.) |
| Google Antigravity (Google) | Entorno de desarrollo con agentes | Su MCP Store o `mcp_config.json` (Google, s. f.) |

En casi todas, un servidor se declara igual: nombre, comando y argumentos. Mi configuración de Claude Desktop se puede copiar casi sin cambios a Cursor o a Antigravity.

## Cómo editan un repositorio sin subir archivos

1. El host corre en mi máquina y le indico la carpeta del proyecto.
2. El modelo pide sólo lo que necesita: listar carpetas, buscar y leer algunos archivos.
3. Los cambios llegan como ediciones de líneas, no como archivos completos, y el host me muestra el *diff* para aprobarlo.
4. Si el host puede ejecutar comandos, el modelo corre las pruebas y corrige. Git queda como red de seguridad.

Leer y editar suelen ser herramientas que ya trae el host. MCP agrega lo que está fuera del repositorio: GitHub para *issues* y *pull requests*, una base de datos o documentación actualizada, todo con el mismo protocolo.

## Referencias

Anthropic. (s. f.). *Connect Claude Code to tools via MCP*. Claude Code Docs. Recuperado el 15 de octubre de 2026, de https://code.claude.com/docs/en/mcp

Anysphere. (s. f.). *Model Context Protocol (MCP)*. Cursor Docs. Recuperado el 15 de octubre de 2026, de https://cursor.com/docs/context/mcp

Google. (s. f.). *Model Context Protocol (MCP)*. Google Antigravity Docs. Recuperado el 15 de octubre de 2026, de https://antigravity.google/docs/mcp

Microsoft. (2026, 14 de octubre). *Add and manage MCP servers in VS Code*. Visual Studio Code Docs. https://code.visualstudio.com/docs/copilot/customization/mcp-servers

Model Context Protocol. (s. f.). *Connect to local MCP servers*. Recuperado el 15 de octubre de 2026, de https://modelcontextprotocol.io/docs/develop/connect-local-servers

Yang, A., Li, A., Yang, B., Zhang, B., Hui, B., Zheng, B., Yu, B., Gao, C., Huang, C., Lv, C., Zheng, C., Liu, D., Zhou, F., Huang, F., Hu, F., Ge, H., Wei, H., Lin, H., Tang, J., … Qiu, Z. (2025). *Qwen3 technical report* [Preprint]. arXiv. https://doi.org/10.48550/arXiv.2505.09388
