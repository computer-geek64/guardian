# auth.py

import os
import hashlib
from flask import session
from functools import wraps


def auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'username' not in session or 'password' not in session:
            return 'HTTP 403', 403
        if authenticate(session.get('username'), session.get('password')):
            return func(*args, **kwargs)
        return 'HTTP 401', 401
    return wrapper


def authenticate(username, password):
    password_hash = hashlib.sha512(password.encode()).hexdigest()
    return username == os.environ['USERNAME'] and password_hash == os.environ['PASSWORD_HASH']