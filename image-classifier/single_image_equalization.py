import cv2
import numpy as np
import glob
import os

img = cv2.imread("./test.png")

img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
planes = cv2.split(img_yuv)
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))

planes[0] = clahe.apply(planes[0])

img_yuv = cv2.merge(planes)
img_output = cv2.cvtColor(img_yuv, cv2.COLOR_LAB2BGR)

cv2.imshow("Display",img_output)
cv2.waitKey(0);