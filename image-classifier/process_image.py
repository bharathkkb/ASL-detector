import cv2
import numpy as np
from skin_segmentation import extract_skin


def equalize_histogram_clahe(img):
    img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    planes = cv2.split(img_yuv)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))

    planes[0] = clahe.apply(planes[0])

    img_yuv = cv2.merge(planes)
    img_output = cv2.cvtColor(img_yuv, cv2.COLOR_LAB2BGR)
    return img_output

def equalize_histogram(img):
    img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    # equalize the histogram of the Y channel
    img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
    # convert the YUV image back to RGB format
    img_output = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
    return img_output

def remove_non_skin(img):
    """
    Extract the skin from the image by masking everything else with black pixels
    
    Input: image
    Output: cv2 image
    """
    return extract_skin(img)