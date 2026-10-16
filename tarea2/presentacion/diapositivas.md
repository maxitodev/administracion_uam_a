---
marp: true
lang: es
title: Tarea 2 · Entorno móvil e IA con MCP
author: Max Uriel Sánchez Díaz
paginate: true
size: 16:9
style: |
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=JetBrains+Mono:wght@500&display=swap');
  :root { --uam: #c8102e; --uam2: #ff4d5e; --fondo: #0f1115; --panel: #1a1d24; --borde: #2a2f3a; --texto: #e8eaed; --gris: #9aa3af; }
  section { font-family: Inter, "Segoe UI", sans-serif; background: var(--fondo); color: var(--texto); font-size: 28px; padding: 64px 80px; }
  section::before { content: ""; position: absolute; left: 0; top: 0; width: 100%; height: 8px; background: linear-gradient(90deg, var(--uam), var(--uam2)); }
  section::after { color: var(--gris); font-size: 0.55em; }
  footer { color: var(--gris); font-size: 0.5em; }
  h1 { font-weight: 800; font-size: 1.7em; color: #fff; margin: 0 0 0.4em; letter-spacing: -0.02em; }
  h1::after { content: ""; display: block; width: 90px; height: 6px; margin-top: 14px; border-radius: 3px; background: var(--uam); }
  h2 { color: var(--uam2); font-weight: 600; font-size: 1.05em; }
  h3 { color: var(--uam2); margin: 0 0 10px; }
  strong { color: var(--uam2); }
  code { font-family: "JetBrains Mono", monospace; background: var(--panel); color: #ffb4bc; border: 1px solid var(--borde); border-radius: 6px; padding: 1px 8px; font-size: 0.8em; }
  table { width: 100%; border-collapse: collapse; font-size: 0.75em; margin-top: 24px; }
  th { background: var(--uam); color: #fff; text-align: left; padding: 12px 16px; }
  td { background: var(--panel); border-bottom: 1px solid var(--borde); padding: 12px 16px; }
  section.portada { justify-content: center; background: radial-gradient(circle at 85% 20%, #3a0a12 0%, var(--fondo) 55%); }
  section.portada h1 { font-size: 2.6em; }
  section.portada h1::after { width: 140px; }
  section.portada p { color: var(--gris); }
  section.grande p { font-size: 1.3em; line-height: 1.4; }
  section.centro { justify-content: center; text-align: center; }
  section.centro h1::after { margin-left: auto; margin-right: auto; }
  .flujo { display: flex; gap: 18px; align-items: center; justify-content: center; margin-top: 30px; flex-wrap: wrap; }
  .caja { background: var(--panel); border: 1px solid var(--borde); border-top: 4px solid var(--uam); border-radius: 14px; padding: 20px 26px; text-align: center; min-width: 180px; }
  .caja small { display: block; color: var(--gris); font-size: 0.6em; margin-top: 6px; }
  .lejos { border-top-color: var(--gris); border-style: dashed; }
  .flecha { font-size: 1.2em; color: var(--gris); }
  .dos { display: grid; grid-template-columns: 1fr 1fr; gap: 32px; }
  .dos > div { background: var(--panel); border: 1px solid var(--borde); border-radius: 16px; padding: 24px 30px; }
footer: Tarea 2 · Administración de Proyectos de Software (1151055) · UAM Azcapotzalco · 26-O
---

<!-- _class: portada -->
<!-- _paginate: false -->
<!-- _footer: "" -->

# Del chat al proyecto

## Entorno móvil e IA con MCP

Max Uriel Sánchez Díaz · 2213026327 · Ingeniería en Computación
UAM Azcapotzalco · Trimestre 26-O

<!--
Presentarme y decir de qué van los 6 minutos.
-->

---

# El entorno quedó listo

<div class="flujo">
  <div class="caja">Flutter 3.47.7<small>Dart 3.13.5</small></div>
  <div class="caja">Android Studio<small>2026.2.1 + Command-line Tools</small></div>
  <div class="caja">Pixel 7 Pro<small>Android 17 · depuración USB</small></div>
</div>

<div class="flujo">
  <div class="caja">HolaMundoFlutter ✔</div>
  <div class="caja">HolaMundoKMP ✔</div>
</div>

<!--
Lo instalado y que las dos apps corren en mi teléfono.
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
Arquitectura: corre en el servidor del proveedor. Seguridad: no debe tocar todo.
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
Pregunta 1: la diferencia es quién decide. MCP no sustituye a la API: la envuelve.
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
El modelo no es un rol de MCP. Claude Desktop todavía usa el handshake con ambos servidores.
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
Pregunta 2. Ojo: si el cliente manda Roots (pestaña Code), la carpeta la define el cliente.
-->

---

<!-- _class: centro grande -->

# Demostración en vivo

listar · leer · crear · modificar

y pedirle algo **fuera** de la carpeta

<!--
Cambiar a Claude Desktop (chat). Prompts en guion.md. Plan B: video.
-->

---

# Seguridad: capas

| Riesgo | Capa |
|---|---|
| Instrucciones escondidas en un archivo o una descripción | Confirmación humana · revisar `tools/list` |
| Salir de la carpeta (`..`, rutas absolutas, enlaces) | El servidor resuelve la ruta real y la rechaza |
| Escribir o borrar sin querer | Carpeta de ejemplo · sólo lectura cuando basta · Git |
| El paquete cambia solo | Versión fija `@1.0.0` |

<!--
El límite de carpetas lo pone el código del servidor, no el sistema operativo.
-->

---

# Extra · servidor `entregas-apsw`

SDK oficial de Python (`mcp` 2.3.0) · 3 herramientas de sólo lectura + 1 recurso

| Herramienta | Para qué |
|---|---|
| `revisar_entrega` | ¿La carpeta tiene lo que pide el enunciado? |
| `buscar_credenciales` | ¿Se me coló un token antes del push? |
| `dias_para_entrega` | ¿Cuánto falta, o cuánto descuento llevo? |

<!--
Sólo si sobra tiempo.
-->

---

<!-- _class: centro grande -->

# Para llevar

**API:** yo decido qué se llama. **MCP:** el modelo descubre y pide; yo apruebo.

El servidor de archivos habilita **14 operaciones** en **una carpeta**. Nada más.

<!--
Cerrar y abrir a preguntas.
-->
