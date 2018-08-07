import json
import os
import logging
import pandas as pd
import requests


from flask import Flask, Response, request, jsonify, render_template
from flask_restful import Resource, Api, reqparse, abort

from VarroaPy.VarroaPy.RunVarroaPop import VarroaPop

try:
    from flask_cors import CORS
    cors = True
except ImportError:
    cors = False


app = Flask(__name__)
api = Api(app)
if cors:
    CORS(app)
else:
    logging.debug("CORS not enabled")


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
os.environ.update({
    'PROJECT_ROOT': PROJECT_ROOT
})


### request parser
parser = reqparse.RequestParser()
parser.add_argument('parameters')
parser.add_argument('weather_file')


class VPServer(Resource):
    def get(self):
        return {'hello': 'world'}

    def post(self):
        args = parser.parse_args()
        params = args['parameters']
        print(params)
        params = json.loads(params)
        weather = args['weather_file']
        vp = VarroaPop(parameters= params, weather_file = weather)
        vp.run_model()
        output = vp.get_output(json_str= True)
        return json.loads(output)


api.add_resource(VPServer, '/varroapop/run/')



if __name__ == '__main__':
    app.run(debug=True)