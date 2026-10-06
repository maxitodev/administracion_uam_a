# Tarea 1 · Introducción a la administración de proyectos y entorno de trabajo

| | |
|---|---|
| **UEA y clave** | Administración de Proyectos de Software (1151055) |
| **Trimestre** | 26-O, otoño 2026 |
| **Licenciatura** | Ingeniería en Computación |
| **Nombre** | Max Uriel Sánchez Díaz |
| **Matrícula** | 2213026327 |
| **Profesor** | M. en C. Gabriel Hurtado Avilés |
| **Fecha** | 6 de octubre de 2026 |

Universidad Autónoma Metropolitana, Unidad Azcapotzalco · División de Ciencias Básicas e Ingeniería · Departamento de Sistemas

## Contenido

1. [Ejercicio 1. El repositorio](#ejercicio-1-el-repositorio)
2. [Ejercicio 2. Investigación](#ejercicio-2-investigación)
3. [Ejercicio 3. De PostgreSQL 17 a 18](#ejercicio-3-de-postgresql-17-a-18)
4. [Ejercicio 4. Otro stack: MySQL + phpMyAdmin](#ejercicio-4-otro-stack-mysql--phpmyadmin)
5. [Ejercicio 5. Capturas](#ejercicio-5-capturas)
6. [Uso de inteligencia artificial](#uso-de-inteligencia-artificial)
7. [Referencias](#referencias)

---

## Ejercicio 1. El repositorio

| Requisito | Dónde está |
|---|---|
| Repositorio público para todo el curso, con licencia MIT | [github.com/maxitodev/administracion_uam_a](https://github.com/maxitodev/administracion_uam_a) · [LICENSE](../LICENSE) |
| `.gitignore` con `data/`, `.env`, `Thumbs.db` y `.DS_Store`, antes del Ejercicio 3 | [.gitignore](../.gitignore), confirmado antes que el contenedor de PostgreSQL 17 |
| `.gitattributes` en la raíz | [.gitattributes](../.gitattributes) |
| Al menos cinco confirmaciones en días distintos | Historial en la [captura 8](#ejercicio-5-capturas) |
| README en la raíz con liga a cada tarea | [README.md](../README.md#-tareas) |

El `.gitattributes` deja que Git normalice los finales de línea (`* text=auto`), pero obliga a usar LF en los `.sh`, `.sql`, `.yaml`, `Dockerfile` y `.env*`. Esos archivos se leen dentro de contenedores Linux, y un script de bash guardado con CRLF de Windows falla con `$'\r': command not found`.

Estructura de la tarea:

```text
tarea1/
├── README.md          este documento
├── img/               las ocho capturas
├── postgres/          PostgreSQL 18 + Adminer (en el historial, antes PostgreSQL 17)
│   ├── Dockerfile
│   ├── compose.yaml
│   ├── .env.example
│   ├── initdb/01-tablero.sql
│   └── extras/comprobar.sh
└── mysql/             MySQL 9.7 + phpMyAdmin
    └── compose.yaml
```

---

## Ejercicio 2. Investigación

### 1. ¿Qué es un proyecto de software?

#### Proyecto frente a operación continua

Según la Guía del PMBOK, un proyecto es un trabajo con duración limitada cuyo fin es crear algo único: un producto, un servicio o un resultado (Project Management Institute [PMI], 2021a). Temporal quiere decir que tiene inicio y fin. Lewis (2007) lo baja a la práctica: un proyecto se hace una sola vez; si el trabajo se repite, no es proyecto. La operación continua es lo contrario: trabajo permanente y repetitivo que mantiene funcionando lo que ya existe. Según el PMI (2021a), los entregables de un proyecto pasan después a operación, junto con la información para darles soporte y mantenimiento.

- **Proyecto:** desarrollar en un trimestre una app para que los alumnos consulten su horario y su salón. Termina al liberar la versión 1.0 y después el equipo se disuelve.
- **Operación:** el soporte diario de esa app ya en producción: respaldos nocturnos, altas de usuarios, atención de reportes y parches de seguridad. Sigue mientras el sistema esté en uso.

#### Proyecto, producto y proceso

En software estos términos se confunden con facilidad. Pressman (2009) los separa al describir el espectro de la gestión, que abarca personas, producto, proceso y proyecto.

| Concepto | Qué es | Cuánto dura | Ejemplo |
|---|---|---|---|
| Producto | El software que se entrega: los programas y su documentación (Sommerville, 2004/2005) | Todo su ciclo de vida, de la introducción al retiro (PMI, 2021a) | La app de horarios |
| Proceso | Las actividades con las que se produce software: especificación, diseño e implementación, validación y evolución (Sommerville, 2004/2005) | Se reutiliza de un proyecto a otro | El modelo en cascada o el desarrollo evolutivo |
| Proyecto | El trabajo temporal, con fechas, presupuesto y alcance definidos, para crear o mejorar un producto (Lewis, 2007; PMI, 2021a) | Termina al entregar su resultado | "App de horarios v1.0, trimestre 26-O" |

Un mismo producto puede pasar por varios proyectos (versión 1.0, migración a la nube, versión 2.0), porque en cualquier punto de su ciclo de vida se pueden abrir proyectos para mejorarlo (PMI, 2021a). Todos pueden seguir el mismo proceso.

#### Alcance, tiempo, costo y calidad

- **Alcance:** las funciones y los entregables que incluye el proyecto.
- **Tiempo:** el plazo para terminarlo.
- **Costo:** el presupuesto. En un equipo de desarrollo, casi todo se va en horas de trabajo.
- **Calidad:** qué tanto cumple el producto sus requisitos (PMI, 2021a); en la práctica, que funcione, que no falle y que se pueda usar sin problemas.

La triple restricción, o triángulo de hierro, no tiene una sola versión. Pollack et al. (2018) revisaron 45 años de literatura: tiempo y costo aparecen siempre, pero el tercer vértice cambia según el autor y el papel de la calidad sigue en discusión. Una versión pone alcance, tiempo y costo en las esquinas y la calidad en medio, porque la calidad no se fija sola: resulta de cómo se equilibren las otras tres. El PMI (2021a) describe ese equilibrio: un requisito nuevo puede exigir más plazo y presupuesto, y un recorte de presupuesto puede obligar a reducir el alcance o la calidad. Lewis (2007) advierte que, cuando el plazo aprieta, la calidad es lo que más se suele sacrificar.

Lewis (2007) también trabaja con cuatro variables: desempeño, costo, tiempo y alcance. El patrocinador puede fijar tres y quien dirige el proyecto debe calcular la cuarta; exigir las cuatro a la vez es una causa frecuente de fracaso. Pressman (2009) añade que decisiones de gestión como la estimación y la calendarización influyen en la calidad del software.

**Ejemplo.** La app de horarios se planeó con ocho funciones, diez semanas y tres desarrolladores. A la mitad, la coordinación pide agregar avisos de cambio de salón. El equipo puede pedir más semanas (tiempo), pagar horas extra o sumar a alguien (costo), o quitar otra función, como exportar el horario a PDF (alcance). Si la coordinación no acepta mover ninguna, el equipo recorta pruebas y revisiones de código para cumplir, y la app sale con más errores: la calidad absorbe el cambio.

### 2. ¿Cómo se administra?

#### La Guía del PMBOK

La Guía del PMBOK es la referencia del PMI para administrar proyectos de cualquier industria. La 6.ª edición se organizaba en 49 procesos, 5 grupos de procesos y 10 áreas de conocimiento (PMI, 2017). La 7.ª edición, publicada en 2021, dejó ese esquema. Se apoya en 12 principios, como valor, calidad y riesgo, y en 8 dominios de desempeño, como interesados, equipo, planeación e incertidumbre (PMI, 2021a). Los grupos de procesos quedan como uno de varios modelos opcionales. La guía pide partir de los principios y ajustar el enfoque, sea predictivo, adaptativo o híbrido, a cada proyecto (PMI, 2021b).

La 8.ª edición salió a finales de 2025. Reduce los principios a seis, cambia a siete dominios, reintroduce los grupos de procesos como "áreas de enfoque" e incluye 40 procesos (PMI, 2025). Aquí me baso en la 7.ª edición, que es la que viene en las referencias del curso; de la 8.ª sólo resumo los cambios principales.

#### Scrum

Scrum es un marco de trabajo ligero para problemas complejos. El equipo entrega valor en ciclos cortos y ajusta el rumbo con base en tres pilares: transparencia, inspección y adaptación (Schwaber & Sutherland, 2020). La guía de 2020 define:

- **3 responsabilidades:** Product Owner (ordena el Product Backlog para maximizar el valor del producto), Scrum Master (ayuda a que el equipo aplique Scrum y sea efectivo) y Developers (construyen el incremento).
- **5 eventos:** el Sprint, de un mes o menos, que contiene a los otros cuatro: Sprint Planning, Daily Scrum (15 minutos), Sprint Review y Sprint Retrospective.
- **3 artefactos, cada uno con su compromiso:** Product Backlog → Objetivo del Producto; Sprint Backlog → Objetivo del Sprint; Increment → Definición de Terminado.

#### Predictivo, iterativo y ágil

En el modelo predictivo, cuyo caso típico es la cascada, el alcance se acuerda al inicio y las fases avanzan en orden. Sirve cuando los requisitos están claros y no se esperan cambios grandes, porque regresar a una fase anterior obliga a rehacer trabajo (Sommerville, 2004/2005). El iterativo construye una versión, la somete a revisión de los usuarios y la mejora en la siguiente vuelta, así que los requisitos se aclaran con el tiempo (PMI, 2021a; Sommerville, 2004/2005). El ágil junta lo iterativo con lo incremental: cada ciclo corto deja una parte funcionando, el cliente colabora todo el tiempo y adaptarse pesa más que apegarse al plan original (Beck et al., 2001; PMI, 2021a).

| Criterio | Predictivo | Iterativo | Ágil |
|---|---|---|---|
| Cuándo se fija el alcance | Al inicio; después solo cambia mediante control formal de cambios | A grandes rasgos al inicio; se precisa en cada iteración | Se fija solo para el ciclo en curso; el resto del backlog se reordena en cada ciclo |
| Entregas | Normalmente una sola, al final del proyecto | Versiones intermedias para revisión; la versión final llega al cierre | Un incremento utilizable en cada ciclo de pocas semanas (en Scrum, un mes o menos) |
| Manejo del cambio | Caro; requiere solicitud y aprobación | Se incorpora en la siguiente iteración | Se espera; se reprioriza al planear cada sprint |
| Participación del cliente | Al inicio (requisitos) y al final (aceptación) | En la revisión de cada iteración | Continua; revisa cada incremento |
| Ejemplo | Sistema con requisitos fijados por contrato o norma | Interfaz que se refina con prototipos sucesivos hasta que el usuario la aprueba | Aplicación web hecha con Scrum en sprints de dos semanas |

*Nota.* Elaboración propia con base en Sommerville (2004/2005), PMI (2021a), Beck et al. (2001) y Schwaber y Sutherland (2020).

#### Qué modelo elegiría para el proyecto del curso

Para un equipo de estudiantes con un trimestre de unas 11 semanas, repositorio en GitHub y contenedores, elegiría Scrum adaptado con tablero Kanban, precedido de una planeación inicial corta de tipo predictivo. Mis razones:

1. **Fecha fija, alcance flexible.** El trimestre no se mueve; lo que alcancemos a construir sí. Con el backlog ordenado por valor se hace primero lo importante y, si falta tiempo, se renegocia el alcance sin bajar la calidad (Schwaber & Sutherland, 2020).
2. **Incertidumbre.** Al inicio no dominamos la tecnología ni el problema, caso en el que el PMI (2021a) sugiere enfoques adaptativos. Mostrarle un incremento al profesor en cada Sprint Review permite corregir a tiempo (Schwaber & Sutherland, 2020).
3. **Herramientas.** GitHub Projects tiene vista de panel kanban y campo de iteración, y se conecta con issues y pull requests (GitHub, Inc., s. f.-a). El contenedor lleva todo lo que la aplicación necesita para ejecutarse, sin depender de lo instalado en cada computadora (Docker, Inc., s. f.-o).

Plan de trabajo:

- **Semana 1:** Objetivo del Producto, alcance mínimo, hitos con las fechas del curso, roles, riesgos y repositorio con contenedores base.
- **Semanas 2 a 11:** cinco sprints de dos semanas, cada uno con planeación, revisión y retrospectiva. Un integrante es Product Owner y enlace con el profesor; el papel de Scrum Master rota. Como los horarios de clase no coinciden, la Daily Scrum se cambia por dos o tres juntas breves por semana.
- **Tablero:** Por hacer, En curso, En revisión y Hecho. La Guía Kanban pide controlar de forma explícita el trabajo en curso (Coleman & Vacanti, 2025); acordamos un máximo de dos tareas por persona.
- **Definición de Terminado:** pull request revisado por otro integrante, pruebas que pasan, aplicación que levanta en su contenedor y README al día.

La Guía de Scrum advierte que alterar u omitir sus elementos limita sus beneficios (Schwaber & Sutherland, 2020); por eso lo llamo Scrum adaptado. Planear de forma predictiva y ejecutar de forma adaptativa es un enfoque híbrido, el tipo de ajuste al contexto que propone el PMI (2021a).

### 3. ¿Con qué herramientas?

#### Herramientas que apoyan la administración del proyecto

**Control de versiones: Git y GitHub.** Git registra cada cambio que se hace a los archivos del proyecto. Con ese registro se puede recuperar un estado anterior, ver en qué difieren dos momentos del trabajo y rastrear quién hizo cada modificación y cuándo (Chacon & Straub, 2014). GitHub hospeda el repositorio en la nube y le añade funciones para el trabajo en equipo: *issues* para dar seguimiento a las tareas y *pull requests* para revisar cambios antes de fusionarlos (GitHub, Inc., s. f.-g). Para quien administra, el historial es una bitácora verificable: cada entrega queda ligada a un *commit* concreto.

**Tableros de trabajo: Kanban.** La Guía Kanban plantea tres prácticas: definir y hacer visible el flujo de trabajo, gestionar de forma activa las tareas en curso (lo que incluye controlar cuántas hay a la vez) y mejorar ese flujo de manera continua (Coleman & Vacanti, 2025). En la práctica, cada tarea es una tarjeta que avanza por columnas como *Por hacer*, *En curso* y *Hecho*. GitHub Projects ofrece esa vista de tablero, además de vistas de tabla y de hoja de ruta, y se mantiene al día con los issues y pull requests del repositorio (GitHub, Inc., s. f.-a). Trello sigue la misma idea: tableros con listas y tarjetas que se arrastran de una lista a otra para mostrar el avance (Atlassian, s. f.). De un vistazo se ve qué tarea está atorada y quién tiene demasiada carga.

**Contenedores.** Un contenedor junta la aplicación con todo lo que necesita para ejecutarse, de modo que se comporta igual en la computadora de cada integrante y en el servidor (Docker, Inc., s. f.-n). Así todo el equipo levanta el mismo entorno con un comando, y su definición se versiona junto al código; se pierde menos tiempo por diferencias entre máquinas.

**Integración continua: GitHub Actions.** GitHub Actions es una plataforma de CI/CD: corre flujos de trabajo automáticos cuando ocurre un evento en el repositorio, como un *push* o un pull request, y con ellos compila, prueba o despliega el proyecto (GitHub, Inc., s. f.-c). Para la administración es un control de calidad permanente: si un cambio rompe las pruebas, se sabe en ese momento y no al cierre del trimestre.

#### Docker frente a una máquina virtual

Una máquina virtual (VM) abstrae el hardware: un hipervisor divide el equipo físico y cada VM arranca su propio sistema operativo. Un contenedor virtualiza el sistema operativo: es un proceso aislado que usa el kernel del anfitrión (Docker, Inc., s. f.-n).

| Criterio | Contenedor (Docker) | Máquina virtual |
|---|---|---|
| Qué virtualiza | El sistema operativo | El hardware, mediante un hipervisor |
| Kernel | Usa el del anfitrión, compartido con los demás contenedores | Cada VM trae el suyo |
| Peso | Ligero: Docker habla de imágenes de decenas de MB; las de esta tarea miden de 116 MB a 934 MB en disco | Pesado: decenas de GB, porque incluye un SO completo, bibliotecas y la aplicación |
| Arranque | Más rápido: no tiene que iniciar un SO completo | Puede ser lento: primero arranca un SO completo |
| Aislamiento | Cada contenedor es un proceso separado, pero todos dependen del mismo kernel | Cada VM es un sistema completo, separado por el hipervisor y con kernel propio |

*Nota.* Elaboración propia con datos de Docker, Inc. (s. f.-n).

Los contenedores de Linux necesitan un kernel Linux. En Windows, Docker Desktop usa por defecto el *backend* WSL 2 cuando el equipo lo admite (la alternativa es Hyper-V). WSL 2 incluye un kernel Linux real mantenido por Microsoft y asigna la memoria según la demanda, así que Docker Desktop no aparta más CPU ni RAM de la que ocupa (Docker, Inc., s. f.-h).

#### Dockerfile frente a compose.yaml

| Aspecto | Dockerfile | compose.yaml |
|---|---|---|
| Qué es | La receta de **una** imagen: instrucciones que Docker ejecuta en orden para construirla (Docker, Inc., s. f.-i) | La descripción de una aplicación de **varios** contenedores: sus servicios, redes y volúmenes (Compose Specification, s. f.) |
| Se usa con | `docker build`, o desde Compose con la clave `build:` | `docker compose up`, `down`, `ps`, etc. |
| En el curso | `FROM postgres:18.6`; un solo `RUN` instala `nano` y `less` y borra `/var/lib/apt/lists`; `ENV LANG=C.UTF-8 TZ=America/Mexico_City PAGER=less`; `WORKDIR /trabajo` | Proyecto `apsw-1151055-contenedor` con dos servicios: `db` (se construye con el Dockerfile y se etiqueta `postgres-1151055:26o`) y `adminer` (`adminer:5.5.1`), más el volumen `datos_db` |

El Dockerfile no declara `CMD` ni `ENTRYPOINT`, así que conserva el arranque definido en la imagen oficial de PostgreSQL (Docker, Inc., s. f.-i). El compose.yaml tampoco declara redes: Compose crea una por proyecto (`apsw-1151055-contenedor_default`) y cada servicio se localiza por su nombre, así que Adminer encuentra la base con `ADMINER_DEFAULT_SERVER=db` (Docker, Inc., s. f.-k). Con `depends_on` y `condition: service_healthy`, Adminer espera a que `db` pase su *healthcheck* antes de arrancar (Compose Specification, s. f.).

La Compose Specification señala `compose.yaml` como el nombre preferido; también acepta `compose.yml` y, por compatibilidad con versiones anteriores, `docker-compose.yaml` y `docker-compose.yml`, que es el nombre del archivo del 22 de septiembre (Compose Specification, s. f.). La clave `version:` es obsoleta: Compose V2, el comando `docker compose` escrito en Go que reemplazó al `docker-compose` de Python, la ignora y valida siempre con el esquema más reciente; si la encuentra, solo avisa que es obsoleta. La línea actual, Compose v5, se comporta igual (Docker, Inc., s. f.-j, s. f.-l). Por eso nuestro archivo no la incluye.

#### Volúmenes

Lo que un contenedor escribe en su capa interna se pierde cuando el contenedor se elimina. Un volumen guarda esos datos aparte, así que siguen ahí aunque el contenedor se borre y se vuelva a crear (Docker, Inc., s. f.-m). En el curso usamos dos tipos de montaje:

- **Volumen con nombre.** Docker lo crea y lo administra. `datos_db:/var/lib/postgresql` guarda la base. Desde PostgreSQL 18, la imagen oficial declara su volumen en `/var/lib/postgresql` (con `PGDATA=/var/lib/postgresql/18/docker`) y ya no en `/var/lib/postgresql/data`; por eso montamos esa ruta (PostgreSQL Docker Community, s. f.).
- **Bind mount.** Monta una carpeta del anfitrión dentro del contenedor, así que depende de cómo estén organizados los directorios de esa máquina; con la opción `ro` el contenedor solo puede leerla (Docker, Inc., s. f.-a). `./initdb:/docker-entrypoint-initdb.d:ro` entrega los scripts de inicio, que solo se ejecutan cuando el directorio de datos está vacío (PostgreSQL Docker Community, s. f.); `./:/trabajo` comparte la carpeta del proyecto con el contenedor.

#### Comandos de Docker Compose

Se ejecutan en la carpeta `tarea1/postgres/`, donde está el `compose.yaml`. Las descripciones se basan en la referencia de la CLI (Docker, Inc., s. f.-c, s. f.-d, s. f.-e, s. f.-f, s. f.-g).

| Comando | Qué hace | Ejemplo con `db` |
|---|---|---|
| `docker compose up -d` | Construye las imágenes que hagan falta, crea y arranca los contenedores; `-d` los deja en segundo plano y libera la terminal | `docker compose up -d db` levanta solo la base; sin el nombre del servicio también arranca `adminer` |
| `docker compose exec` | Ejecuta un comando dentro de un contenedor que ya está corriendo | `docker compose exec db psql -U proyecto -d proyecto` abre `psql` con el usuario y la base por defecto |
| `docker compose stop` | Detiene los contenedores sin eliminarlos; se reanudan con `docker compose start` | `docker compose stop db` |
| `docker compose down` | Detiene y elimina los contenedores y la red del proyecto; los volúmenes con nombre se conservan | `docker compose down` quita `apsw_db`, pero los datos siguen en `datos_db` |
| `docker compose down -v` | Además borra los volúmenes con nombre declarados en el archivo y los anónimos | `docker compose down -v` elimina `datos_db`; en el siguiente `up` la base se crea desde cero y los scripts de `initdb` vuelven a correr |
| `docker compose ps` | Lista los contenedores en ejecución del proyecto con su estado y sus puertos; con `-a` también muestra los detenidos (por ejemplo, después de `stop`) | `docker compose ps db` muestra si `apsw_db` está arriba y, por el *healthcheck*, si está *healthy* |
| `docker compose logs` | Muestra la salida de los contenedores | `docker compose logs db` sirve para revisar errores al iniciar PostgreSQL o al correr los scripts de `initdb` |

### 4. ¿Bajo qué licencia se distribuye el software?

Una licencia de software es el texto con el que el titular de los derechos dice qué puede hacer quien recibe el programa (usarlo, modificarlo, redistribuirlo o venderlo) y qué obligaciones adquiere al hacerlo. Un proyecto sin licencia no queda libre para todos. Aplican los derechos de autor exclusivos, y nadie más puede copiarlo, distribuirlo ni modificarlo sin exponerse a un reclamo legal (GitHub, Inc., s. f.-f). Subirlo a un repositorio público de GitHub tampoco resuelve el problema: los términos de servicio del sitio solo permiten que otros vean el repositorio y le hagan fork, no que reutilicen el código (GitHub, Inc., s. f.-f). Por eso conviene elegir la licencia desde el primer commit.

#### a) Los dos grandes tipos

Cualquier licencia de código abierto deja usar, modificar y compartir el programa. Lo que distingue a unas de otras son las condiciones que piden a cambio (GitHub, Inc., s. f.-e). Hay dos familias:

- **Permisivas (MIT, BSD, Apache 2.0).** Piden muy poco, en esencia conservar el aviso de copyright y el texto de la licencia. Quien reutiliza el código puede distribuir su versión modificada, o un programa más grande que lo incluya, con otra licencia y sin entregar el código fuente (GitHub, Inc., s. f.-e).
- **Copyleft (GPL, LGPL, AGPL).** Dan los mismos permisos, pero con una condición recíproca: quien distribuya el programa o una versión modificada debe entregar el código fuente y mantener la misma licencia. Así las mejoras no se pueden cerrar (Free Software Foundation [FSF], 1991; GitHub, Inc., s. f.-e).

El copyleft tiene grados. El **fuerte** (GPL) alcanza también a las obras más grandes que incorporan el código. El **débil** (LGPL) se limita a la biblioteca. Un programa que solo la usa a través de sus interfaces puede tener otra licencia y no publicar su propio código, pero los cambios a la biblioteca deben seguir bajo LGPL o GPLv3 (GitHub, Inc., s. f.-d). El **de red** (AGPL) es el más estricto. A lo que pide la GPL le suma una regla: si una versión modificada se ofrece como servicio por red, sus usuarios tienen derecho a recibir el código fuente completo (GitHub, Inc., s. f.-e).

| Licencia | Tipo | Qué permite | Aviso de copyright y licencia | Misma licencia en derivados | Publicar código fuente | Indicar cambios | Patentes | Uso en red cuenta como distribución | ¿Se puede usar en software cerrado? |
|---|---|---|---|---|---|---|---|---|---|
| MIT | Permisiva | Usar, copiar, modificar, distribuir, sublicenciar y vender, también con fines comerciales | Sí | No | No | No | No las menciona | No | Sí |
| BSD 3-Clause | Permisiva | Uso comercial y privado, modificar y distribuir | Sí. Además prohíbe usar el nombre del titular o de los contribuidores para promocionar derivados sin permiso por escrito | No | No | No | No las menciona | No | Sí |
| Apache 2.0 | Permisiva | Uso comercial y privado, modificar, distribuir y usar las patentes de los contribuidores; no autoriza usar las marcas del proyecto | Sí | No | No | Sí, en los archivos modificados | Licencia expresa de patentes de los contribuidores | No | Sí |
| GPLv3 | Copyleft fuerte | Uso comercial y privado, modificar, distribuir y usar las patentes | Sí | Sí, incluidas las obras más grandes que lo incorporen | Sí, al distribuir | Sí | Licencia expresa de patentes de los contribuidores | No | No para distribuirlo; usarlo en privado sí |
| LGPLv3 | Copyleft débil | Igual que GPLv3 | Sí | Solo la biblioteca y sus modificaciones (bajo LGPLv3 o GPLv3) | Sí, de la biblioteca y sus cambios | Sí | Licencia expresa de patentes de los contribuidores | No | Con condiciones: un programa cerrado puede usarla por sus interfaces si avisa que la incluye, acompaña los textos de la GPL y la LGPL y permite que el usuario la cambie por una versión modificada |
| AGPLv3 | Copyleft de red | Igual que GPLv3 | Sí | Sí, incluidas las obras más grandes que lo incorporen | Sí, al distribuir y al ofrecer por red una versión modificada | Sí | Licencia expresa de patentes de los contribuidores | Sí | No para distribuirlo ni para ofrecer una versión modificada como servicio en red |

*Nota.* Elaboración propia con base en GitHub, Inc. (s. f.-b, s. f.-d, s. f.-e), Open Source Initiative (OSI, s. f.) y, para las condiciones de la LGPL en programas cerrados, FSF (2007, sección 4). Ninguna de las seis da garantía ni hace responsable al autor por daños (GitHub, Inc., s. f.-e).

#### b) Mi elección: MIT

Para este repositorio elegí la licencia MIT, y el archivo `LICENSE` de la raíz trae su texto. Es un repositorio escolar de prácticas, y lo que busco es que cualquier persona (compañeros, alumnos de otros trimestres o yo mismo en otro proyecto) pueda reutilizar los archivos sin pedirme permiso. La MIT lo resuelve en pocas líneas. Deja usar, copiar, modificar, distribuir, sublicenciar y vender el software, y lo único que pide es que el aviso de copyright y el de permiso vayan en las copias (OSI, s. f.).

Las ventajas que veo:

1. **Es fácil de entender.** Se lee en un minuto y queda claro qué se puede hacer.
2. **Casi no impone obligaciones.** Basta con conservar el aviso.
3. **Es compatible con casi todo.** Como permite redistribuir derivados y obras más grandes bajo otros términos (GitHub, Inc., s. f.-e), el código puede terminar en un proyecto GPL, en uno Apache o en uno privado.

La desventaja es la otra cara de lo mismo: alguien podría tomar mi código, cerrarlo y no compartir sus mejoras. Para un repositorio de tareas eso no me preocupa.

Si hubiera elegido GPL, las cosas cambiarían:

- Quien distribuyera una versión modificada, o un programa más grande con mis archivos, tendría que publicarlo también bajo GPL y entregar el código fuente completo (FSF, 1991; GitHub, Inc., s. f.-e).
- Nadie podría meter el código en un producto cerrado y distribuirlo así. Usarlo en privado sí.
- La compatibilidad iría en un solo sentido. Un proyecto GPL puede incorporar código MIT, pero un proyecto MIT o propietario que incorpore código GPL tendría que distribuirse completo bajo GPL (GitHub, Inc., s. f.-e).

La GPL tiene sentido cuando el objetivo es que las mejoras sigan siendo libres. Para mis prácticas me importa más que el material circule sin trabas, y para eso la MIT basta.

#### c) Un caso real: MySQL, Oracle y MariaDB

MySQL AB se fundó en Suecia en 1995. Sus fundadores fueron Michael "Monty" Widenius, David Axmark y Allan Larsson. Desde 2000 publicó MySQL bajo la GPL y, en paralelo, vendía licencias comerciales a fabricantes que querían meter la base de datos en productos cerrados. Hacia 2004 ese modelo de licencia dual era su principal fuente de ingresos (Buytaert, 2010). Para 2008 la descarga seguía siendo gratuita y la empresa también cobraba suscripciones de soporte (Kirk, 2008). Oracle conserva hoy el mismo esquema: ofrece el servidor bajo GPLv2 y bajo una licencia comercial para quien quiere integrarlo en su producto sin publicar su propio código (Oracle Corporation, s. f.-a).

Así pasaron las cosas:

| Fecha | Hecho |
|---|---|
| Enero de 2008 | Sun Microsystems anuncia que comprará MySQL AB por unos 1,000 millones de dólares: 800 millones en efectivo y 200 millones en opciones (Kirk, 2008). |
| Abril de 2009 | Oracle y Sun anuncian que Oracle comprará Sun a 9.50 dólares por acción, unos 7,400 millones de dólares en total (Oracle Corporation & Sun Microsystems, 2009). |
| 2009 | Widenius hace el fork MariaDB porque desconfía de cómo manejará Oracle el proyecto, y la mayoría de los desarrolladores originales se van con él. MySQL llevaba el nombre de su primera hija, My, y MariaDB lleva el de la segunda, Maria (MariaDB Foundation, s. f.-b). |
| Enero de 2010 | Oracle concluye la compra de Sun y con ella pasa a controlar MySQL (McAllister, 2013; Oracle Corporation, 2010). |
| Diciembre de 2012 | Widenius, Axmark y Larsson anuncian la MariaDB Foundation, una organización sin fines de lucro que cuida el proyecto y que arranca con un millón de euros de respaldo (Clarke, 2012; MariaDB Foundation, s. f.-b). |
| Abril de 2013 | Wikimedia termina de migrar la Wikipedia en inglés, la Wikipedia en alemán y Wikidata de MySQL 5.1 a MariaDB 5.5 (Feldman, 2013). |
| 2013 | Fedora 19 adopta MariaDB como implementación predeterminada de MySQL y Red Hat anuncia lo mismo para RHEL 7. Arch Linux, openSUSE y Slackware ya lo hacían (Fedora Project, s. f.; McAllister, 2013). |
| Septiembre de 2013 | Google informa que está pasando sus servidores internos de MySQL 5.1 a MariaDB 10.0 (Clark, 2013). |
| Junio de 2017 | Debian 9 sale con MariaDB 10.1 como la única variante de MySQL (Kekäläinen, 2017). |

Las migraciones tuvieron razones técnicas, pero también de confianza. Fedora argumentó que Oracle estaba cerrando el proyecto: ya no publicaba información útil sobre vulnerabilidades (CVE), no entregaba pruebas de regresión completas y buena parte de su base de datos de errores había dejado de ser pública (Fedora Project, s. f.). Wikimedia prefirió apoyar proyectos que no separan su código en una edición libre y otra empresarial con licencias distintas (Feldman, 2013).

**La clave: MySQL se distribuía bajo la GPLv2, y esa licencia ya le daba a cualquiera que recibiera el código el derecho de copiarlo, modificarlo y redistribuir versiones modificadas, con la sola condición de mantenerlas bajo la GPLv2. Por eso Widenius pudo crear MariaDB sin pedirle permiso a Oracle.** MySQL estaba publicado bajo la GPLv2, que da a quien recibe el programa el derecho de copiarlo, modificarlo y redistribuirlo, siempre que lo que distribuya a partir de él quede bajo la misma licencia (FSF, 1991, sección 2). Cada persona que recibe una copia obtiene la licencia directamente del titular original, y nadie en la cadena puede agregar restricciones (FSF, 1991, sección 6). Oracle, como dueña de los derechos, podía decidir cómo licenciar sus versiones futuras, y de hecho sigue vendiendo una licencia comercial en paralelo (Oracle Corporation, s. f.-a). Lo que la GPLv2 no contempla es que el titular retire los permisos que ya otorgó. Solo prevé que pierda sus derechos quien viole la licencia (FSF, 1991, sección 4). Por eso la lectura habitual es que el fork fue legal desde el primer día. A cambio, MariaDB Server debe seguir bajo GPLv2 y con su código disponible, un compromiso que la MariaDB Foundation declara mantener (MariaDB Foundation, s. f.-a).

---

## Ejercicio 3. De PostgreSQL 17 a 18

Todo se hizo en `tarea1/postgres/`, en dos confirmaciones:

1. **«Agrega el contenedor de PostgreSQL 17 del 22 de septiembre».** Copié el `Dockerfile` y el `docker-compose.yml` del material tal cual y levanté el contenedor.
2. **«Actualiza el contenedor a PostgreSQL 18.6 con Adminer».** Apagué el de la 17 con `docker compose down`, borré `docker-compose.yml` y puse en su lugar el `Dockerfile` y el `compose.yaml` del material, junto con `.env.example`, `initdb/01-tablero.sql` y `extras/comprobar.sh`, que hice con ayuda de IA a partir del material (ver [Uso de inteligencia artificial](#uso-de-inteligencia-artificial)).

Los dos se comprobaron igual: `docker compose ps` y `SELECT version();`.

**PostgreSQL 17**

```console
> docker compose up -d --build
time="2026-10-06T12:19:23-06:00" level=warning msg="...\\tarea1\\postgres\\docker-compose.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion"
 postgres Pulling
 ...
 postgres Pulled
 Network postgres_default  Created
 Container postgres173CV231AGO2026  Created
 Container postgres173CV231AGO2026  Started

> docker compose ps
NAME                      IMAGE         COMMAND                  SERVICE    CREATED          STATUS          PORTS
postgres173CV231AGO2026   postgres:17   "docker-entrypoint.s…"   postgres   13 seconds ago   Up 12 seconds   0.0.0.0:5432->5432/tcp

> docker compose exec postgres psql -U postgres -c "SELECT version();"
                                                       version
----------------------------------------------------------------------------------------------------------------------
 PostgreSQL 17.11 (Debian 17.11-1.pgdg13+2) on x86_64-pc-linux-gnu, compiled by gcc (Debian 14.2.0-19) 14.2.0, 64-bit
(1 row)
```

**PostgreSQL 18**

```console
> docker compose up -d --build
 ...
 #6 2.546 update-alternatives: using /bin/nano to provide /usr/bin/pico (pico) in auto mode
 #6 DONE 3.2s
 #7 [db 3/3] WORKDIR /trabajo
 #8 naming to docker.io/library/postgres-1151055:26o done
 db  Built
 Network apsw-1151055-contenedor_default  Created
 Volume "apsw-1151055-contenedor_datos_db"  Created
 Container apsw_db  Started
 Container apsw_db  Waiting
 Container apsw_db  Healthy
 Container apsw_adminer  Started

> docker compose ps
NAME           IMAGE                  COMMAND                  SERVICE   CREATED          STATUS                    PORTS
apsw_adminer   adminer:5.5.1          "entrypoint.sh docke…"   adminer   11 seconds ago   Up 5 seconds              127.0.0.1:8080->8080/tcp
apsw_db        postgres-1151055:26o   "docker-entrypoint.s…"   db        11 seconds ago   Up 10 seconds (healthy)   127.0.0.1:5434->5432/tcp

> docker compose exec db psql -U proyecto -d proyecto -c "SELECT version();"
                                                      version
--------------------------------------------------------------------------------------------------------------------
 PostgreSQL 18.6 (Debian 18.6-1.pgdg13+2) on x86_64-pc-linux-gnu, compiled by gcc (Debian 14.2.0-19) 14.2.0, 64-bit
(1 row)

> docker compose exec db bash
root@...:/trabajo# bash extras/comprobar.sh
== Servidor
  OK     responde (pg_isready)
  OK     versión mayor 18
  OK     datos en /var/lib/postgresql/18/docker
  OK     PG_VERSION del cluster es 18
== Base del curso
  OK     codificación UTF8
  OK     colación C
  OK     zona horaria America/Mexico_City
  OK     tablas de initdb/ creadas
  OK     la tabla tarea tiene filas
== Herramientas del Dockerfile
  OK     nano instalado
  OK     less instalado
  OK     LANG=C.UTF-8
  OK     TZ=America/Mexico_City
  OK     carpeta de trabajo /trabajo
  OK     compose.yaml visible en /trabajo
...
Resultado: 15 OK, 0 FALLA
```

`extras/comprobar.sh` revisa, desde dentro del contenedor, que el servidor responda, que la versión mayor sea 18, que la base use UTF8 y colación C, que la hora sea la de la Ciudad de México, que existan las tablas que crea `initdb/`, que estén `nano` y `less`, y que `/trabajo` sea la carpeta del proyecto. Adminer queda en <http://localhost:8080>: en *Motor de base de datos* hay que elegir **PostgreSQL** (por defecto aparece MySQL), servidor `db`, usuario y base `proyecto`, contraseña `practica_local_26o` (o la que se ponga en el `.env`).

### Diferencias entre los dos contenedores

| Aspecto | Qué decía (22 sept, PostgreSQL 17) | Qué dice (29 sept, PostgreSQL 18) | Por qué cambió |
|---|---|---|---|
| Nombre del archivo | `docker-compose.yml` | `compose.yaml` | Es el nombre que recomienda la Compose Specification; el otro viene de cuando Compose era un programa aparte. |
| Clave `version:` | `version: '3.8'` | No existe | Compose V2 la ignora y avisa que es obsoleta (el aviso salió al levantar la 17). |
| Nombre del proyecto | Implícito: el de la carpeta (`postgres`) | `name: apsw-1151055-contenedor` | El nombre de la carpeta cambia entre computadoras y genera contenedores duplicados. |
| Servicio y contenedor | `postgres` / `postgres173CV231AGO2026` | `db` / `apsw_db` | Nombres cortos y estables para usarlos en `exec`, en Adminer (`ADMINER_DEFAULT_SERVER: db`) y en `depends_on`. |
| De dónde sale la imagen | `image: postgres:17`: se descarga la imagen oficial; la etiqueta `17` es flotante (hoy da la 17.11) | `build: .` + `image: postgres-1151055:26o`: se construye con el Dockerfile, que fija `FROM postgres:18.6` | Versión exacta y repetible, y el Dockerfile por fin se usa. |
| Dockerfile | `FROM postgres:17` y `EXPOSE 5432` | `FROM postgres:18.6`, instala `nano` y `less`, define `LANG`, `TZ`, `PAGER` y `WORKDIR /trabajo` | Agrega lo que el entorno del curso necesita y la imagen oficial no trae. `EXPOSE 5432` se quitó porque la imagen oficial ya expone el 5432. |
| Credenciales | Fijas: `postgres` / `postgres` / `postgres` | `${POSTGRES_USER:-proyecto}` y similares, sobreescribibles con `.env` (hay `.env.example`) | Levanta sin preparar nada, pero permite no versionar contraseñas reales. |
| Codificación y colación | Las de la imagen (`en_US.utf8`) | `POSTGRES_INITDB_ARGS: "--encoding=UTF8 --locale=C"` | Que dos equipos ordenen los textos igual. |
| Puerto | `"5432:5432"`: queda en `0.0.0.0`, visible para toda la red local | `"127.0.0.1:${POSTGRES_PORT:-5434}:5432"` | Sólo esta máquina puede conectarse, y el 5434 no choca con un PostgreSQL instalado en el 5432. |
| Datos | *Bind mount* `./data:/var/lib/postgresql/data` | Volumen con nombre `datos_db:/var/lib/postgresql` | La imagen 18 movió `PGDATA` a `/var/lib/postgresql/18/docker`. Lo probé: con la ruta vieja el contenedor sale con código 1 y pide montar `/var/lib/postgresql`. |
| Scripts de arranque | No había | `./initdb:/docker-entrypoint-initdb.d:ro` | Crea las tablas de prueba la primera vez que el volumen está vacío. |
| Carpeta de trabajo | No había | `./:/trabajo` y `working_dir: /trabajo` | Dentro del contenedor se ven los mismos archivos que en Windows. |
| Healthcheck | No había | `pg_isready` cada 10 s | `ps` muestra `(healthy)` y Adminer espera a que la base responda. |
| Interfaz web | No había | Adminer 5.5.1 en `127.0.0.1:8080` | Ver la base sin instalar nada. |
| Cómo se levanta | Instrucción del 22 sept: `docker compose up --build`, en primer plano | Instrucción del `compose.yaml`: `docker compose up -d`, en segundo plano | La terminal queda libre y la primera vez construye sola; `--build` sólo hace falta si cambia el Dockerfile. En esta tarea las dos se levantaron con `up -d --build`. |
| `restart` | `unless-stopped` | `unless-stopped` | Sin cambio. |

### ¿Se usaba el Dockerfile viejo?

No. En el `docker-compose.yml` del 22 de septiembre el servicio tiene `image: postgres:17` y no tiene `build:`. Compose sólo construye los servicios que llevan `build:`; si no lo hay, descarga la imagen indicada en `image:`. Por eso `--build` no hacía nada. Se ve en la salida: al levantar dice `postgres Pulling` / `Pulled` y no aparece ningún paso de construcción, y en `docker compose ps` la columna IMAGE dice `postgres:17`, la imagen oficial, no una construida en la máquina.

Aunque se hubiera usado, no habría cambiado nada: sólo tenía `FROM postgres:17` y `EXPOSE 5432`, y la imagen oficial ya expone el 5432 (`docker image inspect postgres:17` muestra `"5432/tcp"` en `ExposedPorts`). En el contenedor nuevo sí se usa: el compose tiene `build: .`, la salida dice `db Built` y `ps` muestra la imagen `postgres-1151055:26o`.

### Versionado semántico y por qué de 17 a 18 es un cambio mayor

El versionado semántico (SemVer 2.0.0) escribe cada versión como MAYOR.MENOR.PARCHE. El PARCHE sube cuando se corrigen errores sin romper la compatibilidad; la MENOR, cuando se agrega funcionalidad que sigue siendo compatible con lo anterior; la MAYOR, cuando hay un cambio incompatible en la API pública. Al subir la MAYOR, la MENOR y el PARCHE vuelven a 0, y una versión ya publicada no se modifica: cualquier cambio sale como una versión nueva (Preston-Werner, s. f.). Saber qué versión exacta de cada componente forma el sistema es parte de la gestión de configuración; sin eso no se puede reconstruir el sistema ni controlar sus entregas (Pressman, 2009; Sommerville, 2004/2005).

PostgreSQL no usa SemVer, pero su numeración se lee de forma parecida. Desde la versión 10 maneja dos números: el primero es la versión mayor y el segundo la menor, que sólo trae correcciones de errores, de seguridad y de problemas de corrupción de datos (PostgreSQL Global Development Group [PGDG], s. f.-c). En términos de SemVer, ese segundo número equivale más bien al PARCHE. Por ejemplo, la 18.6 trae las correcciones acumuladas desde la 18.4; la 18.5 no llegó a publicarse porque se encontró una regresión (PGDG, 2026b). Pasar de 17 a 18, en cambio, es un cambio MAYOR:

1. **Cambia el formato de los datos.** Entre versiones mayores el contenido del directorio de datos no es compatible con el de la versión anterior (PGDG, s. f.-c): un directorio creado por la 17 no lo abre la 18. Hay que migrarlo con volcado y restauración (`pg_dumpall`), con `pg_upgrade` o con replicación lógica. Las versiones menores nunca cambian el formato interno, así que actualizar dentro de la serie 18 sólo implica detener el servidor, cambiar los binarios y volver a arrancar (PGDG, s. f.-b).
2. **Cambia la imagen oficial de Docker.** Desde la 18, `PGDATA` incluye el número de versión (`/var/lib/postgresql/18/docker`) y el volumen declarado pasó a ser `/var/lib/postgresql` (PostgreSQL Docker Community, s. f.). Si con la imagen 18 se monta algo en la ruta vieja `/var/lib/postgresql/data`, aunque esté vacío, el script de arranque lo detecta, muestra un error que recomienda un solo montaje en `/var/lib/postgresql` y el contenedor termina sin arrancar (docker-library, s. f.-b). Lo comprobé con un contenedor de prueba: salió con código 1. Por eso el `compose.yaml` nuevo monta `datos_db:/var/lib/postgresql` y no reutiliza la carpeta `./data` del contenedor de la 17.
3. **Cambia un valor por defecto.** En la 18, `initdb` activa por defecto las sumas de verificación (*checksums*) de los datos, y `pg_upgrade` exige que el clúster viejo y el nuevo coincidan en ese ajuste; para migrar un clúster de la 17 sin checksums hay que crear el nuevo con `--no-data-checksums` (PGDG, 2025). En el contenedor nuevo, `SHOW data_checksums;` responde `on`.

Otras novedades de la 18 son un subsistema de E/S asíncrona que puede acelerar los recorridos secuenciales y el `VACUUM`, la función `uuidv7()`, que genera UUID ordenados por tiempo, y que las columnas generadas ahora son virtuales por defecto: su valor se calcula al leer y no se guarda (PGDG, 2025).

La 18.6 salió el 13 de agosto de 2026, el mismo día que la 17.11 (PGDG, 2026a, 2026b); por eso hoy la etiqueta flotante `postgres:17` descarga la 17.11. La serie 18 tendrá soporte hasta el 14 de noviembre de 2030 (PGDG, s. f.-c). Al fijar `postgres:18.6`, el número mayor dice qué migración hizo falta y el menor qué correcciones trae el contenedor.

---

## Ejercicio 4. Otro stack: MySQL + phpMyAdmin

En `tarea1/mysql/` está el `compose.yaml`. Tiene la misma forma que el de PostgreSQL 18, traducido con la tabla de equivalencias. Usa la imagen oficial sin Dockerfile, así que sólo lleva `image:`.

```console
> docker compose up -d
 phpmyadmin Pulled
 db Pulled
 Network apsw-1151055-mysql_default  Created
 Volume "apsw-1151055-mysql_datos_mysql"  Created
 Container apsw_mysql  Started
 Container apsw_mysql  Waiting
 Container apsw_mysql  Healthy
 Container apsw_phpmyadmin  Started

> docker compose ps
NAME              IMAGE              COMMAND                  SERVICE      CREATED          STATUS                    PORTS
apsw_mysql        mysql:9.7.2        "docker-entrypoint.s…"   db           20 seconds ago   Up 17 seconds (healthy)   33060/tcp, 127.0.0.1:3307->3306/tcp
apsw_phpmyadmin   phpmyadmin:5.2.3   "/docker-entrypoint.…"   phpmyadmin   17 seconds ago   Up 6 seconds              127.0.0.1:8081->80/tcp

> docker compose exec -T -e MYSQL_PWD=practica_local_26o db mysql -u proyecto proyecto -e "SELECT VERSION(); SELECT @@character_set_server, @@collation_server, @@version_comment;"
VERSION()
9.7.2
@@character_set_server	@@collation_server	@@version_comment
utf8mb4	utf8mb4_0900_ai_ci	MySQL Community Server - GPL
```

phpMyAdmin queda en <http://localhost:8081> (usuario `proyecto`, contraseña `practica_local_26o`; servidor `db:3306` ya viene puesto). Dos puertos son distintos a propósito: MySQL se publica en el **3307** porque en mi computadora el 3306 ya lo ocupa un MySQL 8.4 instalado en Windows, y phpMyAdmin usa el **8081** para poder tener encendidos los dos stacks a la vez sin chocar con Adminer en el 8080.

### Equivalencias usadas

El `compose.yaml` de MySQL es el de PostgreSQL 18 traducido línea por línea, con base en la documentación de cada imagen oficial (Docker Community & MySQL Team, s. f.; Düsterhus, s. f.; phpMyAdmin, s. f.-b; PostgreSQL Docker Community, s. f.).

| Concepto | PostgreSQL 18 + Adminer | MySQL 9.7 + phpMyAdmin | Nota |
|---|---|---|---|
| Nombre del proyecto | `name: apsw-1151055-contenedor` | `name: apsw-1151055-mysql` | Distintos, para que los dos stacks convivan. |
| De dónde sale la imagen | `build: .` + `image: postgres-1151055:26o` | `image: mysql:9.7.2` | No hace falta Dockerfile: la imagen oficial ya trae todo. |
| Contenedor | `apsw_db` | `apsw_mysql` | |
| Base inicial | `POSTGRES_DB` | `MYSQL_DATABASE` | |
| Usuario | `POSTGRES_USER` | `MYSQL_USER` | En PostgreSQL ese usuario es superusuario; en MySQL sólo recibe todos los permisos sobre `MYSQL_DATABASE` y no puede llamarse `root` (docker-library, s. f.-a). |
| Contraseña | `POSTGRES_PASSWORD` | `MYSQL_PASSWORD` | |
| Superusuario | No hay variable aparte | `MYSQL_ROOT_PASSWORD` | Obligatoria, salvo que se use `MYSQL_ALLOW_EMPTY_PASSWORD` o `MYSQL_RANDOM_ROOT_PASSWORD`; sin ninguna de las tres el contenedor no se inicializa (docker-library, s. f.-a). |
| Codificación y colación | `POSTGRES_INITDB_ARGS: "--encoding=UTF8 --locale=C"` | `command: --character-set-server=utf8mb4 --collation-server=utf8mb4_0900_ai_ci` | `initdb` sólo se aplica al crear el clúster; las opciones de `mysqld` se aplican en cada arranque. En MySQL 9.7 esos dos ya son los valores por defecto, pero escribirlos deja la decisión a la vista (Oracle Corporation, s. f.-f). Ojo: no ordenan igual. `C` compara bytes y distingue mayúsculas y acentos; `utf8mb4_0900_ai_ci` no distingue ninguno de los dos (*ai*, *accent-insensitive*; *ci*, *case-insensitive*). Lo más parecido a `C` sería `utf8mb4_0900_bin`. |
| Puerto del motor | `127.0.0.1:5434:5432` | `127.0.0.1:3307:3306` | La imagen de MySQL también expone el 33060 (protocolo X), pero no se publica. |
| Variables de puerto del anfitrión | `POSTGRES_PORT` (5434) y `ADMINER_PORT` (8080) | `MYSQL_PORT` (3307) y `PHPMYADMIN_PORT` (8081) | Se cambian en un `.env`. Es `PHPMYADMIN_PORT` y no `PMA_PORT` porque en la imagen `PMA_PORT` es el puerto de MySQL al que se conecta phpMyAdmin. |
| Datos | `datos_db:/var/lib/postgresql` | `datos_mysql:/var/lib/mysql` | Volumen con nombre en los dos. |
| Scripts de inicio | `./initdb:/docker-entrypoint-initdb.d:ro` | Misma ruta; aquí no se usa | En las dos imágenes sólo corren la primera vez, con el directorio de datos vacío (docker-library, s. f.-a, s. f.-b). |
| Carpeta de trabajo | `./:/trabajo` + `working_dir: /trabajo` | No se monta | Aquí no hay scripts propios que correr dentro del contenedor. |
| Healthcheck | `pg_isready` | `mysqladmin ping -h 127.0.0.1 --silent` | Ver abajo. |
| Interfaz web | `adminer:5.5.1` | `phpmyadmin:5.2.3` | |
| Servidor por defecto de la interfaz | `ADMINER_DEFAULT_SERVER: db` | `PMA_HOST: db` y `PMA_PORT: 3306` | |
| Puerto de la interfaz | `127.0.0.1:8080:8080` | `127.0.0.1:8081:80` | phpMyAdmin corre sobre Apache, en el 80. |
| Cliente de línea de comandos | `psql` | `mysql` | |

**El healthcheck de MySQL.** `mysqladmin ping` regresa 0 si el servidor está corriendo, aunque rechace la conexión por acceso denegado (Oracle Corporation, s. f.-e); por eso no necesita usuario ni contraseña para saber si el motor responde. El detalle está en `-h 127.0.0.1`: con `localhost` el cliente se conecta por el socket de Unix y con una IP lo hace por TCP (Oracle Corporation, s. f.-b). Mientras inicializa la base, la imagen levanta un servidor temporal con `--skip-networking`, que sólo atiende por el socket (docker-library, s. f.-a). Por TCP, la prueba sólo pasa cuando ya arrancó el servidor definitivo, después de los scripts de inicio. Eso se vio al levantarlo: el primer chequeo falló (`exit=1`) y el contenedor quedó `healthy` cuando el servidor abrió el puerto 3306, así que phpMyAdmin no intentó conectarse antes de tiempo. Como no lleva variables, el `test:` usa la forma de lista (`CMD`) y no necesita un shell.

### PostgreSQL + Adminer frente a MySQL + phpMyAdmin

| Aspecto | PostgreSQL + Adminer | MySQL + phpMyAdmin |
|---|---|---|
| Motor y versión | PostgreSQL 18.6 | MySQL Community Server 9.7.2 (LTS) |
| Licencia del motor | PostgreSQL License: permisiva, parecida a BSD o MIT (PGDG, s. f.-a) | GPLv2 con un permiso adicional para enlazarlo con software de otra licencia, como OpenSSL; la biblioteca cliente `libmysqlclient` tiene además la *Universal FOSS Exception* (Oracle Corporation, s. f.-c). El propio servidor se identifica como `MySQL Community Server - GPL`. |
| Quién está detrás | PostgreSQL Global Development Group, una comunidad | Oracle Corporation |
| Puerto | 5432 | 3306 (y 33060 para el protocolo X) |
| Cliente de línea de comandos | `psql` | `mysql`, y `mysqladmin` para administrar |
| Interfaz web | Adminer: un solo archivo PHP, de Jakub Vrána, que maneja MySQL, PostgreSQL, SQLite y otros motores (Vrána, s. f.). Por eso al entrar hay que elegir el motor: trae MySQL por defecto | phpMyAdmin: aplicación PHP que en la imagen corre sobre Apache; trabaja sólo con MySQL y MariaDB (phpMyAdmin, s. f.-b) |
| Licencia de la interfaz | Apache 2.0 o GPL 2, a elección (Vrána, s. f.) | GPL 2 (phpMyAdmin, s. f.-a) |
| Descarga comprimida (amd64) | `postgres:18.6` ≈ 162 MB + `adminer:5.5.1` ≈ 44 MB | `mysql:9.7.2` ≈ 271 MB + `phpmyadmin:5.2.3` ≈ 197 MB |
| Espacio en disco (`docker image ls`) | `postgres-1151055:26o` 461 MB + `adminer:5.5.1` 116 MB | `mysql:9.7.2` 934 MB + `phpmyadmin:5.2.3` 575 MB |
| Puerto web en este stack | 8080 | 8081 |
| Cuándo lo usaría | Cuando quiero una licencia permisiva y una interfaz ligera que sirva para varios motores | Cuando el proyecto ya usa MySQL o el equipo ya conoce phpMyAdmin |

Los tamaños de descarga son los que reportaba Docker Hub el 6 de octubre de 2026; los de disco los medí con `docker image ls` después de levantar los stacks. La última fila es mi opinión.

### LTS, innovation y por qué `mysql:9.7.2`

En julio de 2023, con MySQL 8.1.0, Oracle dividió sus versiones en dos líneas: LTS (*Long-Term Support*, soporte a largo plazo) e *Innovation* (Gryp & Lastori, 2023). Las dos se consideran aptas para producción y reciben correcciones de errores y de seguridad (Oracle Corporation, s. f.-d).

| Aspecto | LTS | Innovation |
|---|---|---|
| Qué cambia | Sólo las correcciones necesarias. Dentro de la serie no se quitan funciones; sólo se pueden agregar o quitar en la primera versión de la serie (por ejemplo, 8.4.0) | Funciones nuevas, cambios de comportamiento y eliminación de lo que estaba en desuso |
| Frecuencia | Una serie nueva aproximadamente cada dos años | Una versión aproximadamente cada trimestre |
| Soporte | 5 años de soporte Premier y 3 de soporte extendido | Sólo hasta que sale la siguiente Innovation |
| Para quién | Sistemas que necesitan estabilidad | Equipos que quieren lo más nuevo y tienen pruebas automatizadas |

*Nota.* Elaboración propia con base en Gryp y Lastori (2023) y Oracle Corporation (s. f.-d).

Hoy hay dos series LTS: la 8.4, que fue la primera, y la 9.7. La 9.7 es LTS desde su primera versión, la 9.7.0, que salió el 21 de abril de 2026 (Oracle Corporation, 2026a); el manual explica que se puede actualizar de 8.4 LTS a 9.7 LTS, pero no saltarse una serie LTS (Oracle Corporation, s. f.-d). La 9.7.2 salió el 28 de julio de 2026 (Oracle Corporation, 2026b). Las notas listan también una 9.7.3, del 18 de agosto de 2026, pero es un parche de seguridad publicado sólo para la imagen de Docker de MySQL Server, no un paquete general (Oracle Corporation, 2026c); en la imagen oficial `mysql` de Docker Hub la más reciente de la serie sigue siendo la 9.7.2 (Docker Community & MySQL Team, s. f.). Además, la 9.7 es la última serie con numeración secuencial: las siguientes se nombran con año y mes, como la 26.7 de julio de 2026 (Oracle Corporation, s. f.-d). Ese número indica una fecha, no el grado de compatibilidad como en SemVer.

**¿Por qué `mysql:9.7.2` y no `mysql:latest`?** Al 6 de octubre de 2026, en Docker Hub las etiquetas `latest` e `innovation` apuntan a MySQL **26.7.0**, una versión Innovation, y la etiqueta `lts` apunta a la 9.7.2 (Docker Community & MySQL Team, s. f.). Lo comprobé comparando sus *digests*: `latest` y `26.7.0` tienen el mismo, y `lts` y `9.7.2` otro. Hay tres razones para fijar la versión:

1. **Reproducibilidad.** Una etiqueta de Docker no es fija: quien publica la imagen puede reasignarla. `latest` cambia sin aviso; con `9.7.2` todos descargan la misma versión del motor. Para tener exactamente los mismos bytes también se puede fijar el *digest* (Docker, Inc., s. f.-b).
2. **Mismo resultado en todas las máquinas.** Con `latest`, quien haga `docker compose pull` hoy y quien lo haga en tres meses tendrían motores distintos, y como una Innovation puede quitar funciones, un script podría funcionar en una máquina y fallar en otra. Fijar la versión crea una línea base: un punto de referencia acordado que sólo se cambia de forma controlada (Pressman, 2009).
3. **Soporte largo.** La serie 9.7 tendrá 5 años de soporte Premier y 3 de soporte extendido; una Innovation sólo tiene soporte hasta que sale la siguiente (Oracle Corporation, s. f.-d).

Es lo mismo que se hizo con `postgres:18.6` y que no se hacía con `postgres:17`: una etiqueta como `17` o `latest` dice «la que haya hoy», no «esta».

---

## Ejercicio 5. Capturas

**1. PostgreSQL 17: `docker compose up -d --build` con el aviso de `version`**

![PostgreSQL 17 levantado con el aviso de que version es obsoleta](img/01-pg17-up-build.png)

**2. PostgreSQL 17: `docker compose ps` y `SELECT version();`**

![PostgreSQL 17 en docker compose ps y su versión](img/02-pg17-ps-version.png)

**3. PostgreSQL 18: `docker compose ps` con `(healthy)` y `SELECT version();`**

![PostgreSQL 18 healthy en docker compose ps y su versión](img/03-pg18-ps-version.png)

**4. PostgreSQL 18: Adminer con las tablas**

![Adminer mostrando las tablas integrante, sprint y tarea](img/04-pg18-adminer-tablas.png)

**5. El diff de la confirmación a la 18, en GitHub**

![Diff en GitHub de la confirmación que actualiza a PostgreSQL 18](img/05-github-diff-pg18.png)

**6. phpMyAdmin con `SELECT VERSION();`**

![phpMyAdmin mostrando la versión 9.7.2 de MySQL](img/06-phpmyadmin-version.png)

**7. Docker Desktop con los dos stacks encendidos**

![Docker Desktop con los stacks de PostgreSQL y MySQL encendidos](img/07-docker-desktop-stacks.png)

**8. El historial de confirmaciones en GitHub**

![Historial de confirmaciones del repositorio en GitHub](img/08-github-historial.png)

---

## Uso de inteligencia artificial

En esta tarea usé un asistente de inteligencia artificial como apoyo. Lo usé para:

- buscar y contrastar fuentes para los cuatro apartados del Ejercicio 2 y para los datos de versiones de los Ejercicios 3 y 4, y redactar los borradores de esos textos;
- escribir `initdb/01-tablero.sql`, `extras/comprobar.sh`, `.env.example` y `mysql/compose.yaml` a partir de los archivos del material del curso;
- ejecutar en mi computadora los comandos de Docker y Git con los que se levantaron y comprobaron los tres contenedores, y tomar las ocho capturas. Las salidas y las capturas que aparecen en este README son las reales de esa ejecución.

El `Dockerfile` y el `docker-compose.yml` de PostgreSQL 17, y el `Dockerfile` y el `compose.yaml` de PostgreSQL 18, son los del material del curso, sin cambios.

---

## Referencias

Atlassian. (s. f.). *El ABC de Trello: Cómo utilizar tarjetas y tableros de Trello*. Trello. https://trello.com/es/guide/trello-101

Beck, K., Beedle, M., van Bennekum, A., Cockburn, A., Cunningham, W., Fowler, M., Grenning, J., Highsmith, J., Hunt, A., Jeffries, R., Kern, J., Marick, B., Martin, R. C., Mellor, S., Schwaber, K., Sutherland, J., & Thomas, D. (2001). *Manifiesto por el desarrollo ágil de software*. https://agilemanifesto.org/iso/es/manifesto.html

Buytaert, D. (2010, 8 de marzo). The history of MySQL AB. *Dries Buytaert*. https://dri.es/the-history-of-mysql-ab

Chacon, S., & Straub, B. (2014). *Pro Git* (2.ª ed.). Apress. https://git-scm.com/book/es/v2

Clark, J. (2013, 12 de septiembre). *Google swaps out MySQL, moves to MariaDB*. The Register. https://www.theregister.com/2013/09/12/google_mariadb_mysql_migration/

Clarke, G. (2012, 5 de diciembre). *MySQL founders launch MariaDB Foundation at Oracle*. The Register. https://www.theregister.com/software/2012/12/05/mysql-founders-launch-mariadb-foundation-at-oracle/1469368

Coleman, J., & Vacanti, D. (2025). *La guía Kanban* (A. Fernández-Ceballos, Trad.; versión 2025.5). Kanban Guides. https://kanbanguides.org/es-es/the-kanban-guide/2025.5/

Compose Specification. (s. f.). *The Compose Specification*. GitHub. https://github.com/compose-spec/compose-spec/blob/main/spec.md

Docker Community & MySQL Team. (s. f.). *mysql - Official image*. Docker Hub. https://hub.docker.com/_/mysql

Docker, Inc. (s. f.-a). *Bind mounts*. Docker Docs. https://docs.docker.com/engine/storage/bind-mounts/

Docker, Inc. (s. f.-b). *Building best practices*. Docker Docs. https://docs.docker.com/build/building/best-practices/

Docker, Inc. (s. f.-c). *docker compose*. Docker Docs. https://docs.docker.com/reference/cli/docker/compose/

Docker, Inc. (s. f.-d). *docker compose down*. Docker Docs. https://docs.docker.com/reference/cli/docker/compose/down/

Docker, Inc. (s. f.-e). *docker compose ps*. Docker Docs. https://docs.docker.com/reference/cli/docker/compose/ps/

Docker, Inc. (s. f.-f). *docker compose stop*. Docker Docs. https://docs.docker.com/reference/cli/docker/compose/stop/

Docker, Inc. (s. f.-g). *docker compose up*. Docker Docs. https://docs.docker.com/reference/cli/docker/compose/up/

Docker, Inc. (s. f.-h). *Docker Desktop WSL 2 backend on Windows*. Docker Docs. https://docs.docker.com/desktop/features/wsl/

Docker, Inc. (s. f.-i). *Dockerfile reference*. Docker Docs. https://docs.docker.com/reference/dockerfile/

Docker, Inc. (s. f.-j). *History and development of Docker Compose*. Docker Docs. https://docs.docker.com/compose/intro/history/

Docker, Inc. (s. f.-k). *Networking in Compose*. Docker Docs. https://docs.docker.com/compose/how-tos/networking/

Docker, Inc. (s. f.-l). *Version and name top-level elements*. Docker Docs. https://docs.docker.com/reference/compose-file/version-and-name/

Docker, Inc. (s. f.-m). *Volumes*. Docker Docs. https://docs.docker.com/engine/storage/volumes/

Docker, Inc. (s. f.-n). *What is a container?* https://www.docker.com/resources/what-container/

Docker, Inc. (s. f.-o). *What is Docker?* Docker Docs. https://docs.docker.com/get-started/docker-overview/

docker-library. (s. f.-a). *docker-entrypoint.sh (imagen mysql)* [Código fuente]. GitHub. https://github.com/docker-library/mysql/blob/master/docker-entrypoint.sh

docker-library. (s. f.-b). *docker-entrypoint.sh (imagen postgres 18)* [Código fuente]. GitHub. https://github.com/docker-library/postgres/blob/master/18/trixie/docker-entrypoint.sh

Düsterhus, T. (s. f.). *adminer - Official image*. Docker Hub. https://hub.docker.com/_/adminer

Fedora Project. (s. f.). *Features/ReplaceMySQLwithMariaDB*. Fedora Project Wiki. https://fedoraproject.org/wiki/Features/ReplaceMySQLwithMariaDB

Feldman, A. (2013, 22 de abril). Wikipedia adopts MariaDB. *Diff*. https://diff.wikimedia.org/2013/04/22/wikipedia-adopts-mariadb/

Free Software Foundation. (1991). *GNU General Public License version 2*. Open Source Initiative. https://opensource.org/license/gpl-2-0

Free Software Foundation. (2007). *GNU Lesser General Public License version 3*. Open Source Initiative. https://opensource.org/license/lgpl-3-0

GitHub, Inc. (s. f.-a). *Acerca de Projects*. Documentación de GitHub. https://docs.github.com/es/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects

GitHub, Inc. (s. f.-b). *BSD 3-Clause "New" or "Revised" License*. Choose a License. https://choosealicense.com/licenses/bsd-3-clause/

GitHub, Inc. (s. f.-c). *Descripción de Acciones de GitHub*. Documentación de GitHub. https://docs.github.com/es/actions/get-started/understand-github-actions

GitHub, Inc. (s. f.-d). *GNU Lesser General Public License v3.0*. Choose a License. https://choosealicense.com/licenses/lgpl-3.0/

GitHub, Inc. (s. f.-e). *Licenses*. Choose a License. https://choosealicense.com/licenses/

GitHub, Inc. (s. f.-f). *No license*. Choose a License. https://choosealicense.com/no-permission/

GitHub, Inc. (s. f.-g). *¿Qué es GitHub?* Documentación de GitHub. https://docs.github.com/es/get-started/start-your-journey/what-is-github

Gryp, K., & Lastori, A. (2023, 18 de julio). Introducing MySQL Innovation and Long-Term Support (LTS) versions. *MySQL Blog Archive*. https://dev.mysql.com/blog-archive/introducing-mysql-innovation-and-long-term-support-lts-versions/

Kekäläinen, O. (2017, 18 de junio). Debian 9 released with MariaDB as the only MySQL variant. *MariaDB.org*. https://mariadb.org/debian-9-released-mariadb-mysql-variant/

Kirk, J. (2008, 16 de enero). Update: Sun to acquire MySQL for $1B. *Computerworld*. https://www.computerworld.com/article/1579016/update-sun-to-acquire-mysql-for-1b.html

Lewis, J. P. (2007). *Fundamentals of project management* (3.ª ed.). AMACOM.

MariaDB Foundation. (s. f.-a). *About MariaDB Server*. MariaDB.org. https://mariadb.org/about/

MariaDB Foundation. (s. f.-b). *MariaDB in brief*. MariaDB.org. https://mariadb.org/en/

McAllister, N. (2013, 15 de junio). *Red Hat to ditch MySQL for MariaDB in RHEL 7*. The Register. https://www.theregister.com/2013/06/15/red_hat_to_ditch_mysql_for_mariadb_in_rhel_7/

Open Source Initiative. (s. f.). *The MIT License*. https://opensource.org/license/mit

Oracle Corporation. (s. f.-a). *Commercial license for OEMs, ISVs and VARs*. MySQL. https://www.mysql.com/about/legal/licensing/oem/

Oracle Corporation. (s. f.-b). Connecting to the MySQL server using command options. En *MySQL 9.7 reference manual*. https://dev.mysql.com/doc/refman/9.7/en/connecting.html

Oracle Corporation. (s. f.-c). *LICENSE* [Archivo de licencia de MySQL 9.7.2 Community]. GitHub. https://github.com/mysql/mysql-server/blob/9.7/LICENSE

Oracle Corporation. (s. f.-d). MySQL releases: Innovation and LTS. En *MySQL 9.7 reference manual*. https://dev.mysql.com/doc/refman/9.7/en/mysql-releases.html

Oracle Corporation. (s. f.-e). mysqladmin — A MySQL server administration program. En *MySQL 9.7 reference manual*. https://dev.mysql.com/doc/refman/9.7/en/mysqladmin.html

Oracle Corporation. (s. f.-f). Server character set and collation. En *MySQL 9.7 reference manual*. https://dev.mysql.com/doc/refman/9.7/en/charset-server.html

Oracle Corporation. (2010, 27 de enero). *Oracle completes acquisition of Sun* [Comunicado de prensa]. U.S. Securities and Exchange Commission. https://www.sec.gov/Archives/edgar/data/1341439/000119312510015241/dex991.htm

Oracle Corporation. (2026a, 21 de abril). *Changes in MySQL 9.7.0 (2026-04-21)*. MySQL 9.7 Release Notes. https://dev.mysql.com/doc/relnotes/mysql/9.7/en/news-9-7-0.html

Oracle Corporation. (2026b, 28 de julio). *Changes in MySQL 9.7.2 (2026-07-28)*. MySQL 9.7 Release Notes. https://dev.mysql.com/doc/relnotes/mysql/9.7/en/news-9-7-2.html

Oracle Corporation. (2026c, 18 de agosto). *Changes in MySQL 9.7.3 (2026-08-18)*. MySQL 9.7 Release Notes. https://dev.mysql.com/doc/relnotes/mysql/9.7/en/news-9-7-3.html

Oracle Corporation & Sun Microsystems. (2009, 20 de abril). *Oracle to buy Sun* [Comunicado de prensa]. U.S. Securities and Exchange Commission. https://www.sec.gov/Archives/edgar/data/0000709519/000119312509082650/dex991.htm

phpMyAdmin. (s. f.-a). *License*. https://www.phpmyadmin.net/license/

phpMyAdmin. (s. f.-b). *phpmyadmin - Official image*. Docker Hub. https://hub.docker.com/_/phpmyadmin

Pollack, J., Helm, J., & Adler, D. (2018). What is the Iron Triangle, and how has it changed? *International Journal of Managing Projects in Business, 11*(2), 527–547. https://doi.org/10.1108/IJMPB-09-2017-0107

PostgreSQL Docker Community. (s. f.). *postgres - Official image*. Docker Hub. https://hub.docker.com/_/postgres

PostgreSQL Global Development Group. (s. f.-a). *License*. PostgreSQL. https://www.postgresql.org/about/licence/

PostgreSQL Global Development Group. (s. f.-b). Upgrading a PostgreSQL cluster. En *PostgreSQL 18 documentation*. https://www.postgresql.org/docs/18/upgrading.html

PostgreSQL Global Development Group. (s. f.-c). *Versioning policy*. PostgreSQL. https://www.postgresql.org/support/versioning/

PostgreSQL Global Development Group. (2025, 25 de septiembre). *Release 18*. PostgreSQL. https://www.postgresql.org/docs/release/18.0/

PostgreSQL Global Development Group. (2026a, 13 de agosto). *Release 17.11*. PostgreSQL. https://www.postgresql.org/docs/release/17.11/

PostgreSQL Global Development Group. (2026b, 13 de agosto). *Release 18.6*. PostgreSQL. https://www.postgresql.org/docs/release/18.6/

Pressman, R. S. (2009). *Software engineering: A practitioner's approach* (7.ª ed.). McGraw-Hill.

Preston-Werner, T. (s. f.). *Versionado semántico 2.0.0*. Semantic Versioning. https://semver.org/lang/es/

Project Management Institute. (2017). *A guide to the project management body of knowledge (PMBOK guide)* (6.ª ed.).

Project Management Institute. (2021a). *A guide to the project management body of knowledge (PMBOK guide) and the standard for project management* (7.ª ed.).

Project Management Institute. (2021b). *PMBOK guide – Seventh edition FAQs*. https://www.pmi.org/-/media/pmi/documents/public/pdf/pmbok-standards/pmbok-guide-public-faqs-1-july-2021.pdf

Project Management Institute. (2025). *A guide to the project management body of knowledge (PMBOK guide)* (8.ª ed.).

Schwaber, K., & Sutherland, J. (2020). *La guía de Scrum: La guía definitiva de Scrum: Las reglas del juego* (M. López, M. García, J. Abad, F. Schwartz y L. Salazar, Trads.). Scrum Guides. https://scrumguides.org/docs/scrumguide/v2020/2020-Scrum-Guide-Spanish-Latin-South-American.pdf

Sommerville, I. (2005). *Ingeniería del software* (M. I. Alfonso Galipienso, A. Botía Martínez, F. Mora Lizán y J. P. Trigueros Jover, Trads.; 7.ª ed.). Pearson Educación. (Trabajo original publicado en 2004)

Vrána, J. (s. f.). *Adminer: Database management in a single PHP file*. Adminer. https://www.adminer.org/en/
