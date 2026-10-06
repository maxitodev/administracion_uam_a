#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Comprobación del entorno · PostgreSQL 18
# UEA 1151055 · Administración de Proyectos de Software · Trimestre 26-O
#
# Se ejecuta DENTRO del contenedor:
#   docker compose exec db bash
#   bash extras/comprobar.sh
#
# Cada línea dice OK o FALLA. Al final, el resumen. Sale con código 0 sólo
# si todo pasó, así que también sirve en un script o en integración continua.
# ---------------------------------------------------------------------------
set -u

if [ -z "${PGDATA:-}" ] || [ -z "${POSTGRES_USER:-}" ]; then
    echo "Este script se ejecuta dentro del contenedor:"
    echo "  docker compose exec db bash"
    echo "  bash extras/comprobar.sh"
    exit 2
fi

ok=0
falla=0

# revisa "descripción" comando [argumentos...]
revisa() {
    local desc=$1
    shift
    if "$@" >/dev/null 2>&1; then
        printf '  OK     %s\n' "$desc"
        ok=$((ok + 1))
    else
        printf '  FALLA  %s\n' "$desc"
        falla=$((falla + 1))
    fi
}

# sql "consulta": imprime el resultado sin encabezados ni alineación.
# Dentro del contenedor el socket local no pide contraseña.
sql() {
    psql -X -A -t -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "$1" 2>/dev/null
}

igual() { [ "$1" = "$2" ]; }

echo
echo "== Servidor"
revisa "responde (pg_isready)"                 pg_isready -q -U "$POSTGRES_USER" -d "$POSTGRES_DB"
revisa "versión mayor 18"                      igual "$(sql 'SHOW server_version_num' | cut -c1-2)" 18
revisa "datos en $PGDATA"                       test -f "$PGDATA/PG_VERSION"
revisa "PG_VERSION del cluster es 18"          igual "$(cat "$PGDATA/PG_VERSION" 2>/dev/null)" 18

echo
echo "== Base del curso"
revisa "codificación UTF8"                     igual "$(sql 'SHOW server_encoding')" UTF8
revisa "colación C"                            igual "$(sql 'SELECT datcollate FROM pg_database WHERE datname = current_database()')" C
revisa "zona horaria America/Mexico_City"      igual "$(sql 'SHOW timezone')" America/Mexico_City
revisa "tablas de initdb/ creadas"             igual "$(sql "SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public' AND table_name IN ('integrante', 'sprint', 'tarea')")" 3
revisa "la tabla tarea tiene filas"            test "$(sql 'SELECT count(*) FROM tarea')" -gt 0

echo
echo "== Herramientas del Dockerfile"
revisa "nano instalado"                        command -v nano
revisa "less instalado"                        command -v less
revisa "LANG=C.UTF-8"                          igual "${LANG:-}" C.UTF-8
revisa "TZ=America/Mexico_City"                igual "${TZ:-}" America/Mexico_City
revisa "carpeta de trabajo /trabajo"           igual "$PWD" /trabajo
revisa "compose.yaml visible en /trabajo"      test -f /trabajo/compose.yaml

echo
echo "== Versión"
sql 'SELECT version()'
psql --version

echo
echo "Resultado: $ok OK, $falla FALLA"
[ "$falla" -eq 0 ]
