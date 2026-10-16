# Tarea 2 · Entorno móvil e inteligencia artificial con MCP

| | |
|---|---|
| **UEA y clave** | Administración de Proyectos de Software (1151055) |
| **Trimestre** | 26-O, otoño 2026 |
| **Licenciatura** | Ingeniería en Computación |
| **Nombre** | Max Uriel Sánchez Díaz |
| **Matrícula** | 2213026327 |
| **Profesor** | M. en C. Gabriel Hurtado Avilés |
| **Fecha** | 16 de octubre de 2026 |

Universidad Autónoma Metropolitana, Unidad Azcapotzalco · División de Ciencias Básicas e Ingeniería · Departamento de Sistemas

## Contenido

1. [Resumen](#resumen)
2. [Parte 1. El entorno de desarrollo móvil](#parte-1-el-entorno-de-desarrollo-móvil)
3. [Parte 2. MCP: investigación](#parte-2-mcp-investigación)
4. [Parte 3. MCP: implementación](#parte-3-mcp-implementación)
5. [Capturas](#capturas)
6. [Exposición](#exposición)
7. [Conclusiones](#conclusiones)
8. [Uso de inteligencia artificial](#uso-de-inteligencia-artificial)
9. [Referencias](#referencias)

---

## Resumen

La tarea tiene dos objetivos. El primero es dejar lista la computadora y el teléfono para la app de navegación del proyecto: instalé Flutter, completé el SDK de Android y corrí los dos ejemplos del profesor, HolaMundoFlutter y HolaMundoKMP, en mi teléfono. El segundo es entender cómo la IA pasó de estar encerrada en un navegador a operar sobre los archivos de un proyecto: investigué el Model Context Protocol (MCP) en la revisión **2026-07-28** de su especificación y dejé funcionando en Claude Desktop el servidor de sistema de archivos, limitado a una carpeta creada para esta tarea. Como punto extra, escribí un servidor MCP propio con el SDK oficial de Python.

Estructura de la entrega:

```text
tarea2/
├── README.md                 este documento
├── docs/                     la investigación, un archivo por punto
├── config/
│   ├── claude_desktop_config.json   la configuración de MCP que usé, sin credenciales
│   └── instalar-mcp.mjs             la registra en Claude Desktop en cualquier máquina
├── img/                      capturas de la instalación y de MCP
├── presentacion/             diapositivas y guion de la exposición
├── sandbox/                  la única carpeta que ve el servidor de archivos
└── servidor-propio/          servidor MCP «entregas-apsw» (opcional)
    ├── servidor.py
    ├── comprobar.py          cliente de prueba por línea de comandos
    └── requirements.txt
```

---

## Parte 1. El entorno de desarrollo móvil

Cloné los dos repositorios del profesor en `C:\dev` (una ruta corta y sin acentos, como recomienda su guía) y seguí sus README (Hurtado Avilés, 2026a, 2026b).

```powershell
git clone https://github.com/gabrielhuav/Flutter-Projects.git C:\dev\Flutter-Projects
git clone https://github.com/gabrielhuav/HolaMundoKMP.git C:\dev\HolaMundoKMP
```

### Lo que instalé

| Pieza | Versión |
|---|---|
| Sistema operativo | Windows 11 Pro 25H2, compilación 10.0.26200.9711 |
| Android Studio | 2026.2.1 (compilación AI-262.9437.185.2621.16467767), con su JDK OpenJDK 25.0.3 |
| Flutter | 3.47.7, canal stable, revisión `abaf9c5237` del 8 de octubre de 2026 |
| Dart | 3.13.5 (incluido en Flutter), DevTools 2.60.0 |
| SDK de Android | Platforms `android-37.0`, `android-36.1` y `android-35`; Build-Tools 37.0.0; Platform-Tools 37.0.0; Emulator 36.5.11; Command-line Tools *[versión que instaló el SDK Manager]* |
| Dispositivo | *[modelo del teléfono]*, Android *[versión]* (API *[nivel]*) |

### 1. Android Studio y las Command-line Tools

Android Studio ya estaba instalado, pero `flutter doctor` marcó que faltaba el componente `cmdline-tools`. Lo instalé desde **Settings → Languages & Frameworks → Android SDK → SDK Tools**, marcando **Android SDK Command-line Tools (latest)** → **Apply** ([captura 1](#capturas)).

### 2. Flutter

Instalé Flutter clonando el canal stable y agregando su carpeta `bin` al `PATH` de mi usuario:

```powershell
git clone -b stable https://github.com/flutter/flutter.git C:\dev\flutter
[Environment]::SetEnvironmentVariable('Path', [Environment]::GetEnvironmentVariable('Path','User') + ';C:\dev\flutter\bin', 'User')
flutter --version
```

```text
Flutter 3.47.7 • channel stable • https://github.com/flutter/flutter.git
Framework • revision abaf9c5237 (8 days ago) • 2026-10-08 09:51:21 -0700
Engine • hash d8a2d6c768c334d53e16277f837970ffa1e2de81 (revision deb287481e) (8 days ago) • 2026-10-07 17:09:12.000Z
Tools • Dart 3.13.5 • DevTools 2.60.0
```

La primera ejecución descarga el SDK de Dart y el motor de Flutter ([captura 2](#capturas)).

### 3. flutter doctor

Con las Command-line Tools instaladas, acepté las licencias del SDK y volví a correr el diagnóstico:

```powershell
flutter doctor --android-licenses
flutter doctor
```

Debe salir **[√] Flutter** y **[√] Android toolchain** ([captura 3](#capturas)). La advertencia de Visual Studio no importa aquí: sólo hace falta para compilar aplicaciones de escritorio para Windows, no para Android (Hurtado Avilés, 2026a).

### 4. El teléfono en modo desarrollador

1. **Ajustes → Acerca del teléfono → Número de compilación**, siete toques, hasta que aparece «Ahora eres desarrollador».
2. **Ajustes → Sistema → Opciones de desarrollador → Depuración por USB**, activada ([captura 4](#capturas)).
3. Conecté el teléfono por USB y acepté en su pantalla la huella RSA de la computadora.
4. `flutter devices` lo lista junto a Windows, Chrome y Edge ([captura 5](#capturas)).

La pantalla «Acerca del teléfono» muestra el número y el IMEI; por eso la captura 4 es de las opciones de desarrollador, no de esa pantalla.

### 5. HolaMundoFlutter en el teléfono

```powershell
cd C:\dev\Flutter-Projects\HolaMundoFlutter
flutter pub get
flutter run -d <id del teléfono>
```

La app muestra el saludo «¡Hola, Mundo!» con el nombre del sistema y un contador que sube con el botón «Tócame» ([captura 6](#capturas)). Antes de conectar el teléfono comprobé que compila con `flutter build apk --debug`, que generó `build\app\outputs\flutter-apk\app-debug.apk` en 231 s la primera vez, porque Gradle descarga sus dependencias.

### 6. HolaMundoKMP desde Android Studio

1. **File → Open** → `C:\dev\HolaMundoKMP` y esperar a que termine el *Gradle sync*.
2. Arriba, elegir la configuración **androidApp** y el teléfono como dispositivo.
3. **Run ▶** ([captura 7](#capturas)).

Antes lo compilé desde la terminal con el JDK de Android Studio para tener listas las dependencias:

```powershell
$env:JAVA_HOME = 'C:\Program Files\Android\Android Studio\jbr'
.\gradlew.bat :androidApp:assembleDebug
# BUILD SUCCESSFUL in 2m 8s
```

Un detalle: el archivo `local.properties` que le dice a Gradle dónde está el SDK debe escribir la ruta con `/` o con `\\`. Con una sola `\` (`C:\Users\…`), Java la lee como secuencia de escape y Gradle falla con `java.io.IOException: Invalid file path`. Android Studio lo genera bien solo; el error me salió al escribirlo a mano.

---

## Parte 2. MCP: investigación

Cada punto está en su archivo de [`docs/`](docs/), con sus propias referencias:

| # | Documento | De qué trata |
|---|---|---|
| 1 | [Evolución de los modelos](docs/01-evolucion-de-los-modelos.md) | Qué es un modelo de lenguaje, cómo llegó a ser un LLM y de dónde sale el razonamiento explícito: entrenamiento y cómputo al responder, no sólo tamaño. |
| 2 | [El problema del aislamiento](docs/02-el-problema-del-aislamiento.md) | Por qué un LLM solo no ve ni toca archivos: razones de arquitectura frente a razones de seguridad. |
| 3 | [MCP frente a una API](docs/03-mcp-frente-a-una-api.md) | El punto central: contrato fijo frente a catálogo que el modelo descubre, con mensajes JSON-RPC reales. |
| 4 | [Arquitectura](docs/04-arquitectura.md) | Host, cliente y servidor en lo que instalé; primitivas, transportes y el cambio de ciclo de vida de 2026-07-28. |
| 5 | [El servidor de sistema de archivos](docs/05-servidor-de-sistema-de-archivos.md) | Sus 14 herramientas, cómo lo limitan los directorios permitidos y qué pasaría sin ese límite. |
| 6 | [Seguridad](docs/06-seguridad.md) | Inyección de instrucciones, salir de la carpeta y escrituras no deseadas; las mitigaciones que apliqué. |
| 7 | [Casos de uso](docs/07-casos-de-uso.md) | Siete herramientas actuales con MCP y cómo editan un repositorio completo sin subir archivos. |

**Versión de la especificación consultada:** revisión **2026-07-28** de la especificación de MCP, la vigente, publicada el 28 de julio de 2026 y consultada el 15 de octubre de 2026 (Model Context Protocol, 2026h, s. f.-f). Para el *handshake* `initialize`, que esa revisión eliminó, consulté también la revisión 2025-11-25.

### La tabla MCP frente a API

El resumen del [punto 3](docs/03-mcp-frente-a-una-api.md#tabla-comparativa):

| Aspecto | API | MCP |
|---|---|---|
| Quién decide qué se invoca | El programador, de antemano, en el código | El modelo, en el momento, entre las herramientas del catálogo; el usuario aprueba |
| Cómo se descubren las capacidades | Leyendo la documentación antes de programar | Preguntándole al servidor: `tools/list`, `resources/list`, `prompts/list` |
| Acoplamiento | Fuerte: un cambio en la API rompe el cliente | Débil: el cliente sólo conoce el protocolo |
| Formato de los mensajes | El que defina cada API | Siempre JSON-RPC 2.0 |
| Autenticación y consentimiento | Llaves o tokens en cada petición; nadie aprueba cada llamada | OAuth 2.1 en HTTP; credenciales locales en stdio; el host pide permiso antes de cada herramienta |
| Reutilización entre aplicaciones | Una integración por aplicación y por API (N × M) | Un servidor sirve a cualquier host compatible (N + M) |

**MCP no sustituye a las APIs:** casi siempre envuelve una. El servidor de archivos envuelve la API de archivos de Node.js, y el de GitHub, la API REST de GitHub.

---

## Parte 3. MCP: implementación

### 1. Cliente: Claude Desktop

Elegí **Claude Desktop** (versión 2.42304 para Windows) por cuatro razones:

- Ya lo tenía instalado y es el host con el que se presentó MCP, así que la documentación oficial del protocolo lo usa en su guía para conectar servidores locales (Model Context Protocol, s. f.-a).
- Se configura con un solo archivo JSON que se puede versionar, sin extensiones ni cuentas extra.
- Muestra cada llamada a una herramienta, con sus argumentos y su resultado, y pide permiso antes de ejecutarla. Eso es justo lo que hay que enseñar en la demostración.
- Permite conectar varios servidores a la vez, así que el servidor propio va al mismo cliente.

### 2. Servidor de sistema de archivos: instalación paso a paso

Probado en Windows 11 Pro 25H2 con Node.js 24.14.0, npm 11.11.1, Python 3.13.4 y Claude Desktop 2.42304. En una máquina limpia:

1. **Instalar Node.js** (versión LTS o más reciente) desde https://nodejs.org y comprobar en una terminal nueva:

   ```powershell
   node --version   # v24.14.0
   npx --version    # 11.11.1
   ```

2. **Instalar Claude Desktop** desde https://claude.com/download e iniciar sesión.

3. **Clonar este repositorio.** La carpeta autorizada, `tarea2/sandbox/`, viene incluida con cuatro archivos de ejemplo:

   ```powershell
   git clone https://github.com/maxitodev/administracion_uam_a.git
   ```

4. **(Opcional) Probar el servidor sin cliente.** El script `comprobar.py` hace lo mismo que Claude Desktop: lanza el servidor, pide su catálogo y llama algunas herramientas (para el entorno de Python, ver el [paso 5](#5-opcional-servidor-propio)):

   ```powershell
   cd administracion_uam_a\tarea2\servidor-propio
   .venv\Scripts\python.exe comprobar.py archivos ..\sandbox
   ```

   ```text
   Servidor: secure-filesystem-server 1.0.0 · protocolo 2025-11-25
   tools/list devolvió 14 herramientas:
     - read_text_file (sólo lectura): Read the complete contents of a file from the file system as text. …
     - write_file: Create a new file or completely overwrite an existing file with new content. …
     …
   >>> list_allowed_directories [ok]
   Allowed directories:
   C:\Users\maxsa\Documents\UAM-A\administracion_uam_a\tarea2\sandbox
   >>> leer un archivo fuera de la carpeta [ERROR]
   Access denied - path outside allowed directories: C:\Users\maxsa\Documents\UAM-A\administracion_uam_a\tarea2\README.md not in C:\Users\maxsa\Documents\UAM-A\administracion_uam_a\tarea2\sandbox
   ```

5. **Registrar el servidor en Claude Desktop.** Hay dos formas:

   - **A mano.** Menú de Claude → **Settings… → Developer → Edit Config**. Se abre `%APPDATA%\Claude\claude_desktop_config.json`. Agregar la clave `mcpServers` del [archivo de configuración](#archivo-de-configuración) con las rutas de la máquina, guardar, y **cerrar Claude Desktop por completo** desde el icono de la bandeja (no basta con cerrar la ventana).
   - **Con el script.** Cerrar Claude Desktop desde la bandeja y correr `node tarea2\config\instalar-mcp.mjs`. El script calcula las rutas según dónde esté clonado el repositorio, respeta lo que ya tenga el archivo y deja un respaldo `.bak`.

   Un aviso, porque me pasó: Claude Desktop guarda sus preferencias en ese mismo archivo y lo reescribe mientras está abierto. Si se edita con la app encendida, puede borrar lo que se agregó. Por eso el script se niega a correr si la encuentra abierta.

6. **Comprobar que el cliente lo reconoce.** Al abrir Claude Desktop, **Settings → Developer** debe mostrar `sistema-archivos` y `entregas-apsw` como *running* ([captura 8](#capturas)). En el botón **+** de la caja de mensaje → **Connectors**, `sistema-archivos` lista sus 14 herramientas ([captura 9](#capturas)). Si algo falla, el registro está en `%APPDATA%\Claude\logs\mcp-server-sistema-archivos.log`.

#### Archivo de configuración

El contenido de [`config/claude_desktop_config.json`](config/claude_desktop_config.json), sin credenciales. Ninguno de los dos servidores necesita llaves ni tokens: trabajan con archivos locales.

```json
{
  "mcpServers": {
    "sistema-archivos": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem@1.0.0",
        "C:\\Users\\maxsa\\Documents\\UAM-A\\administracion_uam_a\\tarea2\\sandbox"
      ]
    },
    "entregas-apsw": {
      "command": "C:\\Users\\maxsa\\Documents\\UAM-A\\administracion_uam_a\\tarea2\\servidor-propio\\.venv\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\maxsa\\Documents\\UAM-A\\administracion_uam_a\\tarea2\\servidor-propio\\servidor.py",
        "C:\\Users\\maxsa\\Documents\\UAM-A\\administracion_uam_a"
      ]
    }
  }
}
```

- `npx -y` descarga el paquete la primera vez y lo ejecuta. La versión va fija (`@1.0.0`) para que no cambie sola: ver el *rug pull* en el [punto 6](docs/06-seguridad.md).
- El último argumento es la **única carpeta permitida**: `tarea2/sandbox/`, creada para esta tarea. Nunca la raíz del disco ni la carpeta de usuario completa.

### 3. Operaciones

Cada operación la pedí en lenguaje natural en un chat de Claude Desktop. El modelo eligió la herramienta y Claude Desktop pidió permiso antes de ejecutarla.

| # | Lo que pedí | Herramienta que usó el modelo | Captura |
|---|---|---|---|
| 1 | «Lista el contenido de la carpeta que tienes permitida en sistema-archivos.» | `list_allowed_directories`, `list_directory` | [10](#capturas) |
| 2 | «Lee `proyecto/bitacora.md` y dime qué se hizo el 15 de octubre.» | `read_text_file` | [11](#capturas) |
| 3 | «Crea `proyecto/minuta-2026-10-16.md` con una minuta breve: fecha, asistente (yo) y dos acuerdos: probar MCP y grabar el video de respaldo.» | `write_file` | [12](#capturas) |
| 4 | «En `proyecto/pendientes.md` marca como hechas las dos primeras tareas.» | `edit_file` (devuelve el *diff*) | [13](#capturas) |
| 5 | «Busca todos los archivos `.md` de la carpeta y dime cuál menciona Gradle.» | `search_files` con `**/*.md` y después `read_text_file` | [14](#capturas) |

La búsqueda del servidor es por nombre (patrones *glob*); para buscar por contenido, el modelo combinó la búsqueda por nombre con la lectura de cada archivo. Los archivos que creó y modificó quedaron en [`sandbox/`](sandbox/) y en el historial del repositorio.

### 4. El límite de seguridad

Le pedí un archivo que está fuera de la carpeta autorizada:

> «Lee el archivo `C:\Users\maxsa\Documents\UAM-A\administracion_uam_a\tarea2\README.md`.»

**Lo que respondió el modelo:** *[resumen de la respuesta de Claude, ver captura 15]*.

**Qué mecanismo lo impidió:** el modelo sí intentó usar `read_text_file`, pero el servidor normalizó la ruta, la comparó con su lista de directorios permitidos y la rechazó antes de tocar el disco, con este error:

```text
Access denied - path outside allowed directories: C:\Users\maxsa\Documents\UAM-A\administracion_uam_a\tarea2\README.md not in C:\Users\maxsa\Documents\UAM-A\administracion_uam_a\tarea2\sandbox
```

No lo detuvo el modelo ni su «buena voluntad»: lo detuvo el código del servidor, que es determinista y no depende de cómo se redacte la petición. Lo mismo pasa con `..\README.md` o con un enlace simbólico que apunte afuera, porque el servidor resuelve la ruta real con `realpath` antes de compararla ([punto 5](docs/05-servidor-de-sistema-de-archivos.md#cómo-lo-limitan-los-directorios-permitidos)). Encima de esa capa está la confirmación de Claude Desktop: aun dentro de la carpeta, ninguna herramienta corre sin que yo la apruebe.

### 5. Opcional: servidor propio

En [`servidor-propio/`](servidor-propio/) está **entregas-apsw**, un servidor MCP que revisa las entregas de este repositorio. Está hecho con el SDK oficial de Python, el paquete `mcp` 2.3.0 (Model Context Protocol, 2026f, s. f.-d). En la versión 2 del SDK, la clase `FastMCP` cambió de nombre a `MCPServer` (Model Context Protocol, s. f.-c).

| Primitiva | Nombre | Qué hace |
|---|---|---|
| Tool | `revisar_entrega(tarea)` | Compara la carpeta de una tarea con la estructura que pide su enunciado y dice qué falta. |
| Tool | `buscar_credenciales(subcarpeta)` | Busca en los archivos de texto cosas con forma de token, llave o contraseña antes de hacer push. Muestra sólo el principio de cada coincidencia. |
| Tool | `dias_para_entrega(fecha_limite, fecha_entrega)` | Dice cuánto falta o, si ya pasó, los días de retraso y el descuento del curso (10 % por día, máximo diez días). |
| Resource | `apsw://reglas-entrega` | Las reglas de entrega del curso. |

Las tres herramientas son de sólo lectura (`readOnlyHint: true`) y, como el servidor de archivos, sólo trabajan dentro de la carpeta que reciben como argumento: cualquier ruta que resuelva fuera de ella se rechaza.

Instalación y prueba:

```powershell
cd tarea2\servidor-propio
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe comprobar.py propio ..\..
```

```text
Servidor: entregas-apsw 1.0.0 · protocolo 2026-07-28

tools/list devolvió 3 herramientas:
  - revisar_entrega (sólo lectura): Revisa que la carpeta de una tarea (por ejemplo «tarea2») tenga lo que pide el enunciado.
  - buscar_credenciales (sólo lectura): Busca en los archivos de texto del repositorio cosas con forma de token, llave o contraseña.
  - dias_para_entrega (sólo lectura): Calcula cuánto falta para la fecha límite o, si ya pasó, el retraso y su descuento.

>>> buscar_credenciales [ok]
4 posible(s) credencial(es) en 17 archivos:
  tarea1/mysql/compose.yaml:33  token o contraseña asignados  (PASSWORD…)
  tarea1/mysql/compose.yaml:36  token o contraseña asignados  (PASSWORD…)
  tarea1/postgres/.env.example:11  token o contraseña asignados  (PASSWORD…)
  tarea1/postgres/compose.yaml:51  token o contraseña asignados  (PASSWORD…)

>>> dias_para_entrega [ok]
Tarde por 2 día(s): la calificación se reduce 20 %.

>>> salir de la raíz [ERROR]
Error executing tool buscar_credenciales: Acceso denegado: «..» queda fuera de C:\Users\maxsa\Documents\UAM-A\administracion_uam_a
```

Las cuatro coincidencias son las contraseñas de desarrollo por omisión de los contenedores de la Tarea 1 (`${MYSQL_PASSWORD:-practica_local_26o}` y similares), que sólo funcionan en `127.0.0.1`. No son secretos, pero es justo lo que conviene revisar antes de cada push. Este servidor negocia la revisión 2026-07-28, la nueva y sin *handshake*, mientras que el de archivos usa la 2025-11-25.

Está conectado al mismo cliente, en la entrada `entregas-apsw` del archivo de configuración. En la [captura 16](#capturas), Claude Desktop lo usa para revisar si esta tarea está completa.

---

## Capturas

**1. SDK Manager con las Command-line Tools marcadas**

![SDK Manager de Android Studio con Android SDK Command-line Tools marcado](img/01-sdk-manager-cmdline-tools.png)

**2. `flutter --version`**

![Salida de flutter --version con Flutter 3.47.7 y Dart 3.13.5](img/02-flutter-version.png)

**3. `flutter doctor`**

![flutter doctor con Flutter y Android toolchain en verde](img/03-flutter-doctor.png)

**4. Opciones de desarrollador con la depuración USB activada**

![Opciones de desarrollador del teléfono con la depuración por USB activada](img/04-telefono-depuracion-usb.png)

**5. `flutter devices` con el teléfono**

![flutter devices mostrando el teléfono conectado](img/05-flutter-devices.png)

**6. HolaMundoFlutter en el teléfono**

![La app HolaMundoFlutter corriendo en el teléfono](img/06-holamundoflutter-telefono.png)

**7. HolaMundoKMP en el teléfono, desde Android Studio**

![Android Studio ejecutando androidApp de HolaMundoKMP en el teléfono](img/07-holamundokmp-android-studio.png)

**8. Claude Desktop reconoce los dos servidores**

![Ajustes de desarrollador de Claude Desktop con sistema-archivos y entregas-apsw en ejecución](img/08-claude-desktop-servidores.png)

**9. Las herramientas de `sistema-archivos`**

![Menú de conectores de Claude Desktop con las herramientas del servidor de archivos](img/09-herramientas-sistema-archivos.png)

**10. Listar la carpeta**

![Claude usando list_directory sobre la carpeta sandbox](img/10-op-listar.png)

**11. Leer un archivo**

![Claude usando read_text_file sobre bitacora.md](img/11-op-leer.png)

**12. Crear un archivo nuevo**

![Claude usando write_file para crear la minuta](img/12-op-crear.png)

**13. Modificar un archivo existente**

![Claude usando edit_file sobre pendientes.md con el diff](img/13-op-modificar.png)

**14. Buscar por nombre y por contenido**

![Claude usando search_files y read_text_file para encontrar el archivo que menciona Gradle](img/14-op-buscar.png)

**15. El límite de seguridad**

![Claude intentando leer un archivo fuera de la carpeta y el servidor negando el acceso](img/15-limite-seguridad.png)

**16. El servidor propio en Claude Desktop**

![Claude usando revisar_entrega de entregas-apsw](img/16-servidor-propio.png)

---

## Exposición

Las diapositivas están en [`presentacion/`](presentacion/): [`diapositivas.md`](presentacion/diapositivas.md) (en formato Marp; también exportadas a [HTML](presentacion/diapositivas.html)) y el [guion](presentacion/guion.md) con los tiempos, la demostración en vivo y el plan B del video de respaldo. Las dos preguntas que hay que poder contestar:

- **¿En qué se diferencia MCP de consumir una API?** En una API, yo decido en el código qué se llama y cuándo; el contrato es fijo y cada aplicación integra cada API por su cuenta. En MCP, el servidor publica un catálogo que el modelo descubre en el momento y decide qué usar, con mi aprobación. Además, el mismo servidor sirve a cualquier host. Y MCP no reemplaza a la API: la envuelve.
- **¿Qué habilita exactamente el servidor de sistema de archivos?** Catorce herramientas para listar, leer, buscar por nombre, crear, editar y mover archivos, **sólo** dentro de las carpetas que recibe al arrancar (aquí, `tarea2/sandbox/`). Fuera de ellas no habilita nada: rechaza la ruta antes de tocar el disco, aunque el modelo la pida.

---

## Conclusiones

Lo más importante que aprendí es que el modelo nunca «entra» a mi computadora. Sigue siendo un programa remoto que recibe texto y devuelve texto. Lo que cambió es que ahora hay un programa local, el servidor MCP, que ejecuta por él un conjunto pequeño y explícito de operaciones. MCP no le da poderes al modelo: estandariza cómo se le ofrecen herramientas y deja en manos del host y del usuario qué se permite. La diferencia con una API no está en la tecnología, que de hecho sigue debajo, sino en quién decide qué se llama: antes, el programador al escribir el código; ahora, el modelo al leer el catálogo, con una persona que aprueba.

La segunda conclusión es de seguridad. El límite de carpetas funcionó: el servidor rechazó la ruta de afuera sin importar cómo la pidiera. Pero ese límite lo pone el código del servidor, no el sistema operativo, así que vale lo que valga ese código. Por eso combiné varias capas: una carpeta creada sólo para esto, una versión fija del paquete, confirmación antes de cada herramienta y todo dentro de Git para poder deshacer.

En la parte móvil, lo que más costó no fue Flutter sino lo que lo rodea: el componente del SDK que faltaba, las licencias y una ruta mal escapada en `local.properties`. La computadora y el teléfono quedaron listos para la app del proyecto, y la investigación también me sirve para el proceso del equipo: un agente con MCP puede leer el repositorio, abrir *issues* y proponer cambios, pero cada cambio debe seguir pasando por el mismo recorrido de rama, *pull request* y revisión.

Y una nota sobre la investigación: la especificación cambió en julio de 2026 y quitó el *handshake* que todavía explican la mayoría de los tutoriales, incluido el video del curso. Indicar la versión consultada no es un trámite: entre una revisión y otra cambia la respuesta.

---

## Uso de inteligencia artificial

En esta tarea usé un asistente de inteligencia artificial como apoyo. Lo usé para:

- buscar y verificar las fuentes de los siete puntos de la investigación y redactar los borradores de `docs/`, que después revisé;
- instalar Flutter, clonar los repositorios del profesor y compilar las dos apps desde la terminal antes de correrlas en el teléfono;
- escribir el servidor `entregas-apsw`, el cliente de prueba `comprobar.py`, el instalador `instalar-mcp.mjs` y los archivos de ejemplo de `sandbox/`, y probarlos;
- redactar este README y las diapositivas.

Conecté el teléfono, corrí las apps en él, hice la demostración en Claude Desktop y tomé las capturas. Las salidas de terminal que aparecen en este README son las reales de esas ejecuciones.

---

## Referencias

Anthropic. (2024, 25 de noviembre). *Introducing the Model Context Protocol*. https://www.anthropic.com/news/model-context-protocol

Anthropic. (2025, 9 de diciembre). *Donating the Model Context Protocol and establishing the Agentic AI Foundation*. https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation

Anthropic. (s. f.-a). *Connect Claude Code to tools via MCP*. Claude Code Docs. Recuperado el 15 de octubre de 2026, de https://code.claude.com/docs/en/mcp

Anthropic. (s. f.-b). *Extended thinking*. Claude Platform Docs. Recuperado el 15 de octubre de 2026, de https://platform.claude.com/docs/en/build-with-claude/extended-thinking

Anthropic. (s. f.-c). *Tool use with Claude*. Claude Platform Docs. Recuperado el 15 de octubre de 2026, de https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview

Anysphere. (s. f.). *Model Context Protocol (MCP)*. Cursor Docs. Recuperado el 15 de octubre de 2026, de https://cursor.com/docs/context/mcp

Bengio, Y., Ducharme, R., Vincent, P., & Jauvin, C. (2003). A neural probabilistic language model. *Journal of Machine Learning Research, 3*, 1137–1155. https://www.jmlr.org/papers/v3/bengio03a.html

Beurer-Kellner, L., & Fischer, M. (2025, 1 de abril). *MCP security notification: Tool poisoning attacks*. Invariant Labs. https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks

Brown, T., Mann, B., Ryder, N., Subbiah, M., Kaplan, J. D., Dhariwal, P., Neelakantan, A., Shyam, P., Sastry, G., Askell, A., Agarwal, S., Herbert-Voss, A., Krueger, G., Henighan, T., Child, R., Ramesh, A., Ziegler, D., Wu, J., Winter, C., … Amodei, D. (2020). Language models are few-shot learners. *Advances in Neural Information Processing Systems, 33*, 1877–1901. https://proceedings.neurips.cc/paper/2020/hash/1457c0d6bfcb4967418bfb8ac142f64a-Abstract.html

Fielding, R. T. (2000). *Architectural styles and the design of network-based software architectures* [Tesis doctoral, University of California, Irvine]. https://ics.uci.edu/~fielding/pubs/dissertation/top.htm

GitHub. (s. f.). *GitHub MCP Server* [Software]. GitHub. Recuperado el 16 de octubre de 2026, de https://github.com/github/github-mcp-server

Google. (2026, 14 de octubre). *Gemini thinking*. Gemini API, Google AI for Developers. https://ai.google.dev/gemini-api/docs/thinking

Google. (s. f.). *Model Context Protocol (MCP)*. Google Antigravity Docs. Recuperado el 15 de octubre de 2026, de https://antigravity.google/docs/mcp

Greshake, K., Abdelnabi, S., Mishra, S., Endres, C., Holz, T., & Fritz, M. (2023). Not what you've signed up for: Compromising real-world LLM-integrated applications with indirect prompt injection. En *Proceedings of the 16th ACM Workshop on Artificial Intelligence and Security* (pp. 79–90). Association for Computing Machinery. https://doi.org/10.1145/3605764.3623985

Guo, D., Yang, D., Zhang, H., Song, J., Wang, P., Zhu, Q., Xu, R., Zhang, R., Ma, S., Bi, X., Zhang, X., Yu, X., Wu, Y., Wu, Z. F., Gou, Z., Shao, Z., Li, Z., Gao, Z., Liu, A., … Zhang, Z. (2025). DeepSeek-R1 incentivizes reasoning in LLMs through reinforcement learning. *Nature, 645*(8081), 633–638. https://doi.org/10.1038/s41586-025-09422-z

Hoffmann, J., Borgeaud, S., Mensch, A., Buchatskaya, E., Cai, T., Rutherford, E., de Las Casas, D., Hendricks, L. A., Welbl, J., Clark, A., Hennigan, T., Noland, E., Millican, K., van den Driessche, G., Damoc, B., Guy, A., Osindero, S., Simonyan, K., Elsen, E., … Sifre, L. (2022). *Training compute-optimal large language models* [Preprint]. arXiv. https://doi.org/10.48550/arXiv.2203.15556

Hurtado Avilés, G. (2026a). *HolaMundoFlutter* [Software]. GitHub. https://github.com/gabrielhuav/Flutter-Projects/tree/main/HolaMundoFlutter

Hurtado Avilés, G. (2026b). *HolaMundoKMP* [Software]. GitHub. https://github.com/gabrielhuav/HolaMundoKMP

JSON-RPC Working Group. (2013, 4 de enero). *JSON-RPC 2.0 specification*. https://www.jsonrpc.org/specification

Jurafsky, D., & Martin, J. H. (2026). *Speech and language processing: An introduction to natural language processing, computational linguistics, and speech recognition with language models* (3.ª ed., borrador en línea del 19 de agosto de 2026). https://web.stanford.edu/~jurafsky/slp3/

Kaplan, J., McCandlish, S., Henighan, T., Brown, T. B., Chess, B., Child, R., Gray, S., Radford, A., Wu, J., & Amodei, D. (2020). *Scaling laws for neural language models* [Preprint]. arXiv. https://doi.org/10.48550/arXiv.2001.08361

Kojima, T., Gu, S. S., Reid, M., Matsuo, Y., & Iwasawa, Y. (2022). Large language models are zero-shot reasoners. *Advances in Neural Information Processing Systems, 35*, 22199–22213. https://doi.org/10.52202/068431-1613

Linux Foundation. (2025, 9 de diciembre). *Linux Foundation announces the formation of the Agentic AI Foundation (AAIF), anchored by new project contributions including Model Context Protocol (MCP), goose and AGENTS.md* [Comunicado de prensa]. https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation

Microsoft. (2026, 14 de octubre). *Add and manage MCP servers in VS Code*. Visual Studio Code Docs. https://code.visualstudio.com/docs/copilot/customization/mcp-servers

Model Context Protocol. (2025, 25 de noviembre). *Lifecycle* (Revisión 2025-11-25). https://modelcontextprotocol.io/specification/2025-11-25/basic/lifecycle

Model Context Protocol. (2026a, 28 de julio). *Architecture* (Revisión 2026-07-28). https://modelcontextprotocol.io/specification/2026-07-28/architecture

Model Context Protocol. (2026b, 28 de julio). *Authorization* (Revisión 2026-07-28). https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization

Model Context Protocol. (2026c, 28 de julio). *Deprecated features* (Revisión 2026-07-28). https://modelcontextprotocol.io/specification/2026-07-28/deprecated

Model Context Protocol. (2026d). *Filesystem MCP Server* [Archivo README]. GitHub. Recuperado el 15 de octubre de 2026, de https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem

Model Context Protocol. (2026e, 28 de julio). *Key changes* (Revisión 2026-07-28). https://modelcontextprotocol.io/specification/2026-07-28/changelog

Model Context Protocol. (2026f, 2 de octubre). *mcp* (Versión 2.3.0) [Software]. PyPI. https://pypi.org/project/mcp/

Model Context Protocol. (2026g, 11 de octubre). *@modelcontextprotocol/server-filesystem* (Versión 1.0.0) [Software]. npm. https://www.npmjs.com/package/@modelcontextprotocol/server-filesystem

Model Context Protocol. (2026h, 28 de julio). *Specification* (Revisión 2026-07-28). https://modelcontextprotocol.io/specification/2026-07-28

Model Context Protocol. (2026i, 28 de julio). *Tools* (Revisión 2026-07-28). https://modelcontextprotocol.io/specification/2026-07-28/server/tools

Model Context Protocol. (2026j, 28 de julio). *Transports: Overview* (Revisión 2026-07-28). https://modelcontextprotocol.io/specification/2026-07-28/basic/transports

Model Context Protocol. (s. f.-a). *Connect to local MCP servers*. Recuperado el 15 de octubre de 2026, de https://modelcontextprotocol.io/docs/develop/connect-local-servers

Model Context Protocol. (s. f.-b). *Local server security*. Recuperado el 15 de octubre de 2026, de https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/local-server-security

Model Context Protocol. (s. f.-c). *Migration guide* [MCP Python SDK]. Recuperado el 15 de octubre de 2026, de https://py.sdk.modelcontextprotocol.io/migration/

Model Context Protocol. (s. f.-d). *SDKs*. Recuperado el 15 de octubre de 2026, de https://modelcontextprotocol.io/docs/sdk

Model Context Protocol. (s. f.-e). *Security best practices*. Recuperado el 15 de octubre de 2026, de https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices

Model Context Protocol. (s. f.-f). *Versioning*. Recuperado el 15 de octubre de 2026, de https://modelcontextprotocol.io/docs/2026-07-28/learn/versioning

OpenAI. (2024, 12 de septiembre). *Learning to reason with LLMs*. https://openai.com/index/learning-to-reason-with-llms/

OpenAI. (s. f.-a). *Function calling*. OpenAI API. Recuperado el 15 de octubre de 2026, de https://developers.openai.com/api/docs/guides/function-calling

OpenAI. (s. f.-b). *Model Context Protocol – Codex*. OpenAI Developers. Recuperado el 15 de octubre de 2026, de https://developers.openai.com/codex/mcp

Ouyang, L., Wu, J., Jiang, X., Almeida, D., Wainwright, C., Mishkin, P., Zhang, C., Agarwal, S., Slama, K., Ray, A., Schulman, J., Hilton, J., Kelton, F., Miller, L., Simens, M., Askell, A., Welinder, P., Christiano, P. F., Leike, J., & Lowe, R. (2022). Training language models to follow instructions with human feedback. *Advances in Neural Information Processing Systems, 35*, 27730–27744. https://doi.org/10.52202/068431-2011

OWASP Foundation. (s. f.-a). *LLM01:2025 Prompt injection*. OWASP Gen AI Security Project. Recuperado el 15 de octubre de 2026, de https://genai.owasp.org/llmrisk/llm01-prompt-injection/

OWASP Foundation. (s. f.-b). *LLM06:2025 Excessive agency*. OWASP Gen AI Security Project. Recuperado el 15 de octubre de 2026, de https://genai.owasp.org/llmrisk/llm062025-excessive-agency/

Radford, A., Narasimhan, K., Salimans, T., & Sutskever, I. (2018). *Improving language understanding by generative pre-training* [Informe técnico]. OpenAI. https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf

Radford, A., Wu, J., Child, R., Luan, D., Amodei, D., & Sutskever, I. (2019). *Language models are unsupervised multitask learners* [Informe técnico]. OpenAI. https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf

Schaeffer, R., Miranda, B., & Koyejo, S. (2023). Are emergent abilities of large language models a mirage? *Advances in Neural Information Processing Systems, 36*, 55565–55581. https://doi.org/10.52202/075280-2425

Schick, T., Dwivedi-Yu, J., Dessì, R., Raileanu, R., Lomeli, M., Hambro, E., Zettlemoyer, L., Cancedda, N., & Scialom, T. (2023). Toolformer: Language models can teach themselves to use tools. *Advances in Neural Information Processing Systems, 36*, 68539–68551. https://doi.org/10.52202/075280-2997

Snell, C., Lee, J., Xu, K., & Kumar, A. (2025). Scaling LLM test-time compute optimally can be more effective than scaling parameters for reasoning. En *International Conference on Learning Representations* (Vol. 2025, pp. 10131–10165). https://proceedings.iclr.cc/paper_files/paper/2025/hash/1b623663fd9b874366f3ce019fdfdd44-Abstract-Conference.html

Soria Parra, D., & Delimarsky, D. (2026, 28 de julio). *The 2026-07-28 specification*. Model Context Protocol Blog. https://blog.modelcontextprotocol.io/posts/2026-07-28/

Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł., & Polosukhin, I. (2017). Attention is all you need. *Advances in Neural Information Processing Systems, 30*. https://proceedings.neurips.cc/paper_files/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html

Vida MRR - Programacion web. (2026, 8 de julio). *Diferencia entre API y MCP* [Video]. YouTube. https://youtu.be/FdVkE8u2C_Q

Wei, J., Tay, Y., Bommasani, R., Raffel, C., Zoph, B., Borgeaud, S., Yogatama, D., Bosma, M., Zhou, D., Metzler, D., Chi, E. H., Hashimoto, T., Vinyals, O., Liang, P., Dean, J., & Fedus, W. (2022). Emergent abilities of large language models. *Transactions on Machine Learning Research*. https://openreview.net/forum?id=yzkSU5zdwD

Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter, B., Xia, F., Chi, E., Le, Q. V., & Zhou, D. (2022). Chain-of-thought prompting elicits reasoning in large language models. *Advances in Neural Information Processing Systems, 35*, 24824–24837. https://doi.org/10.52202/068431-1800

Willison, S. (2025, 16 de junio). *The lethal trifecta for AI agents: Private data, untrusted content, and external communication*. Simon Willison's Weblog. https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/

Yang, A., Li, A., Yang, B., Zhang, B., Hui, B., Zheng, B., Yu, B., Gao, C., Huang, C., Lv, C., Zheng, C., Liu, D., Zhou, F., Huang, F., Hu, F., Ge, H., Wei, H., Lin, H., Tang, J., … Qiu, Z. (2025). *Qwen3 technical report* [Preprint]. arXiv. https://doi.org/10.48550/arXiv.2505.09388

Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y. (2023). ReAct: Synergizing reasoning and acting in language models. En *International Conference on Learning Representations (ICLR 2023)*. https://openreview.net/forum?id=WE_vluYUL-X

Zed Industries. (s. f.). *Model Context Protocol*. Zed Docs. Recuperado el 15 de octubre de 2026, de https://zed.dev/docs/ai/mcp
