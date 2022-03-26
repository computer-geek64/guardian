# auth.py

import os
import json
import hashlib


authentication_credentials = json.loads(os.environ['AUTHENTICATION_CREDENTIALS'])


def authenticate(username, password):
    if username is None or password is None:
        return False

    password_hash = hashlib.sha512(password.encode()).hexdigest()
    return username in authentication_credentials and password_hash == authentication_credentials[username]
