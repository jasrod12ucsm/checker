-- Esquema de Centinela C++ (versión 2). Cada tabla es un agregado del dominio.
-- Una base creada con una versión anterior se actualiza con migraciones.sql al abrirla.
CREATE TABLE usuarios (
  id          TEXT PRIMARY KEY,
  email       TEXT NOT NULL UNIQUE,
  nombre      TEXT NOT NULL,
  rol         TEXT NOT NULL CHECK (rol IN ('administrador', 'desarrollador')),
  hash_clave  TEXT NOT NULL,
  estado      TEXT NOT NULL CHECK (estado IN ('Pendiente', 'Activo', 'Desactivado')),
  creado_en   INTEGER NOT NULL
);

CREATE TABLE sesiones (
  token_hash  TEXT PRIMARY KEY,
  usuario_id  TEXT NOT NULL REFERENCES usuarios(id),
  creada      INTEGER NOT NULL,
  expira      INTEGER NOT NULL
);
CREATE INDEX sesiones_usuario ON sesiones(usuario_id);

CREATE TABLE repositorios (
  id               TEXT PRIMARY KEY,
  nombre           TEXT NOT NULL UNIQUE,
  politica         TEXT NOT NULL CHECK (politica IN ('Silent', 'Possibly')),
  bloquear_merge   INTEGER NOT NULL CHECK (bloquear_merge IN (0, 1)),
  secreto_webhook  TEXT NOT NULL,
  activo           INTEGER NOT NULL CHECK (activo IN (0, 1)),
  conectado_por    TEXT NOT NULL REFERENCES usuarios(id),
  conectado_en     INTEGER NOT NULL
);

-- El estado se guarda aplanado: `estado` dice la variante y solo sus columnas tienen valor.
CREATE TABLE revisiones (
  id              TEXT PRIMARY KEY,
  repositorio_id  TEXT NOT NULL REFERENCES repositorios(id),
  numero_pr       INTEGER NOT NULL CHECK (numero_pr > 0),
  titulo          TEXT NOT NULL,
  autor           TEXT NOT NULL,
  sha_cabeza      TEXT NOT NULL,
  origen          TEXT NOT NULL CHECK (origen IN ('webhook', 'manual')),
  solicitada_por  TEXT REFERENCES usuarios(id),
  creada_en       INTEGER NOT NULL,
  intentos        INTEGER NOT NULL CHECK (intentos >= 1),
  estado          TEXT NOT NULL CHECK (estado IN ('Pendiente', 'EnAnalisis', 'Publicada', 'Fallida')),
  desde           INTEGER NOT NULL,
  veredicto       TEXT CHECK (veredicto IN ('Aprobada', 'ConProblemas')),
  archivos        INTEGER,
  no_compilados   INTEGER,
  confirmados     INTEGER,
  posibles        INTEGER,
  suprimidos      INTEGER,
  motivo          TEXT,
  UNIQUE (repositorio_id, numero_pr, sha_cabeza),
  CHECK ((estado = 'Publicada') = (veredicto IS NOT NULL)),
  CHECK ((estado = 'Fallida') = (motivo IS NOT NULL))
);
CREATE INDEX revisiones_repo ON revisiones(repositorio_id, creada_en DESC);

CREATE TABLE hallazgos (
  id             TEXT PRIMARY KEY,
  revision_id    TEXT NOT NULL REFERENCES revisiones(id) ON DELETE CASCADE,
  archivo        TEXT NOT NULL,
  linea          INTEGER NOT NULL CHECK (linea > 0),
  columna        INTEGER NOT NULL CHECK (columna > 0),
  clase          TEXT NOT NULL CHECK (clase IN ('Confirmado', 'Posible')),
  mensaje        TEXT NOT NULL,
  ruta           TEXT NOT NULL,           -- JSON: [{archivo, linea, mensaje}]
  huella         TEXT NOT NULL,
  clasificacion  TEXT NOT NULL CHECK (clasificacion IN ('SinRevisar', 'Confirmado', 'FalsoPositivo')),
  clasificado_por TEXT REFERENCES usuarios(id),
  clasificado_en  INTEGER,
  CHECK ((clasificado_por IS NULL) = (clasificado_en IS NULL))
);
CREATE INDEX hallazgos_revision ON hallazgos(revision_id);

CREATE TABLE descartes (
  repositorio_id  TEXT NOT NULL REFERENCES repositorios(id),
  huella          TEXT NOT NULL,
  por             TEXT NOT NULL REFERENCES usuarios(id),
  en              INTEGER NOT NULL,
  PRIMARY KEY (repositorio_id, huella)
);

-- Cola de trabajos: se escribe en la misma transacción que la revisión.
CREATE TABLE trabajos (
  revision_id  TEXT PRIMARY KEY REFERENCES revisiones(id),
  encolado_en  INTEGER NOT NULL,
  tomado       INTEGER NOT NULL DEFAULT 0 CHECK (tomado IN (0, 1))
);
