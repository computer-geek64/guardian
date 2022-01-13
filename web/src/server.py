#!/usr/local/bin/python
# server.py

import requests
from auth import auth
from flask import Flask, request, Response
from subprocess import Popen, PIPE, DEVNULL


app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = Popen(['uuidgen', '-r'], stdout=PIPE, stderr=DEVNULL).communicate()[0].decode().strip()


# Home
@app.route('/', methods=['GET'])
def get_home():
    return 'Welcome to Guardian!', 200


@app.route('/1', methods=['GET'])
def get_stream():
    return _proxy()


def _proxy(*args, **kwargs):
    resp = requests.request(
        method=request.method,
        url=request.url.replace(request.host_url, 'web'),
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False)

    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]

    response = Response(resp.content, resp.status_code, headers)
    return response


if __name__ == '__main__':
    app.run('0.0.0.0', 80, debug=False)
