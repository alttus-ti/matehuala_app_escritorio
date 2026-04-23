-- Script de inicialización para SQLite

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    descripcion TEXT
);

CREATE TABLE IF NOT EXISTS tipo_tarjetas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descripcion TEXT NOT NULL,
    clave TEXT NOT NULL,
    saldo_maximo REAL NOT NULL DEFAULT 0.00,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS pasajeros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    documento TEXT NOT NULL,
    curp TEXT,
    foto TEXT,
    fecha_nacimiento TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    role_id INTEGER NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (role_id) REFERENCES roles(id)
        ON DELETE RESTRICT ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS tarjetas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uid TEXT NOT NULL,
    saldo REAL NOT NULL DEFAULT 0.00,
    tipo_tarjeta_id INTEGER NOT NULL,
    pasajero_id INTEGER NOT NULL,
    vigencia TEXT,
    en_lista_negra INTEGER NOT NULL DEFAULT 0,
    fecha_baja TEXT DEFAULT NULL,
    motivo_baja TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (tipo_tarjeta_id) REFERENCES tipo_tarjetas(id)
        ON DELETE RESTRICT ON UPDATE NO ACTION,
    FOREIGN KEY (pasajero_id) REFERENCES pasajeros(id)
        ON DELETE RESTRICT ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS recargas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tarjeta_id INTEGER NOT NULL,
    usuario_id INTEGER NOT NULL,
    monto REAL NOT NULL,
    oficina TEXT,
    fecha_hora TEXT NOT NULL DEFAULT (datetime('now')),
    conexion_internet INTEGER NOT NULL DEFAULT 0,
    referencia TEXT,
    FOREIGN KEY (tarjeta_id) REFERENCES tarjetas(id)
        ON DELETE RESTRICT ON UPDATE NO ACTION,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        ON DELETE RESTRICT ON UPDATE NO ACTION
);

INSERT OR IGNORE INTO roles (id, nombre, descripcion) VALUES
(1, 'administrador', 'Usuario con permisos completos'),
(2, 'empleado', 'Usuario con permisos de empleado');

INSERT OR IGNORE INTO tipo_tarjetas (id, descripcion, clave, saldo_maximo) VALUES
(1, 'Normal', 'normal', 0.00),
(2, 'Preferencial', 'preferencial', 0.00);

INSERT OR IGNORE INTO usuarios (id, username, password, role_id) VALUES
(1, 'admin', '1234', 1),
(2, 'empleado', '1234', 2);


<<<<<<< HEAD
--CREATE TABLEIF NOT EXISTS sync_queue (
--    id INTEGER PRIMARY KEY AUTOINCREMENT,
--    tabla TEXT NOT NULL,
--    accion TEXT NOT NULL,
--    registro_id TEXT,
--    payload_json TEXT NOT NULL, 
--    sincronizado INTEGER NOT NULL DEFAULT 0,
--    error TEXT,
--    created_at TEXT NOT NULL DEFAULT (datetime('now'))
--);
=======
CREATE TABLE IF NOT EXISTS sync_queue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    operation_uuid TEXT NOT NULL UNIQUE,
    event_type TEXT NOT NULL,
    entity_uid TEXT,
    payload_json TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    retries INTEGER NOT NULL DEFAULT 0,
    last_error TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    synced_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_sync_queue_status_created_at
    ON sync_queue (status, created_at);
>>>>>>> 3b4dc0a666cd5a2194eed821832e1d14eae96219
