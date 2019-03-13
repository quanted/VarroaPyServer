import json
import os
import logging

from flask import Flask, Response, request, jsonify, render_template, send_file, send_from_directory
from flask_restful import Resource, Api, reqparse, abort
from waitress import serve
from utilities import clean_files


from VarroaPy.VarroaPy.RunVarroaPop import VarroaPop

LOCAL_DEV = False

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
        clean_files(os.path.abspath('VarroaPy/VarroaPy/files/input'), 7)
        clean_files(os.path.abspath('VarroaPy/VarroaPy/files/logs'), 7)
        clean_files(os.path.abspath('VarroaPy/VarroaPy/files/output'), 7)
        args = parser.parse_args()
        params = args['parameters']
        params = json.loads(params.replace("'", '"'))
        weather = args['weather_file']
        vp = VarroaPop(parameters= params, weather_file=weather, logs=True, keep_files=True)
        vp.run_model()
        output = vp.get_output(json_str= True)
        jobID = vp.get_jobID()
        return json.loads(output), {"session-id": jobID}


class VPGetInput(Resource):
    def get(self, session_id):
        path = os.path.abspath('VarroaPy/VarroaPy/files/input/')
        filename = 'vp_input_' + session_id + '.txt'
        return send_from_directory(path,filename)


class VPGetLog(Resource):
    def get(self, session_id):
        path = os.path.abspath('VarroaPy/VarroaPy/files/logs/')
        filename = 'vp_log_' + session_id + '.txt'
        return send_from_directory(path,filename)


class VPGetOutput(Resource):
    def get(self, session_id):
        path = os.path.abspath('VarroaPy/VarroaPy/files/output/')
        filename = 'vp_results_' + session_id + '.txt'
        return send_from_directory(path,filename)


api.add_resource(VPServer, '/varroapop/run/')
api.add_resource(VPGetInput, '/varroapop/files/input/<session_id>')
api.add_resource(VPGetLog, '/varroapop/files/logs/<session_id>')
api.add_resource(VPGetOutput, '/varroapop/files/output/<session_id>')


if __name__ == '__main__':
    #app.run(debug=True)
    #app.run(host='0.0.0.0', port=80)
    if LOCAL_DEV:
        serve(app, host='127.0.0.1', port=5050)
    else:
        serve(app, host='0.0.0.0', port=5050)

