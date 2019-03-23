from keras.models import load_model
from keras import optimizers
from keras.preprocessing import image
import cv2
import numpy as np
import traceback


class Predictor:
    def __init__(self):
        self.model = load_model('model_keras.h5')
        self.model.compile(loss='categorical_crossentropy', optimizer=optimizers.Adam(
            lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False), metrics=['acc'])

    def predict(self, path):
        try:
            img = cv2.imread(path)
            img = cv2.resize(img, (200, 200))
            img = np.reshape(img, [1, 200, 200, 3])
            classes = model.predict_classes(img)
        except Exception as ex:
            print(ex)
            print(traceback.print_exc())
            return False
