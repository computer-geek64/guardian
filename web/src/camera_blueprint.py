# camera_blueprint.py

import os
import json
from auth import auth
from flask import Blueprint, render_template


camera_blueprint = Blueprint('camera_blueprint', __name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))

rtsp_urls = json.loads(os.environ['RTSP_URLS'])


@camera_blueprint.route('/stream/<string:camera>/', methods=['GET'])
@auth
def get_camera_stream(camera):
    camera_name = get_camera_name(camera)
    return render_template('camera.html', title=camera_name, camera=camera, camera_name=camera_name), 200


@camera_blueprint.route('/stream/', methods=['GET'])
@auth
def get_camera_streams():
    cameras = {camera: get_camera_name(camera) for camera in rtsp_urls}
    return render_template('cameras.html', title='Guardian', cameras=cameras), 200


def get_camera_name(camera):
    return ' '.join(word.capitalize() for word in camera.split('_'))
