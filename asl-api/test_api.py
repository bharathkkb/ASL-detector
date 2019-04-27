
from swagger_spec_validator import validate_spec_url
from server import createApp, createAppThread
import flex
import requests
from flex.core import load, validate_api_call
import pprint
import pytest
import json
import sys
import time
import threading
from requests.exceptions import ConnectionError
"""
**************************************
Setup
**************************************
"""


def appThread():
    app = createAppThread()
    app.run(host='0.0.0.0', port=5000, debug=False)


def test_start_daemon_api_thread(local):
    print(local)
    if(local == "0"):
        print("Starting daemon serve thread")
        apiThread = threading.Thread(name='Web App', target=appThread)
        apiThread.setDaemon(True)
        apiThread.start()

        while not apiThread.is_alive():
            pass
    else:
        print(
            "Not starting daemon serve thread, assuming server running in a seperate process")


def test_thread(url):
    maxTry = 10000
    currentTry = 0
    while currentTry < maxTry:
        currentTry += 1
        try:
            testAPIBasePath = "{}/test/api".format(url)
            response = requests.get(testAPIBasePath + '/hello', timeout=10000)
            if(response.status_code == 200):
                break
        except ConnectionError as ex:
            pass


"""
**************************************
Swagger Infra Tests
**************************************
"""


def validateSwagger(url):
    testAPIBasePath = "{}/test/api".format(url)
    validate_spec_url(testAPIBasePath + '/swagger.json')

# check connection to server


def test_case_connection(url):
    testAPIBasePath = "{}/test/api".format(url)
    response = requests.get(testAPIBasePath + '/hello')
    assert response.status_code == 200

def test_case_mongo_connection(url):

    response = requests.get("http://localhost:27017/")
    assert response.status_code == 200

def test_case_tf_serving_connection(url):

    response = requests.get("http://localhost:8501/v1/models/asl_classifier_model")
    assert response.status_code == 200

# pytest for validating swagger schema


def test_validateSwagger(url):
    assert validateSwagger(url) == None

# helper for validate hello schema


def hello_schema(url, schema):
    testAPIBasePath = "{}/test/api".format(url)
    response = requests.get(testAPIBasePath + '/hello')
    validate_api_call(schema, raw_request=response.request,
                      raw_response=response)

# pytest for validating hello schema


def test_hello_schema(url):
    testAPIBasePath = "{}/test/api".format(url)
    schema = flex.load(testAPIBasePath + '/swagger.json')
    assert hello_schema(url, schema) == None

# pytest for validating data returned by /hello endpoint


def test_hello_data(url):
    testAPIBasePath = "{}/test/api".format(url)
    response = requests.get(testAPIBasePath + '/hello')
    data = response.json()
    print(data)
    assert data["hello"] == "hello"


def test_pred_A(url):
    testAPIBasePath = "{}/test/api/predict".format(url)
    files = {'file_to_upload': open('A_test.jpg', 'rb')}
    response = requests.post(testAPIBasePath, files=files)
    data = response.json()
    pytest.shared = data["id"]
    assert response.status_code == 200

def test_job_A(url):
    testAPIBasePath = "{}/test/api/predict".format(url)
    files = {'file_to_upload': open('A_test.jpg', 'rb')}
    response = requests.post(testAPIBasePath, files=files)
    payload = response.json()
    testAPIBasePath = "{}/test/api/job".format(url)
    response = requests.post(testAPIBasePath, data={'id':payload['id'] })
    data = response.json()
    timeout=0
    while (data["result"] != "complete" and timeout <5):
        testAPIBasePath = "{}/test/api/job".format(url)
        response = requests.post(testAPIBasePath, data={'id':payload['id'] })
        data = response.json()
        timeout+=1
        time.sleep(2)
        #wait till job is complete or is timedout
    assert response.status_code == 200
    assert data["_id"] == payload['id']
    assert data["result"] == "complete"
    assert data["prediction"]["predictions"][0][0] == 1

def test_crop(url):
    testAPIBasePath = "{}/test/api/crop".format(url)
    files = {'file_to_upload': open('test_crop.jpg', 'rb')}
    response = requests.post(testAPIBasePath, files=files)
    data = response.json()
    assert data['croppedimg'] == "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"
    assert response.status_code == 200


# # this is for debugging individual tests
# # if __name__ == "__main__":
# #     test_hello_data()
