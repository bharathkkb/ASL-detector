from matplotlib import pyplot as plt
import imutils
from skin_segmentation import extract_skin
import cv2

image1 = imutils.url_to_image("https://raw.githubusercontent.com/octalpixel/Skin-Extraction-from-Image-and-Finding-Dominant-Color/master/82764696-open-palm-hand-gesture-of-male-hand_image_from_123rf.com.jpg")
image2 = imutils.url_to_image("https://raw.githubusercontent.com/octalpixel/Skin-Extraction-from-Image-and-Finding-Dominant-Color/master/skin.jpg")
image3 = imutils.url_to_image("https://raw.githubusercontent.com/octalpixel/Skin-Extraction-from-Image-and-Finding-Dominant-Color/master/skin_2.jpg")
image4 = imutils.url_to_image("https://raw.githubusercontent.com/octalpixel/Skin-Extraction-from-Image-and-Finding-Dominant-Color/master/Human-Hands-Front-Back-Image-From-Wikipedia.jpg")
z_test = imutils.url_to_image("https://raw.githubusercontent.com/bharathkkb/ASL-detector/master/asl-api/asl_alphabet_test/Z_test.jpg?token=ACQSWNQ3TQCIVKHU4EBNIAK43FNFU")

sample_images = [image1, image2, image3, image4, z_test]
print("Testing!")
for image in sample_images:
    # Resize image to a width of 250
    image = imutils.resize(image,width=250)
    result = extract_skin(image)

    plt.imshow(cv2.cvtColor(result,cv2.COLOR_BGR2RGB))
    plt.show()

