# camera_blueprint.py

import os
import json
import uuid
from multiprocessing import shared_memory
from flask import Blueprint, render_template, session


camera_blueprint = Blueprint('camera_blueprint', __name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))

rtsp_urls = json.loads(os.environ['RTSP_URLS'])


@camera_blueprint.route('/stream/<string:camera>/', methods=['GET'])
def get_camera_stream(camera):
    camera_name = get_camera_name(camera)

    stream_id = str(uuid.uuid1())
    session['stream_id'] = stream_id

    shm = shared_memory.SharedMemory(create=True, name=f'guardian_stream_{stream_id}', size=1)
    shm.buf[0] = 0
    shm.close()

    return render_template('camera.html', title=camera_name, camera=camera, camera_name=camera_name), 200


@camera_blueprint.route('/stream/', methods=['GET'])
def get_camera_streams():
    cameras = {camera: get_camera_name(camera) for camera in rtsp_urls}

    stream_id = str(uuid.uuid1())
    session['stream_id'] = stream_id

    shm = shared_memory.SharedMemory(create=True, name=f'guardian_stream_{stream_id}', size=1)
    shm.buf[0] = 0
    shm.close()

    return render_template('cameras.html', title='Guardian', cameras=cameras), 200


@camera_blueprint.route('/stream/heartbeat', methods=['GET'])
def get_stream_heartbeat():
    shm = shared_memory.SharedMemory(name='guardian_stream_' + session.get('stream_id'))
    shm.buf[0] = int(not shm.buf[0])
    shm.close()
    return 'HTTP 200', 200


def get_camera_name(camera):
    return ' '.join(word.capitalize() for word in camera.split('_'))
