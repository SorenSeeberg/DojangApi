#!/usr/bin/python3
# -*- coding: utf-8 -*-

from database.tables import User
from query import access_token, user
from query import validate_input_data
from database.db import SessionSingleton
from typing import Dict
import response_codes
from response_codes import ResponseKeys


def create_user(session: 'Session', data: Dict) -> Dict:
    input_schema = {
        "email": [str, True],
        "password": [str, True]
    }

    if not validate_input_data(data, input_schema):
        return {ResponseKeys.status: response_codes.ResponseCodes.bad_request_400}

    email: str = data.get('email')
    password: str = data.get('password')

    if not user.create(session, email, password):
        return {ResponseKeys.status: response_codes.ResponseCodes.bad_request_400,
                ResponseKeys.body: {
                    ResponseKeys.message: 'Denne email er taget. Har du glemt dit password?'}
                }

    return {
        ResponseKeys.status: response_codes.ResponseCodes.created_201,
        ResponseKeys.body: {
            ResponseKeys.message:
                f'Velkommen til! Aktivér din profil ved at trykke på linket i den mail vi netop har sendt '
                f'til {email}.'
        }
    }


def get_user(session: 'Session', access_token_string: str) -> Dict:

    if not access_token.validate(session, access_token_string):
        return {ResponseKeys.status: response_codes.ResponseCodes.unauthorized_401}

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


def email_exists(session: 'Session', data: Dict) -> Dict:

    input_schema = {
        "email": [str, True]
    }

    if not validate_input_data(data, input_schema):
        return {ResponseKeys.status: response_codes.ResponseCodes.bad_request_400}

    email: str = data.get('email')

    return {
        ResponseKeys.status: response_codes.ResponseCodes.ok_200,
        ResponseKeys.body: {
            "email": email,
            "taken": user.email_exists(session, email)
        }
    }


def sign_in(session: 'Session', data: Dict) -> Dict:
    input_schema = {
        "email": [str, True],
        "password": [str, True]
    }

    if not validate_input_data(data, input_schema):
        return {ResponseKeys.status: response_codes.ResponseCodes.bad_request_400}

    email: str = data.get('email')
    password: str = data.get('password')

    if not user.email_exists(session, email):
        return {ResponseKeys.status: response_codes.ResponseCodes.not_found_404}

    user_row: User = user.get_by_email(session, email)
    new_access_token: str = access_token.create(session, user_row.id)

    if not user_row.pwdHash == user.hash_password(password):
        return {ResponseKeys.status: response_codes.ResponseCodes.unauthorized_401}

    return {
        ResponseKeys.status: response_codes.ResponseCodes.ok_200,
        ResponseKeys.body: {
            "accessToken": new_access_token
        }
    }


def sign_out(session: 'Session', access_token_string: str) -> Dict:

    if not access_token.validate(session, access_token_string):
        return {ResponseKeys.status: response_codes.ResponseCodes.unauthorized_401}

    if access_token.delete(session, token=access_token_string):
        return {ResponseKeys.status: response_codes.ResponseCodes.ok_200}

    return {ResponseKeys.status: response_codes.ResponseCodes.bad_request_400}


def sign_out_all(session: 'Session', access_token_string: str) -> Dict:
    user_id: int = access_token.get_user_id_by_token(session, access_token_string)

    if not access_token.validate(session, access_token_string):
        return {ResponseKeys.status: response_codes.ResponseCodes.unauthorized_401}

    if access_token.delete_all_by_user_id(session, user_id=user_id):
        return {ResponseKeys.status: response_codes.ResponseCodes.ok_200}

    return {ResponseKeys.status: response_codes.ResponseCodes.bad_request_400}


if __name__ == '__main__':
    _session: 'Session' = SessionSingleton().get_session()
    _token = sign_in(_session, {'email': 'soren.seeberg@gmail.com', 'password': 'hanadulsetmulighet'})
    sign_in(_session, {'email': 'soren.seeberg@gmail.com', 'password': 'hanadulsetmulighet'})
    sign_in(_session, {'email': 'soren.seeberg@gmail.com', 'password': 'hanadulsetmulighet'})
    sign_in(_session, {'email': 'soren.seeberg@gmail.com', 'password': 'hanadulsetmulighet'})
    sign_in(_session, {'email': 'sorense@configit.com', 'password': '1234'})

    sign_out(_session, _token.get('accessToken'))
    sign_out(_session, _token.get('accessToken'))
    sign_out_all(_session, _token.get('accessToken'))
