# Guion de la exposición

[← Volver al README](../README.md#exposición)

Duración: de 5 a 7 minutos. Las [diapositivas](diapositivas.md) son de apoyo: tienen pocas palabras a propósito y no se leen. Para presentarlas basta con abrir [`diapositivas.html`](diapositivas.html) en el navegador y pulsar **F** para pantalla completa. Las notas de cada diapositiva están en el `.md`, dentro de los comentarios `<!-- … -->`, y se ven en el modo presentador de Marp (tecla **P**).

## Tiempos

| # | Diapositiva | Tiempo | Idea que tiene que quedar |
|---|---|---|---|
| 1 | Portada | 0:15 | De qué voy a hablar. |
| 2 | Parte 1 | 0:30 | El teléfono y la computadora quedaron listos; las dos apps corren. |
| 3 | El problema | 0:40 | El LLM sólo recibe y devuelve texto; el canal era yo. |
| 4 | API frente a MCP | 1:00 | **Quién decide** qué se llama. MCP envuelve a la API, no la reemplaza. |
| 5 | Arquitectura | 0:40 | Host, cliente, servidor; el modelo no es un rol. Versión 2026-07-28. |
| 6 | Servidor de archivos | 0:30 | 14 herramientas en una carpeta. |
| 7 | Demostración en vivo | 2:00 | Ver abajo. |
| 8 | Seguridad | 0:30 | El límite lo pone el servidor; por eso hay varias capas. |
| 9 | Servidor propio | 0:20 | Sólo si sobra tiempo. |
| 10 | Para llevar | 0:15 | Las dos respuestas en una frase cada una. |
| | **Total** | **≈ 6:40** | |

## Demostración en vivo

Antes de empezar:

- Claude Desktop abierto, con un chat nuevo y **Settings → Developer** mostrando los dos servidores como *running*.
- El Explorador de archivos abierto en `tarea2\sandbox\`, para que se vea aparecer el archivo nuevo.
- `git status` limpio en el repositorio. Si una prueba anterior dejó cambios en `sandbox/`, se deshacen con `git restore tarea2/sandbox` y `git clean -fd tarea2/sandbox`.
- El video de respaldo en el escritorio.

Los cinco pedidos, en este orden y copiados tal cual:

1. `Lista el contenido de la carpeta que tienes permitida en sistema-archivos.`
2. `Lee proyecto/bitacora.md y dime qué se hizo el 15 de octubre.`
3. `Crea proyecto/minuta-2026-10-16.md con una minuta breve: fecha, asistente (yo) y dos acuerdos: probar MCP y grabar el video de respaldo.` → cambiar al Explorador y mostrar el archivo.
4. `En proyecto/pendientes.md marca como hechas las dos primeras tareas.` → señalar el *diff* que devuelve `edit_file`.
5. `Lee el archivo C:\Users\maxsa\Documents\UAM-A\administracion_uam_a\tarea2\README.md` → señalar el `Access denied` y decir: «no lo frenó el modelo, lo frenó el servidor».

En cada paso, señalar el cuadro de permiso de Claude Desktop antes de aprobar: ésa es la confirmación humana.

## Plan B: video de respaldo (máximo 2 minutos)

Si falla la red, el proyector o Claude Desktop, pongo el video. Para grabarlo:

1. Hacer la demostración completa una vez con los mismos cinco pedidos.
2. Grabar la pantalla con la Herramienta Recortes (**Win + Shift + R**, opción de video) o con la Xbox Game Bar (**Win + Alt + R**).
3. Recortar a 2 minutos como máximo. El video no va al repositorio, porque pesa mucho: queda en mi computadora y en mi nube.

## Las dos preguntas

**¿En qué se diferencia MCP de consumir una API?**
En quién decide. Con una API, yo escribo en el código qué operación se llama y cuándo; el contrato es fijo y cada aplicación integra cada API por su cuenta. Con MCP, el servidor publica un catálogo que el modelo descubre en el momento (`tools/list`) y el modelo decide qué pedir (`tools/call`); el host me pide permiso y lo ejecuta. El mismo servidor sirve para cualquier host compatible. Y MCP no reemplaza a la API: casi siempre la envuelve.

**¿Qué habilita exactamente el servidor de sistema de archivos?**
Catorce herramientas para listar, leer, buscar por nombre, ver información, crear carpetas, escribir, editar y mover archivos, todas **dentro de las carpetas que recibe al arrancar**: aquí, sólo `tarea2/sandbox/`. Fuera de ellas no habilita nada. Resuelve la ruta real de cada petición y, si queda afuera, la rechaza antes de tocar el disco. No da acceso a la red, no ejecuta comandos y no puede borrar: lo más destructivo que tiene es sobrescribir o mover.

## Preguntas que pueden salir

- **¿Qué es stdio?** La entrada y la salida estándar de un proceso. Claude Desktop lanza el servidor como subproceso y se hablan con una línea de JSON por mensaje. Por eso el servidor no debe imprimir nada más en `stdout`.
- **¿Por qué `@1.0.0` en la configuración?** Para que `npx` no descargue una versión nueva sin que yo la revise. Es la defensa contra el *rug pull*.
- **¿Qué pasaría si le doy `C:\`?** El modelo podría leer `.ssh`, `.aws` y los `.env` de otros proyectos, y sobrescribir o mover cualquier cosa. Lo que lee viaja al servidor del proveedor.
- **¿Qué cambió en la especificación 2026-07-28?** Quitaron el *handshake* `initialize`: cada petición lleva su versión y el servidor se anuncia con `server/discover`. Roots y Sampling quedaron obsoletas.
- **¿El modelo ve todo mi disco por tener MCP?** No. Sólo ve lo que devuelven las herramientas que llama, y éstas sólo ven la carpeta permitida.
- **¿La carpeta del argumento es siempre el límite?** No. Si el cliente soporta *Roots*, las raíces que manda reemplazan al argumento. Lo vi en mi máquina: en el chat de Claude Desktop el servidor quedó con `sandbox/`, y en la pestaña Code, abierta en el repositorio, quedó con todo el repositorio. Por eso la demostración va en el chat.
