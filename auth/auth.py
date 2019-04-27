#!/usr/bin/python3
# -*- coding: utf-8 -*-

from database.tables import User
from query import access_token, user
from sqlalchemy.orm.exc import NoResultFound
from exceptions import Exceptions
from database.db import SessionSingleton


def sign_in(session: 'Session', email: str, password: str) -> str:
    print(f'Signing in: {email} {password}')

    try:
        if not user.email_exists(session, email):
            raise NoResultFound

        user_row: User = user.get_by_email(session, email)

        if user_row.pwdHash == user.hash_password(password):
            return access_token.create(session, user_row.id)

        raise Exceptions.Unauthorized
    except NoResultFound as e:
        print(e)
    except Exceptions.Unauthorized as e:
        print(e)


def sign_out(session: 'Session', token: str) -> bool:
    print(f'Signing out {token}')

    try:
        if access_token.validate(session, token):
            if access_token.delete(session, token=token):
                return True
            else:
                raise NoResultFound
        else:
            raise Exceptions.Unauthorized
    except Exceptions.Unauthorized as e:
        print(e)
    except NoResultFound as e:
        print(e)

    return False


def sign_out_all(session: 'Session', token: str) -> bool:
    user_id: int = access_token.get_user_id_by_token(session, token)

    if access_token.validate(session, token):
        if access_token.delete_all_by_user_id(session, user_id=user_id):
            return True

    raise Exceptions.Unauthorized


if __name__ == '__main__':
    _session: 'Session' = SessionSingleton().get_session()
    _token = sign_in(_session, 'soren.seeberg@gmail.com', 'hanadulsetmulighet')
    sign_in(_session, 'soren.seeberg@gmail.com', 'hanadulsetmulighet')
    sign_in(_session, 'soren.seeberg@gmail.com', 'hanadulsetmulighet')
    sign_in(_session, 'soren.seeberg@gmail.com', 'hanadulsetmulighet')
    sign_in(_session, 'sorense@configit.com', '1234')

    sign_out(_session, _token)
    sign_out(_session, _token)
    sign_out_all(_session, _token)