import json
# TODO: in the future investigate if passing a single instance around is faster than spawning one per thread
from prd_predictor_script import Predictor
from mongoDriver import mongoDriver
from bson import Binary
from PIL import Image
import io
from keras.preprocessing import image
def predict_image(file_to_upload):
    image_id=create_pred_doc(file_to_upload)

    predictor = Predictor()
    prediction = predictor.predict(image_id)
    if(prediction):
        return {"prediction": prediction}, 200
    else:
        return False, 500


def create_pred_doc(img_file):
    imgByteArr = io.BytesIO()
    img_file.save(imgByteArr)
    imgByteArr = imgByteArr.getvalue()

    mongo= mongoDriver()
    payload = dict()
    payload["img_for_pred"]=imgByteArr
    payload["result"]="queue"
    r= mongo.putDict("asl-db", "testimg", payload)
    return r.inserted_id
