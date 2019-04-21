import os


def db_connection_string():
    return f'sqlite:///{os.path.realpath(os.path.dirname(__file__))}\quiz.db'


DB_CONNECTION_STRING = db_connection_string()
UUID_LENGTH = 36
PWD_HASH_LENGTH = 64
TEXT_LENGTH = 256
EMAIL_LENGTH = 50
TITLE_LENGTH = 32


LABEL_LENGTH = 32


