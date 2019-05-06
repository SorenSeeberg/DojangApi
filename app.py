#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
from flask import Flask, redirect, url_for, request, make_response
from response_codes import ResponseKeys
from models import quiz, user
from database import db

app = Flask(__name__)


# auth decorator example
# https://github.com/ianunruh/flask-api-skeleton/blob/master/backend/routes/__init__.py


def get_access_token() -> str:
    return request.headers.environ.get('HTTP_AUTHORIZATION', 'no access token')


def to_json(data) -> str:
    return json.dumps(data, indent=4)


@app.route('/')
def index():
    return 'Dojang API'


# USER

@app.route('/user', methods=['POST'])
def create_user():
    print('USER')
    session = db.SessionSingleton().get_session()
    data = json.loads(request.data, encoding='utf-8')
    print(data)

    return_data = user.create_user(session, data)
    return make_response(to_json(return_data), return_data.get(ResponseKeys.status, 400))


@app.route('/user', methods=['GET'])
def get_user():
    session = db.SessionSingleton().get_session()
    access_token: str = get_access_token()
    print(access_token)

    return_data = user.get_user(session, access_token)
    return make_response(to_json(return_data), return_data.get(ResponseKeys.status, 400))


# @app.route('/user', methods=['GET'])
# def get_paginated_users():
#     return "Get Paginated Users"


@app.route('/user', methods=['PUT'])
def update_user():
    return "Update User"


@app.route('/user/<path:user_id>', methods=['DELETE'])
def delete_user(user_id):
    return "Delete User " + user_id


@app.route('/user/results/<path:user_id>', methods=['GET'])
def get_results(user_id):
    return "Get Results " + user_id


@app.route('/user/sign-in', methods=['POST'])
def sign_in():
    return "Sign In"


@app.route('/user/sign-out', methods=['GET'])
def sign_out():
    return "Sign Out"


@app.route('/user/change-password')
def change_password():
    return "Change password"


# QUIZ

@app.route('/quiz', methods=['POST'])
def create_quiz():
    session = db.SessionSingleton().get_session()
    access_token: str = get_access_token()
    data = json.loads(request.data, encoding='utf-8')

    return to_json(quiz.new_quiz(
        session,
        access_token,
        data
    ))


@app.route('/quiz/<path:quiz_token>', methods=['GET'])
def get_quiz(quiz_token: str):
    session = db.SessionSingleton().get_session()
    access_token: str = get_access_token()
    return to_json(quiz.get_quiz(session, access_token, quiz_token))


@app.route('/quiz/question/<path:quiz_token>', methods=['GET'])
def get_question(quiz_token: str):
    session = db.SessionSingleton().get_session()
    access_token: str = get_access_token()
    return to_json(quiz.get_current_question(session, access_token, quiz_token))


@app.route('/quiz/question/<path:quiz_token>', methods=['PUT'])
def answer_question(quiz_token: str):
    session = db.SessionSingleton().get_session()
    access_token: str = get_access_token()
    data = json.loads(request.data, encoding='utf-8')
    return to_json(quiz.answer_question(session, access_token, quiz_token, data))


if __name__ == '__main__':
    app.run()