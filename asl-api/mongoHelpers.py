##helpers
from mongoDriver import mongoDriver
from bson import ObjectId

import json


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

def get_json_from_mongo(data):
    if(data.get("img_for_pred",False)):
        data.pop("img_for_pred")
    return json.loads(JSONEncoder().encode(data))
def get_data_from_db(id):
    try:
        query = dict()
        query["_id"] = ObjectId(id)
        returnData = mongoDriver().getFindOne("asl-db", "testimg", query)
        return returnData
    except Exception as ex:
        print(ex)
        print(traceback.print_exc())
        return False

def update_result_status_to_db(id,status):
    try:
        query = dict()
        query["_id"] = ObjectId(id)
        returnData= mongoDriver().getFindOne("asl-db", "testimg", query)
        returnData["result"]=status
        update=mongoDriver().updateDict("asl-db", "testimg", returnData)
        print(update)
    except Exception as ex:
        print(ex)
        print(traceback.print_exc())
        return False

def update_result_data_to_db(id,data):
    try:
        query = dict()
        query["_id"] = ObjectId(id)
        returnData= mongoDriver().getFindOne("asl-db", "testimg", query)
        returnData["prediction"]=data
        update=mongoDriver().updateDict("asl-db", "testimg", returnData)
        print(update)
    except Exception as ex:
        print(ex)
        print(traceback.print_exc())
        return False
