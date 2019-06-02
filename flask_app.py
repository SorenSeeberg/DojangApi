#!/usr/bin/python3
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.pool import SingletonThreadPool
from config import DB_CONNECTION_STRING, TEST_DB_CONNECTION_STRING
from sqlalchemy.orm import sessionmaker
import os
import json
from typing import Dict
from flask import Flask, request, make_response, render_template, send_from_directory
import response_codes
from authorization import is_authorized
from query import access_token
from response_codes import ResponseKeys
from models import quiz, users, curriculum

app = Flask(__name__)


def validate_db_string() -> str:
    sqlite_root = 'sqlite:///'

    if DB_CONNECTION_STRING.startswith(sqlite_root):
        is_file = os.path.isfile(DB_CONNECTION_STRING[len(sqlite_root):])
    else:
        is_file = None
    return f'{DB_CONNECTION_STRING} ({is_file})'


def get_engine(test=False):
    if test:
        return create_engine(TEST_DB_CONNECTION_STRING, echo=False, poolclass=SingletonThreadPool)
    else:
        return create_engine(DB_CONNECTION_STRING, echo=False, poolclass=SingletonThreadPool)


def get_session(test=False):
    if test:
        engine = create_engine(TEST_DB_CONNECTION_STRING, echo=False, poolclass=SingletonThreadPool)
    else:
        engine = create_engine(DB_CONNECTION_STRING, echo=False, poolclass=SingletonThreadPool)

    session_class = sessionmaker(bind=engine)

    return session_class()


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

@app.route('/pensum', methods=['GET'])
@app.route('/quiz', methods=['GET'])
@app.route('/quiz-category', methods=['GET'])
@app.route('/quiz-configuration', methods=['GET'])
@app.route('/forside', methods=['GET'])
@app.route('/log-ind', methods=['GET'])
@app.route('/opret-bruger', methods=['GET'])
@app.route('/min-bruger', methods=['GET'])
@app.route('/glemt-password', methods=['GET'])
@app.route('/nyt-password', methods=['GET'])
@app.route('/', methods=['GET'])
def index():
    return render_template("index.html", connection_string=validate_db_string())


# USERS

@app.route('/users', methods=['POST'])
def create_user():
    session = get_session()
    form = dict(request.form)
    data = {"email": form.get("email")[0], "password": form.get("password")[0]}
    return_data: Dict = users.create(session, data)
    return make_response(_to_json(return_data), return_data.get(ResponseKeys.status, 500))


@app.route('/users/activate/<path:activation_token>', methods=['GET'])
def activate_user(activation_token):
    session = get_session()
    return_data: Dict = users.activate(session, activation_token)
    if return_data.get('status', 500) == 204:
        return render_template('user-enabled.html')
    else:
        return _unauthorized_response()


@app.route('/users/restore', methods=['PUT'])
def restore_user():
    session = get_session()
    form = dict(request.form)
    print('restore_user')
    print(form.get("email")[0])
    return_data: Dict = users.restore(session, form.get("email")[0])
    if return_data.get('status', 500) == 204:
        return make_response(_to_json(return_data), return_data.get(ResponseKeys.status, 500))
    else:
        return _unauthorized_response()


@app.route('/users', methods=['GET'])
def get_users():
    session = get_session()
    access_token_string: str = _get_access_token()

    # Authorization
    if not is_authorized(session, access_token_string, role='user'):
        return _unauthorized_response()

    user_id: int = access_token.get_user_id_by_token(session, access_token_string)
    return_data: Dict = users.get(session, user_id)
    return make_response(_to_json(return_data), return_data.get(ResponseKeys.status, 500))


@app.route('/users/current-user', methods=['GET'])
def get_current_user():
    session = get_session()
    access_token_string: str = _get_access_token()

    # Authorization
    if not is_authorized(session, access_token_string, role='user'):
        return _unauthorized_response()

    user_id: int = access_token.get_user_id_by_token(session, access_token_string)
    return_data: Dict = users.get_current(session, user_id)
    return make_response(_to_json(return_data), return_data.get(ResponseKeys.status, 500))


@app.route('/users/email-exist', methods=['POST'])
def email_exists():
    session = get_session()
    data = json.loads(request.data, encoding='utf-8')
    return_data: Dict = users.email_exists(session, data)
    return make_response(_to_json(return_data), return_data.get(ResponseKeys.status, 500))


@app.route('/users/paginated-users', methods=['GET'])
def get_paginated_users():
    raise NotImplementedError


@app.route('/users', methods=['PUT'])
def update_user():
    raise NotImplementedError


@app.route('/users/sign-in', methods=['POST'])
def sign_in():
    session = get_session()
    form = dict(request.form)
    data = {"email": form.get("email")[0], "password": form.get("password")[0]}
    return_data: Dict = users.sign_in(session, data)
    return make_response(_to_json(return_data), return_data.get(ResponseKeys.status, 500))


@app.route('/users/sign-out', methods=['GET'])
def sign_out():
    session = get_session()
    access_token_string: str = _get_access_token()

    # Authorization
    if not is_authorized(session, access_token_string, role='user'):
        return _unauthorized_response()

    return_data: Dict = users.sign_out(session, access_token_string)
    return make_response(_to_json(return_data), return_data.get(ResponseKeys.status, 500))


@app.route('/users/change-password')
def change_password():
    raise NotImplementedError


# QUIZ

@app.route('/quiz', methods=['POST'])
def create_quiz():
    session = get_session()
    access_token_string: str = _get_access_token()

    # Authorization
    if not is_authorized(session, access_token_string, role='user'):
        return _unauthorized_response()

    user_id: int = access_token.get_user_id_by_token(session, access_token_string)
    data = json.loads(request.data, encoding='utf-8')
    return_data: Dict = quiz.create(session, user_id, data)
    return make_response(_to_json(return_data), return_data.get(ResponseKeys.status, 500))


@app.route('/quiz/configuration', methods=['GET'])
def get_quiz_configuration():
    session = get_session()
    access_token_string: str = _get_access_token()

    # Authorization
    if not is_authorized(session, access_token_string, role='user'):
        return _unauthorized_response()

    return_data: Dict = quiz.get_configuration(session)
    return make_response(_to_json(return_data), return_data.get(ResponseKeys.status, 500))


@app.route('/quiz/<path:quiz_token>', methods=['GET'])
def get_quiz(quiz_token: str):
    session = get_session()
    access_token_string: str = _get_access_token()

    # Authorization
    if not is_authorized(session, access_token_string, role='user'):
        return _unauthorized_response()

    return_data: Dict = quiz.get(session, quiz_token)
    return make_response(_to_json(return_data), return_data.get(ResponseKeys.status, 500))


@app.route('/quiz/result/<path:quiz_token>', methods=['GET'])
def get_quiz_result(quiz_token):
    session = get_session()
    access_token_string: str = _get_access_token()

    # Authorization
    if not is_authorized(session, access_token_string, role='user'):
        return _unauthorized_response()

    return_data: Dict = quiz.get_result(session, quiz_token)
    return make_response(_to_json(return_data), return_data.get(ResponseKeys.status, 500))


@app.route('/quiz/question/<path:quiz_token>', methods=['PUT'])
def answer_question(quiz_token: str):
    session = get_session()
    access_token_string: str = _get_access_token()

    # Authorization
    if not is_authorized(session, access_token_string, role='user'):
        return _unauthorized_response()

    data = json.loads(request.data, encoding='utf-8')
    return_data: Dict = quiz.answer(session, quiz_token, data)
    return make_response(_to_json(return_data), return_data.get(ResponseKeys.status, 500))


# CURRICULUM
@app.route('/curriculum', methods=['GET'])
def get_curriculum():
    data = {
        'categoryId': int(request.args.get('categoryId', -1)),
        'levelMin': int(request.args.get('levelMin', -1)),
        'levelMax': int(request.args.get('levelMax', -1))
    }

    session = get_session()
    access_token_string: str = _get_access_token()

    # Authorization
    if not is_authorized(session, access_token_string, role='user'):
        return _unauthorized_response()

    return_data: Dict = curriculum.get(session, data)
    return make_response(_to_json(return_data), return_data.get(ResponseKeys.status, 500))


if __name__ == '__main__':
    app.run()
