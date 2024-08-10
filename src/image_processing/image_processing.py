import cv2 as cv


def imshow(self, image, pause=0):
    cv.namedWindow("main")
    cv.imshow("main", image)
    cv.waitKey(pause)
    cv.destroyWindow("main")