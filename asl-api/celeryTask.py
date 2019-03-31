from flask import Flask
from celeryConf import make_celery
from server import *
flask_app = createAppThread()
flask_app.app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)

celery = make_celery(flask_app)

@celery.task()
def add_together(a, b):
    return a + b
