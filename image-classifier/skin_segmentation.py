import numpy as np
import cv2
from sklearn.cluster import KMeans
from collections import Counter
import pprint

def extract_skin(image):
    """
    Using thresholding technique on HSV color space 
    to extract skin pixels form the image
<<<<<<< HEAD

=======
>>>>>>> master
    input: image
    output: cv2 image
    """
    # Taking a copy of the image
    img =  image.copy()
    # Converting from BGR Colours Space to HSV
    img =  cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
<<<<<<< HEAD
    
    # Defining HSV Threadholds
    lower_threshold = np.array([0, 48, 80], dtype=np.uint8)
    upper_threshold = np.array([20, 255, 255], dtype=np.uint8)
    
    # Single Channel mask,denoting presence of colours in the about threshold
    skin_mask = cv2.inRange(img,lower_threshold,upper_threshold)
    
    # Cleaning up mask using Gaussian Filter
    skin_mask = cv2.GaussianBlur(skin_mask,(3,3),0)
    
    # Extracting skin from the threshold mask
    skin = cv2.bitwise_and(img,img,mask=skin_mask)
    
=======

    # Defining HSV Threadholds
    lower_threshold = np.array([0, 12, 20], dtype=np.uint8)
    upper_threshold = np.array([40, 255, 255], dtype=np.uint8)

    # Single Channel mask,denoting presence of colours in the about threshold
    skin_mask = cv2.inRange(img,lower_threshold,upper_threshold)

    # Cleaning up mask using Gaussian Filter
    skin_mask = cv2.GaussianBlur(skin_mask,(3,3),0)

    # Extracting skin from the threshold mask
    skin = cv2.bitwise_and(img,img,mask=skin_mask)

>>>>>>> master
    # Return the Skin image
    return cv2.cvtColor(skin,cv2.COLOR_HSV2BGR)


def remove_black(estimator_labels, estimator_cluster):
    """
    Utility function to remove pixels from the extracted skin
    """

    # Check for black
    hasBlack = False

    # Get the total number of occurance for each color
    occurance_counter = Counter(estimator_labels)


    # Quick lambda function to compare to lists
    compare = lambda x, y: Counter(x) == Counter(y)

    # Loop through the most common occuring color
    for x in occurance_counter.most_common(len(estimator_cluster)):

        # Quick List comprehension to convert each of RBG Numbers to int
        color = [int(i) for i in estimator_cluster[x[0]].tolist() ]

    # Check if the color is [0,0,0] that if it is black 
    if compare(color , [0,0,0]) == True:
        # delete the occurance
        del occurance_counter[x[0]]
        # remove the cluster 
        hasBlack = True
        estimator_cluster = np.delete(estimator_cluster,x[0],0)
        # break
<<<<<<< HEAD
    return (occurance_counter,estimator_cluster,hasBlack)
=======
    return (occurance_counter,estimator_cluster,hasBlack)
>>>>>>> master
