import sqlite3
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_DIR = PROJECT_ROOT / "data"
DATABASE_PATH = DATABASE_DIR / "matehuala.db"
INIT_SCRIPT_PATH = PROJECT_ROOT / "sqlite_init.sql"


def get_connection() -> sqlite3.Connection:
    """Devuelve una conexion SQLite con llaves foraneas activas."""
    connection = sqlite3.connect(DATABASE_PATH, timeout=30)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA busy_timeout = 30000")
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database() -> None:
    """Crea la base local y ejecuta el script inicial si hace falta."""
    DATABASE_DIR.mkdir(exist_ok=True)

    if not INIT_SCRIPT_PATH.exists():
        raise FileNotFoundError(f"No se encontro el script SQL: {INIT_SCRIPT_PATH}")

    script = INIT_SCRIPT_PATH.read_text(encoding="utf-8")

    try:
        with get_connection() as connection:
            connection.execute("PRAGMA journal_mode = WAL")
            connection.executescript(script)
            _ensure_pasajeros_columns(connection)
            _ensure_recargas_columns(connection)
    except sqlite3.OperationalError as error:
        if "database is locked" in str(error).lower():
            raise RuntimeError(
                "La base de datos esta bloqueada. Cierra DB Browser for SQLite, "
                "extensiones del IDE, terminales o ventanas de la app que tengan "
                f"abierto este archivo: {DATABASE_PATH}"
            ) from error

        raise


def _ensure_pasajeros_columns(connection: sqlite3.Connection) -> None:
    """Agrega columnas nuevas cuando la base local ya existia."""
    existing_columns = {
        row["name"]
        for row in connection.execute("PRAGMA table_info(pasajeros)").fetchall()
    }

    for column_name in ("curp", "foto", "fecha_nacimiento"):
        if column_name not in existing_columns:
            connection.execute(f"ALTER TABLE pasajeros ADD COLUMN {column_name} TEXT")


def _ensure_recargas_columns(connection: sqlite3.Connection) -> None:
    """Agrega columnas nuevas cuando la base local ya existia."""
    existing_columns = {
        row["name"]
        for row in connection.execute("PRAGMA table_info(recargas)").fetchall()
    }

    if "oficina" not in existing_columns:
        connection.execute("ALTER TABLE recargas ADD COLUMN oficina TEXT")
