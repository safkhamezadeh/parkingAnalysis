import cv2

def __click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x,y)

def Callibrate(image):

    img = cv2.imread(image)
    cv2.imshow("image", img)
    cv2.setMouseCallback('image', __click_event)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



if __name__ == '__main__':
    print(Callibrate(image="data/test/2012-09-11_16_48_36_jpg.rf.4ecc8c87c61680ccc73edc218a2c8d7d (2).jpg"))

def __drawPolygons(image):
    pass
