# 3. MCP frente a una API

[← Volver al README](../README.md#parte-2-mcp-investigación)

## Qué es una API

Una API es un contrato entre programas: qué operaciones existen, qué reciben y qué devuelven. Quien programa lee la documentación y decide de antemano, en el código, qué se llama y cuándo. Si quiere usar otra operación, cambia el código.

## Qué es MCP

MCP es un protocolo abierto para conectar aplicaciones con LLM a herramientas y datos. Anthropic lo presentó en noviembre de 2024 (Anthropic, 2024), y desde diciembre de 2025 lo administra la Agentic AI Foundation de la Linux Foundation (Linux Foundation, 2025). Sus mensajes son de JSON-RPC 2.0, un formato de llamada remota en el que cada petición lleva un `method`, sus `params` y un `id` (JSON-RPC Working Group, 2013; Model Context Protocol, 2026a).

El servidor publica un catálogo de herramientas, cada una con nombre, descripción y esquema de parámetros. El host lo pide con `tools/list`, el modelo elige qué usar según lo que pidió el usuario y el host lo ejecuta con `tools/call`, después de pedir permiso (Model Context Protocol, 2026b). Así se ve con el servidor de archivos que instalé (recortado):

```text
--> {"jsonrpc":"2.0","id":2,"method":"tools/list"}
<-- {"jsonrpc":"2.0","id":2,"result":{"tools":[ … {"name":"list_directory",
      "description":"Get a detailed listing of all files and directories in a specified path. …",
      "inputSchema":{"type":"object","properties":{"path":{"type":"string"}}}} … ]}}
--> {"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"list_directory","arguments":{"path":"…\\tarea2\\sandbox"}}}
<-- {"jsonrpc":"2.0","id":3,"result":{"content":[{"type":"text","text":"[FILE] LEEME.md\n[DIR] notas\n[DIR] proyecto"}]}}
```

## Tabla comparativa

| Aspecto | API | MCP |
|---|---|---|
| Quién decide qué se invoca | El programador, de antemano, en el código | El modelo, en el momento, entre las herramientas del catálogo; el usuario aprueba |
| Cómo se descubren las capacidades | Leyendo la documentación antes de programar | Preguntándole al servidor: `tools/list`, `resources/list`, `prompts/list` |
| Acoplamiento | Fuerte: si la API cambia, el cliente se rompe | Débil: el cliente sólo conoce el protocolo |
| Formato de los mensajes | El que defina cada API (JSON, XML, gRPC…) | Siempre JSON-RPC 2.0 |
| Autenticación y consentimiento | Llaves o tokens en cada petición; nadie aprueba cada llamada | OAuth 2.1 en HTTP o credenciales locales en stdio; el host pide permiso antes de cada herramienta |
| Reutilización entre aplicaciones | Cada aplicación integra cada API por su cuenta | Un servidor sirve para cualquier host compatible |

## MCP no sustituye a las APIs

Casi siempre envuelve una. El servidor MCP de GitHub traduce `tools/call` a llamadas a la API REST de GitHub (GitHub, s. f.), y el de archivos usa la API de archivos de Node.js. El camino es: modelo → host → servidor MCP → API → servicio. La diferencia está en quién la usa: una API la usa un programador; MCP se la ofrece a un modelo para que la descubra y la pida en el momento.

El video del curso (Vida MRR - Programacion web, 2026) explica bien esta diferencia, con dos detalles que no coinciden con la especificación vigente: pone los *prompts* del lado del cliente, cuando son del servidor, y describe el *handshake* `initialize`, que la revisión 2026-07-28 eliminó ([punto 4](04-arquitectura.md)).

## Referencias

Anthropic. (2024, 25 de noviembre). *Introducing the Model Context Protocol*. https://www.anthropic.com/news/model-context-protocol

GitHub. (s. f.). *GitHub MCP Server* [Software]. GitHub. Recuperado el 16 de octubre de 2026, de https://github.com/github/github-mcp-server

JSON-RPC Working Group. (2013, 4 de enero). *JSON-RPC 2.0 specification*. https://www.jsonrpc.org/specification

Linux Foundation. (2025, 9 de diciembre). *Linux Foundation announces the formation of the Agentic AI Foundation (AAIF), anchored by new project contributions including Model Context Protocol (MCP), goose and AGENTS.md* [Comunicado de prensa]. https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation

Model Context Protocol. (2026a, 28 de julio). *Specification* (Revisión 2026-07-28). https://modelcontextprotocol.io/specification/2026-07-28

Model Context Protocol. (2026b, 28 de julio). *Tools* (Revisión 2026-07-28). https://modelcontextprotocol.io/specification/2026-07-28/server/tools

Vida MRR - Programacion web. (2026, 8 de julio). *Diferencia entre API y MCP* [Video]. YouTube. https://youtu.be/FdVkE8u2C_Q
