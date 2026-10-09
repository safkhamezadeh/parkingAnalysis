import json
import numpy as np
import cv2
from pathlib import Path
from calibration.calibration import Polygon


def SavePolygons(
    polygons: list[Polygon],
    image_path: Path,
    image_size: tuple[int, int]
) -> None:

    data = {
        "image": image_path.name,
        "image_size": [image_size[0], image_size[1]],
        "lot_polygons": [
            {
                "id": p.id,
                "zone": p.zone,
                "type": p.type,
                "points": [[pt.x, pt.y] for pt in p.points],
            }
            for p in polygons
        ],
    }

    json_path = image_path.parent / "calibration.json"

    with json_path.open("w") as f:
        json.dump(data, f, indent=4)



def Load_image(path: Path) -> np.ndarray:
    """
    Read an image from `path` and return it as a BGR uint8 NumPy array
    of shape (height, width, 3).

    Raises FileNotFoundError if the file can't be read (missing, unreadable,
    or not a valid image) — because cv2.imread returns None instead of
    raising, which would otherwise cause a confusing crash later.
    """
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    if img is None:
        raise FileNotFoundError(f"Could not read image: {path}")
    return img


