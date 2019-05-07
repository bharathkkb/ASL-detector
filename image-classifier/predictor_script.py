from keras.models import load_model
from keras import optimizers
from keras.preprocessing import image
import cv2
import numpy as np
import traceback
import process_image

class Predictor:
    def __init__(self):
        self.model = load_model('./model_keras_new_kushal.h5')
        self.model.compile(loss='categorical_crossentropy', optimizer=optimizers.Adam(
            lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False), metrics=['acc'])

    def predict(self, path):
        model = self.model
        try:
            img = cv2.imread(path)
            img = cv2.resize(img, (200, 200))
            img = process_image.equalize_histogram_clahe(img)
            img = np.reshape(img, [1, 200, 200, 3])
            classes = model.predict_classes(img)
            print(classes)
        except Exception as ex:
            print(ex)
            print(traceback.print_exc())
            return False


predict = Predictor()
predict.predict('../asl-data/asl_alphabet_test/D_test.jpg')