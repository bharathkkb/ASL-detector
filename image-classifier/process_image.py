import cv2
import numpy as np
from skin_segmentation import extract_skin


def equalize_histogram_clahe(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv[:,:,2] += 20
    img_bright = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    img_yuv = cv2.cvtColor(img_bright, cv2.COLOR_BGR2YUV)
    planes = cv2.split(img_yuv)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))

    planes[0] = clahe.apply(planes[0])

    img_yuv = cv2.merge(planes)
    img_output = cv2.cvtColor(img_yuv, cv2.COLOR_LAB2BGR)
    
    return img_output

def equalize_histogram_clahe_flip(img):
    img2 = cv2.flip( img, 1 )
    img_yuv = cv2.cvtColor(img2, cv2.COLOR_BGR2YUV)
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

train_dir = '/asl-data/asl_alphabet_test'

test_dir = '../new-asl-data/asl_alphabet_test_real_world_+_kaggle'

test_images = []

# Load Images from directory and store them in an array of test_images
for image_dir in glob.iglob(test_dir + '/**/*.jpg', recursive=True):
  test_images.append(image_dir)

for image_dir in glob.iglob(test_dir + '/**/*.png', recursive=True):
  test_images.append(image_dir)

for image in test_images:
  img = None
  image_name = image.split('/').pop()
  print(image_name)
  if image_name[0:5] == "color":
    img = equalize_histogram_clahe_flip(cv2.imread(image))
  else:
    img = equalize_histogram_clahe(cv2.imread(image))

    
  image_dir = image.split('/')[3]
  if not os.path.exists('../new-asl-data/asl_alphabet_test_real_world_+_kaggle/modified/'+ image_dir):
    os.makedirs('../new-asl-data/asl_alphabet_test_real_world_+_kaggle/modified/'+ image_dir)
  
  cv2.imwrite(os.path.join('../new-asl-data/asl_alphabet_test_real_world_+_kaggle/modified/' +image_dir , image_name), img)
    

