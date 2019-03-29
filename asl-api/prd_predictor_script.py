import argparse
import json
import numpy as np
import requests
import traceback
import cv2
from keras.preprocessing import image


class Predictor:
    def __init__(self):
        self.tf_serving_base = "http://localhost:8501"
        self.tf_serving_version = "v1"
        self.tf_serving_model_name = "asl_classifier_model"

    def predict(self, file):
        try:
            img = image.img_to_array(image.load_img(
                file, target_size=(200, 200)))
            payload = {
                "instances": [img.tolist()]
            }
            r = requests.post("{}/{}/models/{}:predict".format(self.tf_serving_base,
                                                               self.tf_serving_version, self.tf_serving_model_name), json=payload)
            pred = json.loads(r.content.decode('utf-8'))
            return pred
        except Exception as ex:
            print(ex)
            print(traceback.print_exc())
            return False
