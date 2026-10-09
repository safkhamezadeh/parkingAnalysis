from calibration.calibration import Calibrate
from calibration.calibration_io import Load_image, SavePolygons
from pathlib import Path


def test_calibration_integration():

    path: Path = Path("data/testlot_1/2012-09-11_16_48_36_jpg.rf.4ecc8c87c61680ccc73edc218a2c8d7d (2).jpg")

    image = Load_image(path=path)

    calibrated = Calibrate(image)

    image_size = (image.shape[1], image.shape[0])

    SavePolygons(calibrated, path, image_size)

test_calibration_integration()