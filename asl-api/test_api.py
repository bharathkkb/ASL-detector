
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
    print(data)
    assert data["prediction"]["predictions"][0][0] == 1

# # this is for debugging individual tests
# # if __name__ == "__main__":
# #     test_hello_data()
