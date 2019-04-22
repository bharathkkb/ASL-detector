import cv2
import numpy as np
import glob
import os

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

train_dir = '/asl-data/asl_alphabet_test'
test_dir = '../asl-data/asl_alphabet_train'

test_images = []

# Load Images from directory and store them in an array of test_images
for image_dir in glob.iglob(test_dir + '/**/*.jpg', recursive=True):
    test_images.append(image_dir)


for image in test_images:
    image_name = image.split('/').pop()
    image_dir = image.split('/')[3]
    img = equalize_histogram_clahe(cv2.imread(image))
    if not os.path.exists('../asl-data/asl_alphabet_modified/'+ image_dir):
       os.makedirs('../asl-data/asl_alphabet_modified/'+ image_dir)
   
    cv2.imwrite(os.path.join('../asl-data/asl_alphabet_modified/' +image_dir , image_name), img)
    

    