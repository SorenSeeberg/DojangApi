#!/usr/bin/python3
# -*- coding: utf-8 -*-

from database import schemas
from query import access_token
from query import level
from query import category
from query import curriculum
from query import user
from app import get_session, get_engine

if __name__ == '__main__':
    session: 'Session' = get_session()
    engine = get_engine()

    """ Creating tables """
    schemas.setup(engine)

    """ Populating tables """
    [s.setup(session) for s in [user, level, category, curriculum]]
    session.commit()

    access_token.create(session, user_id=1)
