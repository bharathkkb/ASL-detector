import argparse
import json
import numpy as np
import requests
import traceback
import cv2
from PIL import Image
import io
from keras.preprocessing import image
from mongoHelpers import *


class Predictor:
    def __init__(self):
        self.tf_serving_base = "http://localhost:8501"
        self.tf_serving_version = "v1"
        self.tf_serving_model_name = "asl_classifier_model"

    def predict(self, img_id):
        try:
            data=get_data_from_db(img_id)
            print(img_id)
            image_to_pred = Image.open(io.BytesIO(data["img_for_pred"]))
            img = image.img_to_array(image_to_pred)
            payload = {
                "instances": [img.tolist()]
            }
            update_result_status_to_db(img_id,"processing")
            r = requests.post("{}/{}/models/{}:predict".format(self.tf_serving_base,
                                                               self.tf_serving_version, self.tf_serving_model_name), json=payload)
            pred = json.loads(r.content.decode('utf-8'))
            update_result_status_to_db(img_id,"complete")
            update_result_data_to_db(img_id,pred)
            return pred
        except Exception as ex:
            print(ex)
            print(traceback.print_exc())
            return False
