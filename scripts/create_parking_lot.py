import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from repository import (
    CreateParkingLot,
    ParkingLotAlreadyExistsError,
    ProjectNotFoundError,
)


def SetupParkingLot(project_name: str, lot_name: str) -> None:
    """Register a new parking lot under an existing project in the db.

    Prints an error and exits non-zero if the project doesn't exist, or if
    that project already has a lot with this name.
    """
    try:
        CreateParkingLot(project_name, lot_name)
    except (ProjectNotFoundError, ParkingLotAlreadyExistsError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Created parking lot '{lot_name}' for project '{project_name}'.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python create_parking_lot.py <project_name> <lot_name>", file=sys.stderr)
        sys.exit(1)

    SetupParkingLot(sys.argv[1], sys.argv[2])
