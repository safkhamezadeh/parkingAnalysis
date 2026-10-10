import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from repository import (
    ParkingLotAlreadyExistsError,
    ProjectAlreadyExistsError,
    SessionAlreadyExistsError,
    SetupAll as _SetupAll,
)


def SetupAll(project_name: str, lot_name: str, source: str, folder: str) -> None:
    """Create a new project, one parking lot under it, and one session under
    that lot, in a single call — transactional: if any step fails, nothing
    is committed.

    Prints an error and exits non-zero if any of the three already exists, or
    if `source` is invalid.
    """
    try:
        _SetupAll(project_name, lot_name, source, folder)
    except (
        ProjectAlreadyExistsError,
        ParkingLotAlreadyExistsError,
        SessionAlreadyExistsError,
        ValueError,
    ) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    print(
        f"Created project '{project_name}', lot '{lot_name}', "
        f"session '{folder}'."
    )


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print(
            "Usage: python setup_all.py <project_name> <lot_name> <source> <folder>",
            file=sys.stderr,
        )
        sys.exit(1)

    SetupAll(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
