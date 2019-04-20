from database.tables import User
from database import user
from database import access_token
from sqlalchemy.orm.exc import NoResultFound
from exceptions import Exceptions
from database.db import SessionSingleton


def sign_in(session: 'Session', email: str, password: str) -> str:
    print(f'Signing in: {email} {password}')

    if not user.email_exists(session, email):
        raise NoResultFound

    user_row: User = user.get_by_email(session, email)

    if user_row.pwdHash == user.hash_password(password):
        return access_token.create(session, user_row.id)

    raise Exceptions.Unauthorized


def sign_out(session: 'Session', email: str, token: str) -> bool:
    print(f'Signing out {email} {token}')
    if not user.email_exists(session, email):
        raise NoResultFound

    user_row: User = user.get_by_email(session, email)

    if access_token.validate_by_id(session, user_row.id, token):
        if access_token.delete(session, user_id=user_row.id, token=token):
            return True

    raise Exceptions.Unauthorized


def sign_out_all(session: 'Session', email: str, token: str) -> bool:
    print(f'Signing out all {email}')
    if not user.email_exists(session, email):
        raise NoResultFound

    user_row: User = user.get_by_email(session, email)

    if access_token.validate_by_id(session, user_row.id, token):
        if access_token.delete_all_by_user_id(session, user_id=user_row.id):
            return True

    raise Exceptions.Unauthorized


if __name__ == '__main__':
    _session: 'Session' = SessionSingleton().get_session()
    _token = sign_in(_session, 'soren.seeberg@gmail.com', 'hanadulsetmulighet')
    sign_in(_session, 'soren.seeberg@gmail.com', 'hanadulsetmulighet')
    sign_in(_session, 'soren.seeberg@gmail.com', 'hanadulsetmulighet')
    sign_in(_session, 'soren.seeberg@gmail.com', 'hanadulsetmulighet')
    sign_in(_session, 'sorense@configit.com', '1234')

    # sign_out(_session, 'soren.seeberg@gmail.com', _token)
    # sign_out(_session, 'soren.seeberg@gmail.com', _token)
    sign_out_all(_session, 'soren.seeberg@gmail.com', _token)
