from flask import Flask
from flask import render_template
import connexion
from flask_cors import CORS
import argparse
global dbType
app = Flask(__name__)


def parseArgs():
    parser = argparse.ArgumentParser(description='ASL API.')
    parser.add_argument("-p", default=5000,
                        help="Specify port number", action="store")
    parser.add_argument("-t", action="store_true",
                        help="Launch API and run tests")
    return parser.parse_args()


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
    args = parseArgs()
    app = createApp(args)
    app.run(host='0.0.0.0', port=args.p, debug=True)


@app.route('/')
def home():
    return render_template('home.html')
