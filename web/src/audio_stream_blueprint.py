# audio_stream_blueprint.py

import os
import json
import signal
import redis
from time import sleep
from datetime import datetime
from multiprocessing import shared_memory
from subprocess import Popen, PIPE, DEVNULL
from flask import Blueprint, Response, stream_with_context, session


audio_stream_blueprint = Blueprint('audio_stream_blueprint', __name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))

rtsp_urls = json.loads(os.environ['RTSP_URLS'])


@audio_stream_blueprint.route('/stream/<string:camera>/audio.mp3', methods=['GET'])
def get_camera_stream_audio(camera):
    if 'stream_id' not in session or camera not in rtsp_urls:
        return 'HTTP 400', 400

    return Response(stream_with_context(generate_wav(camera)), mimetype='audio/mpeg')


def generate_wav(camera):
    redis_client = redis.Redis(host='redis')
    redis_pubsub = redis_client.pubsub()
    redis_pubsub.subscribe(f'{camera}_audio_stream')

    last_heartbeat_timestamp = datetime.now().timestamp()
    shm = shared_memory.SharedMemory(name='guardian_stream_' + session.get('stream_id'))
    last_heartbeat_value = shm.buf[0]

    for message in redis_pubsub.listen():
        current_timestamp = datetime.now().timestamp()
        if shm.buf[0] != last_heartbeat_value:
            last_heartbeat_value = shm.buf[0]
            last_heartbeat_timestamp = current_timestamp
        elif current_timestamp - last_heartbeat_timestamp >= 7:
            break

        if isinstance(message, dict) and message['type'] == 'message':
            if message['channel'].decode() == f'{camera}_audio_stream':
                yield message['data']

    redis_pubsub.unsubscribe()
    redis_client.close()
    shm.close()

    sleep(1)
    if camera != next(iter(rtsp_urls)):
        shm.unlink()
