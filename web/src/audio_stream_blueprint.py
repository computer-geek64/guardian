# audio_stream_blueprint.py

import os
import json
from subprocess import Popen, PIPE, DEVNULL
from flask import Blueprint, Response, stream_with_context


audio_stream_blueprint = Blueprint('audio_stream_blueprint', __name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))

rtsp_urls = json.loads(os.environ['RTSP_URLS'])


@audio_stream_blueprint.route('/stream/<string:camera>/audio.wav', methods=['GET'])
def get_camera_stream_audio(camera):
    ffmpeg_process = Popen(['ffmpeg', '-rtsp_transport', 'tcp', '-i', rtsp_urls[camera], '-vn', '-f', 'wav', 'pipe:stdout'], stdout=PIPE, stderr=DEVNULL)
    return Response(stream_with_context(generate_wav(ffmpeg_process)), mimetype='audio/wav')


def generate_wav(ffmpeg_process):
    try:
        while True:
            data = ffmpeg_process.stdout.read(1024)
            yield data
    finally:
        ffmpeg_process.terminate()
        print('Terminated')


