#!/usr/bin/python3
# -*- coding: utf-8 -*-
import random

from database.schemas import User
from mailer.mailer import send_activation_mail, send_restoration_mail
from query import access_token, user, result, level
from query import validate_input_data
from query import verification_token
from typing import Dict
from response_codes import ResponseKeys, ResponseCodes


def create(session: 'Session', data: Dict) -> Dict:
    input_schema = {
        "email": [str, True],
        "password": [str, True]
    }

    if not validate_input_data(data, input_schema):
        return {ResponseKeys.status: ResponseCodes.bad_request_400}

    email: str = data.get('email')
    password: str = data.get('password')

    if not user.create(session, email, password):
        return {ResponseKeys.status: ResponseCodes.bad_request_400,
                ResponseKeys.body: {
                    ResponseKeys.message: 'Denne email er taget. Har du glemt dit password?'}
                }

    new_user: User = user.get_by_email(session, email)
    send_activation_mail(email, verification_token.create(session, new_user.id))

    return {
        ResponseKeys.status: ResponseCodes.created_201,
        ResponseKeys.body: {
            ResponseKeys.message:
                f'Velkommen til! Aktivér din profil ved at trykke på linket i den mail vi netop har sendt '
                f'til {email}.'
        }
    }


def restore(session: 'Session', data: Dict) -> Dict:
    input_schema = {
        "email": [str, True]
    }

    if not validate_input_data(data, input_schema):
        return {ResponseKeys.status: ResponseCodes.bad_request_400}

    email: str = data.get('email')

    if not user.email_exists(session, email):
        return {ResponseKeys.status: ResponseCodes.bad_request_400}

    digits = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
    new_password: str = ''.join(random.sample(digits, 6))
    user.update_password(session, email, new_password)
    send_restoration_mail(email, new_password)

    return {
        ResponseKeys.status: ResponseCodes.ok_200,
        ResponseKeys.body: {
            ResponseKeys.message:
                f'Der er lavet nyt password til {email}'
        }
    }


def get(session: 'Session', user_id: int) -> Dict:
    user_row: 'User' = user.get_by_id(session, user_id)

    return {
        ResponseKeys.status: ResponseCodes.ok_200,
        ResponseKeys.body: {
            "email": user_row.email,
            "confirmed": user_row.confirmed,
            "enabled": user_row.enabled,
            "administrator": user_row.administrator
        }
    }


def get_current(session: 'Session', user_id: int) -> Dict:
    user_row: 'User' = user.get_by_id(session, user_id)
    results: 'Result' = result.get_last_user_results(session, user_id)

    def percentage_correct(r) -> int:
        return int(r.correctCount / (r.correctCount + r.incorrectCount) * 100)

    def time_spent(r) -> str:
        minutes = int(r.timeSpent / 60)
        seconds = r.timeSpent - (minutes * 60)

        if seconds < 10:
            seconds_string = f'0{seconds}'
        else:
            seconds_string = seconds

        return f'{minutes}:{seconds_string}'

    def level_label(r) -> str:

        names = level.get_names(session)
        return f'{names[r.levelMin]} til {names[r.levelMax]}'

    processed_results = [{'percentageCorrect': percentage_correct(x), "timeSpent": time_spent(x), "level": level_label(x)} for x in results]

    return {
        ResponseKeys.status: ResponseCodes.ok_200,
        ResponseKeys.body: {
            "email": user_row.email,
            "results": processed_results
        }
    }


def get_paginated(session: 'Session', access_token_string: str) -> Dict:
    raise NotImplementedError


def email_exists(session: 'Session', data: Dict) -> Dict:
    input_schema = {
        "email": [str, True]
    }

    if not validate_input_data(data, input_schema):
        return {ResponseKeys.status: ResponseCodes.bad_request_400}

    email: str = data.get('email')

    return {
        ResponseKeys.status: ResponseCodes.ok_200,
        ResponseKeys.body: {
            "email": email,
            "taken": user.email_exists(session, email)
        }
    }


def delete(session: 'Session', access_token_string: str) -> Dict:
    raise NotImplementedError


def activate(session: 'Session', verification_token_string: str) -> Dict:
    verification_token_row = verification_token.get_by_token(session, verification_token_string)

    if not verification_token_row:
        return {ResponseKeys.status: ResponseCodes.bad_request_400}

    user.update_confirmed(session, verification_token_row.userId, True, True, False)
    verification_token.delete(session, verification_token_row.token, False)
    session.commit()

    return {
        ResponseKeys.status: ResponseCodes.ok_no_content_204,
    }


def sign_in(session: 'Session', data: Dict) -> Dict:
    input_schema = {
        "email": [str, True],
        "password": [str, True]
    }

    if not validate_input_data(data, input_schema):
        return {ResponseKeys.status: ResponseCodes.bad_request_400}

    email: str = data.get('email')
    password: str = data.get('password')

    if not user.email_exists(session, email):
        return {ResponseKeys.status: ResponseCodes.not_found_404}

    user_row: User = user.get_by_email(session, email)

    if not user_row.enabled or not user_row.confirmed:
        return {ResponseKeys.status: ResponseCodes.not_found_404}

    new_access_token: str = access_token.create(session, user_row.id)

    if not user_row.pwdHash == user.hash_password(password):
        return {ResponseKeys.status: ResponseCodes.unauthorized_401}

    return {
        ResponseKeys.status: ResponseCodes.ok_200,
        ResponseKeys.body: {
            "accessToken": new_access_token
        }
    }


def sign_out(session: 'Session', access_token_string: str) -> Dict:
    if access_token.delete(session, token=access_token_string):
        return {ResponseKeys.status: ResponseCodes.ok_200}

    return {ResponseKeys.status: ResponseCodes.bad_request_400}


def sign_out_all(session: 'Session', user_id: int) -> Dict:
    if access_token.delete_all_by_user_id(session, user_id=user_id):
        return {ResponseKeys.status: ResponseCodes.ok_200}

    return {ResponseKeys.status: ResponseCodes.bad_request_400}

