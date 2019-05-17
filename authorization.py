from query import access_token


def is_authorized(session: 'Session', access_token_string: str, role: str) -> bool:

    if role == 'user':
        if access_token.validate(session, access_token_string):
            return True

    if role == 'administrator':
        if access_token.validate(session, access_token_string):
            return True

    return False
