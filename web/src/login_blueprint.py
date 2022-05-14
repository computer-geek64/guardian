# login_blueprint.py

import os
from auth import authenticate
from flask import Blueprint, request, session, redirect, render_template


login_blueprint = Blueprint('login_blueprint', __name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))


@login_blueprint.route('/login', methods=['GET'])
def get_login():
    if 'login_attempts' in session and session.get('login_attempts') > 2:
        return 'HTTP 403', 403
    if authenticate(session.get('username'), session.get('password')):
        # root_url = request.headers.get('X-Forwarded-Proto') + '://' + request.headers.get('X-Forwarded-Host') if 'X-Forwarded-Host' in request.headers and 'X-Forwarded-Proto' in request.headers else ''
        # return redirect(root_url + request.args.get('redirect', default='/stream/')), 302
        return redirect(request.args.get('redirect', '/stream/'))
    return render_template('login.html'), 200


@login_blueprint.route('/login', methods=['POST'])
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
        return 'HTTP 401', 401
    session['username'] = username
    session['password'] = password
    session.pop('login_attempts')

    # root_url = request.headers.get('X-Forwarded-Proto') + '://' + request.headers.get('X-Forwarded-Host') if 'X-Forwarded-Host' in request.headers and 'X-Forwarded-Proto' in request.headers else ''
    # return redirect(root_url + request.args.get('redirect', default='/stream/')), 302
    return redirect(request.args.get('redirect', '/stream/'))


@login_blueprint.route('/logout', methods=['GET'])
def get_logout():
    session.clear()
    return redirect('/login'), 302
