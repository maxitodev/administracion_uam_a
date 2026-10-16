// Agrega los dos servidores MCP de la Tarea 2 al claude_desktop_config.json de Claude Desktop.
//
//   1. Cierra Claude Desktop por completo (icono de la bandeja → Salir).
//   2. node tarea2/config/instalar-mcp.mjs
//   3. Vuelve a abrir Claude Desktop.
//
// Claude Desktop guarda sus preferencias en ese mismo archivo y lo reescribe mientras
// está abierto: si se edita con la app encendida, borra lo que se agregó. Por eso este
// script se niega a correr si la encuentra abierta.
//
// Las rutas se calculan a partir de dónde está clonado el repositorio, así que sirve en
// cualquier máquina. Respeta todo lo que ya tenga el archivo y sólo reemplaza estos dos
// servidores dentro de "mcpServers". Antes de escribir, deja un respaldo .bak junto al original.

import { execSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const tarea2 = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const repo = path.dirname(tarea2);
const windows = process.platform === "win32";

const archivo = windows
  ? path.join(process.env.APPDATA, "Claude", "claude_desktop_config.json")
  : path.join(os.homedir(), "Library", "Application Support", "Claude", "claude_desktop_config.json");

if (windows) {
  // El Claude Desktop de la tienda vive en WindowsApps\Claude_…; el instalador clásico, en AnthropicClaude.
  // Otros claude.exe (como la CLI de Claude Code) no cuentan.
  // Si no hay ningún proceso claude, Get-Process deja la ejecución en error y PowerShell
  // sale con código 1, que execSync toma como fallo: el «exit 0» final lo evita.
  const rutas = execSync(
    'powershell -NoProfile -Command "Get-Process claude -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Path; exit 0"',
    { encoding: "utf8" },
  );
  if (/WindowsApps\\Claude_|AnthropicClaude/i.test(rutas)) {
    console.error("Claude Desktop está abierto. Ciérralo desde la bandeja (Salir) y vuelve a correr el script.");
    process.exit(1);
  }
}

const python = windows
  ? path.join(tarea2, "servidor-propio", ".venv", "Scripts", "python.exe")
  : path.join(tarea2, "servidor-propio", ".venv", "bin", "python");

const servidores = {
  "sistema-archivos": {
    command: "npx",
    args: ["-y", "@modelcontextprotocol/server-filesystem@1.0.0", path.join(tarea2, "sandbox")],
  },
  "entregas-apsw": {
    command: python,
    args: [path.join(tarea2, "servidor-propio", "servidor.py"), repo],
  },
};

if (!fs.existsSync(python)) {
  console.warn(`Aviso: no existe ${python}; entregas-apsw no arrancará hasta crear el entorno virtual (ver README).`);
}

fs.mkdirSync(path.dirname(archivo), { recursive: true });
const config = fs.existsSync(archivo) ? JSON.parse(fs.readFileSync(archivo, "utf8")) : {};
if (fs.existsSync(archivo)) fs.copyFileSync(archivo, archivo + ".bak");

config.mcpServers = { ...(config.mcpServers ?? {}), ...servidores };
fs.writeFileSync(archivo, JSON.stringify(config, null, 2) + "\n", "utf8");

console.log(`Listo: ${archivo}`);
console.log(JSON.stringify({ mcpServers: servidores }, null, 2));
