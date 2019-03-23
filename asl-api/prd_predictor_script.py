from keras.models import load_model
from keras import optimizers
from keras.preprocessing import image
import cv2
import numpy as np
import traceback


class Predictor:
    def __init__(self):
        self.model = load_model('model_keras_old.h5')
        self.model.compile(loss='categorical_crossentropy', optimizer=optimizers.Adam(
            lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False), metrics=['acc'])

    def predict(self, file):
        try:
            filestr = file.read()
            npimg = np.fromstring(filestr, np.uint8)
            img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
            # print(path)
            # img = cv2.imread(path)
            img = cv2.resize(img, (200, 200))
            img = np.reshape(img, [1, 200, 200, 3])
            classes = self.model.predict_classes(img)
            return classes.tolist()
        except Exception as ex:
            print(ex)
            print(traceback.print_exc())
            return False
