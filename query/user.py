#!/usr/bin/python3
# -*- coding: utf-8 -*-

from database.tables import User
from hashlib import sha3_256
from exceptions import Exceptions
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError


def hash_password(password) -> str:
    return str(sha3_256(password.encode()).hexdigest())


def create(session: 'Session', email: str, password: str, commit=True) -> User:
    try:
        if email_exists(session, email):
            raise Exceptions.DuplicateEmailError

        user_row = User(email=email, pwdHash=hash_password(password))
        session.add(user_row)

        if commit:
            session.commit()

        return user_row
    except Exceptions.DuplicateEmailError:
        raise Exceptions.DuplicateEmailError
    except IntegrityError:
        raise IntegrityError


def create_admin(session: 'Session',
                 email: str = 'soren.seeberg@gmail.com',
                 password: str = 'hanadulsetmulighet',
                 commit=True) -> User:

    try:
        if email_exists(session, email):
            raise Exceptions.DuplicateEmailError

        user_row = User(email=email, pwdHash=hash_password(password), confirmed=True, enabled=True, administrator=True)
        session.add(user_row)

        if commit:
            session.commit()

        return user_row
    except Exceptions.DuplicateEmailError:
        raise Exceptions.DuplicateEmailError
    except IntegrityError:
        raise IntegrityError
    except Exception:
        raise Exception


def get_by_email(session: 'Session', email: str) -> 'User':
    try:
        return session.query(User).filter(User.email == email).one()
    except NoResultFound:
        raise NoResultFound


def get_by_id(session: 'Session', id: int) -> 'User':
    try:
        return session.query(User).get(id)
    except NoResultFound:
        raise NoResultFound


def update_password(session: 'Session', email: str, new_password_value: str, commit=True) -> bool:
    # TODO: setup try-except

    user_row = get_by_email(session, email)

    if user_row:
        user_row.pwdHash = hash_password(new_password_value)

        if commit:
            session.commit()

        return True

    return False


def update_confirmed(session: 'Session', email: str, confirmed_value: bool, commit=True) -> bool:
    # TODO: setup try-except

    user_row = get_by_email(session, email)

    if user_row:
        user_row.confirmed = confirmed_value

        if commit:
            session.commit()

        return True

    return False


def delete(session: 'Session', email: str, commit=True) -> bool:
    # TODO: setup try-except

    user_row = get_by_email(session, email)

    if user_row:
        session.delete(user_row)

        if commit:
            session.commit()

        return True

    return False


def email_exists(session: 'Session', email: str) -> bool:
    # TODO: setup try-except

    result = session.query(User).filter(User.email == email).count()

    return False if result == 0 else True


def setup(session: 'Session') -> None:
    create_admin(session, commit=False)
    create(session, 'sorense@configit.com', '1234', commit=False)


if __name__ == '__main__':
    from database import db

    _session = db.SessionSingleton().get_session()
    user = get_by_id(_session, 1)
    print(user.email)
