# audio_stream_blueprint.py

import os
import json
import signal
from time import sleep
from datetime import datetime
from multiprocessing import shared_memory
from subprocess import Popen, PIPE, DEVNULL
from flask import Blueprint, Response, stream_with_context, session


audio_stream_blueprint = Blueprint('audio_stream_blueprint', __name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))

rtsp_urls = json.loads(os.environ['RTSP_URLS'])


class RTSPAudioStream(object):
    def __init__(self, camera):
        self.camera = camera
        self.process = Popen(['ffmpeg', '-rtsp_transport', 'tcp', '-i', rtsp_urls[camera], '-vn', '-f', 'wav', 'pipe:stdout'], stdout=PIPE, stderr=DEVNULL)

    def __del__(self):
        self.process.send_signal(signal.SIGKILL)


@audio_stream_blueprint.route('/stream/<string:camera>/audio.wav', methods=['GET'])
def get_camera_stream_audio(camera):
    if 'stream_id' not in session:
        return 'HTTP 400', 400

    process = Popen(['ffmpeg', '-rtsp_transport', 'tcp', '-i', rtsp_urls[camera], '-vn', '-f', 'wav', 'pipe:stdout'], stdout=PIPE, stderr=DEVNULL)
    return Response(stream_with_context(generate_wav(camera, process)), mimetype='audio/x-wav')


def generate_wav(camera, process):
    last_heartbeat_timestamp = datetime.now().timestamp()
    shm = shared_memory.SharedMemory(name='guardian_stream_' + session.get('stream_id'))
    last_heartbeat_value = shm.buf[0]
    while True:
        current_timestamp = datetime.now().timestamp()
        if shm.buf[0] != last_heartbeat_value:
            last_heartbeat_value = shm.buf[0]
            last_heartbeat_timestamp = current_timestamp
        elif current_timestamp - last_heartbeat_timestamp >= 7:
            break

        data = process.stdout.read(1024)
        yield data

    process.send_signal(signal.SIGKILL)
    shm.close()

    sleep(1)
    if camera != next(iter(rtsp_urls)):
        shm.unlink()
