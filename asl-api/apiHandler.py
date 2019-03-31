import json
# TODO: in the future investigate if passing a single instance around is faster than spawning one per thread
from mongoDriver import mongoDriver
from bson import Binary
from PIL import Image
import io
from keras.preprocessing import image
from celeryTask import predict_image_task
from mongoHelpers import get_data_from_db,get_json_from_mongo

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
