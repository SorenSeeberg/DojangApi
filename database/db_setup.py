#!/usr/bin/python3
# -*- coding: utf-8 -*-

from database.db import EngineSingleton
from database.db import SessionSingleton
from database import schemas
from query import access_token
from query import belt
from query import category
from query import info
from query import user

if __name__ == '__main__':
    engine = EngineSingleton().get_engine()
    session: 'Session' = SessionSingleton().get_session()

    """ Creating tables """
    schemas.setup(engine)

    """ Populating tables """
    [s.setup(session) for s in [user, belt, category, info]]
    session.commit()

    access_token.create(SessionSingleton().get_session(), user_id=1)
