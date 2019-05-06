#!/usr/bin/python3
# -*- coding: utf-8 -*-

from database.tables import User
from query import access_token, user
from query import validate_input_data
from sqlalchemy.orm.exc import NoResultFound
from exceptions import Exceptions
from sqlalchemy.exc import ArgumentError
from sqlalchemy.exc import IntegrityError
from database.db import SessionSingleton
from typing import Dict
import response_codes
from response_codes import ResponseKeys


def create_user(session: 'Session', data: Dict) -> Dict:
    input_schema = {
        "email": [str, True],
        "password": [str, True]
    }

    if validate_input_data(data, input_schema):
        email: str = data.get('email')
        password: str = data.get('password')
    else:
        return {ResponseKeys.status: response_codes.ResponseCodes.bad_request_400}

    try:
        user_row = user.create(session, email, password)
    except Exceptions.DuplicateEmailError:
        return {ResponseKeys.status: response_codes.ResponseCodes.bad_request_400,
                ResponseKeys.body: {
                    ResponseKeys.message: 'Denne email er taget. Har du glemt dit password?'}
                }
    return {
        ResponseKeys.status: response_codes.ResponseCodes.created_201,
        ResponseKeys.body: {
            ResponseKeys.message:
                f'Velkommen til! Aktivér din profil ved at trykke på linket i den mail vi netop har sendt '
                f'til {user_row.email}.'
        }
    }


def get_user(session: 'Session', access_token_string: str) -> Dict:

    try:
        if not access_token.validate(session, access_token_string):
            return {ResponseKeys.status: response_codes.ResponseCodes.unauthorized_401}

    except ArgumentError as e:
        print(e)
        return {ResponseKeys.status: response_codes.ResponseCodes.bad_request_400}

    user_id: int = access_token.get_user_id_by_token(session, access_token_string)
    user_row: 'User' = user.get_by_id(session, user_id)

    return {
        ResponseKeys.status: response_codes.ResponseCodes.ok_200,
        ResponseKeys.body: {
            "email": user_row.email,
            "confirmed": user_row.confirmed,
            "enabled": user_row.enabled,
            "administrator": user_row.administrator
        }
    }


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
