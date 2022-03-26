#!/usr/local/bin/python -B
# auth_server.py

import os
from auth import authenticate
from flask import Flask, session
from login_blueprint import login_blueprint


app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))
app.register_blueprint(login_blueprint)

app.config['SESSION_TYPE'] = 'filesystem'

app.secret_key = os.environ['FLASK_SECRET_KEY']


@app.route('/auth', methods=['GET'])
def get_auth():
    if session.get('login_attempts', default=0) > 2:
        return 'HTTP 403', 403
    if authenticate(session.get('username'), session.get('password')):
        return 'HTTP 200', 200
    return 'HTTP 401', 401


if __name__ == '__main__':
    app.run('0.0.0.0', 80, debug=False)
