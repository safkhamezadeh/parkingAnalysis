import sqlite3
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_MIGRATIONS_DIR = Path(__file__).resolve().parent / "migrations"
_DB_PATH = _PROJECT_ROOT / "var" / "db" / "parking.db"


def GetConnection(db_path: Path = _DB_PATH) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def _ensureMigrationsTable(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS schema_migrations (
            filename    TEXT PRIMARY KEY,
            applied_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()


def _appliedMigrations(conn: sqlite3.Connection) -> set[str]:
    rows = conn.execute("SELECT filename FROM schema_migrations").fetchall()
    return {row[0] for row in rows}


def _pendingMigrations(conn: sqlite3.Connection, migrations_dir: Path) -> list[Path]:
    applied = _appliedMigrations(conn)
    all_migrations = sorted(migrations_dir.glob("*.sql"))
    return [path for path in all_migrations if path.name not in applied]


def RunMigrations(
    db_path: Path = _DB_PATH,
    migrations_dir: Path = _MIGRATIONS_DIR,
) -> list[str]:
    """Apply any *.sql files in `migrations_dir` not yet recorded in
    schema_migrations, in filename order. Returns the filenames applied.
    """
    conn = GetConnection(db_path)
    applied: list[str] = []
    try:
        _ensureMigrationsTable(conn)

        for path in _pendingMigrations(conn, migrations_dir):
            conn.executescript(path.read_text())
            conn.execute(
                "INSERT INTO schema_migrations (filename) VALUES (?)",
                (path.name,),
            )
            conn.commit()
            applied.append(path.name)
    finally:
        conn.close()

    return applied


if __name__ == "__main__":
    ran = RunMigrations()
    if ran:
        print(f"Applied {len(ran)} migration(s): {', '.join(ran)}")
    else:
        print("Already up to date.")
