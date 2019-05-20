from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import SingletonThreadPool

from config import TEST_DB_CONNECTION_STRING, DB_CONNECTION_STRING


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
