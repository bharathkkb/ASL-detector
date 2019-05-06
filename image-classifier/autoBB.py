import cv2
import sys
import logging as log
import datetime as dt
from time import sleep


class handDetector:
    def __init__(self, cascadeXML):
        self.cascadePath = cascadeXML
        self.handDetector = cv2.CascadeClassifier(self.cascadePath)

    def dectectHand(self, img):
        #make to grey scale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        hands = self.handDetector.detectMultiScale(
            gray,
            scaleFactor=1.05,
            minNeighbors=5,
            minSize=(50, 50)
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
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            return img
        else:
            print("No hand found")
            return False


if __name__ == '__main__':
    imgpath = "test-bb4.jpg"
    img = cv2.imread(imgpath, 1)
    #haar cascade from https://github.com/pallabganguly/opcv-project
    hd = handDetector("hand_hc.xml")
    imgProcessed = hd.dectectHand(img)
    cv2.imshow('image', imgProcessed)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
