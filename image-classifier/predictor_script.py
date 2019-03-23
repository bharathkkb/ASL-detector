from keras.models import load_model
from keras import optimizers
import cv2
import numpy as np
model = load_model('model_keras.h5')
model.load_weights('model_weights.h5')
model.compile(loss='categorical_crossentropy',
              optimizer=optimizers.RMSprop(lr=1e-4), metrics=['acc'])

img = cv2.imread('Y_test.jpg')
img = cv2.resize(img, (200, 200))
img = np.reshape(img, [1, 200, 200, 3])
classes = model.predict_classes(img)

print(classes)
