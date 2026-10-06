-- ---------------------------------------------------------------------------
-- Tablero mínimo de trabajo · PostgreSQL 18
-- UEA 1151055 · Administración de Proyectos de Software · Trimestre 26-O
--
-- La imagen oficial ejecuta este archivo UNA sola vez: cuando el volumen
-- datos_db está vacío. Corre como POSTGRES_USER dentro de POSTGRES_DB.
-- Para volver a ejecutarlo hay que borrar el volumen:
--     docker compose down -v
--     docker compose up -d
--
-- Sirve para ver en Adminer que el contenedor quedó con tablas y datos.
-- ---------------------------------------------------------------------------

CREATE TABLE integrante (
    id      integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre  text NOT NULL,
    rol     text NOT NULL
            CHECK (rol IN ('Product Owner', 'Scrum Master', 'Desarrollo'))
);

CREATE TABLE sprint (
    id      integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre  text NOT NULL UNIQUE,
    inicio  date NOT NULL,
    fin     date NOT NULL,
    CHECK (fin >= inicio)
);

CREATE TABLE tarea (
    id           integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    titulo       text NOT NULL,
    estado       text NOT NULL DEFAULT 'Por hacer'
                 CHECK (estado IN ('Por hacer', 'En curso', 'Hecho')),
    sprint_id    integer NOT NULL REFERENCES sprint (id),
    responsable  integer REFERENCES integrante (id),
    creada       timestamptz NOT NULL DEFAULT now()
);

-- Vista tipo tablero Kanban: cuántas tareas hay en cada columna.
CREATE VIEW tablero AS
SELECT s.nombre AS sprint,
       t.estado,
       count(*) AS tareas
FROM tarea t
JOIN sprint s ON s.id = t.sprint_id
GROUP BY s.nombre, t.estado
ORDER BY s.nombre,
         array_position(ARRAY['Por hacer', 'En curso', 'Hecho'], t.estado);

INSERT INTO integrante (nombre, rol) VALUES
    ('Max Uriel Sánchez Díaz', 'Desarrollo');

INSERT INTO sprint (nombre, inicio, fin) VALUES
    ('Tarea 1', DATE '2026-09-29', DATE '2026-10-10');

INSERT INTO tarea (titulo, estado, sprint_id, responsable) VALUES
    ('Crear el repositorio con licencia MIT y .gitignore', 'Hecho',    1, 1),
    ('Levantar el contenedor de PostgreSQL 17',           'Hecho',    1, 1),
    ('Actualizar el contenedor a PostgreSQL 18',          'Hecho',    1, 1),
    ('Montar MySQL 9.7 con phpMyAdmin',                   'En curso', 1, 1),
    ('Investigar licencias de software',                  'En curso', 1, 1),
    ('Tomar las ocho capturas',                           'Por hacer', 1, 1);
