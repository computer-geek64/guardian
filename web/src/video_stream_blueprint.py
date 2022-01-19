# video_stream_blueprint.py

import os
import cv2
import json
from auth import auth
from flask import Blueprint, Response, stream_with_context


video_stream_blueprint = Blueprint('video_stream_blueprint', __name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))

rtsp_urls = json.loads(os.environ['RTSP_URLS'])


@video_stream_blueprint.route('/stream/<string:camera>/<string:resolution>.jpg', methods=['GET'])
@auth
def get_camera_stream_jpeg(camera, resolution):
    stream = cv2.VideoCapture(rtsp_urls[camera])
    return Response(stream_with_context(generate_frames(stream, resolution.lower())), mimetype='multipart/x-mixed-replace; boundary=frame'), 200


def generate_frames(stream, resolution):
    try:
        while True:
            success, frame = stream.read()
            if success:
                if resolution == 'sd':
                    if frame.shape[0] > 640:
                        if frame.shape[0] / 4 == frame.shape[1] / 3:
                            frame.resize(frame, (640, 480))
                        else:
                            frame.resize(frame, (640, 360))
                elif sum(n.isdecimal() for n in resolution.split('x', 1)) == 2:  # Valid resolution string (e.g., 1366x768)
                    frame = cv2.resize(frame, tuple(map(int, resolution.split('x', 1))))
                elif resolution == 'hd':
                    if frame.shape[0] / 4 == frame.shape[1] / 3:
                        frame.resize(frame, (1280, 960))
                    else:
                        frame.resize(frame, (1280, 720))
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
            else:
                break
    finally:
        stream.release()
        print('Done')
