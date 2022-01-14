# stream_blueprint.py

import os
import cv2
from flask import Blueprint, Response, stream_with_context, render_template


stream_blueprint = Blueprint('stream_blueprint', __name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))

rtsp_urls = {'backyard': 'rtsp://{username}:{password}@192.168.0.103:8080/live/ch0'}


@stream_blueprint.route('/stream/<string:camera>.jpg', methods=['GET'])
def get_camera_stream_jpeg(camera):
    stream = cv2.VideoCapture(rtsp_urls[camera].format(username=os.environ['MOTION_USERNAME'], password=os.environ['MOTION_PASSWORD']))
    return Response(stream_with_context(generate_frames(stream)), mimetype='multipart/x-mixed-replace; boundary=frame'), 200


@stream_blueprint.route('/stream/<string:camera>/', methods=['GET'])
def get_camera_stream(camera):
    return render_template('camera.html', title=camera.capitalize(), camera=camera), 200


def generate_frames(stream):
    try:
        while True:
            success, frame = stream.read()
            if success:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
            else:
                break
    finally:
        stream.release()
