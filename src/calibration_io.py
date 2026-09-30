import json

def SavePolygons(polygons: list[Polygon], name_project: str,
                 image_size: tuple[int, int]) -> None:
    data = {
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
    with open(f"{name_project}.json", "w") as f: 
        json.dump(data, f, indent=4)