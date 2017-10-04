# import the necessary packages
from transform import four_point_transform
import cv2
import numpy as np

# coords for checkerboard corners found using calibration pattern and gimp
# tl = (489.5, 191.5)
# tr = (1704, 7)
# br = (1645.5, 1918.5)
# bl = (433.5, 1639)

def process_print(raw_image):
    coords = "[(489.5, 191.5), (1704, 7), (1645.5, 1918.5), (433.5, 1639)]"

    # convert the raw image to grayscale
    img = cv2.cvtColor(raw_image, cv2.COLOR_RGB2GRAY)
    img = cv2.equalizeHist(img)
    # make the ridges dark and valleys white
    img = cv2.bitwise_not(img)

    pts = np.array(eval(coords), dtype="float32")

    # apply homography
    warped = four_point_transform(img, pts, aMaxWidth = 290, aMaxHeight = 267)

    return warped
    





