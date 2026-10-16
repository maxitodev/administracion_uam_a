# 4. Arquitectura

[← Volver al README](../README.md#parte-2-mcp-investigación)

**Versión consultada:** especificación de MCP, revisión **2026-07-28**. Es la vigente, se publicó el 28 de julio de 2026 (Soria Parra & Delimarsky, 2026) y la consulté el 15 de octubre de 2026. Para el *handshake* también revisé la 2025-11-25.

## Host, cliente y servidor

- **Host:** la aplicación con el LLM. Inicia las conexiones, decide qué llega al modelo y pide permiso al usuario.
- **Cliente:** el conector dentro del host. Cada cliente habla con un solo servidor (Model Context Protocol, 2026a).
- **Servidor:** el programa que ofrece herramientas, datos o plantillas (Model Context Protocol, 2026f).

| Rol | En lo que instalé |
|---|---|
| Host | Claude Desktop 2.42304 para Windows |
| Clientes | Dos, uno por servidor, creados por Claude Desktop |
| Servidores | `sistema-archivos` (servidor de referencia 1.0.0, en Node.js) y `entregas-apsw` (mi servidor, en Python) |

El modelo no es uno de los roles. Corre en los servidores del proveedor, y el host le pasa el catálogo y ejecuta lo que pide.

## Primitivas

Del servidor:

| Primitiva | La controla | Qué es | En mis servidores |
|---|---|---|---|
| Tools | El modelo | Funciones que el modelo pide ejecutar | 14 en `sistema-archivos` y 3 en `entregas-apsw` |
| Resources | La aplicación | Datos con una URI que el host puede adjuntar | `apsw://reglas-entrega` |
| Prompts | El usuario | Plantillas que el usuario elige | Ninguno |

Del cliente:

- **Roots.** El cliente le dice al servidor en qué carpetas puede trabajar, y el servidor de archivos las usa en lugar de su argumento (Model Context Protocol, 2026d). En la revisión 2026-07-28 quedó obsoleta (Model Context Protocol, 2026c). En mi máquina, el chat de Claude Desktop no la ofrece y la pestaña Code sí ([punto 5](05-servidor-de-sistema-de-archivos.md#cómo-lo-limitan-los-directorios-permitidos)).
- **Elicitation.** A mitad de una operación, el servidor le pide al usuario un dato o una confirmación por medio de un formulario. Es la función del cliente que sigue vigente.
- **Sampling.** Dejaba que el servidor le pidiera texto al modelo del cliente. También quedó obsoleta.

## Transportes

- **stdio:** el cliente lanza el servidor como subproceso, y se mandan una línea de JSON por mensaje por la entrada y la salida estándar. Es el que usan mis dos servidores (Model Context Protocol, 2026g).
- **Streamable HTTP:** el servidor es un servicio web con un solo *endpoint*, y la autorización usa OAuth 2.1 (Model Context Protocol, 2026b). El transporte HTTP+SSE de la primera versión está obsoleto.

## Ciclo de vida

Hasta la revisión 2025-11-25, cada conexión empezaba con un *handshake*: el cliente manda `initialize` con su versión y sus capacidades, el servidor responde y el cliente confirma con `notifications/initialized` (Model Context Protocol, 2025). La revisión 2026-07-28 lo quitó: ahora cada petición lleva su versión y el servidor se anuncia con `server/discover` (Model Context Protocol, 2026e).

Lo comprobé. Con mi cliente de prueba, mi servidor negoció la 2026-07-28 y el de archivos, que es de la generación anterior, la 2025-11-25. Claude Desktop, en cambio, usó el *handshake* con los dos; su registro dice `Era probe verdict: legacy`.

## Referencias

Model Context Protocol. (2025, 25 de noviembre). *Lifecycle* (Revisión 2025-11-25). https://modelcontextprotocol.io/specification/2025-11-25/basic/lifecycle

Model Context Protocol. (2026a, 28 de julio). *Architecture* (Revisión 2026-07-28). https://modelcontextprotocol.io/specification/2026-07-28/architecture

Model Context Protocol. (2026b, 28 de julio). *Authorization* (Revisión 2026-07-28). https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization

Model Context Protocol. (2026c, 28 de julio). *Deprecated features* (Revisión 2026-07-28). https://modelcontextprotocol.io/specification/2026-07-28/deprecated

Model Context Protocol. (2026d). *Filesystem MCP Server* [Archivo README]. GitHub. Recuperado el 15 de octubre de 2026, de https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem

Model Context Protocol. (2026e, 28 de julio). *Key changes* (Revisión 2026-07-28). https://modelcontextprotocol.io/specification/2026-07-28/changelog

Model Context Protocol. (2026f, 28 de julio). *Specification* (Revisión 2026-07-28). https://modelcontextprotocol.io/specification/2026-07-28

Model Context Protocol. (2026g, 28 de julio). *Transports: Overview* (Revisión 2026-07-28). https://modelcontextprotocol.io/specification/2026-07-28/basic/transports

Soria Parra, D., & Delimarsky, D. (2026, 28 de julio). *The 2026-07-28 specification*. Model Context Protocol Blog. https://blog.modelcontextprotocol.io/posts/2026-07-28/
