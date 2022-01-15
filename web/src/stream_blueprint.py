# stream_blueprint.py

import os
import cv2
from subprocess import Popen, PIPE, DEVNULL
from flask import Blueprint, Response, stream_with_context, render_template


stream_blueprint = Blueprint('stream_blueprint', __name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))

rtsp_urls = {'backyard': 'rtsp://{username}:{password}@192.168.0.103:8080/live/ch0'}


@stream_blueprint.route('/stream/<string:camera>/', methods=['GET'])
def get_camera_stream(camera):
    return render_template('camera.html', title=camera.capitalize(), camera=camera), 200


@stream_blueprint.route('/stream/<string:camera>/<string:resolution>.jpg', methods=['GET'])
def get_camera_stream_jpeg(camera, resolution):
    stream = cv2.VideoCapture(rtsp_urls[camera].format(username=os.environ['MOTION_USERNAME'], password=os.environ['MOTION_PASSWORD']))
    return Response(stream_with_context(generate_frames(stream, resolution.lower())), mimetype='multipart/x-mixed-replace; boundary=frame'), 200


@stream_blueprint.route('/stream/<string:camera>/audio.mp3', methods=['GET'])
def get_camera_stream_audio(camera):
    ffmpeg_process = Popen(['ffmpeg', '-rtsp_transport', 'tcp', '-i', rtsp_urls[camera], '-map', 'a', '-f', 'wav' '-'], stdout=PIPE, stderr=DEVNULL)
    return Response(stream_with_context(generate_wav(ffmpeg_process)), mimetype='audio/x-wav')


def generate_wav(ffmpeg_process):
    def generate():
        try:
            data = ffmpeg_process.stdout.read(1024)
            while True:
                yield data
                data = ffmpeg_process.stdout.read(1024).read(1024)
        finally:
            ffmpeg_process.terminate()
            print('Terminated')
    return Response(generate(), mimetype="audio/x-wav")


def generate_frames(stream, resolution):
    try:
        while True:
            success, frame = stream.read()
            if success:
                if resolution == 'sd':
                    frame = cv2.resize(frame, (480, 270))
                elif sum(n.isdecimal() for n in resolution.split('x', 1)) == 2:  # Valid resolution string (e.g., 1920x1080)
                    frame = cv2.resize(frame, tuple(resolution.split('x', 1)))
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
            else:
                break
    finally:
        stream.release()
        print('Done')
