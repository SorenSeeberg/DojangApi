#!/usr/bin/python3
# -*- coding: utf-8 -*-

from uuid import uuid4

from sqlalchemy.exc import IntegrityError
from database.schemas import VerificationToken
from sqlalchemy.orm.exc import NoResultFound


def get_by_token(session, access_token: str) -> VerificationToken:
    try:
        return session.query(VerificationToken).filter(VerificationToken.token == access_token).one()
    except NoResultFound as e:
        print(e)


def get_by_user_id(session, user_id: int) -> VerificationToken:
    try:
        return session.query(VerificationToken).filter(VerificationToken.userId == user_id).one()
    except NoResultFound as e:
        print(e)


def get_user_id_by_token(session, token: str) -> int:
    try:
        return get_by_token(session, token).userId
    except NoResultFound:
        raise NoResultFound
    except Exception:
        raise Exception


def create(session: 'Session', user_id: int, commit=True) -> str:
    try:
        token = str(uuid4())
        session.add(VerificationToken(userId=user_id, token=token))

        if commit:
            session.commit()

        return token
    except IntegrityError:
        raise IntegrityError
    except Exception:
        raise Exception


def validate(session: 'Session', token: str) -> bool:
    try:
        session.query(VerificationToken).filter(VerificationToken.token == token).one()
        return True
    except NoResultFound:
        return False
    except Exception:
        return False


def delete(session: 'Session', token: str, commit=True) -> bool:
    try:
        access_token_row: VerificationToken = get_by_token(session, token)

        if access_token_row:
            session.delete(access_token_row)

            if commit:
                session.commit()

            return True

    except NoResultFound:
        raise NoResultFound
    except Exception:
        raise Exception


def delete_all_by_user_id(session: 'Session', user_id: int, commit=True) -> bool:
    try:
        statement = VerificationToken.__table__.delete().where(VerificationToken.userId == user_id)
        session.execute(statement)

        if commit:
            session.commit()

        return True

    except NoResultFound:
        raise NoResultFound
    except Exception:
        raise Exception


if __name__ == '__main__':
    from database import db

    _session = db.SessionSingleton().get_session()
    print(get_by_user_id(_session, 1).token)
