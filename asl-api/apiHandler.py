import json
# TODO: in the future investigate if passing a single instance around is faster than spawning one per thread
from mongoDriver import mongoDriver
from bson import Binary
from PIL import Image
import cv2
import numpy as np
import io
import base64
from keras.preprocessing import image
from celeryTask import predict_image_task
from mongoHelpers import get_data_from_db,get_json_from_mongo
from autoBB import getHand
def predict_image_endpoint(file_to_upload):
    image_id=create_pred_doc(file_to_upload)

    result=predict_image_task.delay(str(image_id))
    if(image_id):
        return {"id": str(image_id)}, 200
    else:
        return False, 500

def get_job(id):
    result=get_data_from_db(id)
    if(result):
        return get_json_from_mongo(result), 200
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

def create_crop_img(file_to_upload):
    try:
        img = Image.open(file_to_upload)
        opencvImage = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        croppedimg=getHand(opencvImage)
        retval, buffer=cv2.imencode('.jpg', croppedimg)
        base64_img_bytes = base64.b64encode(buffer)
        base64_string = base64_img_bytes.decode('utf-8')
        returnCrop=dict()
        returnCrop["croppedimg"]=base64_string
        return returnCrop,200
    except Exception as e:
        print(e)
        return False, 500
