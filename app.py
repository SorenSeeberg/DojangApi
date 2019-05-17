#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import json
from typing import Dict
from flask import Flask, redirect, url_for, request, make_response, render_template, send_from_directory

import response_codes
from authorization import is_authorized
from query import access_token
from response_codes import ResponseKeys
from models import quiz, users, curriculum
from database import db

app = Flask(__name__)


def _get_access_token() -> str:
    return request.headers.environ.get('HTTP_AUTHORIZATION', 'no access token')


def _to_json(data) -> str:
    return json.dumps(data, indent=4)


def _unauthorized_response():
    return make_response(_to_json({ResponseKeys.status: response_codes.ResponseCodes.unauthorized_401}),
                         response_codes.ResponseCodes.unauthorized_401)


# FAVICON

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


# SPA ROUTES

@app.route('/quiz')
@app.route('/welcome')
@app.route('/sign-in')
@app.route('/create-user')
@app.route('/')
def index():
    return render_template("index.html")


# USERS

@app.route('/users', methods=['POST'])
def create_user():
    session = db.SessionSingleton().get_session()
    form = dict(request.form)
    data = {"email": form.get("email")[0], "password": form.get("password")[0]}
    return_data: Dict = users.create(session, data)
    return make_response(_to_json(return_data), return_data.get(ResponseKeys.status, 500))


@app.route('/users/activate/<path:activation_token>', methods=['GET'])
def activate_user(activation_token):
    session = db.SessionSingleton().get_session()
    return_data: Dict = users.activate(session, activation_token)
    print(return_data)
    if return_data.get('status', 500) == 204:
        return render_template('user-enabled.html')
    else:
        return _unauthorized_response()


@app.route('/users/current-user', methods=['GET'])
def get_user():
    session = db.SessionSingleton().get_session()
    access_token_string: str = _get_access_token()

    # Authorization
    if not is_authorized(session, access_token_string, role='user'):
        return _unauthorized_response()

    user_id: int = access_token.get_user_id_by_token(session, access_token_string)
    return_data: Dict = users.get(session, user_id)
    return make_response(_to_json(return_data), return_data.get(ResponseKeys.status, 500))


@app.route('/users/email-exist', methods=['POST'])
def email_exists():
    session = db.SessionSingleton().get_session()
    data = json.loads(request.data, encoding='utf-8')
    return_data: Dict = users.email_exists(session, data)
    return make_response(_to_json(return_data), return_data.get(ResponseKeys.status, 500))


@app.route('/users/paginated-users', methods=['GET'])
def get_paginated_users():
    raise NotImplementedError


@app.route('/users', methods=['PUT'])
def update_user():
    raise NotImplementedError


@app.route('/user/results/<path:user_id>', methods=['GET'])
def get_results(user_id):
    return "Get Results " + user_id


@app.route('/users/sign-in', methods=['POST'])
def sign_in():
    session = db.SessionSingleton().get_session()
    form = dict(request.form)
    data = {"email": form.get("email")[0], "password": form.get("password")[0]}
    return_data: Dict = users.sign_in(session, data)
    return make_response(_to_json(return_data), return_data.get(ResponseKeys.status, 500))


@app.route('/users/sign-out', methods=['GET'])
def sign_out():
    session = db.SessionSingleton().get_session()
    access_token_string: str = _get_access_token()

    # Authorization
    if not is_authorized(session, access_token_string, role='user'):
        return _unauthorized_response()

    return_data: Dict = users.sign_out(session, access_token_string)
    return make_response(_to_json(return_data), return_data.get(ResponseKeys.status, 500))


@app.route('/users/change-password')
def change_password():
    return "Change password"


# QUIZ

@app.route('/quiz', methods=['POST'])
def create_quiz():
    session = db.SessionSingleton().get_session()
    access_token_string: str = _get_access_token()

    # Authorization
    if not is_authorized(session, access_token_string, role='user'):
        return _unauthorized_response()

    user_id: int = access_token.get_user_id_by_token(session, access_token_string)
    data = json.loads(request.data, encoding='utf-8')
    return_data: Dict = quiz.create(session, user_id, data)
    return make_response(_to_json(return_data), return_data.get(ResponseKeys.status, 500))


@app.route('/quiz/<path:quiz_token>', methods=['GET'])
def get_quiz(quiz_token: str):
    session = db.SessionSingleton().get_session()
    access_token_string: str = _get_access_token()

    # Authorization
    if not is_authorized(session, access_token_string, role='user'):
        return _unauthorized_response()

    return_data: Dict = quiz.get(session, quiz_token)
    return make_response(_to_json(return_data), return_data.get(ResponseKeys.status, 500))


@app.route('/quiz/question/<path:quiz_token>', methods=['GET'])
def get_question(quiz_token: str):
    session = db.SessionSingleton().get_session()
    access_token_string: str = _get_access_token()

    # Authorization
    if not is_authorized(session, access_token_string, role='user'):
        return _unauthorized_response()

    return_data: Dict = quiz.get_current_question(session, quiz_token)
    return make_response(_to_json(return_data), return_data.get(ResponseKeys.status, 500))


@app.route('/quiz/question/<path:quiz_token>', methods=['PUT'])
def answer_question(quiz_token: str):
    session = db.SessionSingleton().get_session()
    access_token_string: str = _get_access_token()

    # Authorization
    if not is_authorized(session, access_token_string, role='user'):
        return _unauthorized_response()

    data = json.loads(request.data, encoding='utf-8')
    return_data: Dict = quiz.answer(session, quiz_token, data)
    return make_response(_to_json(return_data), return_data.get(ResponseKeys.status, 500))


if __name__ == '__main__':
    app.run()
