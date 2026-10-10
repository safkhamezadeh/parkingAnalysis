import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from repository import (
    CreateSession,
    ParkingLotNotFoundError,
    ProjectNotFoundError,
    SessionAlreadyExistsError,
)


def SetupSession(project_name: str, lot_name: str, source: str, folder: str) -> None:
    """Register a new session for an existing parking lot in the db.

    `folder` is saved as given (relative to the data root) — this does not
    create anything on disk, it only expects the folder to already exist.

    Prints an error and exits non-zero if the project/lot doesn't exist,
    `source` is invalid, or the lot already has a session for this folder.
    """
    try:
        CreateSession(project_name, lot_name, source, folder)
    except (
        ProjectNotFoundError,
        ParkingLotNotFoundError,
        SessionAlreadyExistsError,
        ValueError,
    ) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Created session '{folder}' for lot '{lot_name}' (project '{project_name}').")


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print(
            "Usage: python create_session.py <project_name> <lot_name> <source> <folder>",
            file=sys.stderr,
        )
        sys.exit(1)

    SetupSession(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
