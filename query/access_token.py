#!/usr/bin/python3
# -*- coding: utf-8 -*-

from uuid import uuid4
from database.tables import AccessToken
from database.tables import User
from query import user
from database.db import SessionSingleton
from sqlalchemy.orm.exc import NoResultFound


def get_by_user_id_and_token(session, user_id: int, access_token: str) -> AccessToken:
    try:
        return session.query(AccessToken).filter(AccessToken.userId == user_id, AccessToken.token == access_token).one()
    except NoResultFound as e:
        print(e)


def create(session: 'Session', user_id: int, commit=True) -> str:
    token = str(uuid4())
    session.add(AccessToken(userId=user_id, token=token))

    if commit:
        session.commit()

    return token


def validate_by_id(session: 'Session', user_id: int, access_token: str) -> bool:
    try:
        session.query(AccessToken).filter(AccessToken.userId == user_id, AccessToken.token == access_token).one()
        return True
    except NoResultFound as e:
        print(e)

    return False


def validate_by_email(session: 'Session', email: str, access_token: str) -> bool:
    user_row: User = user.get_by_email(session, email)

    if not user_row:
        return False

    return validate_by_id(session, user_row.id, access_token)


def delete(session: 'Session', user_id: int, token: str, commit=True) -> bool:
    access_token_row: AccessToken = get_by_user_id_and_token(session, user_id, token)

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
