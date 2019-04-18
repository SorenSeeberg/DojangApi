from sqlalchemy import create_engine
from config import DB_CONNECTION_STRING
from sqlalchemy.orm import sessionmaker


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

