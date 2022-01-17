# login_blueprint.py

import os
from auth import authenticate
from flask import Blueprint, request, session, redirect, render_template


login_blueprint = Blueprint('login_blueprint', __name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))


@login_blueprint.route('/login/', methods=['GET'])
def get_login():
    if 'login_attempts' in session and session.get('login_attempts') > 2:
        return 'HTTP 403', 403
    if 'username' in session and 'password' in session and authenticate(session.get('username'), session.get('password')):
        return redirect('/stream/'), 302
    return render_template('login.html'), 200


@login_blueprint.route('/login/', methods=['POST'])
def post_login():
    if 'login_attempts' in session:
        if session.get('login_attempts') > 2:
            return 'HTTP 403', 403
        session['login_attempts'] += 1
    else:
        session['login_attempts'] = 1

    username = request.form.get('username')
    password = request.form.get('password')
    if not authenticate(username, password):
        if session.get('login_attempts') > 2:
            return 'HTTP 403', 403
        return 'HTTP 401', 401
    session['username'] = username
    session['password'] = password
    session.pop('login_attempts')
    return redirect('/stream/'), 302


@login_blueprint.route('/logout/', methods=['GET'])
def get_logout():
    session.clear()
    return redirect('/'), 302
