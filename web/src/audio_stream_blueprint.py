# audio_stream_blueprint.py

import os
import json
from auth import auth
from subprocess import Popen, PIPE, DEVNULL
from flask import Blueprint, Response, stream_with_context


audio_stream_blueprint = Blueprint('audio_stream_blueprint', __name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))

rtsp_urls = json.loads(os.environ['RTSP_URLS'])


class RTSPAudioStream(object):
    def __init__(self, rtsp_url):
        self.process = Popen(['ffmpeg', '-rtsp_transport', 'tcp', '-i', rtsp_url, '-vn', '-f', 'wav', 'pipe:stdout'], stdout=PIPE, stderr=DEVNULL)

    def __del__(self):
        self.process.terminate()
        print('Successfully exited audio stream')


@audio_stream_blueprint.route('/stream/<string:camera>/audio.wav', methods=['GET'])
@auth
def get_camera_stream_audio(camera):
    rtsp_audio_stream = RTSPAudioStream(rtsp_urls[camera])
    return Response(stream_with_context(generate_wav(rtsp_audio_stream)), mimetype='audio/wav')


def generate_wav(rtsp_audio_stream):
    while True:
        data = rtsp_audio_stream.process.stdout.read(1024)
        yield data
