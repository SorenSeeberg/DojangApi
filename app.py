#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
from flask import Flask, redirect, url_for, request
from models import quiz
from database import db

app = Flask(__name__)

# auth decorator example
# https://github.com/ianunruh/flask-api-skeleton/blob/master/backend/routes/__init__.py


def to_json(data) -> str:
    return json.dumps(data, indent=4)


@app.route('/')
def hello_world():
    return 'Hello World!'


# USER

@app.route('/user', methods=['POST'])
def create_user():
    return "Create User"


@app.route('/user', methods=['PUT'])
def update_user():
    return "Update User"


@app.route('/user/<path:user_id>', methods=['GET'])
def get_user(user_id):
    return "Get User " + user_id


@app.route('/user', methods=['GET'])
def get_paginated_users():
    return "Get Paginated Users"


@app.route('/user/<path:user_id>', methods=['DELETE'])
def delete_user(user_id):
    return "Delete User " + user_id


@app.route('/user/results/<path:user_id>', methods=['GET'])
def get_results(user_id):
    return "Get Results " + user_id


@app.route('/user/sign-in')
def sign_in():
    return "Sign In"


@app.route('/user/sign-out')
def sign_out():
    return "Sign Out"


@app.route('/user/change-password')
def change_password():
    return "Change password"


# QUIZ

@app.route('/quiz', methods=['POST'])
def create_quiz():
    return 'Create Quiz'


@app.route('/quiz', methods=['DELETE'])
def delete_quiz():
    return 'Delete Quiz'


@app.route('/quiz/<path:quiz_token>', methods=['GET'])
def get_quiz(quiz_token: str):
    session = db.SessionSingleton().get_session()
    return to_json(quiz.get_quiz(session, 'b2b88120-fb66-4640-ac97-fe315cd250fd', quiz_token))


@app.route('/quiz/question/<path:quiz_token>', methods=['GET'])
def get_question(quiz_token: str):
    session = db.SessionSingleton().get_session()
    r = request.headers.get()
    return to_json(quiz.get_current_question(session, 'b2b88120-fb66-4640-ac97-fe315cd250fd', quiz_token))


if __name__ == '__main__':
    app.run()

# a36ed453-02d3-4190-9de9-520ff1955a82