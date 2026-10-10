import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from repository import CreateProject, ProjectAlreadyExistsError


def SetupProject(name: str) -> None:
    """Register a new project (who the data is being collected for) in the db.

    Prints an error and exits non-zero if a project with this name already exists.
    """
    try:
        CreateProject(name)
    except ProjectAlreadyExistsError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Created project '{name}'.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python setup_project.py <project_name>", file=sys.stderr)
        sys.exit(1)

    SetupProject(sys.argv[1])
