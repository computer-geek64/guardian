# auth.py

import os
import json
import hashlib
from flask import session, request, redirect, url_for
from functools import wraps


authentication_credentials = json.loads(os.environ['AUTHENTICATION_CREDENTIALS'])


def auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'username' not in session or 'password' not in session:
            #return 'HTTP 403', 403
            return redirect(url_for('get_login', redirect=request.path))
        if authenticate(session.get('username'), session.get('password')):
            return func(*args, **kwargs)
        return 'HTTP 401', 401
    return wrapper


def authenticate(username, password):
    password_hash = hashlib.sha512(password.encode()).hexdigest()
    return username in authentication_credentials and password_hash == authentication_credentials[username]
