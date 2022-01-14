#!/usr/local/bin/python
# server.py

import os
from auth import auth
from flask import Flask, render_template
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
    return render_template('cameras.html', title='Guardian'), 200


if __name__ == '__main__':
    app.run('0.0.0.0', 80, debug=False)
