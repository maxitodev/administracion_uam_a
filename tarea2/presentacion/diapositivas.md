---
marp: true
lang: es
title: Tarea 2 · Entorno móvil e IA con MCP
author: Max Uriel Sánchez Díaz
paginate: true
style: |
  :root { --uam: #b5121b; --tinta: #1f2328; --gris: #59636e; --fondo: #f6f8fa; }
  section { font-family: "Segoe UI", system-ui, sans-serif; color: var(--tinta); font-size: 30px; padding: 56px 72px; }
  h1 { color: var(--uam); font-size: 1.6em; margin-bottom: 0.3em; }
  h2 { color: var(--uam); font-size: 1.15em; }
  strong { color: var(--uam); }
  code { background: var(--fondo); border-radius: 6px; padding: 0 6px; font-size: 0.85em; }
  footer, section::after { color: var(--gris); font-size: 0.55em; }
  section.portada { justify-content: center; }
  section.portada h1 { font-size: 2.1em; }
  section.portada p { color: var(--gris); }
  section.grande p { font-size: 1.35em; line-height: 1.35; }
  .flujo { display: flex; gap: 18px; align-items: center; justify-content: center; margin-top: 30px; flex-wrap: wrap; }
  .caja { border: 3px solid var(--uam); border-radius: 14px; padding: 18px 22px; text-align: center; min-width: 170px; background: #fff; }
  .caja small { display: block; color: var(--gris); font-size: 0.6em; margin-top: 6px; }
  .lejos { border-style: dashed; border-color: var(--gris); }
  .flecha { font-size: 1.4em; color: var(--gris); }
  .dos { display: grid; grid-template-columns: 1fr 1fr; gap: 36px; }
  .dos > div { background: var(--fondo); border-radius: 14px; padding: 22px 28px; }
  .dos h3 { margin-top: 0; }
  table { font-size: 0.8em; margin-top: 28px; }
footer: Tarea 2 · Administración de Proyectos de Software (1151055) · UAM Azcapotzalco · 26-O
---

<!-- _class: portada -->
<!-- _paginate: false -->

# Del chat al proyecto

## Entorno móvil e IA con MCP

Max Uriel Sánchez Díaz · 2213026327 · Ingeniería en Computación

<!--
Presentarme y decir de qué van los 6 minutos: primero el teléfono quedó listo (30 s),
luego por qué la IA no veía mis archivos, qué cambió con MCP, la demostración en vivo
y cómo se limita. Termino con las dos preguntas.
-->

---

# Parte 1 · el entorno quedó listo

<div class="flujo">
  <div class="caja">Flutter 3.47.7<small>Dart 3.13.5</small></div>
  <div class="caja">Android Studio<small>2026.2.1 + Command-line Tools</small></div>
  <div class="caja">Mi teléfono<small>depuración USB</small></div>
</div>

<div class="flujo">
  <div class="caja">HolaMundoFlutter ✔</div>
  <div class="caja">HolaMundoKMP ✔</div>
</div>

<!--
Una sola diapositiva: lo instalado y que las dos apps corren en mi teléfono.
El tropiezo: faltaban las Command-line Tools y una ruta mal escapada en local.properties.
No leer la tabla de versiones: está en el README.
-->

---

<!-- _class: grande -->

# El problema

Un LLM recibe **texto** y devuelve **texto**.

No abre archivos. No ejecuta nada. Corre lejos.

<div class="flujo">
  <div class="caja">Mi proyecto</div>
  <div class="flecha">⇄ copiar y pegar ⇄</div>
  <div class="caja lejos">Modelo<small>en la nube</small></div>
</div>

<!--
Arquitectura: corre en el servidor del proveedor, sólo ve lo que le mando, su salida es texto.
Seguridad: no DEBE tocar todo; se equivoca y obedece instrucciones escondidas en lo que lee.
El canal entre el modelo y el proyecto era yo.
-->

---

# API frente a MCP

<div class="dos">
<div>

### API

**Yo** decido en el código qué se llama y cuándo.

Contrato fijo · una integración por app

</div>
<div>

### MCP

El servidor publica un **catálogo**; el **modelo** elige en el momento y yo apruebo.

`tools/list` · `tools/call` · JSON-RPC 2.0

</div>
</div>

<div class="flujo">
  <div class="caja">Modelo</div><div class="flecha">→ MCP →</div>
  <div class="caja">Servidor MCP</div><div class="flecha">→ API →</div>
  <div class="caja">Servicio real</div>
</div>

<!--
Ésta es la pregunta 1. La diferencia es QUIÉN DECIDE: antes el programador, ahora el modelo
leyendo descripciones. Descubrimiento en tiempo de ejecución, acoplamiento débil, N+M.
MCP no sustituye a la API: la envuelve (el de archivos envuelve la API de archivos de Node;
el de GitHub, su API REST).
-->

---

# Arquitectura

<div class="flujo">
  <div class="caja">Host<small>Claude Desktop</small></div>
  <div class="flecha">→</div>
  <div class="caja">Cliente ×2<small>uno por servidor</small></div>
  <div class="flecha">→ stdio →</div>
  <div class="caja">Servidores<small>sistema-archivos · entregas-apsw</small></div>
</div>

| Servidor ofrece | Cliente ofrece | Transportes |
|---|---|---|
| Tools · Resources · Prompts | Elicitation · Roots *(obsoleta)* | stdio · Streamable HTTP |

Especificación **2026-07-28**: sin *handshake*, cada petición lleva su versión.

<!--
El modelo NO es un rol de MCP: el host lo consulta por su API.
Tools las controla el modelo, resources la app, prompts el usuario.
Mi servidor negoció 2026-07-28; el de archivos, 2025-11-25 (generación anterior).
-->

---

# El servidor de sistema de archivos

<div class="flujo">
  <div class="caja">14 herramientas<small>listar · leer · buscar · crear · editar · mover</small></div>
  <div class="flecha">sólo en</div>
  <div class="caja"><code>tarea2/sandbox/</code><small>la carpeta que recibe al arrancar</small></div>
</div>

<br>

`npx -y @modelcontextprotocol/server-filesystem@1.0.0 …\tarea2\sandbox`

<!--
Pregunta 2: qué habilita exactamente. Lo de la caja, y nada fuera de esa carpeta.
Es un servidor de referencia, no parte del protocolo. Valida cada ruta con realpath.
Nunca C:\ ni la carpeta de usuario: ahí están .ssh, .aws, tokens.
-->

---

<!-- _class: grande -->

# Demostración en vivo

listar · leer · crear · modificar · buscar

y pedirle algo **fuera** de la carpeta

<!--
Cambiar a Claude Desktop. Prompts exactos en guion.md.
Si algo falla: video de respaldo (2 min) en el escritorio.
-->

---

# Seguridad: capas

| Riesgo | Capa |
|---|---|
| Instrucciones escondidas en un archivo o en una descripción | Confirmación humana · revisar `tools/list` |
| Salir de la carpeta (`..`, rutas absolutas, enlaces) | El servidor resuelve la ruta real y la rechaza |
| Escribir o borrar sin querer | Carpeta de ejemplo · sólo lectura cuando basta · Git |
| El paquete cambia solo (*rug pull*) | Versión fija `@1.0.0` |

<!--
El límite de carpetas es "cooperativo": lo pone el código del servidor, no el sistema operativo.
Por eso varias capas. Trifecta letal: datos privados + contenido no confiable + salida a red.
-->

---

# Extra · mi servidor `entregas-apsw`

SDK oficial de Python (`mcp` 2.3.0) · 3 herramientas de sólo lectura + 1 recurso

| Herramienta | Para qué |
|---|---|
| `revisar_entrega` | ¿La carpeta tiene lo que pide el enunciado? |
| `buscar_credenciales` | ¿Se me coló un token antes del push? |
| `dias_para_entrega` | ¿Cuánto falta, o cuánto descuento llevo? |

<!--
Mostrarlo en el mismo Claude Desktop si queda tiempo: "revisa si tarea2 está completa".
También se niega a salir de la raíz del repositorio.
-->

---

<!-- _class: grande -->

# Para llevar

**API:** yo decido qué se llama. **MCP:** el modelo descubre y pide; yo apruebo.

El servidor de archivos habilita **14 operaciones** en **una carpeta**. Nada más.

<!--
Cerrar con la conclusión: el modelo nunca entra a mi computadora; un programa local,
pequeño y explícito, actúa por él. Abrir a preguntas.
-->
