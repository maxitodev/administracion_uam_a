# Guion de la exposición

[← Volver al README](../README.md#exposición)

De 5 a 7 minutos. Las diapositivas se abren con [`diapositivas.html`](diapositivas.html) en el navegador; **F** pone pantalla completa y **P** muestra las notas.

| # | Diapositiva | Tiempo |
|---|---|---|
| 1 | Portada | 0:15 |
| 2 | Parte 1: el entorno quedó listo | 0:30 |
| 3 | El problema | 0:40 |
| 4 | API frente a MCP | 1:00 |
| 5 | Arquitectura | 0:40 |
| 6 | Servidor de archivos | 0:30 |
| 7 | Demostración en vivo | 2:00 |
| 8 | Seguridad | 0:30 |
| 9 | Servidor propio (si sobra tiempo) | 0:20 |
| 10 | Cierre | 0:15 |

## Demostración

Antes de empezar: Claude Desktop abierto en un **chat** nuevo (no en la pestaña Code) y el video de respaldo a la mano.

1. `Lista el contenido de la carpeta que tienes permitida en sistema-archivos.`
2. `Lee proyecto/bitacora.md y dime qué se hizo el 15 de octubre.`
3. `Crea proyecto/minuta-expo.md con una minuta breve de la exposición.` Señalar el cuadro de permiso antes de aprobar.
4. `En proyecto/pendientes.md marca como hecha la tercera tarea.`
5. `Lee el archivo C:\Users\maxsa\Documents\UAM-A\administracion_uam_a\tarea2\README.md` y señalar que lo frenó el servidor, no el modelo.

Al terminar, `git restore tarea2/sandbox` y `git clean -fd tarea2/sandbox` regresan la carpeta a como estaba.

Si algo falla, pongo el video de respaldo: la misma demostración, de 2 minutos como máximo, grabada con **Win + Alt + R**.

## Las dos preguntas

**¿En qué se diferencia MCP de consumir una API?** En quién decide. Con una API, yo escribo en el código qué se llama y cuándo. Con MCP, el servidor publica un catálogo, el modelo elige en el momento y el host me pide permiso. MCP no reemplaza a la API: la envuelve.

**¿Qué habilita exactamente el servidor de sistema de archivos?** Listar, leer, buscar por nombre, crear, editar y mover archivos, sólo dentro de `tarea2/sandbox/`. No tiene red, no ejecuta comandos y fuera de esa carpeta rechaza todo.

## Posibles preguntas

- **¿Qué es stdio?** La entrada y la salida estándar del proceso: Claude Desktop lanza el servidor y se mandan una línea de JSON por mensaje.
- **¿Por qué `@1.0.0`?** Para que `npx` no instale una versión nueva sin que yo la revise.
- **¿La carpeta del argumento es siempre el límite?** No. Si el cliente manda *Roots*, mandan las del cliente. En la pestaña Code el servidor quedó con todo el repositorio.
- **¿Qué cambió en la especificación 2026-07-28?** Quitaron el *handshake* `initialize`, y Roots y Sampling quedaron obsoletas.
