#!/usr/local/bin/python
# server.py

import os
import cv2
from auth import auth
from flask import Flask, render_template, Response, stream_with_context
from subprocess import Popen, PIPE, DEVNULL


app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = Popen(['uuidgen', '-r'], stdout=PIPE, stderr=DEVNULL).communicate()[0].decode().strip()


# Home
@app.route('/', methods=['GET'])
def get_home():
    return 'Welcome to Guardian!', 200


# Stream
@app.route('/stream', methods=['GET'])
def get_image():
    camera = cv2.VideoCapture('rtsp://{username}:{password}@192.168.0.103:8000/live/ch0'.format(username=os.environ['MOTION_USERNAME'], password=os.environ['MOTION_PASSWORD']))
    return Response(stream_with_context(generate_frames(camera)), mimetype='multipart/x-mixed-replace; boundary=frame')


def generate_frames(camera):
    try:
        while True:
            success, frame = camera.read()
            if success:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield f'--frame\r\nContent-Type: image/jpeg\r\n\r\n{frame}\r\n'.encode()
            else:
                break
    finally:
        camera.release()


if __name__ == '__main__':
    app.run('0.0.0.0', 80, debug=False)
