#!/usr/local/bin/python -B
# server.py

import os
from flask import Flask
from camera_blueprint import camera_blueprint
from video_stream_blueprint import video_stream_blueprint
from audio_stream_blueprint import audio_stream_blueprint


app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))
app.register_blueprint(camera_blueprint)
app.register_blueprint(video_stream_blueprint)
app.register_blueprint(audio_stream_blueprint)

app.config['SESSION_TYPE'] = 'filesystem'

app.secret_key = os.environ['FLASK_SECRET_KEY']


# Home
@app.route('/', methods=['GET'])
def get_home():
    return 'Welcome to Guardian!', 200


if __name__ == '__main__':
    app.run('0.0.0.0', 80, debug=False)
