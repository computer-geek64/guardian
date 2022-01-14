#!/usr/local/bin/python
# server.py

import os
import cv2
from auth import auth
from flask import Flask, render_template, Response
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
def get_stream():
    return render_template('cameras.html', title='Guardian', motion_username=os.environ['MOTION_USERNAME'], motion_password=os.environ['MOTION_PASSWORD']), 200


@app.route('/image', methods=['GET'])
def get_image():
    camera = cv2.VideoCapture('rtsp://{username}:{password}@192.168.0.108:554/live/ch0'.format(username=os.environ['MOTION_USERNAME'], password=os.environ['MOTION_PASSWORD']))

    def gen_frames():  # generate frame by frame from camera
        while True:
            # Capture frame-by-frame
            success, frame = camera.read()  # read the camera frame
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == '__main__':
    app.run('0.0.0.0', 80, debug=False)
