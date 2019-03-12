from PIL import Image
import io
from bson import Binary
from mongoDriver import mongoDriver
if __name__ == "__main__":
    img_name="test.png"
    img = Image.open(img_name)

    imgByteArr = io.BytesIO()
    img.save(imgByteArr, format='PNG')
    imgByteArr = imgByteArr.getvalue()
    mongo= mongoDriver()
    payload = dict()
    payload["img_id"] = "01"
    payload["img_name"]=img_name
    payload["img_data"]=imgByteArr
    mongo.putDict("asl-db", "testimg", payload)
    query = dict()
    query["img_id"] = "01"
    returnData= mongoDriver().getFindOne("asl-db", "testimg", query)
    returnImg= Image.open(io.BytesIO(returnData["img_data"]))
    returnImg.show()
