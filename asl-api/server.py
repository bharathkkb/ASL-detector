from flask import Flask
from flask import render_template
import connexion
from flask_cors import CORS
import argparse
from google.cloud import storage
global dbType
app = Flask(__name__)


def parseArgs():
    parser = argparse.ArgumentParser(description='ASL API.')
    parser.add_argument("-p", default=5000,
                        help="Specify port number", action="store")
    parser.add_argument("-t", action="store_true",
                        help="Launch API and run tests")
    return parser.parse_args()

# TODO download blob is slow due to chunking, fix later. use gsutil now
# def download_blob(bucket_name, source_blob_name, destination_file_name):
#     """Downloads a blob from the bucket."""
#     storage_client = storage.Client()
#     bucket = storage_client.get_bucket(bucket_name)
#     blob = bucket.blob(source_blob_name)
#
#     blob.download_to_filename(destination_file_name)
#
#     print('Blob {} downloaded to {}.'.format(
#         source_blob_name,
#         destination_file_name))


def createAppThread():

    print("API V1")
    app = connexion.App(__name__, specification_dir='./',
                        arguments={'is_testing': '/test'})
    dbType = "testing_db"
    CORS(app.app)
    app.add_api('swagger.yaml')
    return app


def createApp(args):

    print("API V1")
    if(args.t is True):
        app = connexion.App(__name__, specification_dir='./',
                            arguments={'is_testing': '/test'})
        dbType = "testing_db"
    else:
        app = connexion.App(__name__, specification_dir='./',
                            arguments={'is_testing': ''}, options={"swagger_ui": False})
        dbType = "prd_db"
    CORS(app.app)
    app.add_api('swagger.yaml')
    return app


if __name__ == '__main__':
    # download_blob("asl-models", "model_keras.h5", "model_keras.h5")
    args = parseArgs()
    app = createApp(args)
    app.run(host='0.0.0.0', port=args.p, debug=True)


@app.route('/')
def home():
    return render_template('home.html')
