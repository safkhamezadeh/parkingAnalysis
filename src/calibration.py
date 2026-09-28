import cv2
from typing import NamedTuple
from enum import IntEnum
import math
import numpy as np

class _KeyboardKeys(IntEnum):
    ESCAPE = 27


class _ImagePoint(NamedTuple):
    x: int
    y: int

class _Polygon():
    MAXSIZE = 4

    def __init__(self) -> None:
        self.points: list[_ImagePoint] = []

    def __repr__(self) -> str:
        return f"_Polygon({self.points})"

    def add(self, point: _ImagePoint) -> None:
        self.points.append(point)

    def isFull(self) -> bool:
        return len(self.points) >= self.MAXSIZE



def _order_points(points: list[_ImagePoint]) -> list[_ImagePoint]:
    cx = sum(p.x for p in points) / len(points)
    cy = sum(p.y for p in points) / len(points)
    return sorted(points, key=lambda p: math.atan2(p.y - cy, p.x - cx))

def _add_point(point: _ImagePoint, polygons: list[_Polygon]) -> None:
    if len(polygons) == 0 or polygons[-1].isFull():
        polygons.append(_Polygon())
    polygons[-1].add(point)
    if polygons[-1].isFull():# just completed?
        polygons[-1].points = _order_points(polygons[-1].points)

def _click_event(event, x, y, _flags, polygons: list[_Polygon] | None):
    match event:
        case cv2.EVENT_LBUTTONDOWN:
            if polygons is not None:
                _add_point(_ImagePoint(x,y),polygons)
                print(polygons)
        
            
        

def calibrate(image):

    polygons: list[_Polygon] = []
    
    img = cv2.imread(image, cv2.IMREAD_COLOR)
    if img is None:
        raise FileNotFoundError(f"Could not read image: {image}")
    cv2.namedWindow("image")
    cv2.setMouseCallback('image', _click_event, polygons)
    while True:
        frame = img.copy()
        for polygon in polygons:
            pts = polygon.points
            if len(pts) >= 2:
                np_pts = np.array([(p.x, p.y) for p in pts], dtype=np.int32)
                cv2.polylines(frame, [np_pts], isClosed=polygon.isFull(),
                            color=(0, 255, 0), thickness=2)
            for point in pts:                               # dots on top
                cv2.circle(frame, (point.x, point.y), 3, (0, 0, 255), -1)
        cv2.imshow("image", frame)
                
        k = cv2.waitKey(20)
        if cv2.getWindowProperty("image", cv2.WND_PROP_VISIBLE) < 1:
            break

        match k:
            case _KeyboardKeys.ESCAPE:
                break

    cv2.destroyAllWindows()



if __name__ == '__main__':
    print(calibrate(image="data/test/2012-09-11_16_48_36_jpg.rf.4ecc8c87c61680ccc73edc218a2c8d7d (2).jpg"))
