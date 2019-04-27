#!/usr/bin/python3
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from config import DB_CONNECTION_STRING, TEST_DB_CONNECTION_STRING
from sqlalchemy.orm import sessionmaker
import json


class EngineSingleton:

    engine: create_engine = None

    def __init__(self):
        if not EngineSingleton.engine:
            EngineSingleton.engine = create_engine(DB_CONNECTION_STRING, echo=False)

    def get_engine(self) -> 'Engine':
        return EngineSingleton.engine


class SessionSingleton:

    session: sessionmaker = None

    def __init__(self):
        if not SessionSingleton.session:
            SessionSingleton.session = sessionmaker(bind=EngineSingleton().get_engine())

    def get_session(self) -> 'Session':
        return SessionSingleton.session()


class TestEngineSingleton:

    engine: create_engine = None

    def __init__(self):
        if not TestEngineSingleton.engine:
            TestEngineSingleton.engine = create_engine(TEST_DB_CONNECTION_STRING, echo=False)

    def get_engine(self) -> 'Engine':
        return TestEngineSingleton.engine


class TestSessionSingleton:

    session: sessionmaker = None

    def __init__(self):
        if not TestSessionSingleton.session:
            TestSessionSingleton.session = sessionmaker(bind=TestEngineSingleton().get_engine())

    def get_session(self) -> 'Session':
        return TestSessionSingleton.session()


def to_json(data) -> str:
    return json.dumps(data, indent=2)
