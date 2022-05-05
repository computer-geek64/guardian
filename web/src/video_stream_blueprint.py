# video_stream_blueprint.py

import os
import cv2
import json
from time import sleep
from datetime import datetime
from multiprocessing import shared_memory
from flask import Blueprint, Response, stream_with_context, session


video_stream_blueprint = Blueprint('video_stream_blueprint', __name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))

rtsp_urls = json.loads(os.environ['RTSP_URLS'])


class RTSPVideoStream(object):
    def __init__(self, camera):
        self.camera = camera
        self.stream = cv2.VideoCapture(rtsp_urls[camera])

    def __del__(self):
        self.stream.release()


@video_stream_blueprint.route('/stream/<string:camera>/<string:resolution>.jpg', methods=['GET'])
def get_camera_stream_jpeg(camera, resolution):
    if 'stream_id' not in session:
        return 'HTTP 400', 400

    stream = cv2.VideoCapture(rtsp_urls[camera])
    return Response(stream_with_context(generate_frames(camera, stream, resolution.lower())), mimetype='multipart/x-mixed-replace; boundary=frame'), 200


def generate_frames(camera, stream, resolution):
    last_heartbeat_timestamp = datetime.now().timestamp()
    shm = shared_memory.SharedMemory(name='guardian_stream_' + session.get('stream_id'))
    last_heartbeat_value = shm.buf[0]
    i = 0
    while True:
        current_timestamp = datetime.now().timestamp()
        if shm.buf[0] != last_heartbeat_value:
            last_heartbeat_value = shm.buf[0]
            last_heartbeat_timestamp = current_timestamp
        elif current_timestamp - last_heartbeat_timestamp >= 7:
            break

        if i < 5:
            i += 1
            stream.grab()
            continue
        i = 0

        success, frame = stream.read()
        if success:
            if resolution == 'sd':
                if frame.shape[1] / 4 == frame.shape[0] / 3:
                    frame = cv2.resize(frame, (640, 480))
                else:
                    frame = cv2.resize(frame, (640, 360))
            elif sum(n.isdecimal() for n in resolution.split('x', 1)) == 2:  # Valid resolution string (e.g., 1366x768)
                frame = cv2.resize(frame, tuple(map(int, resolution.split('x', 1))))
            elif resolution == 'hd':
                if frame.shape[1] / 4 == frame.shape[0] / 3:
                    frame = cv2.resize(frame, (1280, 960))
                else:
                    frame = cv2.resize(frame, (1280, 720))
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
        # else:
        #     break

    stream.release()
    shm.close()

    sleep(1)
    if camera == next(iter(rtsp_urls)):
        shm.unlink()
