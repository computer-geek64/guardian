# camera_blueprint.py

import os
import json
from flask import Blueprint, render_template


camera_blueprint = Blueprint('camera_blueprint', __name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))

rtsp_urls = json.loads(os.environ['RTSP_URLS'])


@camera_blueprint.route('/stream/<string:camera>/', methods=['GET'])
def get_camera_stream(camera):
    return render_template('camera.html', title=camera.capitalize(), camera=camera), 200


@camera_blueprint.route('/stream/', methods=['GET'])
def get_camera_streams():
    cameras = {camera_name: ' '.join(word.capitalize() for word in camera_name.split('_')) for camera_name in rtsp_urls}
    return render_template('cameras.html', title='Guardian', cameras=cameras), 200
