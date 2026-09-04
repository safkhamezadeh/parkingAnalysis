import cv2
from typing import NamedTuple


class _image_Point(NamedTuple):
    x: int
    y: int

class _polygon():
    MAXSIZE = 4

    def __init__(self) -> None:
        self.points: list[_image_Point] = []

    def __repr__(self) -> str:
        return f"_polygon({self.points})"

    def add(self, point: _image_Point) -> None:
        self.points.append(point)

    def isFull(self) -> bool:
        if len(self.points) >= self.MAXSIZE:
            return True
        else: return False


def _add_point(point: _image_Point, polygons: list[_polygon]) -> None:
    if len(polygons) == 0 or polygons[-1].isFull():
        polygons.append(_polygon())
    polygons[-1].add(point)

def _click_event(event, x, y, flags, polygons: list[_polygon] | None):
    if event == cv2.EVENT_LBUTTONDOWN:
        if polygons is not None:
            _add_point(_image_Point(x,y),polygons)
            print(polygons)
        

def Callibrate(image):

    polygons: list[_polygon] = []
    

    img = cv2.imread(image, cv2.IMREAD_COLOR)
    if img is None:
        raise FileNotFoundError(f"Could not read image: {image}")
    cv2.imshow("image", img)
    cv2.setMouseCallback('image', _click_event, polygons)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



if __name__ == '__main__':
    print(Callibrate(image="data/test/2012-09-11_16_48_36_jpg.rf.4ecc8c87c61680ccc73edc218a2c8d7d (2).jpg"))
