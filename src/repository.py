import sqlite3

from db import GetConnection

_VALID_SOURCES = ("pklot", "own_video", "pilot")


class ProjectAlreadyExistsError(Exception):
    pass


class ProjectNotFoundError(Exception):
    pass


class ParkingLotAlreadyExistsError(Exception):
    pass


class ParkingLotNotFoundError(Exception):
    pass


class SessionAlreadyExistsError(Exception):
    pass


def _findProjectIdByName(conn: sqlite3.Connection, name: str) -> int | None:
    row = conn.execute(
        "SELECT project_id FROM project WHERE name = ?", (name,)
    ).fetchone()
    return row[0] if row is not None else None


def _findLotId(conn: sqlite3.Connection, project_id: int, name: str) -> int | None:
    row = conn.execute(
        "SELECT lot_id FROM parking_lot WHERE project_id = ? AND name = ?",
        (project_id, name),
    ).fetchone()
    return row[0] if row is not None else None


def _findSessionId(conn: sqlite3.Connection, lot_id: int, folder: str) -> int | None:
    row = conn.execute(
        "SELECT session_id FROM session WHERE lot_id = ? AND folder = ?",
        (lot_id, folder),
    ).fetchone()
    return row[0] if row is not None else None


def _createProject(conn: sqlite3.Connection, name: str, notes: str = "Undefined") -> int:
    """Core insert, no commit. Raises ProjectAlreadyExistsError if `name` is taken."""
    if _findProjectIdByName(conn, name) is not None:
        raise ProjectAlreadyExistsError(f"a project named '{name}' already exists")

    cursor = conn.execute(
        "INSERT INTO project (name, notes) VALUES (?, ?)", (name, notes)
    )
    new_id = cursor.lastrowid
    assert new_id is not None
    return new_id


def _createParkingLot(
    conn: sqlite3.Connection, project_name: str, lot_name: str, notes: str = "Undefined"
) -> int:
    """Core insert, no commit. Raises ProjectNotFoundError / ParkingLotAlreadyExistsError."""
    project_id = _findProjectIdByName(conn, project_name)
    if project_id is None:
        raise ProjectNotFoundError(f"no project named '{project_name}'")

    if _findLotId(conn, project_id, lot_name) is not None:
        raise ParkingLotAlreadyExistsError(
            f"project '{project_name}' already has a parking lot named '{lot_name}'"
        )

    cursor = conn.execute(
        "INSERT INTO parking_lot (project_id, name, notes) VALUES (?, ?, ?)",
        (project_id, lot_name, notes),
    )
    new_id = cursor.lastrowid
    assert new_id is not None
    return new_id


def _createSession(
    conn: sqlite3.Connection,
    project_name: str,
    lot_name: str,
    source: str,
    folder: str,
    notes: str = "Undefined",
) -> int:
    """Core insert, no commit. Raises ProjectNotFoundError / ParkingLotNotFoundError /
    ValueError (bad source) / SessionAlreadyExistsError."""
    if source not in _VALID_SOURCES:
        raise ValueError(f"source must be one of {_VALID_SOURCES}, got '{source}'")

    project_id = _findProjectIdByName(conn, project_name)
    if project_id is None:
        raise ProjectNotFoundError(f"no project named '{project_name}'")

    lot_id = _findLotId(conn, project_id, lot_name)
    if lot_id is None:
        raise ParkingLotNotFoundError(
            f"project '{project_name}' has no parking lot named '{lot_name}'"
        )

    if _findSessionId(conn, lot_id, folder) is not None:
        raise SessionAlreadyExistsError(
            f"parking lot '{lot_name}' already has a session for folder '{folder}'"
        )

    cursor = conn.execute(
        "INSERT INTO session (lot_id, source, folder, notes) VALUES (?, ?, ?, ?)",
        (lot_id, source, folder, notes),
    )
    new_id = cursor.lastrowid
    assert new_id is not None
    return new_id


def CreateProject(name: str, notes: str = "Undefined") -> int:
    """Insert a new project named `name`. Returns the new project_id.

    Raises ProjectAlreadyExistsError if a project with this name already exists.
    """
    conn = GetConnection()
    try:
        new_id = _createProject(conn, name, notes)
        conn.commit()
        return new_id
    finally:
        conn.close()


def CreateParkingLot(project_name: str, lot_name: str, notes: str = "Undefined") -> int:
    """Insert a new parking lot named `lot_name` under project `project_name`.
    Returns the new lot_id.

    Raises ProjectNotFoundError if the project does not exist, or
    ParkingLotAlreadyExistsError if that project already has a lot with this name.
    """
    conn = GetConnection()
    try:
        new_id = _createParkingLot(conn, project_name, lot_name, notes)
        conn.commit()
        return new_id
    finally:
        conn.close()


def CreateSession(
    project_name: str,
    lot_name: str,
    source: str,
    folder: str,
    notes: str = "Undefined",
) -> int:
    """Insert a new session for lot `lot_name` under project `project_name`.
    `folder` (relative to the data root) is saved as given — no directory is
    created on disk. Returns the new session_id.

    Raises ProjectNotFoundError / ParkingLotNotFoundError if either does not
    exist, ValueError if `source` isn't one of _VALID_SOURCES, or
    SessionAlreadyExistsError if that lot already has a session with this folder.
    """
    conn = GetConnection()
    try:
        new_id = _createSession(conn, project_name, lot_name, source, folder, notes)
        conn.commit()
        return new_id
    finally:
        conn.close()


def SetupAll(project_name: str, lot_name: str, source: str, folder: str) -> tuple[int, int, int]:
    """Create a project, a parking lot under it, and a session under that lot,
    as a single transaction: if any step fails, none of them are committed.

    Returns (project_id, lot_id, session_id).
    """
    conn = GetConnection()
    try:
        project_id = _createProject(conn, project_name)
        lot_id = _createParkingLot(conn, project_name, lot_name)
        session_id = _createSession(conn, project_name, lot_name, source, folder)
        conn.commit()
        return project_id, lot_id, session_id
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
