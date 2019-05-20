from unittest import TestCase
from mock import patch, Mock
from PIL import Image
import requests
import io
import sys
sys.path.append("../")
from prd_predictor_script import Predictor
def test_get_data_from_db(id):
    imgByteArr = io.BytesIO()
    img=Image.new('RGB', (60, 30), color = 'red')
    img.save(imgByteArr,format='PNG')
    testDict=dict()
    testDict["img_for_pred"]=imgByteArr.getvalue()
    return testDict
def test_update_result_status_to_db(id,status):
    return True
def test_requests_post(url,json):
    assert "instances" in json.keys()
    def _mock_response(
            status=200,
            content="CONTENT",
            json_data=None,
            raise_for_status=None):
        mock_resp = Mock()
        # mock raise_for_status call w/optional error
        mock_resp.raise_for_status = Mock()
        if raise_for_status:
            mock_resp.raise_for_status.side_effect = raise_for_status
        # set status code and content
        mock_resp.status_code = status
        mock_resp.content = content
        # add json data if provided
        if json_data:
            mock_resp.json = Mock(
                return_value=json_data
            )
        return mock_resp
    return _mock_response(content='{"foo":"bar"}'.encode('utf-8'))
def test_update_result_data_to_db(id,prediction):
    assert prediction is not None
class Predictor_testing(TestCase):
    """
    The basic class that inherits TestCase
    """
    def test_configs(self):
        predictor=Predictor()
        assert predictor.tf_serving_base == "http://localhost:8501"
        assert predictor.tf_serving_version == "v1"
        assert predictor.tf_serving_model_name == "asl_classifier_model"
    @patch('mongoHelpers.MongoHelper.get_data_from_db', side_effect=test_get_data_from_db)
    @patch('mongoHelpers.MongoHelper.update_result_data_to_db', side_effect=test_update_result_data_to_db)
    @patch('mongoHelpers.MongoHelper.update_result_status_to_db', side_effect=test_update_result_status_to_db)
    @patch('requests.post', side_effect=test_requests_post)
    def test_prediction(self,get_data_from_db_func,update_result_data_to_db_func,update_result_status_to_db_func,post_func):
        predictor=Predictor()
        pred=predictor.predict("test")

