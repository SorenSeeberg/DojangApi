from database.tables import User
from database import api_user
from database import api_access_token
from sqlalchemy.orm.exc import NoResultFound
from exceptions import Exceptions
from database.db import SessionSingleton


def sign_in(session: 'Session', email: str, password: str) -> str:
    print(f'Signing in: {email} {password}')

    if not api_user.email_exists(session, email):
        raise NoResultFound

    user: User = api_user.get_by_email(session, email)

    if user.pwdHash == api_user.hash_password(password):
        return api_access_token.create(session, user.id)

    raise Exceptions.Unauthorized


def sign_out(session: 'Session', email: str, access_token: str) -> bool:
    print(f'Signing out {email} {access_token}')
    if not api_user.email_exists(session, email):
        raise NoResultFound

    user: User = api_user.get_by_email(session, email)

    if api_access_token.validate_by_id(session, user.id, access_token):
        deleted = api_access_token.delete(session, user_id=user.id, access_token=access_token)

        if deleted:
            return True

    raise Exceptions.Unauthorized


if __name__ == '__main__':
    _session: 'Session' = SessionSingleton().get_session()

    token = sign_in(_session, 'soren.seeberg@gmail.com', 'hanadulsetmulighet')
    print(token)
    sign_out(_session, 'soren.seeberg@gmail.com', token)
