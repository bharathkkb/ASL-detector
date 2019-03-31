from celery import Celery
from prd_predictor_script import Predictor
import json
import os

app = Celery('tasks')
SECRET_KEY = os.environ.get('AM_I_IN_A_DOCKER_CONTAINER', False)
if SECRET_KEY:
    app.conf.result_backend = 'redis://redis:6379/0'
    app.conf.broker_url = 'redis://redis:6379/0'
else:
    app.conf.result_backend = 'redis://localhost:6379/0'
    app.conf.broker_url = 'redis://localhost:6379/0'


@app.task()
def predict_image_task(id):
    predictor = Predictor()
    prediction = predictor.predict(id)
    return prediction

@app.task
def add(x, y):
    return x + y
