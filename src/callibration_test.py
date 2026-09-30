"""
make_test_polygons.py

Generates fake parking-spot polygons for developing and testing your
save/load logic WITHOUT needing the dataset or any real images.

A polygon here is just 4 (x, y) corners, so we can build them by hand.
Use these to test:
  - save_polygons(polygons, path)   -> writes spots.json
  - load_polygons(path)             -> reads it back
  - a round-trip test (save then load then compare)

The classes below mirror the ones in your calibration tool. If you import
your real ones instead, delete these and import from calibrate.py.
"""

from typing import NamedTuple


# --- minimal stand-ins for your real classes (mirror calibrate.py) ---

class ImagePoint(NamedTuple):
    x: int
    y: int


class Polygon:
    MAXSIZE = 4

    def __init__(self, id: str = "", zone: str = "", type: str = "general") -> None:
        self.points: list[ImagePoint] = []
        self.id = id
        self.zone = zone
        self.type = type

    def add(self, point: ImagePoint) -> None:
        self.points.append(point)

    def is_full(self) -> bool:
        return len(self.points) >= self.MAXSIZE

    def __repr__(self) -> str:
        return f"Polygon(id={self.id!r}, zone={self.zone!r}, type={self.type!r}, points={self.points})"


# --- helpers to build fake polygons ---

def make_rect(x: int, y: int, w: int, h: int,
              id: str = "", zone: str = "", type: str = "general") -> Polygon:
    """Build a rectangular parking-spot polygon with its top-left at (x, y)."""
    p = Polygon(id=id, zone=zone, type=type)
    p.add(ImagePoint(x, y))          # top-left
    p.add(ImagePoint(x + w, y))      # top-right
    p.add(ImagePoint(x + w, y + h))  # bottom-right
    p.add(ImagePoint(x, y + h))      # bottom-left
    return p


def make_test_polygons() -> list[Polygon]:
    """
    A small lot: two rows of spots, with a mix of zones and types,
    laid out on a notional 1920x1080 image.
    """
    polygons: list[Polygon] = []

    spot_w, spot_h = 120, 220
    gap = 10

    # Row A (top) - visitor spots
    y_top = 100
    for i in range(4):
        x = 100 + i * (spot_w + gap)
        polygons.append(
            make_rect(x, y_top, spot_w, spot_h,
                      id=f"spot_{i + 1}", zone="row_a", type="visitor")
        )

    # Row B (bottom) - employee spots, last one disabled
    y_bottom = 600
    for i in range(4):
        x = 100 + i * (spot_w + gap)
        spot_type = "disabled" if i == 3 else "employee"
        polygons.append(
            make_rect(x, y_bottom, spot_w, spot_h,
                      id=f"spot_{i + 5}", zone="row_b", type=spot_type)
        )

    return polygons


if __name__ == "__main__":
    polys = make_test_polygons()
    print(f"Generated {len(polys)} test polygons:\n")
    for p in polys:
        print(" ", p)