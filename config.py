#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os


def db_connection_string(db_name:str):
    return f'sqlite:///{os.path.realpath(os.path.dirname(__file__))}\\{db_name}'


DB_CONNECTION_STRING = db_connection_string('quiz.db')
TEST_DB_CONNECTION_STRING = db_connection_string('test.db')
UUID_LENGTH = 36
PWD_HASH_LENGTH = 64
TEXT_LENGTH = 256
EMAIL_LENGTH = 50
TITLE_LENGTH = 32


LABEL_LENGTH = 32


