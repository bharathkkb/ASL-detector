import cv2
import sys
import logging as log
import datetime as dt
from time import sleep


def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized

class handDetector:
    def __init__(self, cascadeXML):
        self.cascadePath = cascadeXML
        self.handDetector = cv2.CascadeClassifier(self.cascadePath)

    def dectectHand(self, img):
        #make to grey scale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        hands = self.handDetector.detectMultiScale(
            gray,
            scaleFactor=1.5,
            minNeighbors=1,
            minSize=(100, 100)
        )
        #keep track of biggest ROI
        biggestBoundArea=0
        biggestBound=None
        for hand in hands:
            x,y,w,h=hand
            area = w*h
            if area>biggestBoundArea:
                biggestBoundArea=area
                biggestBound=hand
        if(biggestBound is not None):
            x,y,w,h=biggestBound
            # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            roi= img[y:y+h, x:x+w]
            return image_resize(roi,200,200)
        else:
            print("No hand found")
            return False

def getHand(img):
    hd = handDetector("hand_hc.xml")
    imgProcessed = hd.dectectHand(img)
    return imgProcessed
if __name__ == '__main__':
    imgpath = "rand.jpg"
    img = cv2.imread(imgpath, 1)
    #haar cascade from https://github.com/pallabganguly/opcv-project
    imgProcessed = getHand(img)
    cv2.imshow('image', imgProcessed)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
