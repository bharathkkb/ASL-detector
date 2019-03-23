from keras.models import load_model
from keras import optimizers
import cv2
import numpy as np
import argparse

#Call is as follows python3 predictor_script.py './path_to_image/img_name.jpg

model = load_model('model_keras.h5')
model.load_weights('model_weights.h5')
model.compile(loss='categorical_crossentropy',
              optimizer=optimizers.RMSprop(lr=1e-4), metrics=['acc'])

parser = argparse.ArgumentParser(description='Get Image Location')
parser.add_argument("img_location")
args = parser.parse_args()

img = cv2.imread(args.img_location)
img = cv2.resize(img, (200, 200))
img = np.reshape(img, [1, 200, 200, 3])
classes = model.predict_classes(img)

print(classes)
