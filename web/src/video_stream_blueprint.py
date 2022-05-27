# video_stream_blueprint.py

import os
import json
import redis
from time import sleep
from datetime import datetime
from multiprocessing import shared_memory
from flask import Blueprint, Response, stream_with_context, session


video_stream_blueprint = Blueprint('video_stream_blueprint', __name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))

rtsp_urls = json.loads(os.environ['RTSP_URLS'])


@video_stream_blueprint.route('/stream/<string:camera>/<string:resolution>.jpg', methods=['GET'])
def get_camera_stream_jpeg(camera, resolution):
    if 'stream_id' not in session or camera not in rtsp_urls or resolution not in {'raw', 'hd', 'sd'}:
        return 'HTTP 400', 400

    return Response(stream_with_context(generate_frames(camera, resolution)), mimetype='multipart/x-mixed-replace; boundary=frame'), 200


def generate_frames(camera, resolution):
    redis_client = redis.Redis(host='redis')
    redis_pubsub = redis_client.pubsub()
    redis_pubsub.subscribe(f'{camera}_video_stream_{resolution}')

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
            if message['channel'].decode() == f'{camera}_video_stream_{resolution}':
                yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + message['data'] + b'\r\n'

    redis_pubsub.unsubscribe()
    redis_client.close()
    shm.close()

    sleep(1)
    if camera == next(iter(rtsp_urls)):
        shm.unlink()
