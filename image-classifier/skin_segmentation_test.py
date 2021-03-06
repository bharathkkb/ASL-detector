from matplotlib import pyplot as plt
import imutils
from skin_segmentation import extract_skin
import cv2

image1 = imutils.url_to_image("https://raw.githubusercontent.com/octalpixel/Skin-Extraction-from-Image-and-Finding-Dominant-Color/master/82764696-open-palm-hand-gesture-of-male-hand_image_from_123rf.com.jpg")
image2 = imutils.url_to_image("https://raw.githubusercontent.com/octalpixel/Skin-Extraction-from-Image-and-Finding-Dominant-Color/master/skin.jpg")
image3 = imutils.url_to_image("https://raw.githubusercontent.com/octalpixel/Skin-Extraction-from-Image-and-Finding-Dominant-Color/master/skin_2.jpg")
image4 = imutils.url_to_image("https://raw.githubusercontent.com/octalpixel/Skin-Extraction-from-Image-and-Finding-Dominant-Color/master/Human-Hands-Front-Back-Image-From-Wikipedia.jpg")
test = imutils.url_to_image("https://scontent-lax3-1.xx.fbcdn.net/v/t1.15752-9/59595988_342269703331501_8576568108314001408_n.jpg?_nc_cat=109&_nc_ht=scontent-lax3-1.xx&oh=24f7acde76123d9325db487f70e4d771&oe=5D6B3A9F")

sample_images = [test]
print("Testing!")
for image in sample_images:
    # Resize image to a width of 250
    image = imutils.resize(image,width=250)
    result = extract_skin(image)

    plt.imshow(cv2.cvtColor(result,cv2.COLOR_BGR2RGB))
    plt.show()

