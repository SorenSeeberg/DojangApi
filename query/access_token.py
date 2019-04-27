#!/usr/bin/python3
# -*- coding: utf-8 -*-

from uuid import uuid4
from database.tables import AccessToken
from database.db import SessionSingleton
from sqlalchemy.orm.exc import NoResultFound


def get_by_token(session, access_token: str) -> AccessToken:
    try:
        return session.query(AccessToken).filter(AccessToken.token == access_token).one()
    except NoResultFound as e:
        print(e)


def get_user_id_by_token(session, access_token: str) -> int:
    try:
        return get_by_token(session, access_token).userId
    except NoResultFound as e:
        print(e)


def create(session: 'Session', user_id: int, commit=True) -> str:
    token = str(uuid4())
    session.add(AccessToken(userId=user_id, token=token))

    if commit:
        session.commit()

    return token


def validate(session: 'Session', access_token: str) -> bool:
    try:
        session.query(AccessToken).filter(AccessToken.token == access_token).one()
        return True
    except NoResultFound as e:
        print(e)

    return False


def delete(session: 'Session', token: str, commit=True) -> bool:
    access_token_row: AccessToken = get_by_token(session, token)

    if access_token_row:
        session.delete(access_token_row)

        if commit:
            session.commit()

        return True

    return False


def delete_all_by_user_id(session: 'Session', user_id: int, commit=True) -> bool:

    try:
        statement = AccessToken.__table__.delete().where(AccessToken.userId == user_id)
        session.execute(statement)

        if commit:
            session.commit()

        return True

    except NoResultFound as e:
        print(e)

    return False


if __name__ == '__main__':
    _session: 'Session' = SessionSingleton().get_session()
