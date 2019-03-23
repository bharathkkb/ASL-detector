import json
# TODO: in the future investigate if passing a single instance around is faster than spawning one per thread
from prd_predictor_script import Predictor


def predict_image(file_to_upload):
    predictor = Predictor()
    prediction = predictor.predict(file_to_upload)
    if(prediction):
        return {"prediction": prediction}, 200
    else:
        return False, 500
