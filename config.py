#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os

DEV = True


def db_connection_string(db_name: str):
    if DEV:
        return f'sqlite:///{os.path.dirname(os.path.realpath(__file__))}\\{db_name}'
    else:
        return f'sqlite:////{os.path.join("home", "sorenseeberg", "dojang", db_name)}'


DB_CONNECTION_STRING = db_connection_string('quiz.db')
TEST_DB_CONNECTION_STRING = db_connection_string('test.db')
UUID_LENGTH = 36
PWD_HASH_LENGTH = 64
TEXT_LENGTH = 256
EMAIL_LENGTH = 50
TITLE_LENGTH = 32
LABEL_LENGTH = 32

MAIL_SENDER = 'soren.seeberg@gmail.com'
MAIL_KEY = 'yyismfzcsgtolcgi'

if DEV:
    SITE_URL = 'http://127.0.0.1:5000'
else:
    SITE_URL = 'http://sorenseeberg.pythonanywhere.com'
